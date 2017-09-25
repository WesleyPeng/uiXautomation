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

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement as SeElement

from taf.foundation.api.web import Page
from taf.foundation.api.web import WebElement as IWebElement
from taf.foundation.plugins.web.selenium.support import ElementFinder
from taf.foundation.plugins.web.selenium.support import FindBy
from taf.foundation.plugins.web.selenium.support.elementwaiter import \
    ElementWaiter


class WebElement(IWebElement):
    def __init__(self, element=None, **conditions):
        super(WebElement, self).__init__(
            element, **conditions
        )

    @property
    def parent(self):
        if self._parent:
            if isinstance(self._parent, Page):
                self._parent = self._parent.parent

            if isinstance(self._parent, WebElement):
                self._parent = self._parent.current

        return self._parent

    def activate(self):
        if self.exists():
            self._get_web_driver().execute_script(
                'arguments[0].focus();',
                self.object
            )

    def exists(self, timeout=30):
        _visible = False

        try:
            ElementWaiter(
                self._get_web_driver(), timeout
            ).wait()
        except:
            pass

        try:
            _visible = self.current.is_displayed()
        except:
            pass

        return _visible

    def _is_valid_element(self, element):
        return isinstance(element, SeElement)

    def _parse_conditions(self, **conditions):
        _conditions = {}

        for key, value in conditions.iteritems():
            try:
                key = FindBy[key.upper()]
            except:
                pass

            if key in FindBy:
                _conditions[key] = value

        if not _conditions:
            raise ValueError(
                'Unable to parse conditions'
            )

        return _conditions

    def _build_element_finder(self):
        return ElementFinder(self.parent).find_element

    def _get_web_driver(self):
        _driver = self.parent

        if isinstance(self._parent, WebElement):
            _driver = self._parent.parent

        if isinstance(_driver, WebDriver):
            return _driver
        else:
            raise ValueError(
                'Unable to identify the web driver'
            )
