"""Wikidot syntax previewer
"""
from skippy.api import PageData

from skippy.utils.logger import log

from requests.exceptions import RequestException
from abc import ABCMeta, abstractmethod
from typing import TypeVar, Union, Tuple, List, Type
import unicodedata
import pyftml
import pyscp
import html
import re


def render(pdata: PageData) -> str:
    """Render page by page data

    Args:
        pdata (PageData): Page data (title, source, tags and files)

    Returns:
        str: Rendered HTML
    """
    preprocess = PreProcessorsHandler(pdata).process()
    htmlprocess = HTMLProcessorsHandler(preprocess, pdata).process()
    return PostProcessorsHandler(htmlprocess, pdata).process()


#################################################
# Base Classes
#################################################
class AbstractProcessor(metaclass=ABCMeta):

    """Abstract processor class"""

    pattern: str

    def __init__(self, source: str, pdata: PageData):
        """Initializing Processor

        Args:
            source (str): Page source
            pdata (PageData): Page data
        """
        self.source: str = source
        self.pdata: PageData = pdata

    @property
    def matches(self) -> List[Union[Tuple[str, ...], str]]:
        """Get all matches in source by pattern

        Returns:
            List[Union[Tuple[str, ...], str]]: List of matches
        """
        return re.findall(
            self.pattern,
            self.source,
        )

    @abstractmethod
    def process(self):
        """Abstract process method"""
        pass


_Processor = TypeVar("_Processor", bound=AbstractProcessor)


class ProcessorsHandlerBase:

    """Abstract processor's handler class"""

    def __init__(self, source: str, pdata: PageData):
        """Summary

        Args:
            source (str): Page source
            pdata (PageData): Page data
        """
        self.source: str = source
        self.pdata: PageData = pdata
        self.processors: List[Type[_Processor]] = []

    def register(self, processor: Type[_Processor]):
        """Register a processor

        Args:
            processor (Type[_Processor]): Processor class
        """
        self.processors.append(processor)

    def process(self) -> str:
        """Run all processor

        Returns:
            str: Processed source
        """
        for processor in self.processors:
            try:
                self.source = processor(self.source, self.pdata).process()
            except Exception as e:
                log.error(e, exc_info=True)
        return self.source


#################################################
# ProcessorsHandlers
#################################################
class PreProcessorsHandler(ProcessorsHandlerBase):

    """Handler of preprocessors"""

    def __init__(self, pdata: PageData):
        """Initializing preprocessors handler

        Args:
            pdata (PageData): Page data
        """
        super(PreProcessorsHandler, self).__init__(pdata["source"], pdata)
        self.register(IncludesProcessor)
        self.register(IftagsProcessor)


class HTMLProcessorsHandler(ProcessorsHandlerBase):

    """Handler of HTML processors"""

    def __init__(self, source: str, pdata: PageData):
        """Initializing HTML processors handler

        Args:
            source (str): Page source
            pdata (PageData): Page data
        """
        super(HTMLProcessorsHandler, self).__init__(source, pdata)
        self.register(MarkdownProcessor)
        self.register(InsertDataProcessor)
        self.register(ModuleCSSProcessor)

    def process(self) -> str:
        """Run all processor

        Returns:
            str: Processed source
        """
        self.html = self.processors[0](self.source, self.pdata).process()
        for processor in self.processors[1:]:
            try:
                self.html = processor(self.source, self.pdata, self.html).process()
            except Exception as e:
                log.error(e, exc_info=True)
        return self.html


class PostProcessorsHandler(ProcessorsHandlerBase):

    """Handler of postprocessors"""

    def __init__(self, source: str, pdata: PageData):
        """Initializing postprocessors handler

        Args:
            source (str): Page source
            pdata (PageData): Page data
        """
        super(PostProcessorsHandler, self).__init__(source, pdata)
        self.register(LocalImagesProcessor)
        self.register(HTMLTagsProcessor)


