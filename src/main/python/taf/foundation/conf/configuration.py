# Copyright (c) 2017-2018 {Flair Inc.} WESLEY PENG
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

import os

from taf.foundation.utils import YAMLData


class Configuration(object):
    _instance = None
    _settings = None

    def __init__(self):
        if not Configuration._instance:
            Configuration._settings = YAMLData.load(
                os.path.join(
                    os.path.dirname(__file__),
                    'config.yml'
                )
            )

            Configuration._instance = self

    @classmethod
    def get_instance(cls):
        if not Configuration._instance:
            Configuration()

        return Configuration._instance

    @property
    def plugins(self):
        return self._settings.plugins

    def save_as(self, path):
        self.plugins.dump(path)
