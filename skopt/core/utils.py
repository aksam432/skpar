"""
"""
import numpy as np
import logging

def configure_logger(name, filename='skopt.debug.log', verbosity=logging.INFO):
    """Get parent logger: logging INFO on the console and DEBUG to file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # may need this if running within ipython notebook, to avoid duplicates
    logger.propagate = False
    # console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(verbosity)
    # file handler with full debug info
    fh = logging.FileHandler(filename, mode='w')
    fh.setLevel(logging.DEBUG)
    # message formatting
    fileformat = logging.Formatter('%(name)s - %(levelname)s: %(message)s')
    consformat = logging.Formatter('%(levelname)7s: %(message)s')
    fh.setFormatter(fileformat)
    ch.setFormatter(consformat)
    # add the configured handlers
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def get_logger(name, filename=None, verbosity=logging.INFO):
    """Return a named logger with file and console handlers.

    Get a `name`-logger. Check if it is(has) a parent logger.
    If parent logger is not configured, configure it, and if a child logger
    is needed, return the child.
    The check for parent logger is based on `name`: a child if it contains '.',
    i.e. looking for 'parent.child' form of `name`.
    A parent logger is configured by defining a console handler at `verbosity`
    level, and a file handler at DEBUG level, writing to `filename`.
    """
    parent = name.split('.')[0]
    if filename is None:
        filename = parent+'.debug.log'
    parent_logger = logging.getLogger(parent)
    if not parent_logger.handlers:
        configure_logger(parent, filename, verbosity)
    return logging.getLogger(name)

def normalise(a):
    """Normalise the given array so that sum of its elements yields 1.

    Args:
        a (array): input array

    Returns:
        a/norm (array): The norm is the sum of all elements across all dimensions.
    """
    norm = np.sum(np.asarray(a))
    return np.asarray(a)/norm

def is_monotonic(x):
    dx = np.diff(x)
    return np.all(dx <= 0) or np.all(dx >= 0)

def normaliseWeights(weights):
    """
    normalise weights so that their sum evaluates to 1
    """
    return np.asarray(weights)/np.sum(np.asarray(weights))

def flatten (dd):
    """
    Take a dictionary or list of dictionaries/lists dd,
    and produce a lists of values corresponding, dropping the keys.
    """
    try: # assume current item is a dictionary; iterate over its items
        for key,val in dd.items():
            for nested_val in flatten(val):
                yield nested_val
    except AttributeError: # not a dictionary
        try: # assume current item is a list; iterate over its items
            for i,val in enumerate(dd):
                for nested_val in flatten(val):
                    yield nested_val
        except TypeError: # it is just a number then; return it
            yield dd

def flatten_two (d1, d2):
    """
    Take two dictionaries or lists of dictionaries/lists d1 and d2,
    and produce two lists of values corresponding to the keys/order in d1.
    d2 is optional.
    Assume that the keys of d1 are a subset of the keys of d2.
    Assume nesting, i.e. some of the items in d1 are dictionaries
    and some are lists, numpy arrays, or a non-sequence type.
    The assumption is again: nested dictionaries in d2 must have
    at least the keys of the corresponding nested dictionaries in d1,
    and the lists in d1 must be no shorter than the lists in d2.
    ...some assertions may help here...
    """
    try: # assume current item is a dictionary; iterate over its items
        for key, val in d1.items():
            for nested_val_1,nested_val_2 in flatten_two(val,d2[key]):
                yield nested_val_1, nested_val_2
    except AttributeError: # not a dictionary
        try: # assume current item is a list; iterate over its items
            for i, val in enumerate(d1):
                for nested_val_1, nested_val_2 in flatten_two(val,d2[i]):
                    yield nested_val_1, nested_val_2
        except TypeError: # it is just a number then; return it
# this fails if one number is native python number while
# the other is a numpy scalar
            #assert isinstance(d2,type(d1)), (
            #    '\n{0} \n and \n{1} \nare of different type '
            #    '\n{2} \n and \n{3}'
            #    '\nand cannot be flattened simultaneously.'.
            #    format(d2,d1,type(d2),type(d1)))
            assert not (hasattr(d1,'__iter__') or hasattr(d2,'__iter__')), (
                '\n\t{0}\n{1}' 
                '\n\tand'
                '\n\t{2}\n{3}' 
                '\n\tcannot be flattened simultaneously.'.
                format(type(d1),d1,type(d2),d2))
            yield d1, d2