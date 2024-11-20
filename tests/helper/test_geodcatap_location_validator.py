# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

from fuji_server.helper.geodcatap_location_validator import GeoDCAT_AP_Location_Validator, LocationFormat
import logging
from shapely import from_wkt, to_wkb

def test_instance_with_logger():
    logger = logging.getLogger(__name__)
    gdval = GeoDCAT_AP_Location_Validator(logger)
    assert gdval


def test_instance_without_logger():
    gdval = GeoDCAT_AP_Location_Validator()
    assert gdval

###  ------------------------------------- is_valid_format tests ------------------------------------- ###


def test_is_valid_wkt_with_valid_input():

    wkt_point = 'POINT (30 10)'
    wkt_linestring = 'LINESTRING (30 10, 10 30, 40 40)'
    wkt_polygon = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
    wkt_multipoint = 'MULTIPOINT (10 40, 40 30, 20 20, 30 10)'
    wkt_multilinestring = 'MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20, 30 10))'
    wkt_multipolygon = 'MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))'
    wkt_geometrycollection = 'GEOMETRYCOLLECTION (POINT (40 10), LINESTRING (10 10, 20 20, 10 40))'

    logger = logging.getLogger(__name__)

    valid_wkt_strings = [wkt_point, wkt_linestring, wkt_polygon, wkt_multipoint, wkt_multilinestring, wkt_multipolygon, wkt_geometrycollection]

    gdval = GeoDCAT_AP_Location_Validator(logger)
    for wkt in valid_wkt_strings:
        is_valid, _ = gdval.is_valid_wkt(wkt)
        assert is_valid, f"Expected valid WKT string: {wkt}"


def test_is_valid_wkt_with_invalid_input():

    wkt_invalid1 = "hello world"
    wkt_invalid2 = 'POINT'

    logger = logging.getLogger(__name__)

    invalid_wkt_strings = [wkt_invalid1, wkt_invalid2]

    gdval = GeoDCAT_AP_Location_Validator(logger)
    for wkt in invalid_wkt_strings:
        is_valid, _ = gdval.is_valid_wkt(wkt)
        assert not is_valid, f"Expected invalid WKT string: {wkt}"


def test_is_valid_geojson_with_valid_input():

    valid_geojson1 = """{ "type": "Point", "coordinates": [125.6, 10.1] }"""

    logger = logging.getLogger(__name__)

    valid_geojson_strings = [valid_geojson1]

    gdval = GeoDCAT_AP_Location_Validator(logger)
    for geojson in valid_geojson_strings:
        is_valid, _ = gdval.is_valid_geojson(geojson)
        assert is_valid, f"Expected valid GeoJSON string: {geojson}"


def test_is_valid_geojson_with_invalid_input():

    invalid_geojson1 = 'POINT (30 10)'
    invalid_geojson2 = """{ "type": "Dunno", "coordinates": [] }"""

    logger = logging.getLogger(__name__)

    valid_geojson_strings = [invalid_geojson1, invalid_geojson2]

    gdval = GeoDCAT_AP_Location_Validator(logger)
    for geojson in valid_geojson_strings:
        is_valid, _ = gdval.is_valid_geojson(geojson)
        assert not is_valid, f"Expected invalid GeoJSON string: {geojson}"


def test_is_valid_kml_with_valid_input():
    valid_kml1 = """<kml xmlns="http://www.opengis.net/kml/2.2">
            <Document>
            <name>Document.kml</name>
            <open>1</open>
            <Style id="exampleStyleDocument">
                <LabelStyle>
                <color>ff0000cc</color>
                </LabelStyle>
            </Style>
            <Placemark>
                <name>Document Feature 1</name>
                <styleUrl>#exampleStyleDocument</styleUrl>
                <Point>
                <coordinates>-122.371,37.816,0</coordinates>
                </Point>
            </Placemark>
            <Placemark>
                <name>Document Feature 2</name>
                <styleUrl>#exampleStyleDocument</styleUrl>
                <Point>
                <coordinates>-122.370,37.817,0</coordinates>
                </Point>
            </Placemark>
            </Document>
            </kml>"""

    valid_kml_strings = [valid_kml1]

    gdval = GeoDCAT_AP_Location_Validator()
    for kml in valid_kml_strings:
        is_valid, _ = gdval.is_valid_kml(kml)
        assert is_valid, f"Expected valid KML string: {kml}"


