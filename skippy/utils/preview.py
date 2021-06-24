from skippy.utils.logger import log

from abc import ABCMeta, abstractmethod
import unicodedata
import tempfile
import pyscp
import html
import re


class Preview:
    def __init__(self, data):
        self.data = data

    def process(self):
        preprocess = PreProcessorsHandler(self.data).process()
        htmlprocess = HTMLProcessorsHandler(preprocess, self.data).process()
        postprocess = PostProcessorsHandler(htmlprocess, self.data).process()

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".html", mode="w", encoding="utf-8"
        ) as tmp:
            tmp.write(postprocess)
            return tmp.name


#################################################
# Base Classes
#################################################
class ProcessorBase(metaclass=ABCMeta):
    pattern = r""

    def __init__(self, source, data):
        self.source = source
        self.data = data

    @property
    def matches(self):
        return re.findall(
            self.pattern,
            self.source,
        )

    @abstractmethod
    def process(self):
        pass


class ProcessorsHandler(metaclass=ABCMeta):
    def __init__(self, source, data):
        self.source = source
        self.data = data
        self.processors = []

    def register(self, processor):
        self.processors.append(processor)

    def process(self):
        for processor in self.processors:
            try:
                self.source = processor(self.source, self.data).process()
            except Exception as e:
                log.error(e, exc_info=True)
        return self.source


#################################################
# ProcessorsHandlers
#################################################
class PreProcessorsHandler(ProcessorsHandler):
    def __init__(self, data):
        super(PreProcessorsHandler, self).__init__(data["source"], data)
        self.register(IncludesProcessor)
        self.register(IftagsProcessor)


class HTMLProcessorsHandler(ProcessorsHandler):
    def __init__(self, source, data):
        super(HTMLProcessorsHandler, self).__init__(source, data)
        self.register(MarkdownProcessor)
        self.register(InsertDataProcessor)
        self.register(ModuleCSSProcessor)

    def process(self):
        self.html = self.processors[0](self.source, self.data).process()
        for processor in self.processors[1:]:
            try:
                self.html = processor(self.source, self.data, self.html).process()
            except Exception as e:
                log.error(e, exc_info=True)
        return self.html


class PostProcessorsHandler(ProcessorsHandler):
    def __init__(self, source, data):
        super(PostProcessorsHandler, self).__init__(source, data)
        self.register(LocalImagesProcessor)
        self.register(HTMLTagsProcessor)


#################################################
# PreProcessors
#################################################
class IncludesProcessor(ProcessorBase):
    pattern = r"(\[\[include\s(?::.+?:|)(?:.+?:|)(?:.+)(?:\s((?:.|\n)+?)|)]])"

    def process(self, iteration=0):
        for include in self.matches:
            path = re.findall(
                r"(:.+?:|)(.+?:|)(.+)",
                include[0].split()[1].replace("]]", ""),
            )[0]
            site = path[0].replace(":", "")
            page = path[1] + path[2]
            try:
                wiki = pyscp.wikidot.Wiki(site)
                p = wiki(page).source
                args = [
                    i[1:] if i.startswith("\n") else i for i in include[1].split("|")
                ]
                if args[0] == "":
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


class IftagsProcessor(ProcessorBase):
    pattern = r"(\[\[iftags (.+?)]]((?:(?:.|\n|\s)+?))\[\[\/iftags]])"

    def process(self):
        for iftag in self.matches:
            match = True
            elem = re.findall(r"(\+.+?(?=\s|$)|-.+?(?=\s|$))", iftag[1])
            for e in elem:
                if e.startswith("+"):
                    if e[1:] not in self.data["tags"]:
                        match = False
                else:
                    if e[1:] in self.data["tags"]:
                        match = False
            if match:
                self.source = self.source.replace(iftag[0], iftag[2])
        return self.source


#################################################
# HTMLProcessors
#################################################
class MarkdownProcessor(ProcessorBase):
    wiki = pyscp.wikidot.Wiki("www.wikidot.com")

    def process(self):
        return self.wiki._module("edit/PagePreviewModule", source=self.source)["body"]


class InsertDataProcessor(ProcessorBase):
    html_base = """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru" data-lt-installed="true">
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
				padding: 2em;
			}
		</style>
		</head>
		<body id="html-body">
		<div id="dummy-ondomready-block" style="display:none;"></div>
		<div id="page-title">
			<<TITLE>>
		</div>
		<div id="page-content">
			<<CONTENT>>
		</div>
		<div class="page-tags">
		<span>
			<<TAGS>>
		</span>
		</div>
		</body>
		</html>"""

    def __init__(self, source, data, html):
        super(InsertDataProcessor, self).__init__(source, data)
        self.html = html

    def process(self):
        html = self.html_base.replace("<<TITLE>>", self.data["title"])
        html = html.replace("<<CONTENT>>", self.html)
        html = html.replace(
            "<<TAGS>>",
            " ".join([f"<a href='#'>{tag}</a>" for tag in self.data["tags"]]),
        )
        return html


class ModuleCSSProcessor(ProcessorBase):
    pattern = r"(?:(?:\[\[module) (?:CSS|css)(?:(.+?)|)\]\]\n)((.|\n)+?)(?:\n\[\[\/module\]\])"

    def __init__(self, source, data, html):
        super(ModuleCSSProcessor, self).__init__(source, data)
        self.html = html

    def process(self):
        styles = ""
        for style in self.matches:
            style = unicodedata.normalize("NFKD", style[1])
            styles += f"<style>\n{style}\n</style>\n"
        self.html = self.html.replace("<<MODULE-CSS-PREVIEW>>", styles)
        return self.html


#################################################
# PostProcessor
#################################################
class LocalImagesProcessor(ProcessorBase):
    pattern = r"""(?<=(<img src="))(http://www.wdfiles.com/local--files//)(.+?)(?=")"""

    def process(self):
        files = self.data["files"]
        for img in self.matches:
            img = img[1:]
            if img[1] in files:
                self.source = self.source.replace(
                    img[0] + img[1],
                    f"data:{img[1].split('.')[1]}/;base64,{files[img[1]]}",
                )
        return self.source


class HTMLTagsProcessor(ProcessorBase):
    pattern = r"(\[\[html(?:(?:.+?)| |)]]((?:.|\n|\s)+?)\[\[\/html]])"

    def process(self):
        for htmltags in self.matches:
            self.source = self.source.replace(htmltags[0], html.unescape(htmltags[1]))
        return self.source
