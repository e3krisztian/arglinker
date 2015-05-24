# Glued

Glued is a [py.test](http://pytest.org/latest/fixture.html) like automatic
fixture injection for `unittest` and derivatives.

Glued works with both Python 2 and 3.

The name comes from its behavior: fixtures will automatically stick to the
parameter names of the test methods of the glued class.


## Usage

from [glued's test](https://github.com/krisztianfekete/glued/blob/master/test_glued.py):

Enable fixture injection by using the returned class of the
`glue_test_methods` function as `TestCase`:

```python
import unittest

from glued import glue_test_methods

TestCase = glue_test_methods(unittest.TestCase)
```

we can now define fixtures as methods of the class, and other methods
can refer to fixtures by naming them as parameters:

```python
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
```

----

For more complete experience, I recommend using it together with
 - [testtools](https://pypi.python.org/pypi/testtools)'s `TestCase`
 - [fixtures](https://pypi.python.org/pypi/fixtures)
