
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

    name = 'doc_rocker'

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
        snippet = pkgutil.get_data('doc_rocker', 'templates/%s_snippet.Dockerfile.em' % self.name).decode('utf-8')
        return em.expand(snippet, cliargs)

    def get_files(self, cliargs):
        all_files = {}
        all_files['build_docs.py'] = pkgutil.get_data('doc_rocker', 'files/build_docs.py').decode('utf-8')
        all_files['conf.py.em'] = pkgutil.get_data('doc_rocker', 'templates/conf.py.em').decode('utf-8')
        all_files['index.rst.em'] = pkgutil.get_data('doc_rocker', 'templates/index.rst.em').decode('utf-8')
        return all_files

    def get_docker_args(self, cliargs):
        args = ''
        #TODO(tfoote) a good exception here if the dir doesn't exist
        package_dir = cliargs.get('documentation-package-dir')
        output_dir = cliargs.get('output_dir')
        crossref_dir = cliargs.get('crossref_dir')
        # doc_root = cliargs.get('doc-root', None)
        args += '  -v %s:/doc_root/package' % package_dir
        if os.path.exists(output_dir) and not os.path.isdir(output_dir):
            print("ERROR output is not a directory")
        os.makedirs(output_dir, exist_ok=True)
        args += '  -v %s:/output' % output_dir
        args += '  -v %s:/crossref' % crossref_dir

        return args

    @staticmethod
    def register_arguments(parser, defaults={}):
        parser.add_argument('--doc_rocker',
            action='store_true',
            default=defaults.get('doc_rocker', False),
            help="Setup environment for doc_rocker")
        parser.add_argument('--output-dir',
            default='/tmp/package_docs',
            help="The directory into which to put the documentation.")
            # TODO(tfoote) add support for multiple crossref dirs
        parser.add_argument('--crossref-dir',
            help="The directories in which to find cross references.")
        parser.add_argument('--doxygen-inputs',
            nargs='+',
            help="The inputs for doxygen, relative to the package")
        parser.add_argument('--doc-root',
            help="The directory in which to put the generated document configs.")