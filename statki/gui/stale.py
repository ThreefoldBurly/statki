"""

    statki.gui.stale
    ~~~~~~~~~~~~~~~~

    Stałe współdzielone przez moduły GUI.

"""

from collections import namedtuple

Czcionki = namedtuple("Czcionki", "mala mala_pogrubiona duza_pogrubiona pogrubiona")
CZCIONKI = Czcionki(
    mala=("TkDefaultFont", 8),
    mala_pogrubiona=("TkDefaultFont", 8, "bold"),
    duza_pogrubiona=("TkDefaultFont", 10, "bold"),
    pogrubiona=("TkDefaultFont", 9, "bold")
    # mala_mono=("TkFixedFont", 8)
)

Kolory = namedtuple("Kolory", "pozycja_pola szary")
KOLORY = Kolory(
    pozycja_pola="LemonChiffon2",
    szary="dim gray"
)
