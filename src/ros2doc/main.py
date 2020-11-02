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
    # TODO(tfoote) add prebuilt images for faster operations 
    # parser.add_argument('--develop', action='store_true',
    #    help='Build the image locally not using the prebuilt image.')
    parser.add_argument('--cross-ref-paths', action='store',
        nargs='+')
    parser.add_argument('-v', '--version', action='version',
        version='%(prog)s ' + get_rocker_version())
    parser.add_argument('--debug-inside', action='store_true')
    # TODO(tfoote) add verbose parser.add_argument('--verbose', action='store_true')


    extension_manager = RockerExtensionManager()
    default_args = {'ros2doc': True, 'user': True}
    extension_manager.extend_cli_parser(parser, default_args)

    args = parser.parse_args()
    args_dict = vars(args)
    args_dict['documentation-package-dir'] = os.path.abspath(args_dict['documentation-package-dir'])


    # temp_root_dir = None
    # if not args_dict.get('doc-root', None):
    #     # TODO(tfoote) cleanup using a context
    #     temp_root_dir = tempfile.TemporaryDirectory()
    #     args_dict['doc-root'] = temp_root_dir.name


    # conf_template = pkgutil.get_data('ros2doc', 'templates/conf.py.em').decode('utf-8')
    # with open(os.path.join(temp_root_dir.name, 'conf.py'), 'w') as confpy:
    #     confpy.write(em.expand(conf_template, args_dict))

    # index_template = pkgutil.get_data('ros2doc', 'templates/index.rst.em').decode('utf-8')
    # with open(os.path.join(temp_root_dir.name, 'index.rst'), 'w') as indexrst:
    #     indexrst.write(em.expand(index_template, args_dict))

    # package_dir = args_dict.get('documentation-package-dir', None)
    # shutil.copytree(package_dir, os.path.join(temp_root_dir.name, 'package'))

    # if args.build_only:
    #     args_dict['command'] = 'jekyll build -V --trace'
    #     del args_dict['network']
    # else:
    #     args_dict['command'] = 'jekyll serve -w'
    #     if args.baseurl is not None:
    #         # Don't output to the default location if generating using a modified baseurl
    #         args_dict['command'] += ' --baseurl=\'{baseurl}\' -d /tmp/aliased_site'.format(**args_dict)

    subprojects = ''
    if 'sphinx_subprojects' in args_dict:
        subprojects = ' '.join([os.path.join('/doc_root/package', sp) for sp in args_dict.get('sphinx_subprojects', [])])
    args_dict['command'] = 'sphinx-build /doc_root /output %s' % subprojects
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