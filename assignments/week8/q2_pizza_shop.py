"""Question 2: classes for a pizza shop.

Chef and Server extend Employee; PizzaRobot extends Chef. Each subclass
overrides work(). This file only defines the classes; Question 3 tests them.
"""

# Each class has one public method by design; pylint expects at least two.
# pylint: disable=too-few-public-methods


class Employee:
    """A pizza shop employee with a name and an optional salary."""

    def __init__(self, name, salary=None):
        self.name = name
        self.salary = salary  # None means no salary given, not 0

    def work(self):
        """Print what this employee does."""
        print(f"{self.name} does stuff")

    def __repr__(self):
        """Label the object with its actual class, name and salary."""
        return f"<{type(self).__name__}: name={self.name}, salary={self.salary}>"


class Chef(Employee):
    """An employee who makes food, paid 50000."""

    def __init__(self, name):
        # Reuse Employee's constructor, with the chef's salary.
        Employee.__init__(self, name, salary=50000)

    def work(self):
        """Override Employee.work."""
        print(f"{self.name} makes food")


class PizzaRobot(Chef):
    """A chef that makes pizza and has no salary."""

    def __init__(self, name):
        Chef.__init__(self, name)  # sets the name, and salary 50000
        self.salary = None  # must come second, or Chef's 50000 wins

    def work(self):
        """Override Chef.work."""
        print(f"{self.name} makes pizza")


class Server(Employee):
    """An employee who takes orders, paid 40000."""

    def __init__(self, name):
        Employee.__init__(self, name, salary=40000)

    def work(self):
        """Override Employee.work."""
        print(f"{self.name} takes orders")
