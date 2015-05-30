from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

import unittest
import arglinker

TestCase = arglinker.add_test_linker(unittest.TestCase)


class Test_fixture_evaluation(TestCase):

    # fixtures with automatic fixture injection
    def one(self):
        return 1

    def two(self, one):
        return one + one

    def three(self, two, one):
        return one + two

    def five(self, three, two):
        return three + two

    def ten(self, five):
        return five + five

    # tests
    def test_fixture_method_parameters_are_auto_injected(self, ten):
        self.assertEqual(10, ten)

    def test_fixture_methods_are_simple_methods(self):
        self.assertEqual(10, self.ten(five=5))


class Test_fixture_sharing(TestCase):

    # fixtures
    def value(self):
        return object()

    def implicit_value(self, value):
        return value

    # test
    def test_fixtures_are_evaluated_only_once_per_tests(
        self, value, implicit_value
    ):
        # calling value twice returns different objects
        self.assertIsNot(self.value(), self.value())
        self.assertIsNot(value, self.value())
        # yet implicit_value is the same as value
        self.assertIs(value, implicit_value)


class Test_invalid_tests_and_fixtures(TestCase):

    # fixtures
    def value(self):
        return 1

    @property
    def property_value(self):
        return 'property as fixture will not work'

    # tests
    @unittest.expectedFailure
    def test_property_as_fixture_does_not_work(self, property_value):
        pass

    @classmethod
    @unittest.expectedFailure
    def test_classmethod_as_test_does_not_work(cls, value):
        pass

    @staticmethod
    @unittest.expectedFailure
    def test_staticmethod_as_test_does_not_work(value):
        pass


if __name__ == '__main__':
    unittest.main()
