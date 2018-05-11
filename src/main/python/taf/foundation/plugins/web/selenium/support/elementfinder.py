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

from taf.foundation.api.ui.support import ElementFinder as IElementFinder
from taf.foundation.plugins.web.selenium.support.locator import Locator


class ElementFinder(IElementFinder):
    def __init__(self, anchor):
        super(ElementFinder, self).__init__(anchor)

    @property
    def elements_finding_strategies(self):
        return {
            Locator.ID: 'find_elements_by_id',
            Locator.XPATH: 'find_elements_by_xpath',
            Locator.NAME: 'find_elements_by_name',
            Locator.TAG: 'find_elements_by_tag_name',
            Locator.CSS: 'find_elements_by_css_selector',
            Locator.CLASSNAME: 'find_elements_by_class_name',
            Locator.TEXT: 'find_elements_by_link_text',
            Locator.TEXT_CONTAINS: 'find_elements_by_partial_link_text'
        }

    @property
    def excluded_screening_locators(self):
        return Locator.XPATH, Locator.CSS

    def find_elements(self, locator, value):
        return super(
            ElementFinder, self
        ).find_elements(
            locator, value
        )
