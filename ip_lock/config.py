"""YAML Config Parser."""

import yaml


class Config:
    """Converts YAML file into Config Object"""

    def __init__(self, args):
        with open(args.config) as f:
            self.__dict__.update(yaml.safe_load(f))
        self.__dict__.update(args.__dict__)
