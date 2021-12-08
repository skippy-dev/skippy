"""Singleton facade for pyscp module.
"""
from skippy.api import Singleton, PageData, critical, ignore

from urllib.parse import urlparse
from pyscp.wikidot import Wiki
from typing import Optional
import requests
import base64


RequestException = requests.exceptions.RequestException


class SCPClient(metaclass=Singleton):

    """Singleton facade for pyscp module."""

    def __init__(self, login: Optional[str] = None, password: Optional[str] = None):
        """Initialize SCPClient.

        Args:
            login (Optional[str], optional): User login
            password (Optional[str], optional): User password
        """
        self._session = None

        if login and password:
            self.auth(login, password)

    @critical
    @ignore(RequestException)
    def auth(self, login: str, password: str):
        """Retrieving Wikidot Session from Credentials.

        Args:
            login (str): User login
            password (str): User password
        """
        wikidot = Wiki("www.wikidot.com")
        wikidot.auth(login, password)

        self._session = wikidot.cookies

    @critical
    @ignore(RequestException)
    def get_wiki(self, site: str) -> Wiki:
        """Get Wiki object instance by Wikidot site name with current session cookies.

        Args:
            site (str): Wikidot site name

        Returns:
            Wiki: Wiki object instance with current session cookies
        """
        wiki = Wiki(site)
        if self._session:
            wiki.cookies = self._session

        return wiki

    @staticmethod
    def download_file(url: str):
        with requests.get(url) as res:
            return base64.b64encode(res.content).decode("utf-8")

    @critical
    @ignore(RequestException)
    def upload(self, page: PageData, comment: str = "Edit using Skippy"):
        """Upload page with tags and files to selected Wikidot site.

        Args:
            page (PageData): Page for given Wikidot site
            comment (str, optional): Comment for uploaded changes
        """
        wiki = self.get_wiki(page["link"][0])
        p = wiki(page["link"][1])

        try:
            p.edit(title=page["title"], source=page["source"], comment=comment)
        except AttributeError:
            p.create(title=page["title"], source=page["source"], comment=comment)

        p.set_tags(page["tags"])

        file_urls = {file.name: file.url for file in p.files}

        for file in page["files"]:
            file_source = base64.b64decode(page["files"][file])
            if file not in file_urls:
                p.upload(file, file_source)
            elif file in file_urls and page["files"][file] != self.download_file(
                file_urls[file]
            ):
                p.remove_file(file)
                p.upload(file, file_source)

        for file in p.files:
            name = file.name
            if name not in page["files"]:
                p.remove_file(name)

    @ignore(Exception, {})
    @ignore(RequestException)
    def download(self, site: str, page: str) -> PageData:
        """Download page with tags and files fron selected Wikidot site.

        Args:
            site (str): Wikidot site name
            page (str): Page for given Wikidot site

        Returns:
            PageData: Page data
        """
        wiki = self.get_wiki(site)
        p = wiki(page)

        files = {file.name: self.download_file(file.url) for file in p.files}
        return {
            "title": p.title,
            "source": p.source,
            "tags": list(p.tags),
            "files": files,
            "link": (urlparse(wiki.site).netloc, page),
        }