def test_is_valid_kml_with_invalid_input():
    invalid_kml1 = """<kml xmlns="http://www.opengis.net/kml/2.2">
            <Document>
            <name>Document.kml
            </Placemark>
            </Document>
            </kml>"""

    invalid_kml_strings = [invalid_kml1]

    gdval = GeoDCAT_AP_Location_Validator()
    for kml in invalid_kml_strings:
        is_valid, _ = gdval.is_valid_kml(kml)
        assert not is_valid, f"Expected invalid KML string: {kml}"


def test_is_valid_gml_with_valid_input():
    valid_gml1 = """<gml:Point xmlns:gml="http://www.opengis.net/gml" srsDimension="2" srsName="http://www.opengis.net/def/crs/EPSG/0/4326">
                     <gml:pos>49.40 -123.26</gml:pos>
                 </gml:Point>"""
    valid_gml_strings = [valid_gml1]

    gdval = GeoDCAT_AP_Location_Validator()
    for gml in valid_gml_strings:
        is_valid, _ = gdval.is_valid_gml(gml)
        assert is_valid, f"Expected valid GML string: {gml}"


def test_is_valid_gml_with_invalid_input():
    invalid_gml1 = """<gml:Pointy xmlns:gml="http://www.opengis.net/gml">
            <gml:coordinatesAndSomeMore>45.67,88.56
            </gml:Pointy>"""

    invalid_gml_strings = [invalid_gml1]

    gdval = GeoDCAT_AP_Location_Validator()
    for gml in invalid_gml_strings:
        is_valid, _ = gdval.is_valid_gml(gml)
        assert not is_valid, f"Expected invalid GML string: {gml}"


def test_is_valid_wkb_with_valid_input():
    wkt_point_str = 'POINT (30 10)'
    wkt_linestring_str = 'LINESTRING (30 10, 10 30, 40 40)'
    wkt_polygon_str = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'

    shapely_point = from_wkt(wkt_point_str)
    shapely_linestring = from_wkt(wkt_linestring_str)
    shapely_polygon = from_wkt(wkt_polygon_str)

    valid_wkb1 : bytes = to_wkb(shapely_point)
    valid_wkb2 : bytes = to_wkb(shapely_linestring)
    valid_wkb3 : bytes = to_wkb(shapely_polygon)

    valid_wkbs = [valid_wkb1, valid_wkb2, valid_wkb3]

    gdval = GeoDCAT_AP_Location_Validator()
    for wkb in valid_wkbs:
        is_valid, _ = gdval.is_valid_wkb(wkb)
        assert is_valid, f"Expected valid WKB string: {wkb}"


### -------------------------------- Identify format tests -------------------------------- ###

def test_geojson_is_identified_correctly():
    valid_geojson1 = """{ "type": "Point", "coordinates": [125.6, 10.1] }"""
    gdval = GeoDCAT_AP_Location_Validator()
    is_validated, is_format, normalized_input = gdval.validate(valid_geojson1)
    assert is_validated, f"Expected valid GeoJSON string: {valid_geojson1}"
    assert is_format == LocationFormat.GEOJSON, f"Expected format 'geojson', got {str(is_format)}"
    assert isinstance(normalized_input, str), f"Expected normalized input to be a string, got {normalized_input}"


def test_wkt_is_identified_correctly():
    wkt_point = 'POINT (30 10)'
    gdval = GeoDCAT_AP_Location_Validator()
    is_validated, is_format, normalized_input = gdval.validate(wkt_point)
    assert is_validated, f"Expected valid WKT string: {wkt_point}"
    assert is_format == LocationFormat.WKT, f"Expected format 'wkt', got {str(is_format)}"
    assert isinstance(normalized_input, str), f"Expected normalized input to be a string, got {normalized_input}"

