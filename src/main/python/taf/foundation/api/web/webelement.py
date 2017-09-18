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

from taf.foundation.api import UIElement
from .page import Page


class WebElement(UIElement):
    def __init__(self, element=None, **conditions):
        super(WebElement, self).__init__(element)

        self._conditions = {}
        self._finder = None
        self._initialize(element, **conditions)

    @property
    def current(self):
        if self._finder and self._conditions:
            self._current = self._finder(
                **self._conditions
            )

        return self._current

    @property
    def object(self):
        return self._current or self.current

    def _initialize(self, element=None, **conditions):
        if 'parent' in conditions:
            self._parent = conditions.pop('parent')

        if not self._parent:
            self._parent = Page()

        if not self._current:
            if not (element or conditions):
                raise ValueError(
                    'Unable to initialize the element'
                )

            if self._is_valid_element(element):
                self._wrap_element(element)
            else:
                self._conditions = self._parse_conditions(
                    **conditions
                )
                self._finder = self._build_element_finder()

    def _is_valid_element(self, element):
        return isinstance(element, WebElement)

    def _wrap_element(self, element):
        self._current = element

    def _parse_conditions(self, **conditions):
        raise NotImplementedError(
            'Parse conditions'
        )

    def _build_element_finder(self):
        raise NotImplementedError(
            'Build web element locator'
        )
