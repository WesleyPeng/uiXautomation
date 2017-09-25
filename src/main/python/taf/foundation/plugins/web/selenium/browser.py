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

from selenium import webdriver

from taf.foundation.api.web import Browser as IBrowser
from taf.foundation.plugins.web.selenium.support.browserwaiter import \
    BrowserWaiter


class Browser(IBrowser):
    def __init__(
            self,
            name='firefox',
            identifier=None
    ):
        super(Browser, self).__init__(
            name, identifier
        )

    @staticmethod
    def launch(url='about:blank', **kwargs):
        if not Browser.cache:
            Browser(
                kwargs.get('type'),
                kwargs.get('id')
            )

        Browser.cache.current.get(url)

        BrowserWaiter(
            Browser.cache.current,
            kwargs.get('timeout', 30.0)
        ).wait()

    def activate(self):
        super(Browser, self).activate()

        self.cache.current.switch_to.window(
            self.cache.current.current_window_handle
        )

    def maximize(self):
        self.cache.current.maximize_window()

    def _create_instance(self, browser_type):
        _browser_creation_strategies = {
            'ff': self._make_firefox,
            'firefox': self._make_firefox,
            'googlechrome': self._make_chrome,
            'chrome': self._make_chrome,
            'gc': self._make_chrome,
        }

        _creator = _browser_creation_strategies.get(
            browser_type.lower()
        )

        if not callable(_creator):
            raise ValueError('Unsupported browser type')

        _instance = _creator()
        _instance.get('about:blank')

        return _instance

    def _make_firefox(self):
        return webdriver.Firefox()

    def _make_chrome(self):
        return webdriver.Chrome
