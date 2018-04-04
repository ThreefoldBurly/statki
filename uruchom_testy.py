#!/usr/bin/env python3

"""

    Skrypt uruchomieniowy wszystkich modułów testowych.

"""
import unittest

import testy.test_plansza as tpl

loader, suite = unittest.TestLoader(), unittest.TestSuite()

# zbierz moduły testowe w jeden komplet
suite.addTests(loader.loadTestsFromModule(tpl))

# uruchom komplet testów
rezultat = unittest.TextTestRunner(verbosity=2).run(suite)
