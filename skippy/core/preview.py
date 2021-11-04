"""Summary
"""
from skippy.api import PageData

from skippy.utils.logger import log

from requests.exceptions import RequestException
from abc import ABCMeta, abstractmethod
from typing import Union, Tuple, List
import unicodedata
import pyftml
import pyscp
import html
import re


def render(pdata: PageData) -> str:
    """Summary
    
    Args:
        pdata (PageData): Description
    
    Returns:
        str: Description
    """
    preprocess = PreProcessorsHandler(pdata).process()
    htmlprocess = HTMLProcessorsHandler(preprocess, pdata).process()
    return PostProcessorsHandler(htmlprocess, pdata).process()


#################################################
# Base Classes
#################################################
class AbstractProcessor(metaclass=ABCMeta):

    """Summary
    """

    pattern: str

    def __init__(self, source: str, pdata: PageData):
        """Summary
        
        Args:
            source (str): Description
            pdata (PageData): Description
        """
        self.source: str = source
        self.pdata: PageData = pdata

    @property
    def matches(self) -> List[Union[Tuple[str, ...], str]]:
        """Summary
        
        Returns:
            List[Union[Tuple[str, ...], str]]: Description
        """
        return re.findall(
            self.pattern,
            self.source,
        )

    @abstractmethod
    def process(self):
        """Summary
        """
        pass


class ProcessorsHandler(metaclass=ABCMeta):

    """Summary
    
    Attributes:
        source (str): Description
    """

    def __init__(self, source: str, pdata: PageData):
        """Summary
        
        Args:
            source (str): Description
            pdata (PageData): Description
        """
        self.source: str = source
        self.pdata: PageData = pdata
        self.processors: List[AbstractProcessor] = []

    def register(self, processor: AbstractProcessor):
        """Summary
        
        Args:
            processor (AbstractProcessor): Description
        """
        self.processors.append(processor)

    def process(self) -> str:
        """Summary
        
        Returns:
            str: Description
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
class PreProcessorsHandler(ProcessorsHandler):

    """Summary
    """

    def __init__(self, pdata: PageData):
        """Summary
        
        Args:
            pdata (PageData): Description
        """
        super(PreProcessorsHandler, self).__init__(pdata["source"], pdata)
        self.register(IncludesProcessor)
        self.register(IftagsProcessor)


class HTMLProcessorsHandler(ProcessorsHandler):

    """Summary
    
    Attributes:
        html (str): Description
    """

    def __init__(self, source: str, pdata: PageData):
        """Summary
        
        Args:
            source (str): Description
            pdata (PageData): Description
        """
        super(HTMLProcessorsHandler, self).__init__(source, pdata)
        self.register(MarkdownProcessor)
        self.register(InsertDataProcessor)
        self.register(ModuleCSSProcessor)

    def process(self):
        """Summary
        
        Returns:
            TYPE: Description
        """
        self.html = self.processors[0](self.source, self.pdata).process()
        for processor in self.processors[1:]:
            try:
                self.html = processor(self.source, self.pdata, self.html).process()
            except Exception as e:
                log.error(e, exc_info=True)
        return self.html


class PostProcessorsHandler(ProcessorsHandler):

    """Summary
    """

    def __init__(self, source: str, pdata: PageData):
        """Summary
        
        Args:
            source (str): Description
            pdata (PageData): Description
        """
        super(PostProcessorsHandler, self).__init__(source, pdata)
        self.register(LocalImagesProcessor)
        self.register(HTMLTagsProcessor)


#################################################
# PreProcessors
#################################################
class IncludesProcessor(AbstractProcessor):

    """Summary
    
    Attributes:
        source (str): Description
    """

    pattern: str = r"(\[\[include\s(?::.+?:|)(?:.+?:|)(?:.+)(?:\s((?:.|\n)+?)|)]])"

    def process(self, iteration: int = 0) -> str:
        """Summary
        
        Returns:
            str: Description
        
        Args:
            iteration (int, optional): Description
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
                        r"(?:([\w-]+)(?:(?:\s|)=(?:\s|))((?:.|\n+?)+))",
                        arg,
                    )[0]
                    p = p.replace("{$" + arg[0] + "}", arg[1])
                self.source = self.source.replace(include[0], p)
            except Exception as e:
                log.error(e)
        if (
            re.findall(
                r"(\[\[include(?:(?:.|\n)+?)]])",
                self.source,
            )
            and iteration != 5
        ):
            self.process(iteration + 1)
        return self.source


