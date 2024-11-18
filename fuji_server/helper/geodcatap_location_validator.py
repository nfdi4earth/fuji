
import shapely.wkt
import shapely.errors
from shapely import from_wkt, to_wkt, to_geojson
import logging
from typing import List, Dict, Any, Tuple
from enum import Enum
import rdflib

class LocationFormat(Enum):
    WKT_RAW = "WKT_RAW"    # Raw means that the WKT string is not wrapped in a GeoJSON object, or any other object.
    GEOJSON = "GEOJSON"    # GeoJSON format


"""
Validates the location of a dataset in GeoDCAT-AP 3.0 format.

See https://semiceu.github.io/GeoDCAT-AP/releases/3.0.0/#Location for more information.
"""
class GeoDCAT_AP_Location_Validator:
    logger: logging.Logger | None = None


    def __init__(self, logger: logging.Logger):
        self.logger = logger


    def validate(self, input : str) -> Tuple[bool, str]:
        """
        Validates the coordinates of a dataset in GeoDCAT-AP 3.0 format.

        :param coordinates: The coordinates of the dataset.
        :type coordinates: str
        :return: 3-Tuple of bool, LocationFormat and str. The bool is True if the input could be parsed successfully as one of the tested formats, coordinates are valid, and False otherwise. Note that a False does not mean the string is broken, it may be freeform, which is fine, or in a different format. The LocationFormat is the format of the input, if it could be parsed successfully, otherwise None. The str is the normalized input in WKT format, if it could be parsed successfully, otherwise None.
        :rtype: bool
        """
        is_validated = False
        is_format = None
        normalized_input = None   # Normalized to WKT

        if isinstance(input, rdflib.term.Literal):
            input = input.value

        if input is None:
            return (is_validated, is_format, normalized_input) # Return early if input is None

        is_valid_wkt, normalized = self.is_valid_wkt(input)
        if is_valid_wkt:
            is_validated = True
            is_format = LocationFormat.WKT_RAW
            normalized_input = normalized

        is_valid_geojson, normalized = self.is_valid_geojson(input)
        if is_valid_geojson:
            is_validated = True
            is_format = LocationFormat.GEOJSON
            normalized_input = normalized

        return (is_validated, is_format, normalized_input)

    def normalize_shapely_object_to_string(self, shapely_obj : shapely.geometry.base.BaseGeometry) -> str:
        """Normalize a Shapely object to a string.

        Parameters
        ----------
        shapely_obj : shapely.geometry.base.BaseGeometry
            Shapely object

        Returns
        ------
        str
            Normalized string
        """
        return to_wkt(shapely_obj)


    def is_valid_geojson(self, geojson : str) -> bool:
        """Check if the GeoJSON string is valid.

        Parameters
        ----------
        geojson : str
            GeoJSON string

        Returns
        ------
        bool
            True if GeoJSON is valid, False otherwise
        """
        try:
            geom = shapely.geometry.shape(geojson)
            return True, self.normalize_shapely_object_to_string(geom)
        except shapely.errors.WKTReadingError:
            self.logger.error(f"Invalid GeoJSON string: {geojson}")
            return False, None


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
            geom = shapely.wkt.loads(wkt)
            return True, self.normalize_shapely_object_to_string(geom)
        except shapely.errors.WKTReadingError:
            self.logger.info(f"Check for WKT negative: Invalid WKT string: {wkt}")
            return False, None
