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

from taf.foundation.enums import Controls


class ServiceLocator(object):
    @classmethod
    def get_control(cls, control_type):
        if control_type not in Controls:
            raise TypeError('Unsupported Control Type')

        control = {}.get(control_type, None)

        if not control:
            raise NotImplementedError(
                'Control Type: {}'.format(control_type)
            )

        return control
