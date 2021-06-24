import skippy.config

import json
import os


class Profile:
    @staticmethod
    def load():
        profile_path = os.path.join(skippy.config.PROPERTY_FOLDER, "profile.json")
        if os.path.exists(profile_path):
            with open(profile_path, "r") as f:
                profile = json.loads(f.read())
                return (profile["login"], profile["password"])
        return ("", "")

    @staticmethod
    def save(login, password):
        data = {"login": login, "password": password}
        profile = json.dumps(data)
        with open(
            os.path.join(skippy.config.PROPERTY_FOLDER, "profile.json"), "w"
        ) as f:
            f.write(profile)
