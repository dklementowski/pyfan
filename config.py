import yaml, os

class ConfigNotFound(Exception):
    pass

class Config:
    CONFIG_DIRECTORIES=[
        "/usr/local/etc/pyfan",
        "/etc/pyfan",
    ]

    def __init__(self):
        self._data = None
        self.config_path = self.get_config_path()

        if self.config_path == None:
            raise ConfigNotFound()

    @property
    def data(self):
        if self._data == None:
            self.load()

        return self._data

    def load(self):
        with open(self.config_path, 'r') as yaml_file:
            self._data = yaml.load(yaml_file, Loader=yaml.FullLoader)

    def get_config_path(self):
        for directory in self.CONFIG_DIRECTORIES:
            target_path = os.path.join(directory, "pyfan.yml")
            if os.path.isfile(target_path):
                return target_path
