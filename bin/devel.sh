# ----------------------------------------------------------------------------
# None of the lists below can have white space or a dollar sign in an entry.
#
# The person of company that owns the copyright for this package
# (if empty then no copyright for this package).
copyright_owner='University of Washington'
#
# Web address linked by run_omhelp.sh to the Home icon on each page.
# (if empty, no home icon appears in pages generated by run_omhelp.sh).
image_link='https://bradbell.github.io/at_cascade'
#
# List of files, besides CMakeLists.txt, that have have a copy of the
# version number (can be empty).
version_files='
   at_cascade.xrst
   at_cascade/__init__.py
'
#
# List of special files, for this repository, that the devel tools ignore.
# The files /.gitignore, /batch_edit.sed, /bin/devel.sh should be in this list.
# Files that are created by a program, and checked into the repository,
# should also be in this list. Names that end with / are directories to ignore.
# Names that begin with a / are relative to top source directroy.
# All other names are relavie paths somewhere below the top source directory.
ignore_files='
   /.readthedocs.yaml
   /.gitignore
   /batch_edit.sed
   /bin/devel.sh
   /readme.md
   /sphinx/
'
# ----------------------------------------------------------------------------
echo "copyright_owner=$copyright_owner"
echo "image_link=$version_files"
echo "ignore_files=$ignore_files"
echo "version_files=$version_files"
# ----------------------------------------------------------------------------
