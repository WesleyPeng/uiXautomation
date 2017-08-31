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

import os
import unittest

from taf.common.model import YAMLData


class TestYAMLData(unittest.TestCase):
    def test_dump_load(self):
        file_path = os.path.join(
            os.path.dirname(__file__),
            'data.yaml'
        )
        key = 'unittest'

        data = YAMLData(
            **{key: []}
        )
        data.dump(file_path)

        self.assertIsInstance(
            YAMLData.load(file_path),
            YAMLData
        )
        os.remove(file_path)

        value = 'dummy data'
        data[key] += [value]
        self.assertIn(
            value,
            data[key]
        )
        data.unittest.pop()

        data[key] = value
        self.assertEqual(
            getattr(data, key),
            value
        )

        data += {
            key: self._testMethodName,
            'other': 'any'
        }

        self.assertEqual(
            data[key],
            self._testMethodName
        )

        with self.assertRaises(ValueError):
            data += value

        with self.assertRaises(ValueError):
            data += [value]
