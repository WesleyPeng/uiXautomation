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


class UIElement(object):
    __slots__ = [
        '_current', '_root', '_parent',
        '_children', '_locators', '_constraints'
    ]

    def __init__(self, *elements, **conditions):
        self._current = None
        self._root = None
        self._parent = None
        self._children = set()
        self._locators = {}
        self._constraints = {}

        self.initialize(*elements, **conditions)

    def __iter__(self):
        return iter(self._children)

    def exists(self, timeout=30):
        """
        Identify if the UI element is presented
        :param timeout: Default timeout value in seconds
        :return: Boolean
        """
        self._sync(timeout)

        return self.object is not None

    def highlight(self):
        raise NotImplementedError(
            'Highlight element'
        )

    @classmethod
    def create(cls, **conditions):
        return cls(**conditions)

    # @classmethod
    # def compose(cls, *elements, **conditions):
    #     return cls(*elements, **conditions)

    @property
    def root(self):
        if not self._root:
            self._resolve_root()

        return self._root

    @property
    def parent(self):
        if not self._parent:
            self._resolve_parent()

        return self._parent

    @property
    def object(self):
        return self._current or self.current

    @property
    def current(self):
        if not self._locators:
            if not self._current:
                raise ValueError(
                    'Unable to find element without locator'
                )
        else:
            self._current = self._find_current_element()

        return self._current

    def initialize(self, *elements, **conditions):
        self._initialize_children(*elements)

        if 'element' in conditions:
            self._initialize_instant_element(
                conditions.pop('element')
            )

        if 'parent' in conditions:
            self._resolve_parent(
                conditions.pop('parent')
            )

        if not self._current:
            self._parse_conditions(
                **conditions
            )

    def _initialize_children(self, *elements):
        for element in elements:
            if not isinstance(element, UIElement):
                element = self.create(element=element)

            element._parent = self
            self._children.add(element)

    def _initialize_instant_element(self, element):
        if isinstance(element, UIElement):
            self._unwrap_element(element)
        else:
            self._wrap_element(element)

    def _unwrap_element(self, element):
        [
            setattr(
                self, prop, getattr(element, prop)
            ) for prop in self.__slots__
        ]

    def _wrap_element(self, element):
        raise NotImplementedError(
            'Raw UI element wrapper'
        )

    def _find_current_element(self):
        raise NotImplementedError(
            'Build UIElement by locator(s)'
        )

    def _resolve_parent(self, element=None):
        raise NotImplementedError(
            'UIElement logic parent'
        )

    def _resolve_root(self):
        raise NotImplementedError(
            'UIAutomation Driver'
        )

    def _parse_conditions(
            self, **conditions
    ):
        pass
        # raise NotImplementedError(
        #     'Identify locators and constraints'
        # )

    def _sync(self, timeout=30):
        import time

        _now = time.time()
        while self.current is None and (
                timeout > (time.time() - _now)
        ):
            time.sleep(1)
