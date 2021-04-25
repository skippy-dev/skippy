from skippy.utils.logger import log
import skippy.config

import json
import os


class Session:
    def __init__(self, app):
        self.app = app
        self.tab = self.app.tab

        self.load()

    def get_session(self):
        session = {"session": []}
        for tab in range(self.tab.tabs.count()):
            widget = self.tab.tabs.widget(tab)
            if type(widget.data["tags"]) == str:
                widget.data["tags"] = widget.data["tags"].split()
            session["session"].append(widget.data)

        return session

    def set_session(self, session):
        self.tab.tabs.clear()
        for page in session["session"]:
            self.tab.new_tab(
                page["title"],
                page["source"],
                page["tags"],
                page["files"],
                page["parent"],
            )

    def save(self, path=os.path.join(skippy.config.PROPERTY_FOLDER, "session.json")):
        session = self.get_session()
        with open(path, "w") as f:
            f.write(json.dumps(session))
        log.debug(f"Save session to {path}")

    def load(self, path=os.path.join(skippy.config.PROPERTY_FOLDER, "session.json")):
        if os.path.exists(path):
            with open(path, "r") as f:
                session = f.read()
        else:
            session = ""
        if session != "":
            session = json.loads(session)
            self.set_session(session)
        log.debug(f"Load session from {path}")
