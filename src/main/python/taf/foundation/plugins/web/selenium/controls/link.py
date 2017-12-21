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

from taf.foundation.api.ui.controls import Link as ILink
from taf.foundation.plugins.web.selenium.webelement import WebElement


class Link(WebElement, ILink):
    @property
    def enabled(self):
        if self.exists():
            return self.object.is_enabled()

        return False

    def click(self):
        assert self.enabled, 'NA - disabled element'

        self.object.click()

    def get_selection(self):
        raise RuntimeError(
            'Unsupported feature for web element'
        )

    @property
    def text(self):
        if self.exists():
            return self.object.text

        return r''

    @property
    def supports_text_selection(self):
        return True
