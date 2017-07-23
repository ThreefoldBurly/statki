#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Graficzny interfejs użytkownika dla gry w statki stworzony z wykorzystaniem biblioteki Kivy
"""

import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from statki import Plansza
from wspolne import *


class KvPlansza(GridLayout):
    """Plansza do gry w statki"""

    def __init__(self, **kwargs):
        super(KvPlansza, self).__init__(**kwargs)
        self.plansza = przygotujPlansze(self.cols, self.rows)

    @staticmethod
    def przygotujPlansze(kolumny, rzedy):
        # testy
        plansza = Plansza(kolumny, rzedy)
        plansza.rysujSie()
        plansza.wypelnijStatkami()
        plansza.rysujSie()
        return plansza


class KvPole(Button):
    """Pole planszy do gry w statki"""

    def __init__(self, **kwargs):
        super(KvPole, self).__init__(**kwargs)


class StatkiApp(App):
    """Aplikacja interfejs użytkownika dla gry w statki"""

    def __init__(self, **kwargs):
        super(StatkiApp, self).__init__(**kwargs)

    def build(self):
        return KvPlansza(cols=50, rows=50)
