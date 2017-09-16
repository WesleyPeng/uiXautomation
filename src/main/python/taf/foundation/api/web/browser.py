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

from taf.foundation.api import AUT
from taf.foundation.utils import ConnectionCache


class Browser(AUT):
    cache = None

    def __init__(
            self,
            name='firefox',
            identifier=None
    ):
        Browser.cache = ConnectionCache(
            identifier
        )

        self.name = name
        self.id = Browser.cache.register(
            self._create_instance(self.name),
            identifier
        )

    @staticmethod
    def launch(url='about:blank', **kwargs):
        raise NotImplementedError(
            'Web browser navigates to specific page'
        )

    def close(self):
        self.cache.close(self.id)
        Browser.cache = None

    def _create_instance(
            self,
            browser_type
    ):
        raise NotImplementedError(
            'Create web browser instance (type={})'.format(
                browser_type
            )
        )
