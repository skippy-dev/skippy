"""Elements core module

Attributes:
    elements (List[AbstractElement]): List of elements
"""
from skippy.api import Field

from abc import ABCMeta, abstractmethod
from typing import Dict, List


class AbstractElement(metaclass=ABCMeta):

    """Abstract element class
    
    Attributes:
        required_fields (List[Field]): List of element fields
    """
    
    __alias__: str
    __description__: str

    base: str

    def __init__(self):
        """Initializing element
        """
        self.required_fields: List[Field] = []
        self._init_fields()

    def check_args(self, args: Dict[str, str]):
        """Check required arguments
        
        Args:
            args (Dict[str, str]): Arguments for fields
        
        Raises:
            TypeError: Don't received required argument
        """
        for field in self.required_fields:
            if field.tag not in args:
                raise TypeError(
                    f"{self.__class__.__name__}.preview() don't received required argument: {field.tag}"
                )

    @abstractmethod
    def _init_fields(self):
        """Abstract init fields method
        """
        pass

    def add_field(self, tag: str, name: str = "", description: str = ""):
        """Add field to element
        
        Args:
            tag (str): Field tag
            name (str, optional): Field name
            description (str, optional): Field description
        """
        self.required_fields.append(Field(tag, name, description))

    def prepare_args(self, args: Dict[str, str]) -> Dict[str, str]:
        """Prepare arguments
        
        Args:
            args (Dict[str, str]): Arguments for fields
        
        Returns:
            Dict[str, str]: Prepared arguments
        """
        return args

    def preview(self, args: Dict[str, str]) -> str:
        """Preview element using arguments
        
        Args:
            args (Dict[str, str]): Arguments for fields
        
        Returns:
            str: Description
        """
        self.check_args(args)
        args = self.prepare_args(args)

        data = self.base
        for name in args:
            data = data.replace(f"<<{name}>>", args[name])
        return data


class AbstractComponent(AbstractElement):

    """Abstract included component
    """
    
    component: str
    base: str = "[[include <<component>> <<args>>]]"

    multiline: bool = True

    def prepare_args(self, args: Dict[str, str]) -> Dict[str, str]:
        """Prepare arguments

        Args:
            args (Dict[str, str]): Arguments for fields

        Returns:
            Dict[str, str]: Prepared arguments
        """
        next_line = "\n" if self.multiline else " "
        return {
            "component": self.component,
            "args": f" |{next_line}".join([f"{arg}={args[arg]}" for arg in args if args[arg]]),
        }


class BaseImageBlock(AbstractComponent):

    """Base image block
    """
    
    component: str = "component:image-block"

    multiline: bool = False

    align: str

    def _init_fields(self):
        """Initializing fields
        """
        self.add_field("name", "ELEMENTS.BASE_IMAGE.NAME.NAME", "ELEMENTS.BASE_IMAGE.NAME.DESC")
        self.add_field("caption", "ELEMENTS.BASE_IMAGE.CAPTION.NAME", "ELEMENTS.BASE_IMAGE.CAPTION.DESC")
        self.add_field("width", "ELEMENTS.BASE_IMAGE.WIDTH.NAME", "ELEMENTS.BASE_IMAGE.WIDTH.DESC")
        self.add_field("link", "ELEMENTS.BASE_IMAGE.LINK.NAME", "ELEMENTS.BASE_IMAGE.LINK.DESC")

    def prepare_args(self, args: Dict[str, str]) -> Dict[str, str]:
        """Prepare arguments

        Args:
            args (Dict[str, str]): Arguments for fields

        Returns:
            Dict[str, str]: Prepared arguments
        """
        args["align"] = self.align
        return super(BaseImageBlock, self).prepare_args(args)


class RightImageBlock(BaseImageBlock):

    """Right image block
    """
    
    __alias__: str = "ELEMENTS.RIGHT_IMAGE_BLOCK.ALIAS"
    __description__: str = "ELEMENTS.RIGHT_IMAGE_BLOCK.DESC"

    align: str = ""


class LeftImageBlock(BaseImageBlock):

    """Left image block
    """

    __alias__: str = "ELEMENTS.LEFT_IMAGE_BLOCK.ALIAS"
    __description__: str = "ELEMENTS.LEFT_IMAGE_BLOCK.DESC"

    align: str = "left"


class CenterImageBlock(BaseImageBlock):

    """Center image block
    """
    
    __alias__: str = "ELEMENTS.CENTER_IMAGE_BLOCK.ALIAS"
    __description__: str = "ELEMENTS.CENTER_IMAGE_BLOCK.DESC"

    align: str = "center"


class ACSBarComponent(AbstractComponent):

    """Anomaly Classification Bar component
    """

    __alias__: str = "ELEMENTS.ACS_BAR.ALIAS"
    __description__: str = "ELEMENTS.ACS_BAR.DESC"

    component: str = "component:anomaly-class-bar-source"

    def _init_fields(self):
        self.add_field("item-number", "ELEMENTS.ACS_BAR.ITEM.NAME", "ELEMENTS.ACS_BAR.ITEM.DESC")
        self.add_field("clearance", "ELEMENTS.ACS_BAR.CLEARANCE.NAME", "ELEMENTS.ACS_BAR.CLEARANCE.DESC")
        self.add_field("container-class", "ELEMENTS.ACS_BAR.CONTAINER.NAME", "ELEMENTS.ACS_BAR.CONTAINER.DESC")
        self.add_field("disruption-class", "ELEMENTS.ACS_BAR.DISRUPTION.NAME", "ELEMENTS.ACS_BAR.DISRUPTION.DESC")
        self.add_field("risk-class", "ELEMENTS.ACS_BAR.RISK.NAME", "ELEMENTS.ACS_BAR.RISK.DESC")
        self.add_field("secondary-class", "ELEMENTS.ACS_BAR.SEC_CLASS.NAME", "ELEMENTS.ACS_BAR.SEC_CLASS.DESC")
        self.add_field("secondary-icon", "ELEMENTS.ACS_BAR.SEC_ICON.NAME", "ELEMENTS.ACS_BAR.SEC_ICON.DESC")


elements: List[AbstractElement] = [RightImageBlock, LeftImageBlock, CenterImageBlock, ACSBarComponent]
