import em
import os
import subprocess


from catkin_pkg.package import package_exists_at
from catkin_pkg.package import parse_package


def expand_templates(input_dir, output_dir, arg_dict):
    for f in ['conf.py', 'index.rst']:
        with open(os.path.join(input_dir, f + '.em'), 'r') as template:
            with open(os.path.join(output_dir, f), 'w') as output:
                output.write(em.expand(template.read(), arg_dict))


def aggregate_tag_files(dependencies):
    tagfiles = []
    # TODO(tfoote) add support for a few extra tag files ala https://en.cppreference.com/w/Cppreference:Archives
    for d in set(dependencies):
        tagfile = '/crossref/%s/generated/doxygen/%s.tag' % (d,d)
        if os.path.exists(tagfile):
            #TODO(tfoote) parameterize rosdistro and maybe whole link pattern
            tagfiles.append('      TAGFILES += "' + tagfile + '=http://docs.ros.org/en/latest/p/%s"' % d)
        else:
            print("No tag file found for dependency %s: %s" % (d, tagfile))
    # TODO(tfoote) tagfiles are broken by default with breathe + exhale need to find a workaround:
    # See: https://github.com/michaeljones/breathe/issues/328
    # and https://github.com/svenevs/exhale/issues/63
    return '' # Disabling tagfiles for now
    if tagfiles:
        return '\n'.join(tagfiles) + '\n'
    return ''


def aggregate_sphinx_inventories(dependencies):
    inventories = []
    # TODO(tfoote) add support for generics
    for d in set(dependencies):
        inventory = '/crossref/%s/objects.inv' % (d)
        if os.path.exists(inventory):
            #TODO(tfoote) parameterize rosdistro and maybe whole link pattern
            inventories.append('\'%s\': (\'http://docs.ros.org/en/latest/p/%s\', (\'%s\'))' % (d, d, inventory))
        else:
            print("No sphinx inventory file found for dependency %s: %s" % (d, inventory))
    return ',\n' + ',\n'.join(inventories)


def document_package(pkg_dir):
    args_dict = {}
    if not package_exists_at(pkg_dir):
        parser.error("No ROS package found at %s" % pkg_dir)
    package = parse_package(pkg_dir)
    args_dict['package_name'] = package.name
    args_dict['package_version'] = package.version
    args_dict['package_short_version'] = '.'.join(package.version.split('.')[0:2])
    args_dict['package_licenses'] = ', '.join(package.licenses)
    doxygen_inputs = [e.content for e in package.exports if e.tagname == 'doxygen_inputs']
    args_dict['doxygen_inputs'] = doxygen_inputs
    args_dict['found_tag_files'] = aggregate_tag_files([d.name for d in package.build_depends + package.build_export_depends])
    args_dict['inventories'] = aggregate_sphinx_inventories([d.name for d in package.build_depends + package.build_export_depends])
    
    sphinx_subprojects = ' '.join([e.content for e in package.exports if e.tagname == 'sphinx_subprojects'])

    expand_templates('/doc_root', '/doc_root', args_dict)

    subprocess.check_call('mkdir -p /output/generated/doxygen/xml'.split())
    subprocess.check_call(('sphinx-build /doc_root /output %s' % sphinx_subprojects).split())

if __name__ == '__main__':
    document_package('/doc_root/package')
