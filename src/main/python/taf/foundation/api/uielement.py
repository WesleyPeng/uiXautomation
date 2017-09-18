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


class UIElement(object):
    def __init__(self, element=None):
        self._parent = getattr(
            element, 'parent', None
        )
        self._current = getattr(
            element, 'current', None
        )

    def exists(self, timeout=30):
        """
        Identify if the UI element is presented
        :param timeout: Default timeout value in seconds
        :return: Boolean
        """
        return self._current is not None

    @property
    def parent(self):
        return self._parent

    @property
    def current(self):
        return self._current
