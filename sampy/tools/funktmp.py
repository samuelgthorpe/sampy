#! /usr/bin/python3
"""
funktmp.py funkname.py


Create a file with the name "funkname.py" from a template.
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
funktmp.py testfunk.py


Written 02/10/2015
By Sam Thorpe
"""


# # Module Imports
# -----------------------------------------------------|
from sys import argv
from subprocess import call
from datetime import datetime


# # Defs
# -----------------------------------------------------|
def build_template(fn):
    #  pylint: disable=invalid-name
    """ build the class template
    """
    lines = []
    lines.append('"""\n')
    lines.append('Insert description.\n\n')

    # # Default Commenting style
    # -----------------------------------------------------|
    hdl = ['# NOTES\n']
    bnk = "{}{}{}\n\n\n".format("# ", "-" * 76, "|")
    smbnk = "{}{}{}\n".format("# ", "-" * 53, "|")
    for n in range(1):
        lines.append(hdl[n-1])
        lines.append(bnk)
    now = datetime.now()
    lines.append('Written {}\n'.format(now.strftime("%B %d, %Y")))
    lines.append('By Samuel Thorpe\n')
    lines.append('"""\n\n\n')

    # # Default Imports
    # -----------------------------------------------------|
    lines.append('# # Imports\n')
    lines.append(smbnk)
    default_imports = ['os', 'numpy as np', 'matplotlib.pyplot as plt']
    for mod in default_imports:
        lines.append('import {}\n'.format(mod))
    lines.append('\n\n')

    # # Default Function Def
    # -----------------------------------------------------|
    lines.append('# # Defs\n')
    lines.append(smbnk)
    lines.append('def main():\n')
    lines.append('    """Run main method."""\n')
    lines.append('    from sampy.common import keyboard\n')
    lines.append('    keyboard(locals(), globals())\n\n\n')

    # # Default Main Entry
    # -----------------------------------------------------|
    lines.append('# # Main Entry\n')
    lines.append(smbnk)
    lines.append('if __name__ == "__main__":\n')
    lines.append('    main()\n')
    return lines


def write_template(lines, args):
    #  pylint: disable=invalid-name
    """ Write output file & open
        'gnome-terminal', '-e', '/opt/sublime_text/sublime_text {}'.format(fn)
    """
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
