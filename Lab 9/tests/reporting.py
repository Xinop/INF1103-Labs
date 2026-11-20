"""Readable test reports, following the BiteFinder test layout."""

from pprint import pformat


def show_case(name, test_input, expected, actual):
    passed = actual == expected
    print("\n" + "=" * 72)
    print(f"Test name: {name}")
    print("=" * 72)

    for label, value in (
        ("Input", test_input),
        ("Expected output", expected),
        ("Actual output", actual),
    ):
        print(f"\n{label}:")
        if isinstance(value, str):
            print(value)
        else:
            print(pformat(value, sort_dicts=False, width=72))

    print(f"\nResult: {'PASS' if passed else 'FAIL'}")
    return passed


def capture_value_error(operation):
    """Return the exception actually raised, or report its absence."""
    try:
        operation()
    except ValueError as error:
        return f"{type(error).__name__}: {error}"
    return "No ValueError raised"
