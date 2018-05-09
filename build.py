"""
Extensible Test Automation Framework
"""

from pybuilder.core import init, use_plugin

use_plugin('python.core')
use_plugin('python.install_dependencies')
use_plugin('python.unittest')
# use_plugin('python.integrationtest')
use_plugin('python.distutils')

name = 'PyXTaf'
summary = 'Extensible Test Automation Framework'

default_task = [
    'clean',
    'install_build_dependencies',
    'publish'
]


@init
def initializer(project):
    project.version = '0.5.0'
    project.summary = summary
    project.description = __doc__

    project.build_depends_on('setuptools')
    project.build_depends_on('wheel')
    project.build_depends_on('pip')

    # project.build_depends_on_requirements(
    #     'src/main/python/requirements.dev.txt'
    # )
    project.depends_on_requirements(
        'src/main/python/requirements.txt'
    )

    # unit tests
    project.set_property(
        'dir_source_unittest_python',
        'src/test/python/ut'
    )

    project.set_property(
        'unittest_module_glob',
        'test_*'
    )

    project.set_property(
        'unittest_test_method_prefix',
        'test_'
    )

    # integration tests
    # project.set_property(
    #     "dir_source_integrationtest_python",
    #     "src/test/python/atests"
    # )
    # project.set_property(
    #     "integrationtest_file_glob",
    #     "test_*"
    # )
    #
    # project.set_property(
    #     "integrationtest_inherit_environment",
    #     True
    # )

    # project.set_property(
    #     'dir_source_main_python',
    #     'src/main/python'
    # )
    project.set_property(
        'dir_source_main_scripts',
        None
    )
    project.set_property(
        'dir_dist_scripts',
        None
    )
    project.set_property('dir_target', 'build')
    project.set_property('dir_dist', 'dist')

    exclude = (
        ''
    )
    packages = project.list_packages()

    def list_packages():
        for pkg in packages:
            for ex in exclude:
                if ex in pkg:
                    break
            else:
                yield pkg

    project.list_packages = list_packages
    project.list_modules = lambda: ''

    project.set_property(
        'distutils_use_setuptools', True
    )
    project.set_property(
        'distutils_setup_keywords',
        'Automation Framework'
    )
    project.set_property(
        'distutils_classifiers', []
    )
    project.set_property(
        'distutils_commands', ['bdist_wheel']
    )
