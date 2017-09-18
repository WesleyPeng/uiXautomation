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

from functools import reduce

from taf.foundation.plugins.web.selenium.support.findby import FindBy


class ElementFinder(object):
    BY = {
        FindBy.ID: 'find_elements_by_id',
        FindBy.XPATH: 'find_elements_by_xpath',
        FindBy.NAME: 'find_elements_by_name',
        FindBy.TAG: 'find_elements_by_tag_name',
        FindBy.CSS: 'find_elements_by_css_selector',
        FindBy.CLASSNAME: 'find_elements_by_class_name'
    }

    def __init__(self, anchor):
        self.anchor = anchor

    def find_elements(self, by=FindBy.ID, value=None):
        elements = []

        _invoker = getattr(
            self.anchor,
            ElementFinder.BY.get(by),
            None
        )

        if _invoker and callable(_invoker):
            elements.extend(_invoker(value))

        return elements

    def find_elements_by_conditions(
            self, **conditions
    ):
        elements = []

        for by, value in conditions.iteritems():
            elements = reduce(
                lambda accum, current:
                accum if current in accum
                else accum + [current],
                [elements, ] + self.find_elements(
                    by, value
                )
            )

        return elements

    def find_element(self, **conditions):
        for element in self.find_elements_by_conditions(
                **conditions
        ):
            for key, value in conditions.iteritems():
                _attr_value = element.get_attribute(
                    '{}'.format(key)
                ) or getattr(
                    element, '{}'.format(key), None
                )

                if key in (
                        FindBy.ID, FindBy.NAME,
                        FindBy.CLASSNAME, FindBy.TAG
                ) and _attr_value != value:
                    break
            else:
                break
        else:
            element = None

        return element
