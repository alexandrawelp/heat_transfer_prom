"""
created on 22.11.2022
compare compressor performance of Bitzer compressor
author: Alexandra Welp
"""

def calculate_polynom(coefficients, to, tc):
    """
    calculates value of polynom for Q, P, m, I depending of coefficients
    :param coefficients: array 1*10
    :param to: evaporating temperature
    :param tc: condensing temperature
    :return: Q, P, m, I depending of input coefficients
    """
    y = coefficients[0] + coefficients[1] * to + coefficients[2] tc + coefficients[3] * to ** 2 + coefficients[4] * to * tc\
        + coefficients[5] * tc ** 2 + coefficients[6] * to ** 3 + coefficients[7] * tc * to ** 2 + coefficients[8] * to * tc ** 2\
        + coefficients[9] * tc ** 3
    return y

