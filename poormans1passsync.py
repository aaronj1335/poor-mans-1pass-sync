#!/usr/bin/env python
"""
What this does:

1. Read in existing contents.js from laptop into memory
2. Copy everything from Dropbox zip to ~/1Password
3. Update new contents.js with missing keys from old contents.js

Example usage:

    $ poormans1passsync.py 1Password.zip

Make sure to use a zip of the whole 1Password dir, not the *.agilekeychain
file.
"""

import json, sys, tempfile
from os.path import join, expanduser
from zipfile import ZipFile
from shutil import rmtree
from distutils.dir_util import copy_tree

if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print __doc__
    sys.exit(0)

ONEPASS = join(expanduser('~'), '1Password')
CONTENTS = '1password.agilekeychain/data/default/contents.js'

tempdir = tempfile.mkdtemp()
ZipFile(sys.argv[1], 'r').extractall(path=tempdir)
latest_onepass = join(tempdir, '1Password')

old = json.load(open(join(ONEPASS, CONTENTS)))
latest = json.load(open(join(latest_onepass, CONTENTS)))

old = {i[0]: i for i in old}
new = {i[0]: i for i in latest}
latest = {i[0]: i for i in latest}


for k in set(old.keys()) - set(latest.keys()):
    new[k] = old[k]

assert (set(new.keys()) - set(latest.keys())) == (set(old.keys()) - set(latest.keys()))

copy_tree(latest_onepass, ONEPASS)
json.dump(new.values(), open(join(ONEPASS, CONTENTS), 'w'))

rmtree(latest_onepass)

