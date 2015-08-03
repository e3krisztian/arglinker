# arglinker

`arglinker` is a [py.test](http://pytest.org/latest/fixture.html) like automatic
fixture injector for `unittest` and derivatives.

`arglinker` works with both Python 2 and 3.

At runtime a test method will be called with arguments that are the return
values of respectively named *fixture methods*.

Fixture methods are normal methods without the `test` prefix, they can have
arguments, which are recursively resolved when used as argument fixture.


## Usage

from [arglinker's test](https://github.com/krisztianfekete/arglinker/blob/master/test_arglinker.py):

Enable fixture injection by using the returned class of the
`add_test_linker` function as `TestCase`:

```python
import unittest
import arglinker

TestCase = arglinker.add_test_linker(unittest.TestCase)
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


## How does it work?

Test methods are replaced with an enhanced argumentless version of the method,
that calls the *fixture methods* and calls the original method with the
appropriate fixtures.

Stdlib's introspection module `inspect` gives access to argument names and
a metaclass does the method replacing at class definition time.

The implementation fits on a page and although uses advanced Python constructs,
it is relatively simple - take a look!
