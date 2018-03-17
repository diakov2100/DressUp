import numpy

from colormath import color_diff_matrix
from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, sRGBColor

def hex_to_rgb(value: str) -> list:
    """
    Converts from hex string to rgb list
    """
    value = value.lstrip('#')
    value_length = len(value)
    if value_length != 3 and value_length != 6:
        raise ValueError('hex string must be of length 3 or 6')
    if value_length == 3:
        value = ''.join(map(lambda x: x + x, value))
        value_length = len(value)
    return list(int(value[i:i + value_length // 3], 16) for i in
                range(0, value_length, value_length // 3))

def _get_lab_color1_vector(color):
    """
    Converts an LabColor into a NumPy vector.
    :param LabColor color:
    :rtype: numpy.ndarray
    """
    if not color.__class__.__name__ == 'LabColor':
        raise ValueError(
            "Delta E functions can only be used with two LabColor objects.")
    return numpy.array([color.lab_l, color.lab_a, color.lab_b])


def _get_lab_color2_matrix(color):
    """
    Converts an LabColor into a NumPy matrix.
    :param LabColor color:
    :rtype: numpy.ndarray
    """
    if not color.__class__.__name__ == 'LabColor':
        raise ValueError(
            "Delta E functions can only be used with two LabColor objects.")
    return numpy.array([(color.lab_l, color.lab_a, color.lab_b)])


# noinspection PyPep8Naming
def delta_e_cie1976(color1, color2):
    """
    Calculates the Delta E (CIE1976) of two colors.
    """
    color1_vector = _get_lab_color1_vector(color1)
    color2_matrix = _get_lab_color2_matrix(color2)
    delta_e = color_diff_matrix.delta_e_cie1976(color1_vector, color2_matrix)[0]
    return numpy.asscalar(delta_e)


# noinspection PyPep8Naming
def delta_e_cie1994(color1, color2, K_L=1, K_C=1, K_H=1, K_1=0.045, K_2=0.015):
    """
    Calculates the Delta E (CIE1994) of two colors.
    K_l:
      0.045 graphic arts
      0.048 textiles
    K_2:
      0.015 graphic arts
      0.014 textiles
    K_L:
      1 default
      2 textiles
    """
    color1_vector = _get_lab_color1_vector(color1)
    color2_matrix = _get_lab_color2_matrix(color2)
    delta_e = color_diff_matrix.delta_e_cie1994(
        color1_vector, color2_matrix, K_L=K_L, K_C=K_C, K_H=K_H, K_1=K_1, K_2=K_2)[0]
    return numpy.asscalar(delta_e)


# noinspection PyPep8Naming
def delta_e_cie2000(color1, color2, Kl=1, Kc=1, Kh=1):
    """
    Calculates the Delta E (CIE2000) of two colors.
    """
    color1_vector = _get_lab_color1_vector(color1)
    color2_matrix = _get_lab_color2_matrix(color2)
    delta_e = color_diff_matrix.delta_e_cie2000(
        color1_vector, color2_matrix, Kl=Kl, Kc=Kc, Kh=Kh)[0]
    return numpy.asscalar(delta_e)


# noinspection PyPep8Naming
def delta_e_cmc(color1, color2, pl=2, pc=1):
    """
    Calculates the Delta E (CMC) of two colors.
    CMC values
      Acceptability: pl=2, pc=1
      Perceptability: pl=1, pc=1
    """
    color1_vector = _get_lab_color1_vector(color1)
    color2_matrix = _get_lab_color2_matrix(color2)
    delta_e = color_diff_matrix.delta_e_cmc(
        color1_vector, color2_matrix, pl=pl, pc=pc)[0]
    return numpy.asscalar(delta_e)

def _to_lab(color):
    """
    Converts to Lab color space
    """
    try:
        color = hex_to_rgb(color) if isinstance(color, str) else color
        return convert_color(sRGBColor(*color), LabColor)
    except (TypeError, ValueError):
        return None
    
def compare(set1, set2, set3, colors):
        """
        Tests for colors.close_color._to_lab function
        """
        sets=[set1, set2, set3]
        for set in sets:
            for set_color in set:
                s=0;
                for color in colors:
                    x=_to_lab(set_color)
                    y=_to_lab(color['value'])
                    s+=delta_e_cmc(x, y) + delta_e_cie2000(x, y)
                    print(s);
                if s<len(colors)*210:
                    return True;
        return False;
