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

from unittest import TestCase

from taf.foundation.plugins.cli.paramiko import SSHClient
from taf.modeling.cli import CLIRunner


class TestCLIRunner(TestCase):
    def setUp(self):
        self.hostname = 'localhost'
        self.username = 'username'
        self.password = 'password'

    def test_run_command(self):
        with CLIRunner(
            hostname=self.hostname,
            username=self.username,
            password=self.password
        ) as runner:
            self.assertIsInstance(
                runner,
                SSHClient
            )

            response = runner.run_command(
                'ls', '-lat'
            )
            self.assertEqual(
                len(response),
                2
            )
            self.assertEqual(
                response[-1],
                ''
            )
            self.assertIn(
                self.username,
                response[0]
            )
