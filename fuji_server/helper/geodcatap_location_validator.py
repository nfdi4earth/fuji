
import rdflib.term
import shapely.wkt
import shapely.errors
from shapely import from_wkt, to_wkt, to_geojson, from_wkb, from_wkt
import logging
from typing import List, Dict, Any, Tuple, Union
from enum import Enum
import rdflib
from rdflib.namespace import XSD
import json

class LocationFormat(Enum):
    WKT = "WKT"            # Well-Known Text format
    GEOJSON = "GEOJSON"    # GeoJSON format
    KML = "KML"            # KML format: Keyhole Markup Language
    GML = "GML"            # GML format: Geography Markup Language
    WKB = "WKB"            # WKB format: Well-Known Binary




"""
Validates the location of a dataset in GeoDCAT-AP 3.0 format.

See https://semiceu.github.io/GeoDCAT-AP/releases/3.0.0/#Location for more information.
"""
class GeoDCAT_AP_Location_Validator:
    logger: logging.Logger | None = None


    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger
        if self.logger is None:
            self.logger = logging.getLogger(__name__)

    def get_formats_for_literal_datatype(self, datatype: rdflib.term.URIRef) -> List[LocationFormat]:
        """
        Get the supported formats for a given datatype of a literal.

        :param datatype: The datatype of the literal.
        :type datatype: rdflib.term.URIRef
        :return: List of supported formats for the given datatype.
        :rtype: List[LocationFormat]
        """
        if datatype == XSD.wktLiteral:
            return [LocationFormat.WKT]
        elif datatype == XSD.geojson:
            return [LocationFormat.GEOJSON]
        elif datatype == XSD.string:
            # we don't know, return all available formats
            [lf for lf in LocationFormat]
        elif datatype == XSD.anyURI:
            # we don't know, return all available formats
            [lf for lf in LocationFormat]  # We could check for custom strings here
        else:
            # we don't know, return all available formats
            self.logger.debug(f"Could not auto-detect format for datatype: {datatype}. Will check all available formats.")
            return [lf for lf in LocationFormat]




    def validate(self, input : Union[rdflib.term.Literal, str, None], check_values : Union[List[LocationFormat], str] = [lf for lf in LocationFormat]) -> Tuple[bool, str]:
        """
        Validates the coordinates of a dataset in GeoDCAT-AP 3.0 format.

        :param input: The coordinate metadata of the dataset.
        :type input: str, None, or rdflib.term.Literal
        :param check_values: The formats to check for. If set to "auto_detect", the function will try to detect the format based on the datatype of the input, if the input is of type ```rdflib.term.Literal```. If set to a list of LocationFormat values, the function will only check for the specified formats. Defaults to all available formats from the enum ```LocationFormat```.
        :type check_values: List[LocationFormat], str
        :return: 3-Tuple of ```bool```, ```LocationFormat``` and ```str```. The ```bool``` is ```True``` if the input could be parsed successfully as one of the tested formats, and ```False``` otherwise. Note that a ```False``` does not mean the string is broken, it may be freeform, which is fine, or in a different format which we did not check for. The ```LocationFormat``` entry in the tuple is the format of the input, if it could be parsed successfully, otherwise ```None```. The ```str``` is the normalized input in WKT format, if it could be parsed successfully, otherwise ```None```.
        :rtype: bool
        """
        is_validated = False
        is_format = None
        normalized_input = None   # Normalized to WKT

        if input is None:
            return (is_validated, is_format, normalized_input) # Return early if input is None

        if isinstance(input, rdflib.term.Literal):
            datatype = input.datatype
            self.logger.debug(f"Type of input: {type(input)}")
            input = str(input)
            self.logger.debug(f"Input is Literal with datatype: {datatype} and value: {input}")
        else:
            # Check if input is a string
            if not isinstance(input, str):
                raise ValueError("Expected input to be a string or rdflib.term.Literal")
            self.logger.debug(f"Input is string: {input}")
            datatype = None

        self.logger.debug(f"validate() Input: {input}")

        if datatype is not None and check_values == "auto_detect":
            check_values = self.get_formats_for_literal_datatype(datatype)
            self.logger.debug(f"Formats to check for (auto-detected): {check_values}")
        else:
            self.logger.debug(f"Formats to check for (requested by user): {check_values}")

        for format in check_values:
            is_valid, normalized = self.is_valid_format(input, format)
            if is_valid:
                is_validated = True
                is_format = format
                normalized_input = normalized
                break

        return (is_validated, is_format, normalized_input)


    def is_valid_format(self, input: str, format: LocationFormat) -> Tuple[bool, str]:
        """
        Check if the input string is valid in the specified format.

        :param input: The input string to check.
        :type input: str
        :param format: The format to check for.
        :type format: LocationFormat
        :return: 2-Tuple of ```bool``` and ```str```. The ```bool``` is ```True``` if the input could be parsed successfully as the specified format, and ```False``` otherwise. Note that a ```False``` does not mean the string is broken, it may be freeform, which is fine, or in a different format which we did not check for. The ```str``` is the normalized input in WKT format, if it could be parsed successfully, otherwise ```None```.
        :rtype: Tuple[bool, str]
        """
        is_valid = False
        normalized = None

        if format == LocationFormat.WKT:
            is_valid, normalized = self.is_valid_wkt(input)
        elif format == LocationFormat.GEOJSON:
            is_valid, normalized = self.is_valid_geojson(input)
        elif format == LocationFormat.KML:
            is_valid, normalized = self.is_valid_kml(input)
        elif format == LocationFormat.GML:
            is_valid, normalized = self.is_valid_gml(input)
        elif format == LocationFormat.WKB:
            is_valid, normalized = self.is_valid_wkb(input)
        else:
            raise ValueError(f"Unsupported format: {format}")

        self.logger.debug(f"# Checking for {format}... Yes") if is_valid else self.logger.debug(f"# Checking for {format}... No")

        return (is_valid, normalized)


    def normalize_shapely_object_to_string(self, shapely_obj : shapely.geometry.base.BaseGeometry) -> str:
        """
        Normalize a Shapely object to a string. We use this function to convert all different
        input coordinate representation to a single one we consider our standard. For now, this
        standard is WKT.


        Parameters
        ----------
        shapely_obj : shapely.geometry.base.BaseGeometry
            Shapely object

        Returns
        ------
        str
            Normalized string in WKT format
        """
        return to_wkt(shapely_obj)


    def is_valid_geojson(self, input : str) -> Tuple[bool, str]:
        """
        Check if the input string is valid GeoJSON.
        Tries to load the input as JSON. If successful, tries to load the JSON using ```shapely```.

        Parameters
        ----------
        input : str
            string to check for GeoJSON format

        Returns
        ------
        bool
            ```True``` if input could be parsed as GeoJSON format, ```False``` otherwise
        input_converted : str | None
            the input converted to a WKT format ```str``` if the parsing was successful, otherwise ```None```
        """
        try:
            input_json = json.loads(input)
            geom = shapely.geometry.shape(input_json)
            return True, self.normalize_shapely_object_to_string(geom)
        except Exception as e:
            self.logger.debug(f"Check for GeoJSON negative for input: '{input}' with error: {str(e)}")
            return False, None


    def is_valid_wkt(self, input : str) -> Tuple[bool, str]:
        """Check if the input string is valid WKT.

        Parameters
        ----------
        input : str
            string to check for WKT format

        Returns
        ------
        bool
            True if input could be parsed as WKT format, False otherwise
        input_converted : str | None
            input as WKT format, if the parsing was successful, otherwise None
        """
        try:
            geom = from_wkt(input)
            return True, self.normalize_shapely_object_to_string(geom)
        except Exception as e:
            self.logger.debug(f"Check for WKT negative for input: '{input}' with error: {str(e)}")
            return False, None


    def is_valid_kml(self, input : str) -> Tuple[bool, str]:
        """
        Check if the input string is valid KML.
        KML is the Keyhole Markup Language, an XML-based language schema for expressing geographic annotations.

        Parameters
        ----------
        input : str
            string to check for KML format

        Returns
        ------
        bool
            True if input could be parsed as KML format, False otherwise
        input_converted : str | None
            input as WKT format, if the parsing was successful, otherwise None
        """
        try:
            import fastkml.kml as kml
            k = kml.KML.from_string(input)
            # KML is a container format that may contain information on several Placemarks, which each may have a 'geometry' feature.
            # In the following, we arbitrarily test the first feature to see whether it has a geometry.
            norm = None
            try:
                if len(k.__geo_interface__["features"]) >= 1:
                    feature = k.__geo_interface__["features"][0] # Get the first feature or Placemark
                    geometry = shapely.geometry.shape(feature["geometry"])
                    geom = shapely.geometry.shape(geometry)
                    norm = self.normalize_shapely_object_to_string(geom)
            except Exception as e:
                pass  # It's fine if we can't parse the geometry. We cannot convert to a common format in this case.
            return True, norm
        except Exception as e:
            self.logger.debug(f"Check for KML negative for input: '{input}' with error: {str(e)}")
            return False, None


    def is_valid_gml(self, input : str) -> Tuple[bool, str]:
        """
        Check if the input string is valid GML.
        GML is the Geography Markup Language, an XML grammar for expressing geographical features.

        Parameters
        ----------
        input : str
            string to check for GML format

        Returns
        ------
        bool
            True if input could be parsed as GML format, False otherwise
        input_converted : str | None
            input as WKT format, if the parsing was successful, otherwise None
        """
        try:
            import pygml
            geom_xml_tree = pygml.parse(input)
            geom = shapely.geometry.shape(geom_xml_tree.__geo_interface__)
            return True, self.normalize_shapely_object_to_string(geom)
        except Exception as e:
            print(f"Check for GML negative for input: '{input}' with error: {str(e)}")
            return False, None


    def is_valid_wkb(self, input : str) -> Tuple[bool, str]:
        """
        Check if the input string is valid WKB.
        WKB is the Well-Known Binary format for representing geometry.

        Parameters
        ----------
        input : str
            string to check for WKB format

        Returns
        ------
        bool
            True if input could be parsed as WKB format, False otherwise
        input_converted : str | None
            input as WKT format, if the parsing was successful, otherwise None
        """
        try:
            geom = from_wkb(input)
            return True, self.normalize_shapely_object_to_string(geom)
        except Exception as e:
            self.logger.debug(f"Check for WKB negative for input: '{input}' with error: {str(e)}")
            return False, None




    def test_stuff(self):
        """This function will be removed later. It's just for testing purposes."""
        self.logger.warning("Testing stuff... This function will be removed later.")
        geojson = '{"type":"MultiPolygon","coordinates":[[[[11.822662353515623,50.42415935070463],[11.822662353515623,50.82491508698821],[12.564239501953123,50.82491508698821],[12.564239501953123,50.42415935070463],[11.822662353515623,50.42415935070463]]]]}'
        geojson = json.loads(geojson)
        geom = shapely.geometry.shape(geojson)
        self.logger.debug(f"test_stuff: geom: {geom}")


