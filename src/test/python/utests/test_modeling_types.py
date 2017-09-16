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

from unittest import TestCase

from taf.foundation.plugins.web.selenium.browser import Browser as SeBrowser
from taf.foundation.plugins.web.selenium.controls import Button as SeButton
from taf.modeling.web import Browser, WebButton


class TestModelingTypes(TestCase):
    def setUp(self):
        self.browser = Browser()

    def tearDown(self):
        self.browser.close()
        del self.browser

    def test_web_browser(self):
        self.assertTrue(
            issubclass(
                Browser,
                SeBrowser
            )
        )

        self.assertIsInstance(
            self.browser,
            SeBrowser
        )

    def test_web_button(self):
        self.assertTrue(
            issubclass(
                WebButton,
                SeButton
            )
        )

        self.browser.launch('http://www.bing.com')
        self.assertIsInstance(
            WebButton(),
            SeButton
        )
