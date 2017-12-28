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

from collections import namedtuple

from taf.foundation.api.ui.controls import RadioGroup as IRadioGroup
from taf.foundation.plugins.web.selenium.controls.edit import Edit
from taf.foundation.plugins.web.selenium.controls.listitem import ListItem
from taf.foundation.plugins.web.selenium.support.elementfinder import \
    ElementFinder
from taf.foundation.plugins.web.selenium.support.findby import FindBy
from taf.foundation.plugins.web.selenium.webelement import WebElement

RadioButton = namedtuple(
    'RadioButton', ['option', 'label']
)


class RadioGroup(WebElement, IRadioGroup):
    def __init__(self, element=None, **conditions):
        _arg_tag = 'tag'
        _arg_option = 'option'
        _arg_opt_label = 'label'

        conditions.setdefault(_arg_tag, 'form')

        if _arg_option in conditions:
            self._option_tag = conditions.pop(_arg_option)
        else:
            self._option_tag = 'input'

        if _arg_opt_label in conditions:
            self._label_tag = conditions.pop(_arg_opt_label)
        else:
            self._label_tag = _arg_opt_label

        WebElement.__init__(
            self, element, **conditions
        )

        self._items = []

    def set(self, value):
        if str(value).isdigit() and (
                    int(value) < len(self.items)
        ):
            self.items[int(value)].option.select()
        else:
            for item in self.items:
                if (
                            value == item.option.current.get_attribute('value')
                ) or (value == item.label.text):
                    item.option.select()
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
                if item.option.is_selected:
                    return item.label.text

        return r''

    @property
    def items(self):
        if self._items:
            return self._items

        if self.exists():
            _options = ElementFinder(
                self.object
            ).find_elements(
                FindBy.XPATH,
                './/{}[@type="radio"]'.format(
                    self._option_tag
                )
            )
            _labels = ElementFinder(
                self.object
            ).find_elements(
                FindBy.XPATH,
                './/{}'.format(self._label_tag)
            )

            for index, element in enumerate(_options):
                self._items.append(
                    RadioButton(
                        ListItem(element, parent=self),
                        Edit(_labels[index], parent=self)
                    )
                )

        return self._items
