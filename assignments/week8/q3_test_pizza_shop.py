"""Question 3: create one of each employee and test their salaries.

Each salary should be what its constructor chain sets. The robot is the
deliberate exception: it runs Chef's constructor, then has no salary.

Run it with:  python q3_test_pizza_shop.py
"""

from q2_pizza_shop import Chef, Employee, PizzaRobot, Server


def check(description, actual, expected):
    """Stop with an error if actual differs from expected; otherwise print PASS."""
    assert actual == expected, f"{description}: got {actual!r}, expected {expected!r}"
    print(f"PASS  {description}: {actual!r}")


def main():
    """Create the employees, run the tests, then call work() on each."""
    pat = Employee("Pat")
    paid_pat = Employee("Pat", 30000)  # tests the optional salary
    maria = Chef("Maria")
    robo = PizzaRobot("Robo")
    sam = Server("Sam")

    print("Salary tests")
    check("Employee with no salary given defaults to None", pat.salary, None)
    check("Employee given a salary keeps it", paid_pat.salary, 30000)
    check("Chef salary is 50000", maria.salary, 50000)
    check("Server salary is 40000", sam.salary, 40000)
    check("PizzaRobot has no salary", robo.salary, None)
    check("PizzaRobot does not keep its base class Chef's 50000",
          robo.salary != maria.salary, True)

    print("\nInheritance tests")
    check("A Chef is an Employee", isinstance(maria, Employee), True)
    check("A Server is an Employee", isinstance(sam, Employee), True)
    check("A PizzaRobot is a Chef", isinstance(robo, Chef), True)
    check("A PizzaRobot is also an Employee", isinstance(robo, Employee), True)
    check("A Server is not a Chef", isinstance(sam, Chef), False)

    # The order Python searches for a method: the object's class, then parents.
    search_order = [cls.__name__ for cls in PizzaRobot.__mro__]
    print(f"\nPizzaRobot's method search order: {search_order}")

    # Same call, different behavior: each subclass overrides work().
    print("\nEveryone works")
    for employee in [pat, maria, robo, sam]:
        print(f"{employee!r:45} -> ", end="")
        employee.work()

    print("\nAll Question 3 checks passed.")


if __name__ == "__main__":
    main()
