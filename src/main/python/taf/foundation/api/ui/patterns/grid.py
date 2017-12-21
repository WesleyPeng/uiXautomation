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

from .basepattern import BasePattern


class Grid(BasePattern):
    def get_cell(self, row, column):
        raise NotImplementedError(
            'Get the cell element by location'
        )

    @property
    def row_count(self):
        raise NotImplementedError(
            'Get row count'
        )

    @property
    def column_count(self):
        raise NotImplementedError(
            'Get column count'
        )
