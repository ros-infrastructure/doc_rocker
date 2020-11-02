import argparse
import em
import os
import pkgutil
import shlex
import shutil
import tempfile

from rocker.core import DockerImageGenerator
from rocker.core import get_rocker_version
from rocker.core import RockerExtensionManager


def main():

    parser = argparse.ArgumentParser(
        description='Generate documentation for a specific package',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('documentation-package-dir')
    #parser.add_argument('command', nargs='*', default='')
    parser.add_argument('--nocache', action='store_true',
        help='Force a rebuild of the image')
    # parser.add_argument('--develop', action='store_true',
    #    help='Build the image locally not using the prebuilt image.')
    parser.add_argument('-v', '--version', action='version',
        version='%(prog)s ' + get_rocker_version())
    parser.add_argument('--debug-inside', action='store_true')
    # TODO(tfoote) add verbose parser.add_argument('--verbose', action='store_true')


    extension_manager = RockerExtensionManager()
    default_args = {'doc_rocker': True, 'user': True}
    extension_manager.extend_cli_parser(parser, default_args)

    args = parser.parse_args()
    args_dict = vars(args)
    args_dict['documentation-package-dir'] = os.path.abspath(args_dict['documentation-package-dir'])

    args_dict['command'] = 'python3 /doc_root/build_docs.py'

    active_extensions = extension_manager.get_active_extensions(args_dict)
    print("Active extensions %s" % [e.get_name() for e in active_extensions])

    dig = DockerImageGenerator(active_extensions, args_dict, 'ubuntu:focal')

    exit_code = dig.build(**vars(args))
    if exit_code != 0:
        print("Build failed exiting")
        return exit_code

    if args.debug_inside:
        args_dict['command'] = 'bash'

    print(args_dict)
    return dig.run(**args_dict)