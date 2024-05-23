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
import numpy as np


# # General Exception Class
# -----------------------------------------------------|
CommonException = type('CommonException', (Exception,), {})


# # Defs
# -----------------------------------------------------|
def keyboard(loc, glob):
    """Mimics Matlab's keyboard, but with locals, globals as inputs."""
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


# # Check Approximate Equality
# -----------------------------------------------------|
def check_equality(x, y, tol=np.finfo(np.float32).eps):
    """Check approximate equality for general data types.

    NOTE: this will only work with iterables (i.e. which have a
          '__iter__' method) for which the len() function can be
          used to determine size (i.e. no generators)
    """
    # # check objects are of comparable type
    if isinstance(x, numbers.Number):
        assert isinstance(x, numbers.Number)
    else:
        assert type(x) is type(y), \
            "MISMATCH: ({type(x)}) {x} != ({type(y)}) {y}"

    # # check exact/approximate equality as appropriate
    if isinstance(x, float) and np.isnan(x):
        assert np.isnan(y)
    if isinstance(x, float) and np.isinf(x):
        assert x == y
    elif isinstance(x, numbers.Number):
        assert np.abs(x - y) < tol
    elif isinstance(x, (str, bool)):
        assert x == y
    elif hasattr(x, '__iter__'):
        assert hasattr(y, '__iter__') and len(x) == len(y)
        for x_itr, y_itr in zip(x, y):
            check_equality(x_itr, y_itr)


def _cmp_str(x, y):
    """Compare string."""
    return f"MISMATCH: ({type(x)}) {x} != ({type(y)}) {y}"


# # Common Time Series Manipulation
# -----------------------------------------------------|
def refine_series(coarse_ts, refined_ts):
    """Refine a coarse time series to finer resolution."""
    ridx = np.zeros(refined_ts.shape[0]).astype(int)
    for idx, tim in enumerate(refined_ts):
        leading_samps = np.where(coarse_ts <= tim)[0]
        if leading_samps.shape[0]:
            ridx[idx] = leading_samps[-1]
    return ridx


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


# # Main Entry
# -----------------------------------------------------|
if __name__ == '__main__':
    pass
