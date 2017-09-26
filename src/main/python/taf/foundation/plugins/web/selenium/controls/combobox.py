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

from taf.foundation.api.ui.controls import ComboBox as IComboBox
from taf.foundation.plugins.web.selenium.controls.listitem import ListItem
from taf.foundation.plugins.web.selenium.support import ElementFinder
from taf.foundation.plugins.web.selenium.support import FindBy
from taf.foundation.plugins.web.selenium.webelement import WebElement


class ComboBox(WebElement, IComboBox):
    def __init__(self, element=None, **conditions):
        _arg_tag = 'tag'
        _arg_option = 'option'
        _arg_multi_selection = 'multiple'

        conditions.setdefault(_arg_tag, 'select')

        if _arg_option in conditions:
            self._option_tag = conditions.pop(_arg_option)
        else:
            self._option_tag = _arg_option

        if _arg_multi_selection in conditions:
            self._multi_attr = conditions.pop(
                _arg_multi_selection
            )
        else:
            self._multi_attr = _arg_multi_selection

        WebElement.__init__(
            self, element, **conditions
        )

        self._options = []

    def set(self, value):
        if isinstance(value, (list, tuple)):
            if not self.can_select_multiple:
                raise RuntimeError(
                    'Multi-selection is not supported'
                )
        else:
            value = [value]

        for val in value:
            if str(val).isdigit():
                self.options[int(val)].select()
                continue
            else:
                for opt in self.options:
                    if (
                                val == opt.current.get_attribute('value')
                    ) or (val == opt.object.text):
                        opt.select()
                        break
                else:
                    raise ValueError(
                        'Could not locate element with value: {}'.format(
                            val
                        )
                    )

    @property
    def value(self):
        if self.exists():
            return ';'.join(
                [
                    opt.object.text
                    for opt in self.options
                    if opt.is_selected
                ]
            )

        return r''

    @property
    def options(self):
        if self._options:
            return self._options

        if self.exists():
            for element in ElementFinder(
                    self.object
            ).find_elements(
                FindBy.TAG,
                self._option_tag
            ):
                self._options.append(
                    ListItem(element, parent=self)
                )

        return self._options

    @property
    def is_read_only(self):
        assert self.exists(), 'N/A - invisible element'

        return not self.object.is_enabled()

    @property
    def can_select_multiple(self):
        return self._get_attribute(
            self._multi_attr
        )

    @property
    def is_selection_required(self):
        return self._get_attribute('required')

    def _get_attribute(self, name):
        assert not self.is_read_only, \
            'N/A - disabled element'

        attr_value = self.object.get_attribute(
            name
        )
        return attr_value and attr_value != 'false'
