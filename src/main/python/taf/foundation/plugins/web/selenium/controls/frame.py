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

from taf.foundation.api.ui.controls import Frame as IFrame
from taf.foundation.plugins.web.selenium.support.elementfinder import ElementFinder
from taf.foundation.plugins.web.selenium.support.locator import Locator
from taf.foundation.plugins.web.selenium.webelement import WebElement


class Frame(WebElement, IFrame):
    def __init__(self, *elements, **conditions):
        conditions.setdefault('tag', 'iframe')

        WebElement.__init__(
            self, *elements, **conditions
        )

    def __enter__(self):
        self.activate()

        return self

    def __exit__(self, *args):
        self.deactivate()

    def activate(self):
        if isinstance(self.parent, Frame):
            self.parent.activate()
        else:
            self.root.cache.current.switch_to.default_content()

        if self.exists():
            self.root.cache.current.switch_to.frame(
                self.object
            )

    def deactivate(self):
        if isinstance(self.parent, Frame):
            self.parent.activate()
        else:
            self.root.cache.current.switch_to.default_content()

    @property
    def items(self):
        if not self._children:
            self.activate()

            for element in ElementFinder(
                    self.object
            ).find_elements(Locator.XPATH, './/*'):
                self._children.add(
                    WebElement.create(element=element)
                )

        return (child for child in self._children)
