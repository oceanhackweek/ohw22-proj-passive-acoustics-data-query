# Author: Roman Battisti
# Project: Passive Acoustic Data Query
# Ocean Hack Week 2022
# GitHub: https://github.com/oceanhackweek/ohw22-proj-passive-acoustics-data-query


def compute_min_max(point: float, radius: float):
    """
    Computes the minimum and maximum of range given a central point and a radius from that point.
    
    :param point: (float) center point for the range.
    :param radius: (float) distance from point. Should be at same scale as point.
    
    :return: (float) minimum and maximum of range.
    """
    
    return (point - radius, point + radius)


def none_or_float(val):
    """Simple check that val exists and converts it to float.
    
    :param val: (None or float convertable object) value to check and convert.
    """
    
    if val:
        return float(val)
    else:
        return val
