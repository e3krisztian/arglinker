# coding: utf-8

'''
Enable a py.test like automatic fixture injection with

    # unittest
    TestCase = glue_test_methods(unittest.TestCase)

or

    # https://github.com/testing-cabal/testtools
    TestCase = glue_test_methods(testtools.TestCase)

and using the returned TestCase for base class for tests.
Fixtures will automatically stick to the parameter names of
the test methods of the glued class!

Where fixture `a` is defined as the return value of non-test method `a()`
of the same TestCase derived class.

----

Motivated by py.test's similar feature, but it is a clean-room implementation
of the idea.

Author: Krisztián Fekete
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

import functools
import inspect


__all__ = ('glue_test_methods',)


def call_with_fixtures(testobj, function, fixtures):
    args = inspect.getargspec(function).args[1:]
    for arg in args:
        add_fixture(testobj, arg, fixtures)
    # python2: self must be positional parameter, not keyword parameter!
    return function(testobj, **dict((arg, fixtures[arg]) for arg in args))


def add_fixture(testobj, arg_name, fixtures):
    if arg_name in fixtures:
        return
    create_fixture = getattr(testobj.__class__, arg_name)
    fixture = call_with_fixtures(testobj, create_fixture, fixtures)
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


class GlueMeta(type):
    '''\
    Metaclass glueing fixtures to parameter names.

    This is done by replacing test methods with closure methods
    that create/resolve fixtures from the given parameter name
    and call the original test method with the fixtures.
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
            super(GlueMeta, cls).__new__(cls, name, parents, new_dct))


def glue_test_methods(test_case_class):
    '''\
    Return an enhanced test case class, that automagically resolves fixtures.

    Test methods can name their fixtures as parameters, which is resolved to
    return values of methods having the same name as the parameter.

    Non-destructive: returns a new class.
    '''
    # create class by instantiating the metaclass (python 2 & 3 compatible!)
    return GlueMeta(
        # class name
        str('Glued_') + test_case_class.__name__,
        # base classes
        (test_case_class,),
        # newly defined stuff
        {})
