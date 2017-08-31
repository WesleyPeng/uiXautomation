# Copyright 2017 {Flair} WESLEY PENG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import yaml

from taf.common.api import Serializable


class YAMLData(yaml.YAMLObject, Serializable):
    """
    Recursive YAML Data Model
    """

    yaml_tag = '!YAMLData'

    def __init__(self, **kwargs):
        super(YAMLData, self).__init__()

        for key, value in kwargs.iteritems():
            self.__setitem__(key, value)

    def __setattr__(self, name, value):
        self[name] = value

    def __setitem__(self, key, value):
        assert (key is not None) and getattr(
            key, 'strip', lambda: None
        )()

        vars(self).update(
            **{key: YAMLData.normalize_data(
                value
            )}
        )

    def dump(self, path):
        try:
            data = vars(self).copy()

            for key, value in vars(self).iteritems():
                if hasattr(value, '__dict__') and (
                        not isinstance(value, yaml.YAMLObject)
                ):
                    delattr(data, key)

            with open(path, 'w') as stream:
                yaml.dump(data, stream)
        except Exception:
            raise

    @classmethod
    def load(cls, path):
        try:
            with open(path, 'r') as stream:
                data = yaml.load(stream)
        except IOError as ioe:
            data = dict(
                errno=ioe.errno,
                filename=ioe.filename,
                message=ioe.message,
                strerror=ioe.strerror
            )
        except Exception:
            raise

        return cls.normalize_data(data)

    @staticmethod
    def normalize_data(data):
        if isinstance(data, YAMLData):
            return data

        if hasattr(data, '__dict__'):
            return YAMLData(**vars(data))

        if hasattr(data, 'iteritems'):
            return YAMLData(**data)

        if hasattr(data, '__iter__'):
            _data = []

            for datum in data:
                _data.append(
                    YAMLData.normalize_data(datum)
                )

            return _data

        try:
            _data = yaml.safe_load(
                yaml.safe_dump(data)
            )
        except:
            raise

        return _data