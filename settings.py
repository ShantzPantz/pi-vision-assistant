import yaml

class ConfigSingleton:
    _instance = None

    def __new__(cls, defaults_yaml=None, overrides_yaml=None):
        if cls._instance is None:
            cls._instance = super(ConfigSingleton, cls).__new__(cls)
            cls._instance._config = cls._load_config(defaults_yaml, overrides_yaml)
        return cls._instance

    @staticmethod
    def _load_config(defaults_yaml, overrides_yaml):
        config = {}

        if defaults_yaml:
            with open(defaults_yaml, 'r') as stream:
                try:
                    defaults_config = yaml.safe_load(stream)
                    config.update(defaults_config)
                except yaml.YAMLError as exc:
                    print(exc)

        if overrides_yaml:
            with open(overrides_yaml, 'r') as stream:
                try:
                    overrides_config = yaml.safe_load(stream)
                    config.update(overrides_config)
                except yaml.YAMLError as exc:
                    print(exc)

        return config

    def get_property(self, property_name):
        return self._config.get(property_name, None)
    
    def get_open_ai_key(self):
        return self.get_property("api_key").get("api_key")
    
    def get_elevenlabs_key(self):
        return self.get_property("elevenlabs").get("api_key")
    
    def get_image_dir(self):
        return self.get_property("image_output_dir")

    def get_audio_dir(self):
        return self.get_property("audio_output_dir")
    
    def get_minimum_humans_required(self):
        return self.get_property("minimum_humans_required")