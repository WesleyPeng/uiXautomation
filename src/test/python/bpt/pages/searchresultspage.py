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

from taf.foundation.api.ui.web import Page
from taf.modeling.web import WebLink


class SearchResultsPage(Page):
    def __init__(self, *elements, **conditions):
        super(SearchResultsPage, self).__init__(
            *elements, **conditions
        )

        self.lnk_first_record = WebLink(
            tag='a',
            xpath='//div[@id="b_content"]/ol[@id="b_results"]/li//a'
        )

    @property
    def text_of_first_record(self):
        return self.lnk_first_record.text
