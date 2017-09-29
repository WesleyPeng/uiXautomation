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

from taf.foundation.api.plugins import CLIPlugin
from taf.foundation.api.plugins import RESTPlugin
from taf.foundation.api.plugins import WebPlugin
from taf.foundation.api.ui import AUT
from taf.foundation.api.ui.controls import Button
from taf.foundation.api.ui.controls import CheckBox
from taf.foundation.api.ui.controls import ComboBox
from taf.foundation.api.ui.controls import Edit
from taf.foundation.api.ui.controls import Link
from taf.foundation.api.ui.controls import RadioGroup
from taf.foundation.api.ui.controls import Table
from taf.foundation.conf import Configuration
from taf.foundation.enums import Controls
from taf.foundation.enums import Plugins


class ServiceLocator(object):
    _plugins = {}
    _aut = None
    _controls = {}
    _clients = {}

    def __init__(self):
        if not ServiceLocator._plugins:
            self._load_plugins()

    @classmethod
    def get_app_under_test(
            cls,
            plugin=Plugins.WEB
    ):
        if not cls._aut:
            ServiceLocator._aut = \
                cls._get_instance_by_plugin_type(
                    plugin
                ).app_under_test

        assert (cls._aut is not None) and issubclass(
            cls._aut, AUT
        )

        return cls._aut

    @classmethod
    def get_modeled_control(
            cls,
            control_type,
            plugin=Plugins.WEB
    ):
        if control_type not in Controls:
            raise TypeError('Unsupported Control Type')

        if not cls._controls:
            cls._inspect_controls(plugin)

        control = cls._controls.get(control_type, None)

        if not control:
            raise NotImplementedError(
                'Control Type - {}'.format(
                    control_type.name
                )
            )

        return control

    @classmethod
    def get_client(
            cls,
            plugin=Plugins.CLI
    ):
        if plugin not in cls._clients:
            _instance = cls._get_instance_by_plugin_type(
                plugin
            )

            assert hasattr(_instance, 'client')

            ServiceLocator._clients[plugin] = _instance.client

        return cls._clients.get(plugin)

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
                        lambda cls_: issubclass(cls_, WebPlugin) and (
                                    cls_ is not WebPlugin
                        ): Plugins.WEB,
                        lambda cls_: issubclass(cls_, CLIPlugin) and (
                                    cls_ is not CLIPlugin
                        ): Plugins.CLI,
                        lambda cls_: issubclass(cls_, RESTPlugin) and (
                                    cls_ is not RESTPlugin
                        ): Plugins.REST,
                    }.iteritems():
                        if func(cls):
                            ServiceLocator._plugins[key] = cls
                            break

    def _inspect_classes(self, plugin_dir):
        classes = []

        try:
            for py in self._find_python_files(plugin_dir):
                classes.extend(
                    cls for cls in self._import_classes(py)
                )
        except Exception:
            raise

        return classes

    def _find_python_files(self, directory):
        _cd = os.path.realpath(directory)

        files = [
            os.path.abspath(_file)
            for _file in glob.iglob(
                os.path.join(_cd, '*.py'))
        ]

        for _chdir in os.listdir(_cd):
            if os.path.isdir(
                    os.path.join(_cd, _chdir)
            ):
                files.extend(
                    self._find_python_files(
                        os.path.join(_cd, _chdir)
                    )
                )

        return files

    def _import_classes(self, location):
        fp, classes = None, []

        try:
            path, filename = os.path.split(location)
            module_name = os.path.splitext(filename)[0]

            fp, imp_loc, desc = imp.find_module(
                module_name, [path]
            )
        except Exception:
            raise
        else:
            try:
                module = imp.load_module(
                    module_name, fp, imp_loc, desc
                )

                classes.extend(
                    cls for _, cls in inspect.getmembers(
                        module,
                        predicate=inspect.isclass
                    )
                )
            except (ValueError, ImportError):
                raise
            except Exception:
                pass
        finally:
            if fp:
                fp.close()

        return classes

    @classmethod
    def _inspect_controls(cls, plugin):
        _instance = cls._get_instance_by_plugin_type(plugin)

        for control in _instance.controls:
            for func, key in {
                lambda ctrl: issubclass(ctrl, Button):
                    Controls.Button,
                lambda ctrl: issubclass(ctrl, CheckBox):
                    Controls.CheckBox,
                lambda ctrl: issubclass(ctrl, ComboBox):
                    Controls.ComboBox,
                lambda ctrl: issubclass(ctrl, Edit):
                    Controls.TextBox,
                lambda ctrl: issubclass(ctrl, Link):
                    Controls.Link,
                lambda ctrl: issubclass(ctrl, RadioGroup):
                    Controls.RadioGroup,
                lambda ctrl: issubclass(ctrl, Table):
                    Controls.Table,
            }.iteritems():
                if func(control):
                    ServiceLocator._controls[key] = control
                    break

    @classmethod
    def _get_instance_by_plugin_type(cls, plugin):
        if not ServiceLocator._plugins:
            ServiceLocator()

        cls_plugin = ServiceLocator._plugins.get(
            plugin, None
        )

        if cls_plugin is None:
            raise TypeError(
                'Unable to load {} plugin'.format(
                    plugin
                )
            )

        return cls_plugin()