#################################################
# PreProcessors
#################################################
class IncludesProcessor(AbstractProcessor):

    """Include processor"""

    pattern: str = r"(\[\[include\s(?::.+?:|)(?:.+?:|)(?:.+)(?:\s((?:.|\n)+?)|)]])"

    def process(self, iteration: int = 0) -> str:
        """Replace all include tags with included page source

        Args:
            iteration (int, optional): Include iteration (max=5)

        Returns:
            str: Processed source
        """
        for include in self.matches:
            path = re.findall(
                r"(?::(.+?):|)((?:.+?:|).+)",
                include[0].split()[1].replace("]]", ""),
            )[0]
            site = path[0]
            page = path[1]
            try:
                wiki = pyscp.wikidot.Wiki(site)
                p = wiki(page).source
                args = [
                    i[1:] if i.startswith("\n") else i for i in include[1].split("|")
                ]
                if not args[0]:
                    args = []
                for arg in args:
                    arg = re.findall(
                        r"([\w-]+)(?:(?:\s|)=(?:\s|))((?:.|\n+?)+)",
                        arg,
                    )[0]
                    p = p.replace("{$" + arg[0] + "}", arg[1])
                self.source = self.source.replace(include[0], p)
            except Exception as e:
                log.error(e)
        if (
            re.findall(
                r"(\[\[include(?:.|\n)+?]])",
                self.source,
            )
            and iteration != 5
        ):
            self.process(iteration + 1)
        return self.source


class IftagsProcessor(AbstractProcessor):

    """Iftags processor"""

    pattern: str = r"(\[\[iftags (.+?)]]((?:(?:.|\n|\s)+?))\[\[\/iftags]])"

    def process(self) -> str:
        """Remove iftags if it not matches with page tags

        Returns:
            str: Processed source
        """
        for iftag in self.matches:
            match = True
            elem = re.findall(r"(\+.+?(?=\s|$)|-.+?(?=\s|$))", iftag[1])
            for e in elem:
                if e.startswith("+"):
                    if e[1:] not in self.pdata["tags"]:
                        match = False
                elif e[1:] in self.pdata["tags"]:
                    match = False
            if match:
                self.source = self.source.replace(iftag[0], iftag[2])
        return self.source


#################################################
# HTMLProcessors
#################################################
class MarkdownProcessor(AbstractProcessor):

    """Markdown processor"""

    wiki: pyscp.wikidot.Wiki = pyscp.wikidot.Wiki("www.wikidot.com")

    def _wikidot(self) -> str:
        """If connected to internet, get previewed HTML from Wikidot

        Returns:
            str: Previewed source
        """
        return self.wiki._module("edit/PagePreviewModule", source=self.source)["body"]

    def _ftml(self) -> str:
        """If don't have connection to internet, get previewed HTML from local FTML previewer

        Returns:
            str: Previewed source
        """
        return pyftml.render_html(self.source)["body"]

    def process(self) -> str:
        """Get previewed page with online/offline methods

        Returns:
            str: Processed source
        """
        try:
            return self._wikidot()
        except RequestException:
            return self._ftml()


