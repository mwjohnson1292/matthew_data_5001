"""Question 1: add an applyRaise method to the Person class.

applyRaise takes a whole-number percent: applyRaise(10) is a 10% raise.

Run it with:  python q1_person.py
"""


# The assignment's Person has one method; pylint expects at least two.
class Person:  # pylint: disable=too-few-public-methods
    """A person with a name, an optional job, and pay."""

    def __init__(self, name, job=None, pay=0):
        self.name = name
        self.job = job
        self.pay = pay

    # The assignment specifies this camelCase name.
    def applyRaise(self, percent):  # pylint: disable=invalid-name
        """Raise pay by percent (10 means 10%). Changes self.pay; returns None."""
        # Round to cents: 50000 * 1.1 is 55000.00000000001 in floating point.
        self.pay = round(self.pay * (1 + percent / 100), 2)


def main():
    """Apply raises to a Person and check the pay after each one."""
    bob = Person("Bob Smith", job="developer", pay=50000)
    print(f"{bob.name} starts at ${bob.pay:,.2f}")

    bob.applyRaise(10)
    print(f"Bob's Pay after a 10% raise:       ${bob.pay:,.2f}")
    assert bob.pay == 55000.00, bob.pay

    # Raises compound: this is 5% of 55,000, not of 50,000.
    bob.applyRaise(5)
    print(f"Bob's Pay after a further 5% raise: ${bob.pay:,.2f}")
    assert bob.pay == 57750.00, bob.pay

    # The defaults: no job, pay of 0.
    sue = Person("Sue Jones")
    sue.applyRaise(10)
    print(f"{sue.name} (job={sue.job}) after a 10% raise: ${sue.pay:,.2f}")
    assert sue.pay == 0, sue.pay

    print("All Question 1 checks passed.")


# Runs only when this file is run directly, not when it is imported.
if __name__ == "__main__":
    main()
