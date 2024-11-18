
import shapely.wkt
import shapely.errors
import logging
from typing import List, Dict, Any, Tuple
from enum import Enum


class LocationFormat(Enum):
    WKT_RAW = "WKT_RAW"   # Raw means that the WKT string is not wrapped in a GeoJSON object, or any other object.
    WKT_GEOJSON = "WKT_GEOJSON" # GeoJSON means that the WKT string is wrapped in a GeoJSON object.


"""
Validates the location of a dataset in GeoDCAT-AP 3.0 format.

See https://semiceu.github.io/GeoDCAT-AP/releases/3.0.0/#Location for more information.
"""
class GeoDCAT_AP_Location_Validator:
    logger: logging.Logger | None = None


    def __init__(self, logger: logging.Logger):
        self.logger = logger


    def validate_coordinates(self, coordinates : str) -> Tuple[bool, str]:
        """
        Validates the coordinates of a dataset in GeoDCAT-AP 3.0 format.

        :param coordinates: The coordinates of the dataset.
        :type coordinates: str
        :return: True if the coordinates are valid, False otherwise.
        :rtype: bool
        """
        is_validated = False
        is_format = "unknown"

        if self.is_valid_wkt(coordinates):
            is_validated = True
            is_format = "WKT"

        return (is_validated, is_format)




    def is_valid_wkt(self, wkt : str) -> bool:
        """Check if the WKT string is valid.

        Parameters
        ----------
        wkt : str
            WKT string

        Returns
        ------
        bool
            True if WKT is valid, False otherwise
        """
        try:
            shapely.wkt.loads(wkt)
            return True
        except shapely.errors.WKTReadingError:
            self.logger.error(f"Invalid WKT string: {wkt}")
            return False
