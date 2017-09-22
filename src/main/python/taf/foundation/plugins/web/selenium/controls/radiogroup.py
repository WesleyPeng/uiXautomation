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

from taf.foundation.api.controls import RadioGroup as IRadioGroup
from taf.foundation.plugins.web.selenium.controls.listitem import ListItem
from taf.foundation.plugins.web.selenium.support import ElementFinder
from taf.foundation.plugins.web.selenium.support import FindBy
from taf.foundation.plugins.web.selenium.webelement import WebElement


class RadioGroup(WebElement, IRadioGroup):
    def __init__(self, element=None, **conditions):
        _arg_tag = 'tag'
        _arg_option = 'option'

        conditions.setdefault(_arg_tag, 'form')

        if _arg_option in conditions:
            self._option_tag = conditions.pop(_arg_option)
        else:
            self._option_tag = 'input'

        WebElement.__init__(
            self, element, **conditions
        )

    def set(self, value):
        if str(value).isdigit() and (
                    int(value) < len(self.items)
        ):
            self.items[int(value)].select()
        else:
            for item in self.items:
                if (
                            value == item.current.get_attribute('value')
                ) or (value == item.object.text):
                    item.select()
                    break
            else:
                raise ValueError(
                    'Could not locate element with value: {}'.format(
                        value
                    )
                )

    @property
    def value(self):
        if self.exists():
            for item in self.items:
                if item.is_selected:
                    return item.object.get_attribute('value')

        return r''

    @property
    def items(self):
        _items = []

        if self.exists():
            for element in ElementFinder(
                    self.object
            ).find_elements(
                FindBy.XPATH,
                './/{}[@type="radio"]'.format(
                    self._option_tag
                )
            ):
                _items.append(
                    ListItem(element, parent=self)
                )

        return _items

    def _get_attribute(self, name):
        assert not self.is_read_only, \
            'N/A - disabled element'

        attr_value = self.object.get_attribute(
            name
        )
        return attr_value and attr_value != 'false'
