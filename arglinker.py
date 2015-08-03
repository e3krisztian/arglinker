# coding: utf-8

'''
Enable a py.test like automatic fixture injection with

    # unittest
    TestCase = arglinker.add_test_linker(unittest.TestCase)

and using the returned TestCase for base class for tests.
Fixtures will be automatically passed as the appropriate parameters of
the test methods of the linked class.

Fixture `a` is defined as the return value of non-test method `a()`
of the same TestCase derived class.

Author: Krisztián Fekete
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

import functools
import inspect


__all__ = ('add_test_linker',)


def call_with_fixtures(obj, function, fixtures):
    args = inspect.getargspec(function).args[1:]
    for arg in args:
        add_fixture(obj, arg, fixtures)
    # python2: `self` must be positional parameter, not keyword parameter
    return function(obj, **dict((arg, fixtures[arg]) for arg in args))


def add_fixture(obj, arg_name, fixtures):
    if arg_name in fixtures:
        return
    create_fixture = getattr(obj.__class__, arg_name)
    fixture = call_with_fixtures(obj, create_fixture, fixtures)
    fixtures[arg_name] = fixture


def func_with_fixture_resolver(f):
    argspec = inspect.getargspec(f)
    does_not_need_transform = (
        argspec.args == ['self'] or argspec.varargs or argspec.keywords
    )
    if does_not_need_transform:
        return f

    # strong python convention: subject of method is named self
    # assumption: developers follow convention
    assert argspec.args[0] == 'self'

    @functools.wraps(f)
    def f_with_fixtures(self):
        return call_with_fixtures(self, f, fixtures={})

    return f_with_fixtures


class ArgLinkerMeta(type):
    '''
    Metaclass linking fixtures to parameter names.

    Replaces test methods with closure methods that create/resolve fixtures
    from parameter names and call the original test method with the fixtures.
    '''

    def __new__(cls, name, parents, dct):
        new_dct = {}
        for obj_name, obj in dct.items():
            is_test_method = (
                obj_name.startswith('test') and inspect.isfunction(obj))
            if is_test_method:
                new_dct[obj_name] = func_with_fixture_resolver(obj)
            else:
                new_dct[obj_name] = obj

        return (
            super(ArgLinkerMeta, cls).__new__(cls, name, parents, new_dct))


def add_test_linker(test_case_class):
    '''
    Return a new, enhanced test case class.

    The returned class' test methods resolve fixtures from argument names.

    The fixtures are simply return values of methods having the same name
    as the parameter.
    '''
    # create class by instantiating the metaclass (python 2 & 3 compatible)
    return ArgLinkerMeta(
        # class name
        test_case_class.__name__,
        # base classes
        (test_case_class,),
        # newly defined stuff
        {})
