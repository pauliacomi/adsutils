import os
import pytest

HERE = os.path.dirname(__file__)

DATA = {
    'MCM-41': {
        'file': 'MCM-41 N2 77.355.json',
        'bet_area': 400.0,
        's_bet_area': 350.0,
        't_pore_volume': 0.28,
        't_area': 80.0,
    },
    'NaY': {
        'file': 'NaY N2 77.355.json',
        'bet_area': 700.0,
        't_pore_volume': 0.20,
        't_area': 200.0,
    },
    'SiO2': {
        'file': 'SiO2 N2 77.355.json',
        'bet_area': 200.0,
        't_pore_volume': 0.06,
        't_area': 280.0,
    },
    'Takeda 5A': {
        'file': 'Takeda 5A N2 77.355.json',
        'bet_area': 1075.0,
        't_pore_volume': 0.43,
        't_area': 130.0,
    },
    'UiO-66(Zr)': {
        'file': 'UiO-66(Zr) N2 77.355.json',
        'bet_area': 1250.0,
        't_pore_volume': 0.48,
        't_area': 6.0,
    },
}


# ('MCM-41 N2 77.355.json', 60, -0.1),
# ('NaY N2 77.355.json', 100, 0.17),
# ('SiO2 N2 77.355.json', 250, -0.1),
# ('Takeda 5A N2 77.355.json', 85, 0),
# ('UiO-66(Zr) N2 77.355.json', 3.5, 0.13),

def approx(value1, value2, error):
    return (abs(value1) < abs(value2 * (1 + error))
            ) and (abs(value1) > abs(value2 * (1 - error)))