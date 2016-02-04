import math

import numpy as np

###
### Small LTE library for the LTE calculations in Chyexmachina project
###

###
### Natural Constants
###

kboltz = 1.380658e-16  # ergs/kelvin
cc = 2.99792458e10  # cm/s
hplanck = 6.6260755e-27  # ergs*second
tbg = 2.73  # Temperature of the CMB, put a more realistic value


def jnu(temp, nu):
    """
    Calculates Jnu for given temperature and frequency
    :param temp: Temperature [K]
    :param nu: Frequency [Hz]
    :return: brightness temperature [K]
    """
    tbrilho = hplanck / kboltz * nu * (math.exp((hplanck * nu) / (kboltz * temp)) - 1) ** (-1)
    return tbrilho


def ijnu(tbrilho, nu):
    """
    Calculates a emiting temperature from a brightness temperature at given frequency
    :param tbrilho: Brightness temperature [K]
    :param nu: Frequency [Hz]
    :return: Temperature [K]
    """
    logpart = 1.0 + hplanck * nu / tbrilho / kboltz
    temp = (kboltz / hplanck / nu * math.log(logpart)) ** -1
    return temp


def djnu(temp1, temp2, nu):
    """
    Calculates difference between two brightness temperatures
    :param temp1: temperature 1 [k]
    :param temp2: temperature 2 [k]
    :param nu: Frequency [Hz]
    :return: jnu(temp1,nu)-jnu(temp2,nu) [k]
    """
    return jnu(temp1, nu) - jnu(temp2, nu)


def bnu(temp, freq):
    """
    Black body radiation flux at give intensity and frequency
    :param temp: Temperature [K]
    :param freq: Frequency [K]
    :return: Intensity [?]
    """
    flux = (2 * hplanck * freq ** 3 / cc ** 2) / (math.exp(hplanck / kboltz * (freq / temp)) - 1.)
    return flux


def ibnu(flux, freq):
    """
    Temperature for a given black body radiation flux at given frequency
    :param flux: Flux [?]
    :param freq: Frequency [Hz]
    :return: Temperature [K]
    """
    temp = 4.7992476435716E-11 * freq * ((math.log(((1.4745e-47 * freq ** 3) / flux) + 1.)) ** -1)
    return temp


def coldens(*args):
    """
    Calculates column densities for molecules with known spectroscopic properties.
    Distinguishes between optically thin and optically thick case.
    *** Thin case is assumed when given line width is 0
        In this case it is assumed that args[8] is an integrated
        intensity and args[9] its error.
    *** Thick case is assumed for non zero line width.
        In this case  it is assumed that args[8] is the opacity of the
        line and args[9] its error.
    :param args:
        [0] Frequency [Hz]
        [1] Einsteins Coefficient [s^{-1}] ?
        [2] Upper level Degeneracy
        [3] Upper level Energy
        [4] Lower level Quantum number
        [5] Partition Function at given Tex []?
        [6] Excitation Temperature [K]
        [7] Excitation Temperature error [k]
        [8] Opacity/Integrated Intensity [n/a]/[K*km/s]
        [9] Opacity/Integrated Intensity error [n/a]/[K*km/s]
        [10] Line width [km*s^{-1}]
        [11] Line width error [km*s^{-1}]
    :return: Column density, propagated column density error [cm^{-2}],[cm^{-2}]
    """
    const = 8.0 * np.pi / (cc ** 3)
    nu = args[0] * 1.0e9
    einstein = args[1]
    gup = args[2]
    eup = args[3]
    jlow = args[4]
    qpart = args[5]
    tex = args[6]
    etex = args[7]
    tau = args[8]
    etau = args[9]
    deltav = args[10]
    edeltav = args[11]
    tt = (eup / ((jlow + 1) * (jlow + 2))) * jlow * (jlow + 1)
    if deltav == 0:
        protocol = const * (nu ** 3) / (einstein) / gup
        dejnu = djnu(tex, tbg, nu)
        edejnu = max(abs(djnu(tex + etex, tex, nu)), abs(djnu(tex - etex, tex, nu)))
        ratio = tau / dejnu
        etau = ratio * math.sqrt(etau ** 2 / tau ** 2 + edejnu ** 2 / dejnu ** 2)
        tau = ratio
        eprotocol = 0.0
    else:
        vperfi = deltav * 1.e5 / np.sqrt(8 * np.log(2)) * np.sqrt(2 * np.pi)
        evperfi = edeltav * 1.e5 / np.sqrt(8 * np.log(2)) * np.sqrt(2 * np.pi)
        protocol = const * vperfi * (nu ** 3) / (einstein) / gup
        eprotocol = const * evperfi * (nu ** 3) / einstein / gup
    exps = part_statistics_ratio(eup, tt, tex)
    eexps = max(abs(part_statistics_ratio(eup, tt, tex + etex) - part_statistics_ratio(eup, tt, tex)),
                abs(part_statistics_ratio(eup, tt, tex - etex) - part_statistics_ratio(eup, tt, tex)))
    prefac = protocol * tau * exps
    eprefac = protocol * np.sqrt(etau ** 2 + eexps ** 2 + eprotocol ** 2)
    ncol = prefac * qpart
    encol = eprefac * qpart
    return ncol, encol


def part_statistics_ratio(eup, tt, tex):
    """
    ? Ratio between particle statistics Bosons x Fermions??
    ***NEED TO REMEMBER THE THEORETICAL GROUNDS HERE
    :param eup: Upper level energy [K]
    :param tt: Lower level energy [K]
    :param tex: Excitation Temperature [K]
    :return:
    """
    return (np.exp(tt / tex)) / (1.0 - np.exp(-(eup - tt) / tex))


def calc_tex(tau, etau, tr, etr, freq):
    exptau = 1 - math.exp(-tau)
    eexptau = max(abs(1 - math.exp(-(tau + etau)) - exptau), abs(1 - math.exp(-(tau - etau)) - exptau))
    jnubg = jnu(tbg, freq)
    ratio = tr / exptau
    jnutex = jnubg + ratio
    ejnutex = ratio * math.sqrt(etr ** 2 / tr ** 2 + eexptau ** 2 / exptau ** 2)
    tex = ijnu(jnutex, freq)
    etex = max(abs(ijnu(jnutex + ejnutex, freq) - tex), abs(ijnu(jnutex - ejnutex, freq) - tex))
    return tex, etex


def part_interp():
    return 0
