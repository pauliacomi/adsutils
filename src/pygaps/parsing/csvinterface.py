"""
This module contains the csv interface.
"""

import pandas

from ..classes.modelisotherm import ModelIsotherm
from ..classes.pointisotherm import PointIsotherm


def isotherm_to_csv(isotherm, path, separator=','):
    '''

    A function that turns the isotherm into a csv
    file with the data and properties.

    Parameters
    ----------
    isotherm : PointIsotherm
        Isotherm to be written to csv.
    path : str
        Path to the file to be written.
    separator : str, optional
        Separator used int the csv file. Defaults to '',''.

    '''

    with open(path, mode='w') as file:

        isotherm_data = isotherm.to_dict()

        file.writelines([x + separator + str(y) + '\n'
                         for (x, y) in isotherm_data.items()])

        if isinstance(isotherm, PointIsotherm):

            # get headings in an ordered way
            headings = [
                isotherm.pressure_key,
                isotherm.loading_key,
            ]
            if isotherm.other_keys:
                headings.extend(isotherm.other_keys)
            data = isotherm.data()[headings]

            file.write('data:[pressure, loading, other...]\n')
            file.write(data.to_csv(None, sep=separator, index=False, header=True))

        elif isinstance(isotherm, ModelIsotherm):
            raise NotImplementedError
    return


def isotherm_from_csv(path, separator=',', branch='guess'):
    """
    A function that will get the experiment and sample data from a csv file
    file and return the isotherm object.

    Parameters
    ----------
    path : str
        Path to the file to be read.
    separator : str, optional
        Separator used int the csv file. Defaults to '',''.

    Returns
    -------
    PointIsotherm
        The isotherm contained in the csv file.
    """

    with open(path) as file:
        line = file.readline().rstrip()
        material_info = {}

        while not line.startswith('data'):
            values = line.split(sep=separator)
            material_info.update({values[0]: values[1]})
            line = file.readline().rstrip()

        data_df = pandas.read_csv(file, sep=separator)

    isotherm = PointIsotherm(
        data_df,
        branch=branch,
        pressure_key=data_df.columns[0],
        loading_key=data_df.columns[1],
        other_keys=list(data_df.columns[2:]),
        **material_info)

    return isotherm
