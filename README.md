# Prototype for ROS 2 documentatoin

## Prerequisites

This package needs a rocker with https://github.com/osrf/rocker/tree/support_file_injection patch.

It's recommended to create a venv and pip install the above and then use this repo in develop mode. 

The package.xml needs a little bit of metadata: 
https://github.com/ros2/geometry2/pull/339

Some extra smarts to guess paths w/o the explicit metadata could be done.

## Examples of running

To 

    doc_rocker_package ../geometry2_clean/tf2 --output /tmp/docs/tf2 --cross /tmp/docs

    doc_rocker_package ../geometry2_clean/tf2_ros --output /tmp/docs/tf2_ros --cross /tmp/docs

### Debugging

If you add `--debug` to the command line above it will create the environment and drop you into a bash shell. 
To invoke the standard entrypoint at that point just run `python3 build_docs.py`

It will generate the `conf.py` and `index.rst` and then invoke sphinx. As well as create a few directories that sphinx will crash if they aren't there.



## Known issues

* Breathe and Exhale have problems with tagfiles. See: https://github.com/michaeljones/breathe/issues/32 and https://github.com/svenevs/exhale/issues/63
* Moving the exhale generation to anything but a single layer directory doesn't seem to work.
* You are supposed to be able to invoke sphinx with additional subprojets with subsequent arguments to sphinx-build but that seems to break the exhale generation.

## Next steps
* This needs to be parameterized on the rosdistro.
* Support finding and iterating over packages in a workspace and interacting with the build system to generate content prior to documentation.
* Add an easy way to pull tagfiles and other resources locally for use in generation.

