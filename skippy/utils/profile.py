import skippy.config

import json
import os

class Profile:
    @staticmethod
    def load():
        try:
            with open(os.path.join(skippy.config.PROPERTY_FOLDER, 'profile.json'), 'r') as f:
                profile = json.loads(f.read())
            
            return (profile['login'], profile['password'])
        except json.decoder.JSONDecodeError:
            return ('','')

    @staticmethod
    def save(login,password):
        data = {'login': login, 'password': password}
        profile = json.dumps(data)
        with open(os.path.join(skippy.config.PROPERTY_FOLDER, 'profile.json'), 'w') as f:
            f.write(profile)