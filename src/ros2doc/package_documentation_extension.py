
# Copyright 2020 Open Source Robotics Foundation

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from argparse import ArgumentTypeError
import em
import os
import pkgutil
import shlex


from rocker.extensions import RockerExtension


class ROS2Doc(RockerExtension):

    name = 'ros2doc'

    @classmethod
    def get_name(cls):
        return cls.name

    def precondition_environment(self, cli_args):
        pass

    def validate_environment(self, cli_args):
        pass

    def get_preamble(self, cli_args):
        return ''

    def get_snippet(self, cliargs):
        snippet = pkgutil.get_data('ros2doc', 'templates/%s_snippet.Dockerfile.em' % self.name).decode('utf-8')
        return em.expand(snippet, cliargs)

    def get_files(self, cliargs):
        all_files = {}
        all_files['build_docs.py'] = pkgutil.get_data('ros2doc', 'files/build_docs.py').decode('utf-8')
        all_files['conf.py'] = em.expand(pkgutil.get_data('ros2doc', 'templates/conf.py.em').decode('utf-8'), cliargs)
        all_files['index.rst'] = em.expand(pkgutil.get_data('ros2doc', 'templates/index.rst.em').decode('utf-8'), cliargs)
        # all_files['build_config.yaml'] = em.expand(pkgutil.get_data('ros2doc', 'templates/build_config.yaml.em').decode('utf-8'), cliargs)
        return all_files

    def get_docker_args(self, cliargs):
        args = ''
        #TODO(tfoote) a good exception here if the dir doesn't exist
        package_dir = cliargs.get('documentation-package-dir', None)
        # doc_root = cliargs.get('doc-root', None)
        args += '  -v %s:/doc_root/package' % package_dir
        #TODO(tfoote!!!!) hardcoded
        args += '  -v /home/tfoote/output:/output'
        # args += '  -v %s:/doc_root' % doc_root

        return args

    @staticmethod
    def register_arguments(parser, defaults={}):
        parser.add_argument('--ros2doc',
            action='store_true',
            default=defaults.get('ros2doc', False),
            help="Setup environment for ros2doc")
        parser.add_argument('--documentation-package-dir',
            help="The directory in which the package is to document.")
        parser.add_argument('--crossref-dirs',
            nargs='+',
            help="The directories in which to find cross references.")
        parser.add_argument('--sphinx-subprojects',
            nargs='+',
            default = [],
            help="The directories in which to find sphinx subprojects. TODO(tfoote) Do not use breaks exhale output of doxygen content")
        parser.add_argument('--sphinx-output-dir',
            help="The directory in which to put the sphinx output.")
        parser.add_argument('--doxygen-inputs',
            nargs='+',
            help="The inputs for doxygen, relative to the package")
        parser.add_argument('--doc-root',
            help="The directory in which to put the generated document configs.")