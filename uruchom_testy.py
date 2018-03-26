#!/usr/bin/env python3

"""

    Skrypt uruchomieniowy wszystkich modułów testowych.

"""
import unittest

import testy.test_plansza as tp

loader, suite = unittest.TestLoader(), unittest.TestSuite()

# zbierz moduły testowe w jeden komplet
suite.addTests(loader.loadTestsFromModule(tp))

# uruchom testy
rezultat = unittest.TextTestRunner().run(suite)
