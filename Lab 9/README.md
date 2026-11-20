Running and testing:

- Management system `python main.py`

- All 34 tests, with input/expected/actual reports `python -m unittest discover -s tests -q`

- Strategy, factory, validation, CSV and persistence tests `python -m tests.test_patterns_and_validation`

- Product substitutability and polymorphism test `python -m tests.test_substitutability`

- Standalone sample CSV import `python load_products.py`

