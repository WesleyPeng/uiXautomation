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

import os
from unittest import TestCase

from taf.foundation.conf import Configuration
from taf.foundation.utils import YAMLData


class TestConfiguration(TestCase):
    def setUp(self):
        self.conf = Configuration()

    def test_configuration(self):
        self.assertIs(
            self.conf.get_instance(),
            Configuration.get_instance()
        )

        self.assertIsInstance(
            Configuration.get_instance().plugins,
            YAMLData
        )

        _conf_file = 'test_config.yml'
        _conf_key = 'test_config_dummy_key'
        _conf_value = 'enabled'

        plugins = Configuration.get_instance().plugins
        plugins += {
            _conf_key: _conf_value
        }

        self.conf.save_as(_conf_file)

        self.assertTrue(
            os.path.isfile(_conf_file)
        )
        with open(_conf_file, 'r') as conf:
            for line in conf:
                if (_conf_key in line) and (_conf_value in line):
                    found = True
                    break
            else:
                found = False
        self.assertTrue(found)

        os.remove(_conf_file)