class InsertDataProcessor(AbstractProcessor):

    """InsertData processor"""

    html_base: str = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru" pdata-lt-installed="true">
            <head>
                <style type="text/css">
                    @import url(http://d3g0gp89917ko0.cloudfront.net/v--3e3a6f7dbcc9/common--theme/base/css/style.css);
                    @import url(http://scp-ru.wdfiles.com/local--code/component:theme2/1);
                    @import url(http://d3g0gp89917ko0.cloudfront.net/v--3e3a6f7dbcc9/common--modules/css/pagerate/PageRateWidgetModule.css);
                </style>
                <script type="text/javascript" src="http://d3g0gp89917ko0.cloudfront.net/v--3e3a6f7dbcc9/common--javascript/init.combined.js"></script>
                <script type="text/javascript">
                    var URL_HOST = 'www.wikidot.com';
                    var URL_DOMAIN = 'wikidot.com';
                    var USE_SSL =  true ;
                    var URL_STATIC = 'http://d3g0gp89917ko0.cloudfront.net/v--3e3a6f7dbcc9';
                    // global request information
                    
                    var WIKIREQUEST = {};
                    WIKIREQUEST.info = {};
                    
                    WIKIREQUEST.info.domain = "www.wikidot.com";
                    WIKIREQUEST.info.siteId = 648902;
                    WIKIREQUEST.info.siteUnixName = "www";
                    WIKIREQUEST.info.categoryId = 4388020;
                    WIKIREQUEST.info.themeId = 192064;
                    WIKIREQUEST.info.requestPageName = "start:start";
                    OZONE.request.timestamp = 1619763822;
                    OZONE.request.date = new Date();
                    WIKIREQUEST.info.lang = 'en';
                            WIKIREQUEST.info.pageUnixName = "start:start";
                    WIKIREQUEST.info.pageId = 22129557;
                                    WIKIREQUEST.info.lang = "en";
                    OZONE.lang = "en";
                    var isUAMobile = !!/Android|webOS|iPhone|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
                </script>
                <script type="text/javascript">
            
                    require.config({
                        baseUrl: URL_STATIC + '/common--javascript',
                        paths: {
                            'jquery.ui': 'jquery-ui.min',
                            'jquery.form': 'jquery.form'
                        }
                    });
            
                </script>
                <script type="text/javascript" src="http://d3g0gp89917ko0.cloudfront.net/v--3e3a6f7dbcc9/common--javascript/WIKIDOT.combined.js"></script>
                <<MODULE-CSS-PREVIEW>>
                <style>
                    body {
                        padding: 2em !important;
                    }
                </style>
            </head>
            <body id="html-body">
                <div id="dummy-ondomready-block" style="display:none;"></div>
                <div id="page-title">
                    <<TITLE>>
                </div>
                <div id="page-content" style="min-height: 500px;">
                    <<CONTENT>>
                </div>
                <div class="page-tags">
                    <span>
                        <<TAGS>>
                    </span>
                </div>
            </body>
        </html>
        """

    def __init__(self, source: str, pdata: PageData, html: str):
        """Initializing InsertData processor

        Args:
            source (str): Page source
            pdata (PageData): Page data
            html (str): Previewed page html
        """
        super(InsertDataProcessor, self).__init__(source, pdata)
        self.html: str = html

    def process(self) -> str:
        """Insert page data to HTML template

        Returns:
            str: Processed HTML page
        """
        self.source = self.html_base.replace(
            "<<TITLE>>", html.escape(self.pdata["title"])
        )
        self.source = self.source.replace("<<CONTENT>>", self.html)
        self.source = self.source.replace(
            "<<TAGS>>",
            " ".join([f"<a href='#'>{tag}</a>" for tag in self.pdata["tags"]]),
        )
        return self.source


class ModuleCSSProcessor(AbstractProcessor):

    """Module CSS processor"""

    pattern: str = r"(?:(?:\[\[module) (?:CSS|css)(?:(.+?)|)\]\]\n)((.|\n)+?)(?:\n\[\[\/module\]\])"

    def __init__(self, source: str, pdata: PageData, html: str):
        """Initializing Module CSS processor

        Args:
            source (str): Page source
            pdata (PageData): Page data
            html (str): Previewed page html
        """
        super(ModuleCSSProcessor, self).__init__(source, pdata)
        self.html: str = html

    def process(self) -> str:
        """Convert [[module CSS]] block to <style> tag

        Returns:
            str: Processed HTML page
        """
        styles = ""
        for style in self.matches:
            style = unicodedata.normalize("NFKD", style[1])
            styles += f"<style>\n{style}\n</style>\n"
        self.html = self.html.replace("<<MODULE-CSS-PREVIEW>>", styles)
        return self.html


#################################################
# PostProcessor
#################################################
class LocalImagesProcessor(AbstractProcessor):

    """Local images processor"""

    pattern: str = r'<img src="http://www.wdfiles.com/local--files//(.+?)"'

    def process(self) -> str:
        """Insert local images to page

        Returns:
            str: Processed HTML page
        """
        files = self.pdata["files"]
        for img in self.matches:
            if img in files:
                self.source = self.source.replace(
                    f"http://www.wdfiles.com/local--files//{img}",
                    f"data:{img.split('.')[1]}/;base64,{files[img]}",
                )
        return self.source


class HTMLTagsProcessor(AbstractProcessor):

    """HTML tags processor"""

    pattern: str = r"(\[\[html(?:(?:.+?)| |)]]((?:.|\n|\s)+?)\[\[\/html]])"

    def process(self) -> str:
        """Unescape [[html]] tags

        Returns:
            str: Processed HTML page
        """
        for tag in self.matches:
            self.source = self.source.replace(tag[0], html.unescape(tag[1]))
        return self.source
