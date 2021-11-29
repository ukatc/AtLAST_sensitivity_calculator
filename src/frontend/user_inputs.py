# Script to get user input from the terminal for user input parameters:
# - target coordinates
# - central observing frequency
# - bandwidth (?)
# - number of polarizations
# - precipitable water vapour
# Frontend structure not decided, this was just playing around with inputs. Will need work down the line.

from astropy.coordinates import SkyCoord
import astropy.units as u


def get_coordinates():
    raise NotImplementedError


def get_frequency():
    """
    Return the required central observing frequency
    Must be in the AtLAST range of 84 -- 950 GHz
    """
    while True:
        try:
            freq = int(input("Central observing frequency in GHz: "))
        except ValueError:
            print("~~~ Please enter a numeric value ~~~")
            continue
        if freq < 84 or freq > 950:
            print("~~~ Outside AtLAST range of 84 -- 950 GHz! ~~~")
            continue
        else:
            return freq


def get_bandwidth():
    raise NotImplementedError


def get_polarizations():
    """
    Return the number of polarizations required
    Must be an int between 0 and 4
    """
    while True:
        try:
            n_pol = int(input("Number of polarizations required: "))
        except ValueError:
            print("~~~ Please enter a numeric value ~~~")
            continue
        if n_pol < 0 or n_pol > 4:
            print("~~~ Must be a number between 0 and 4! ~~~")
            continue
        else:
            return n_pol


def get_pwv():
    """
    Return the estimated PWV
    Must be in the range of 0 -- 6 GHz
    """
    while True:
        try:
            pwv = float(input("Estimated PWV in mm : "))
        except ValueError:
            print("~~~ Please enter a numeric value ~~~")
            continue
        if pwv < 0.0 or pwv > 6.0:
            print("~~~ PWV should be between 0 and 6 mm! ~~~")
            continue
        else:
            return pwv


freq = get_frequency() * u.GHz
n_pol = get_polarizations()
pwv = get_pwv() * u.mm
