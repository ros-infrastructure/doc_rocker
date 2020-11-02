@{import os}@


# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.intersphinx', 'sphinx.ext.imgmath',
  'breathe',
  'exhale']

breathe_projects = { "@(package_name) Doxygen Project": "/output/generated/doxygen/xml" }
breathe_default_project = "@(package_name) Doxygen Project"

# Setup the exhale extension
import textwrap
exhale_args = {
    # These arguments are required
    "containmentFolder":     "./api",
    "rootFileName":          "library_root.rst",
    "rootFileTitle":         "Library API",
    "doxygenStripFromPath":  "..",
    # Suggested optional arguments
    "createTreeView":        True,
    # TIP: if using the sphinx-bootstrap-theme, you need
    # "treeViewIsBootstrap": True,
    "exhaleExecutesDoxygen": True,
    "exhaleDoxygenStdin":    textwrap.dedent("""
      INPUT = @(' '.join([os.path.join('package', d) for d in doxygen_inputs]))
      GENERATE_HTML          = YES
@(found_tag_files)@
      GENERATE_TAGFILE = "/output/generated/doxygen/@(package_name).tag"
      """)
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'@(package_name)'
# TODO(tfoote) The docs say year and author but we have this and it seems more relevant.
copyright = u'@(package_licenses)'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '@(package_short_version)'
# The full version, including alpha/beta/rc tags.
release = '@(package_version)'


# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['_build']


# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'



# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'default'


# Output file base name for HTML help builder.
htmlhelp_basename = '@(package_name)'



# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'http://docs.python.org/': None,
    'http://docs.opencv.org/3.0-last-rst/': None,
    'http://docs.scipy.org/doc/numpy' : None@(inventories)
    }

autoclass_content = "both"
