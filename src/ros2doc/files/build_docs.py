import subprocess
import yaml

# with open('build_config.yaml', 'r') as fh:
#     params = yaml.load(fh)

subprocess.check_call('mkdir -p /output/generated/doxygen/xml'.split())
subprocess.check_call('sphinx-build /doc_root /output'.split())