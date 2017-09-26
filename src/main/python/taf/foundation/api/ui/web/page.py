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

from .browser import Browser


class Page(object):
    def __init__(self, parent=None):
        if parent:
            self._parent = parent
        elif Browser.cache:
            self._parent = Browser.cache.current
        else:
            raise RuntimeError('Web browser is required')

    @property
    def parent(self):
        return self._parent
