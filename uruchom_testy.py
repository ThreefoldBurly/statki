#!/usr/bin/env python3

"""

    Skrypt uruchomieniowy wszystkich modułów testowych.

"""
import unittest

import testy.test_plansza as tpl
import testy.test_pamiec as tpm

loader, suite = unittest.TestLoader(), unittest.TestSuite()

# zbierz moduły testowe w jeden komplet
suite.addTests(loader.loadTestsFromModule(tpl))
suite.addTests(loader.loadTestsFromModule(tpm))

# uruchom komplet testów
rezultat = unittest.TextTestRunner(verbosity=2).run(suite)
