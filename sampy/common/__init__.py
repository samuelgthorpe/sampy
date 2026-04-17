"""
Module containing common sampy tools.

# NOTES
# ----------------------------------------------------------------------------|


written March 2024
by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import sys
from collections import namedtuple
import functools
import operator
import code
import inspect
import time
import numbers
import pdb


# # General Exception Class
# -----------------------------------------------------|
CommonException = type('CommonException', (Exception,), {})


# # Defs
# -----------------------------------------------------|
def keyboard(loc, glob):
    """Mimics Matlab's keyboard, but with locals, globals as inputs."""
    # frame = inspect.currentframe().f_back
    # pdb.Pdb().set_trace(frame)
    tag = '\n\n>>> (InteractiveConsole) : {} : line {} : {} >>>'.\
        format(*check_stack_phrase(inspect.stack()))
    code.interact(banner=tag, local={**loc, **glob})


def check_stack_phrase(stack, phrase='keyboard(locals(), globals())'):
    """Check stack for keyboard phrase."""
    for elmnt in stack:
        for line in elmnt[-2]:
            if phrase in line:
                return elmnt[1:4]
    return ('STACK', 'NOT', 'PARSED')


def struct(dat, loc=None):
    """Initialize namedtuple with data object.

    Useful for grouping variables together similar to matlab strutures.

    Args:
        dat (TYPE): variable name list OR data object (list, dict or class)
             If dat is a list of string variable names, then the loc object
             must be a dict or class with those strings as keys/attributes.
             If dat is a dict, then loc is ignored, and the returned namedtuple
             has fields corresponding to the keys of dat.
        loc (None, optional): if dat is a variable name list, then loc
            specifies the data object (most commonly locals() or self).

    Returns:
        named tuple: grouped variables

    NOTE: Doing the input variable order this way, i.e. "list first if list
    else data" may be counterintuitive but there is a certain sanity to it
    the way I use this function.
    """
    def _get(obj, attr):
        """Return key/attribute value."""
        return obj.get(attr) if isinstance(obj, dict) else getattr(obj, attr)

    if isinstance(dat, list):  # specified list of variable names
        structure = namedtuple('canonical_tuple', dat)
        named_tup = structure(*[_get(loc, q) for q in dat])
    else:
        loc = dat.keys() if isinstance(dat, dict) else \
            [x for x in dir(dat) if x not in dir(type(dat))]
        structure = namedtuple('canonical_tuple', loc)
        named_tup = structure(*[_get(dat, q) for q in loc])
    return named_tup


def struct_replace(strct, fields, val):
    """Replace (possibly nested) canonical tuple fields with new value.

    Args:
        strct (TYPE): the canonical tuple (see struct above) to be modified
        fields (TYPE): list of strings indicating the (possibly nested) fields
                       to edit can also be a single string
        val (TYPE): replacement value

    Returns:
        TYPE: Description
    """
    fields = [fields] if isinstance(fields, str) else fields
    dct = recursive_dict(strct)
    set_in_dict(dct, fields, val)
    return recursive_struct(dct)


def recursive_dict(strct):
    """Recursively walk a structure to convert to nested dict."""
    dct = strct._asdict()
    for key, val in dct.items():
        if hasattr(val, '_fields') and hasattr(val, '_asdict'):
            dct[key] = recursive_dict(val)
    return dct


def recursive_struct(dct):
    """Recursively walk a nested dict and replace with struct."""
    for key, val in dct.items():
        if isinstance(val, dict):
            dct[key] = recursive_struct(val)
    return struct(dct)


def get_from_dict(dct, map_list):
    """Access nested dict through list of keys (must already exist).

    https://stackoverflow.com/questions/14692690/ ...
        access-nested-dictionary-items-via-a-list-of-keys
    """
    return functools.reduce(operator.getitem, map_list, dct)


def set_in_dict(dct, map_list, val):
    """Set value of nested dict through list of keys (must already exist).

    https://stackoverflow.com/questions/14692690/ ...
        access-nested-dictionary-items-via-a-list-of-keys
    """
    get_from_dict(dct, map_list[:-1])[map_list[-1]] = val


def info(obj, spacing=10):
    """Print methods and doc strings for module and class objects."""
    print("\n\nTYPE\n" + "-"*25)
    print("{}\n".format(type(obj)))
    # # attributes info
    attr_list = obj.__dict__.keys()
    attr_info = [type(getattr(obj, x)) for x in attr_list]
    if attr_list:
        print_info = ["{} {}".format(attr.ljust(spacing), attr_inf)
                      for attr, attr_inf in zip(attr_list, attr_info)]
        print('\nATTRIBUTES\n' + "-"*25)
        print("\n".join(print_info))
    # # Methods info
    method_list = [method for method in dir(object)
                   if callable(getattr(object, method))]
    proc_func = (lambda s: " ".join(s.split()))
    print_info = ["{} {}".format(method.ljust(spacing),
                                 proc_func(str(getattr(obj, method).__doc__)))
                  for method in method_list]
    print('\nMETHODS\n' + "-"*25)
    print("\n".join(print_info) + "\n")


# # Timers
# -----------------------------------------------------|
class LoopStatusTimer():
    """Display status bar in terminal."""

    def __init__(self, n_loops, n_cols=60, msg=''):
        """Initialize."""
        self.n_loops = n_loops
        self.n_cols = n_cols
        self.msg = msg

    def setup(self):
        """Set up the status bar."""
        print('{}0/{}'.format(' '*self.n_cols, self.n_loops), end='\r')
        sys.stdout.flush()

    def update(self, loop):
        """Update the status bar."""
        updated = self._update_string(loop+1)
        print(updated, end='\r')
        sys.stdout.flush()

    def _update_string(self, loop):
        """Return the updated string."""
        n_char = int(float(loop)*float(self.n_cols)/float(self.n_loops))
        updated = \
            '\033[92m' + ':'*n_char + ' '*(self.n_cols-n_char) + \
            '\033[0m' + '{}/{}'.format(loop, self.n_loops)
        return updated

    def run(self, method, *args, **kwrgs):
        """Wrap a function call in some standard way."""
        start = time.time()
        print('running  {} {} ...'.format(method.__name__, self.msg))
        self.setup()
        out = method(*args, **kwrgs)
        print('\n{} sec elapsed'.format(time.time() - start))
        return out