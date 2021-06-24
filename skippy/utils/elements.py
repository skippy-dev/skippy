from abc import ABCMeta, abstractmethod
try:
	from collections.abc import namedtuple
except ImportError:
	from collections import namedtuple

Field = namedtuple("Field","tag name description")

class Elements:
	elements = []

	@classmethod
	def register(cls, generator):
		cls.elements.append(generator)

#############################
# Elements Base
#############################
class BaseElement(metaclass=ABCMeta):
	__alias__ = ""
	__description__ = ""

	base = ""

	def __init__(self):
		self.requiredFieldList = []
		self.requiredFields()

	def checkRequiredArgs(self, args):
		for field in self.requiredFieldList:
			if field.tag not in args:
				raise TypeError(f"{self.__class__.__name__}.generate() don't received required argument: {field.tag}")

	@abstractmethod
	def requiredFields(self):
		pass

	def addField(self, tag, name="", description=""):
		self.requiredFieldList.append(Field(tag,name,description))

	def prepareArgs(self,args):
		return args

	def generate(self, **args):
		self.checkRequiredArgs(args)
		args = self.prepareArgs(args)

		data = self.base
		for name in args:
			data = data.replace(f"<<{name}>>",args[name])
		return data

class BaseComponent(BaseElement):
	component = ""
	base = "[[include <<component>> <<args>>]]"

	def prepareArgs(self,args):
		return {"component":self.component,"args":" |\n".join([f"{arg} = {args[arg]}" for arg in args if args[arg]])}

class BaseModule(BaseElement):
	module = ""
	base = "[[module <<module>> <<args>>]]\n<<content>>\n[[/module]]"

	def __init__(self):
		self.requiredFieldList = []
		self.addField("content", "Content", f"Module {self.module} Content")
		self.requiredFields()

	def prepareArgs(self,args):
		return {"module":self.module, "content": args["content"], "args": " ".join([f'{arg}="{args[arg]}"' for arg in args if arg != "content" and args[arg]])}


#############################
# Wikidot Modules
#############################
class ModuleCSS(BaseModule):
	__alias__ = "Module CSS"
	__description__ = "lets you insert CSS code into a wiki page. This is particularly useful for cross-site include (CSI) packages that need to use custom styling for their code. When you use the CSS module in a CSI, that CSS code will be included in all pages that use the CSI."

	module = "CSS"

	def requiredFields(self):
		self.addField("show", "Show CSS Code", 'You can render the module`s CSS code on the page in a [[code type="css"]] block by adding: show="true"')
		self.addField("disable", "Disable Module CSS", 'You can disable the module`s CSS code so that it doesn`t affect the theme by adding: disable="true"')

class ModuleListUsers(BaseModule):
	__alias__ = "Module ListUsers"
	__description__ = "produces formatted output that lets you report on a set of users working with a site."

	module = "ListUsers"

	def requiredFields(self): pass

	def prepareArgs(self,args):
		return {"module":self.module, "content": args["content"], "args": 'users="."'}

class ModuleListPages(BaseModule):
	__alias__ = "Module ListPages"
	__description__ = "is a general-purpose and widely-used tool that selects and display pages within a site."

	module = "ListPages"

	def requiredFields(self):
		#############################
		# Ordering pages
		#############################
		self.addField("order", "Order", "Specify order criteria")
		#############################
		# Pagination
		#############################
		self.addField("limit", "Limit", "Limit total items")
		self.addField("perPage", "Per page", "Limit per pagination")
		self.addField("reverse", "Reverse", "Show pages in reversed order")
		#############################
		# Module body
		#############################
		self.addField("separate", "Separate", "Separation specifier")
		self.addField("wrapper", "Wrapper", "Wrapper specifier")
		self.addField("prependLine", "Prepend Line", "Specify order criteria")
		self.addField("appendLine", "Append Line", "Footer specifier")
		#############################
		# Selecting pages
		#############################
		self.addField("pagetype", "Page type", "Select by type of page")
		self.addField("category", "Category", "Select by category")
		self.addField("tags", "Tags", "Select by tags")
		self.addField("parent", "Parent", "Select by parent page")
		self.addField("link_to", "Outgoing links", "Select by outgoing links")
		self.addField("created_at", "Created at", "Select by date of creation")
		self.addField("updated_at", "Updated at", "Select by date of update")
		self.addField("created_by", "Author", "Select by original author")
		self.addField("rating", "Rating", "Select by rating")
		self.addField("votes", "Votes", "Select by number of votes")
		self.addField("offset", "Offset", "Start list after an offset of pages")
		self.addField("range", "Range", "Select a range of pages")
		self.addField("name", "Page name", "Select by page name")
		self.addField("fullname", "Page fullname", "Select by fullname")

Elements.register(ModuleCSS)
Elements.register(ModuleListPages)
Elements.register(ModuleListUsers)