class IftagsProcessor(AbstractProcessor):

    """Summary
    
    Attributes:
        source (str): Description
    """

    pattern: str = r"(\[\[iftags (.+?)]]((?:(?:.|\n|\s)+?))\[\[\/iftags]])"

    def process(self) -> str:
        """Summary
        
        Returns:
            str: Description
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

    """Summary
    """

    wiki: pyscp.core.Wiki = pyscp.wikidot.Wiki("www.wikidot.com")

    def _wikidot(self) -> str:
        """Summary
        
        Returns:
            str: Description
        """
        return self.wiki._module("edit/PagePreviewModule", source=self.source)["body"]

    def _ftml(self) -> str:
        """Summary
        
        Returns:
            str: Description
        """
        return pyftml.render_html(self.source)["body"]

    def process(self) -> str:
        """Summary
        
        Returns:
            str: Description
        """
        try:
            return self._wikidot()
        except RequestException:
            return self._ftml()


class InsertDataProcessor(AbstractProcessor):

    """Summary
    """

    html_base: str = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru" pdata-lt-installed="true">
            <head>
                <style type="text/css">
                    @import url(http://d3g0gp89917ko0.cloudfront.net/v--3e3a6f7dbcc9/common--theme/base/css/style.css);
                    @import url(http://scp-ru.wdfiles.com/local--code/component:theme2/1);
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
        """Summary
        
        Args:
            source (str): Description
            pdata (PageData): Description
            html (str): Description
        """
        super(InsertDataProcessor, self).__init__(source, pdata)
        self.html: str = html

    def process(self) -> str:
        """Summary
        
        Returns:
            str: Description
        """
        self.source = self.html_base.replace("<<TITLE>>", html.escape(self.pdata["title"]))
        self.source = self.source.replace("<<CONTENT>>", self.html)
        self.source = self.source.replace(
            "<<TAGS>>",
            " ".join([f"<a href='#'>{tag}</a>" for tag in self.pdata["tags"]]),
        )
        return self.source


class ModuleCSSProcessor(AbstractProcessor):

    """Summary
    
    Attributes:
        html (str): Description
    """

    pattern: str = r"(?:(?:\[\[module) (?:CSS|css)(?:(.+?)|)\]\]\n)((.|\n)+?)(?:\n\[\[\/module\]\])"

    def __init__(self, source: str, pdata: PageData, html: str):
        """Summary
        
        Args:
            source (str): Description
            pdata (PageData): Description
            html (str): Description
        """
        super(ModuleCSSProcessor, self).__init__(source, pdata)
        self.html: str = html

    def process(self) -> str:
        """Summary
        
        Returns:
            str: Description
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

    """Summary
    
    Attributes:
        source (str): Description
    """

    pattern: str = r'<img src="http://www.wdfiles.com/local--files//(.+?)"'

    def process(self) -> str:
        """Summary
        
        Returns:
            str: Description
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

    """Summary
    
    Attributes:
        source (str): Description
    """

    pattern: str = r"(\[\[html(?:(?:.+?)| |)]]((?:.|\n|\s)+?)\[\[\/html]])"

    def process(self) -> str:
        """Summary
        
        Returns:
            str: Description
        """
        for htmltags in self.matches:
            self.source = self.source.replace(htmltags[0], html.unescape(htmltags[1]))
        return self.source
