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

from taf.foundation.utils import ConnectionCache


class AUT(object):
    cache = None
    current = None

    def __init__(
            self,
            name=None,
            identifier=None,
            **kwargs
    ):
        if not AUT.cache:
            AUT.cache = ConnectionCache(identifier)

        self.id = self.cache.register(
            self._create_instance(name, **kwargs),
            identifier
        )

        AUT.current = self

    @staticmethod
    def launch(app_location, **kwargs):
        raise NotImplementedError(
            'Launch application'
        )

    def activate(self):
        if self.id != self.cache.current_key:
            self.cache.current_key = self.id

            AUT.current = self

    def take_screenshot(self):
        self.activate()

        return self.get_screenshot_data()

    def close(self):
        self.cache.close(self.id)

        if not self.cache.current:
            AUT.cache = None
            AUT.current = None

    def get_screenshot_data(self):
        raise NotImplementedError(
            'Get screenshot data from AUT'
        )

    def _create_instance(self, name, **kwargs):
        raise NotImplementedError(
            'Create instance of AUT'
        )
