#!/usr/bin/env python3
"""
Create a file with the name "funkname.py" from a class template.

Save the corresponding file in the current directory, and open it in
sublime.


# INPUTS
# ----------------------------------------------------------------------------|
funkname: name of desired function (make sure to include .py ext)


# OUTPUTS
# ----------------------------------------------------------------------------|
funkname.py


# NOTES
# ----------------------------------------------------------------------------|
Example of usage:
classtmp.py test_class.py


Written 02/10/2015
By Sam Thorpe
"""


# # Module Imports
# -----------------------------------------------------|
from sys import argv
from subprocess import call
from datetime import datetime
import re


# # Defs
# -----------------------------------------------------|
def build_template(fn):
    """Build the class template."""
    cn = re.sub('.py', '', fn).split('_')
    cn = ''.join([c.capitalize() for c in cn if c])
    lines = []
    lines.append('"""\n')
    lines.append('Insert description.\n\n')

    # # Default Commenting style
    # -----------------------------------------------------|
    hdl = ['# NOTES\n']
    bnk = "{}{}{}\n\n\n".format("# ", "-" * 76, "|")
    smbnk = "{}{}{}\n".format("# ", "-" * 53, "|")
    for h in hdl:
        lines.append(h)
        lines.append(bnk)
    now = datetime.now()
    lines.append('Written %s\n' % now.strftime("%B %d, %Y"))
    lines.append('By Samuel Thorpe\n')
    lines.append('"""\n\n\n')

    # # Default Imports
    # -----------------------------------------------------|
    lines.append('# # Imports\n')
    lines.append(smbnk)
    default_imports = ['os', 'numpy as np']
    for mod in default_imports:
        lines.append('import {}\n'.format(mod))
    lines.append('\n\n')

    # # Default Class Structure
    # -----------------------------------------------------|
    lines.append('# # Main Class\n')
    lines.append('%s' % smbnk)
    lines.append('class {}:\n'.format(cn))
    lines.append('    """ class object description\n')
    lines.append('    """\n')
    lines.append('    def __init__(self):\n')
    lines.append('        """Initialize class."""\n')
    lines.append('        from sampy.common import keyboard\n')
    lines.append('        keyboard(locals(), globals())\n\n\n')

    # # Default Main Entry
    # -----------------------------------------------------|
    lines.append('# # Main Entry\n')
    lines.append(smbnk)
    lines.append('if __name__ == "__main__":\n')
    lines.append('    CLS = {}()\n'.format(cn))
    return lines


def write_template(lines, args):
    """Write output file & open."""
    fn = args[1]
    txt = open(fn, 'w')
    txt.write(''.join(lines))
    txt.close()
    call(['chmod', '+x', fn])
    # if '-blind' not in args:
    #     commands = ['gnome-terminal', '-e', 'subl {}'.format(fn)]
    #     call(commands)


# # Main Entry
# -----------------------------------------------------|
if __name__ == '__main__':
    LINES = build_template(argv[1])
    write_template(LINES, argv)
