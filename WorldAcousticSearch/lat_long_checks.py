# Author: Roman Battisti
# Project: Passive Acoustic Data Query
# Ocean Hack Week 2022
# GitHub: https://github.com/oceanhackweek/ohw22-proj-passive-acoustics-data-query


def min_max_coords(coords: list, type_gps: str):
    assert type_gps in ["lat", "long"]
    
    isLong = (type_gps == "long")
    coords_out = []
    for i, c in enumerate(coords):
        if not c:
            coords_out.append(90. * (1 + (1 * isLong)) * (-1 + (2 * i)))
        else:
            coords_out.append(convertLatLong(c, type_gps))
    return coords_out


def convertLatLong(l, type_gps: str) -> float:
    """
    Converts a string latitude/longitude to float.
    
    :param l: latitude. If latitude is type str, convert to float.
    :param type_gps: (str) specify whether latitude (lat) or longitude (long)
    
    :return: (float)
    """
    
    assert type_gps in ["lat", "long"]
    
    if not l:
        return l
    
    if type(l) == str:
        try:
            l = float(l)
        except ValueError as e:
            print(e)
    
    if type_gps == "lat":
        try:
            return latCheck(l)
        except LatitudeException as e:
            print(e)
    else:
        try:
            return longCheck(l)
        except LongitudeException as e:
            print(e)
    return e
    

def latCheck(lat: float) -> float:
    """
    Check that Latitude is between -90 and 90. Raises error if not.
    
    :param lat: (float) latitude
    
    :return: (float) latitude
    """
    
    if lat >= -90 and lat <= 90:
        return lat
    else:
        raise LatitudeException(f"The latitude {lat} does not lie between -90 and 90!")
    


def longCheck(long: float) -> float:
    """
    Check that Longitude is between -180 and 180
    
    :param long: (float) longitude
    
    :return: (float) longitude
    """
    
    if long >= -180 and long <= 180:
        return long
    else:
        raise LongitudeException(f"The longitude {long} does not lie between -180 and 180!")


class LatitudeException(Exception):
    pass


class LongitudeException(Exception):
    pass