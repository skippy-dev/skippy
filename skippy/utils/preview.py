from skippy.utils.logger import log
import unicodedata
import tempfile
import pyscp
import re

class Preview:
	def __init__(self):
		self.wiki = pyscp.wikidot.Wiki("www.wikidot.com")

	def __call__(self, data):
		source = self.preprocess(data)
		content = self.wiki._module("edit/PagePreviewModule", source=source)["body"]
		html = (
			"""
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
		<script type="text/javascript" src="http://d3g0gp89917ko0.cloudfront.net/v--3e3a6f7dbcc9/common--javascript/WIKIDOT.combined.js"></script>\n"""
			+ self.module_css_preview(source)
			+ """
		<style>
			body {
				padding: 2em;
			}
		</style>
		</head>
		<body id="html-body">
		<div id="dummy-ondomready-block" style="display:none;"></div>
		<div id="page-title">\n"""
			+ data["title"]
			+ """
		</div>
		<div id="page-content">\n"""
			+ content
			+ """
		</div>
		<div class="page-tags">
		<span>\n"""
			+ " ".join([f"<a href='#'>{tag}</a>" for tag in data["tags"]])
			+ """
		</span>
		</div>
		</body>
		</html>"""
		)
		html = self.replace_local_images(html, data["files"])
		with tempfile.NamedTemporaryFile(
			delete=False, suffix=".html", mode="w", encoding="utf-8"
		) as tmp:
			tmp.write(html)
			return tmp.name

	def module_css_preview(self, source):
		styles = re.findall(
			r"(?:(?:\[\[module) (?:CSS|css)(?:(.+?)|)\]\]\n)((.|\n)+?)(?:\n\[\[\/module\]\])",
			source,
		)
		data = ""
		for style in styles:
			style = unicodedata.normalize("NFKD", style[1])
			data += f"<style>\n{style}\n</style>\n"
		return data

	def replace_local_images(self, source, files):
		images = re.findall(
			r"""(?<=(<img src="))(http://www.wdfiles.com/local--files//)(.+?)(?=")""",
			source,
		)
		for img in images:
			img = img[1:]
			if img[1] in files:
				source = source.replace(
					img[0] + img[1],
					f"data:{img[1].split('.')[1]}/;base64,{files[img[1]]}",
				)
		return source

	def includes(self, source, iteration=0):
		includes = re.findall(
			r"(\[\[include\s(?::.+?:|)(?:.+?:|)(?:.+)(?:\s((?:.|\n)+?)|)]])",
			source,
		)
		for include in includes:
			try:
				path = re.findall(
					r"(:.+?:|)(.+?:|)(.+)",
					include[0].split()[1].replace("]]",""),
				)[0]
				site = path[0].replace(":","")
				page = path[1]+path[2]
				wiki = pyscp.wikidot.Wiki(site)
				p = wiki(page).source
				args = [i[1:] if i.startswith("\n") else i for i in include[1].split("|")]
				if args[0] == "":
					args = []
				for arg in args:
					arg = re.findall(
						r"(?:([\w-]+)(?:(?:\s|)=(?:\s|))((?:.|\n+?)+))",
						arg,
					)[0]
					p = p.replace("{$"+arg[0]+"}",arg[1])
				source = source.replace(include[0],p)
			except Exception as e:
				log.error(e)
		if re.findall(
			r"(\[\[include(?:(?:.|\n)+?)]])",
			source,
		) and iteration != 10:
			source = self.includes(source, iteration+1)
		return source

	def iftags(self, source, tags):
		iftags = re.findall(
			r"(\[\[iftags (.+?)]]((?:(?:.|\n|\s)+?))\[\[\/iftags]])",
			source,
		)
		for iftag in iftags:
			match = True
			elem = re.findall(
				r"(\+.+?(?=\s|$)|-.+?(?=\s|$))",
				iftag[1]
			)
			for e in elem:
				if e.startswith("+"):
					if e[1:] not in tags:
						match = False
				else:
					if e[1:] in tags:
						match = False
			if match:
				source = source.replace(iftag[0],iftag[2])
		return source
	def preprocess(self, data):
		source = self.includes(data["source"])
		source = self.iftags(source,data["tags"])
		return source