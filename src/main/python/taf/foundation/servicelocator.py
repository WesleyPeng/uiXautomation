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

import glob
import imp
import inspect
import os

from taf.foundation.api.controls import Button
from taf.foundation.conf import Configuration
from taf.foundation.enums import Controls
from taf.foundation.enums import Plugins
from taf.foundation.plugins import WebPlugin


class ServiceLocator(object):
    _plugins = {}
    _aut = None
    _controls = {}

    def __init__(self, plugin=Plugins.Web):
        # self._load_aut()
        self._load_controls(plugin)

    def _load_controls(self, plugin):
        if not ServiceLocator._plugins:
            self._load_plugins()

        cls = ServiceLocator._plugins.get(plugin, None)

        if cls is None:
            raise TypeError('Unable to load plugin')

        for control in cls().controls:
            for func, key in {
                lambda ctrl: issubclass(ctrl, Button):
                    Controls.Button,
                # lambda ctrl: issubclass(ctrl, TextBox):
                #     Controls.TextBox
            }.iteritems():
                if func(control):
                    ServiceLocator._controls[key] = control
                    break

    def _load_plugins(self):
        _base_dir = os.path.join(
            os.path.dirname(__file__),
            'conf'
        )

        for _, plugin in vars(
                Configuration.get_instance().plugins
        ).iteritems():
            if plugin.enabled:
                for cls in self._inspect_classes(
                        os.path.abspath(
                            os.path.join(
                                _base_dir,
                                plugin.location
                            )
                        )
                ):
                    for func, key in {
                        lambda cls: issubclass(cls, WebPlugin):
                            Plugins.Web,
                        # lambda cls: issubclass(cls, DesktopPlugin):
                        #     Plugins.Desktop,
                    }.iteritems():
                        if func(cls):
                            ServiceLocator._plugins[key] = cls
                            break

    def _inspect_classes(self, plugin_dir):
        classes = []
        for py in self._find_python_files(plugin_dir):
            classes.extend(
                cls for cls in self._import_classes(py)
            )

        return classes

    def _find_python_files(self, plugin_dir):
        _cd = os.path.realpath(plugin_dir)

        files = [
            os.path.abspath(_file)
            for _file in glob.iglob(
                os.path.join(_cd, '*.py'))
        ]

        [
            files.extend(
                self._find_python_files(
                    os.path.join(_cd, _chdir)
                )
            )
            for _chdir in os.listdir(_cd)
            if os.path.isdir(os.path.join(_cd, _chdir))
        ]

        return files

    def _import_classes(self, location):
        path, filename = os.path.split(location)
        module_name = os.path.splitext(filename)[0]

        try:
            fp, imp_loc, desc = imp.find_module(
                module_name, [path]
            )
        except ImportError:
            return []

        try:
            try:
                module = imp.load_module(
                    module_name, fp, imp_loc, desc
                )
            except Exception:
                return []
        finally:
            if fp:
                fp.close()

        return [
            cls for _, cls in
            inspect.getmembers(
                module, predicate=inspect.isclass
            )
        ]

    @classmethod
    def get_control(
            cls,
            control_type,
            plugin=Plugins.Web
    ):
        if control_type not in Controls:
            raise TypeError('Unsupported Control Type')

        if not cls._controls:
            ServiceLocator(plugin)

        control = cls._controls.get(control_type, None)

        if not control:
            raise NotImplementedError(
                'Control Type - {}'.format(
                    control_type.name
                )
            )

        return control
