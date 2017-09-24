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

from collections import namedtuple

from taf.foundation.api.controls import RadioGroup as IRadioGroup
from taf.foundation.plugins.web.selenium.controls.listitem import ListItem
from taf.foundation.plugins.web.selenium.support import ElementFinder
from taf.foundation.plugins.web.selenium.support import FindBy
from taf.foundation.plugins.web.selenium.webelement import WebElement

RadioButton = namedtuple(
    'RadioButton', ['name', 'element']
)


class RadioGroup(WebElement, IRadioGroup):
    def __init__(self, element=None, **conditions):
        _arg_tag = 'tag'
        _arg_option = 'option'
        _arg_opt_label_tag = 'label'

        conditions.setdefault(_arg_tag, 'form')

        if _arg_option in conditions:
            self._option_tag = conditions.pop(_arg_option)
        else:
            self._option_tag = 'input'

        if _arg_opt_label_tag in conditions:
            self._opt_label_tag = conditions.pop(_arg_opt_label_tag)
        else:
            self._opt_label_tag = 'label'

        WebElement.__init__(
            self, element, **conditions
        )

        self._items = []

    def set(self, value):
        if str(value).isdigit() and (
                    int(value) < len(self.items)
        ):
            self.items[int(value)].element.select()
        else:
            for item in self.items:
                if (
                            value == item.element
                                .current.get_attribute('value')
                ) or (value == item.name):
                    item.element.select()
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
                if item.element.is_selected:
                    return item.name

        return r''

    @property
    def items(self):
        if self._items:
            return self._items

        if self.exists():
            _input_elements = ElementFinder(
                self.object
            ).find_elements(
                FindBy.XPATH,
                './/{}[@type="radio"]'.format(
                    self._option_tag
                )
            )
            _label_elements = ElementFinder(
                self.object
            ).find_elements(
                FindBy.XPATH,
                './/{}'.format(self._opt_label_tag)
            )

            for index, element in enumerate(_input_elements):
                self._items.append(
                    RadioButton(
                        _label_elements[index].text.strip(),
                        ListItem(element, parent=self)
                    )
                )

        return self._items
