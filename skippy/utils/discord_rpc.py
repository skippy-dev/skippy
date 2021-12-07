"""Discord Rich Presence
"""
from skippy.api import Singleton, ignore

from pypresence import PyPresenceException, Presence
from struct import error as StructError
import time


class DiscordRPC(Presence, metaclass=Singleton):

    """Discord Rich Presence class"""

    def __init__(self):
        """Init DiscordRPC"""
        super(DiscordRPC, self).__init__("828818867568640071")

        self._words = 0
        self._letters = 0
        self._time = int(time.mktime(time.localtime()))

    @ignore((PyPresenceException, StructError))
    def connect(self):
        """Connect to Discord RPC"""
        super(DiscordRPC, self).connect()
        self.update("SCP")

    @ignore((PyPresenceException, AssertionError))
    def update(self, title: str, words: int = 0, letters: int = 0):
        super(DiscordRPC, self).update(
            state=f"Words: {str(words)}, Letters: {str(letters)}",
            details=f"Writing an \"{title}\"",
            start=self._time,
            small_text="Skippy",
            small_image="none",
            large_text="Skippy",
            large_image="skippy",
        )

    @ignore((PyPresenceException, AssertionError))
    def close(self):
        """Close RPC connection"""
        super(DiscordRPC, self).close()
