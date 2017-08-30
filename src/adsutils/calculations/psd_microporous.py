"""
Module contains 'classical' methods of calculating a pore size distribution for pores in
the micropore range (<2 nm).
"""

import numpy
import scipy


def psd_horvath_kawazoe(loading, pressure, temperature, pore_geometry,
                        maximum_adsorbed, adsorbate_properties,
                        adsorbent_properties=None):
    """
    Calculates the pore size distribution using the Horvath-Kawazoe method

    :param loading: in mmol/g
    :param pressure: relative
    :param temperature: in K
    :param pore_geometry: 'sphere', 'cylinder' or 'slit'
    :param maximum_adsorbed: the amount of adsorbate filling the micropores
    :param adsorbate_properties: dictionary of properties for the adsorbate in the form of::
        adsorbate_properties = dict(
            molecular_diameter=0,           # nm
            polarizability=0,               # m3
            magnetic_susceptibility=0,      # m3
            surface_density=0,              # molecules/m2
        )
    :param adsorbent_properties: dictionary of properties for the adsorbate in the same form
        A list of common models can be found in .calculations.adsorbent_parameters

    :returns: pore widths, pore distribution
    :rtype: arrays

    **Description:**

    The assumptions made by using the H-K method are:
        - pore is uniform and of infinite extent
        - the wall is made up of single layer atoms
        - only dispersive forces are allowed for
        - the interactions are only between the adsorbent and adsorbate

    The equation underpinning the H-K method is:

    .. math::

        RTln(p/p_0) =   & N_A\\frac{n_a A_a + n_A A_A}{2 \\sigma^{4}(l-d)} \\\\
                        & \\times \\int_{d/_2}^{1-d/_2}
                            \\Big[
                            - \\Big(\\frac{\\sigma}{r}\\Big)^{4}
                            + \\Big(\\frac{\\sigma}{r}\\Big)^{10}
                            - \\Big(\\frac{\\sigma}{l-r}\\Big)^{4}
                            + \\Big(\\frac{\\sigma}{l-r}\\Big)^{4}
                            \\Big] \\mathrm{d}x

    Where:

    * :math:`R` -- gas constant
    * :math:`T` -- temperature
    * :math:`l` -- width of pore
    * :math:`d` -- defined as :math:`d=d_a+d_A` the sum of the diameters of the adsorbate and
      adsorbent molecules
    * :math:`N_A` -- avogadro's number
    * :math:`n_a` -- number of molecules of adsorbent
    * :math:`A_a` -- the Lennard-Jones potential constant of the adsorbent molecule defined as
    .. math::
        A_a = \\frac{6mc^2\\alpha_a\\alpha_A}{\\alpha_a/\\varkappa_a + \\alpha_A/\\varkappa_A}

    * :math:`A_A` -- the Lennard-Jones potential constant of the adsorbate molecule defined as
    .. math::
        A_a = \\frac{3mc^2\\alpha_A\\varkappa_A}{2}

    * :math:`m` -- mass of an electron
    * :math:`c` -- speed of light in vacuum
    * :math:`\\alpha_a` -- polarizability of the adsorbate molecule
    * :math:`\\alpha_A` -- polarizability of the adsorbent molecule
    * :math:`\\varkappa_a` -- magnetic susceptibility of the adsorbate molecule
    * :math:`\\varkappa_A` -- magnetic susceptibility of the adsorbent molecule

    **Limitations:**

    The term :math:`T \\Delta S^{tr}(w/w_{\\infty})` is negligible such that
    The amount adsorbed in the pores is the amount at p/p0 = 0.9

    """

    # Paramter checks
    if pore_geometry == 'slit':
        pass
    elif pore_geometry == 'cylinder':
        raise Exception('Not implemented')
    elif pore_geometry == 'sphere':
        raise Exception('Not implemented')

    if adsorbent_properties is None:
        raise Exception("A dictionary of adsorbent properties must be provided"
                        " for the HK method. The properties required are:"
                        "molecular_diameter, polarizability,"
                        "magnetic_susceptibility and surface_density"
                        "Some standard models can be found in "
                        " .calculations.adsorbent_parameters")
    missing = [x for x in adsorbent_properties if x not in ['molecular_diameter',
                                                            'polarizability',
                                                            'magnetic_susceptibility',
                                                            'surface_density']]
    if len(missing) != 0:
        raise Exception("Adsorbent properties dictionary is missing parameters: "
                        "{}".format(' '.join(missing)))

    if adsorbate_properties is None:
        raise Exception("A dictionary of adsorbate properties must be provided"
                        " for the HK method. The properties required are:"
                        "molecular_diameter, liquid_density, polarizability,"
                        "magnetic_susceptibility, surface_density")
    missing = [x for x in adsorbate_properties if x not in ['molecular_diameter',
                                                            'liquid_density',
                                                            'polarizability',
                                                            'magnetic_susceptibility',
                                                            'surface_density']]
    if len(missing) != 0:
        raise Exception("Adsorbate properties dictionary is missing parameters: "
                        "{}".format(' '.join(missing)))

    # dictionary unpacking
    d_adsorbate = adsorbate_properties.get('molecular_diameter')
    d_adsorbent = adsorbent_properties.get('molecular_diameter')
    p_adsorbate = adsorbate_properties.get('polarizability')
    p_adsorbent = adsorbent_properties.get('polarizability')
    m_adsorbate = adsorbate_properties.get('magnetic_susceptibility')
    m_adsorbent = adsorbent_properties.get('magnetic_susceptibility')
    n_adsorbate = adsorbate_properties.get('surface_density')
    n_adsorbent = adsorbent_properties.get('surface_density')

    # calculation of constants and terms
    e_m = scipy.constants.electron_mass
    c = scipy.constants.speed_of_light
    effective_diameter = d_adsorbate + d_adsorbent
    sigma = (2 / 5)**(1 / 6) * effective_diameter / 2
    sigma_si = sigma * 1e-9

    a_adsorbent = 6 * e_m * c ** 2 * p_adsorbate * p_adsorbent /\
        (p_adsorbate / m_adsorbate + p_adsorbent / m_adsorbent)
    a_adsorbate = 3 * e_m * c**2 * p_adsorbate * m_adsorbate / 2

    constant_coefficient = scipy.constants.Avogadro / \
        (scipy.constants.gas_constant * temperature) * \
        (n_adsorbate * a_adsorbate + n_adsorbent * a_adsorbent) / \
        (sigma_si**4)

    constant_interaction_term = - \
        ((sigma**4) / (3 * (effective_diameter / 2)**3) -
         (sigma**10) / (9 * (effective_diameter / 2)**9))

    def h_k_pressure(l_pore):
        pressure = numpy.exp(constant_coefficient / (l_pore - effective_diameter) *
                             ((sigma**4) / (3 * (l_pore - effective_diameter / 2)**3) -
                              (sigma**10) / (9 * (l_pore - effective_diameter / 2)**9) +
                              constant_interaction_term))

        return pressure

    p_w = []

    for index, p_point in enumerate(pressure):
        # minimise to find pore length
        def h_k_minimization(l_pore):
            return numpy.abs(h_k_pressure(l_pore) - p_point)
        res = scipy.optimize.minimize_scalar(h_k_minimization)
        p_w.append(res.x - d_adsorbent)

    # finally calculate pore distribution
    pore_widths = numpy.array(p_w)
    avg_pore_widths = numpy.add(pore_widths[:-1], pore_widths[1:]) / 2
    pore_dist = numpy.diff(loading / maximum_adsorbed) / \
        numpy.diff(pore_widths)
    c_pore_dist = loading / maximum_adsorbed

    return avg_pore_widths, pore_dist