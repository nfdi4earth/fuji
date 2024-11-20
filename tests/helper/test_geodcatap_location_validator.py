# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

from fuji_server.helper.geodcatap_location_validator import GeoDCAT_AP_Location_Validator
import logging


def test_instance():
    logger = logging.getLogger(__name__)
    gdval = GeoDCAT_AP_Location_Validator(logger)
    assert gdval


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
        assert is_valid


def test_is_valid_wkt_with_invalid_input():

    wkt_invalid1 = "hello world"
    wkt_invalid2 = 'POINT'

    logger = logging.getLogger(__name__)

    invalid_wkt_strings = [wkt_invalid1, wkt_invalid2]

    gdval = GeoDCAT_AP_Location_Validator(logger)
    for wkt in invalid_wkt_strings:
        is_valid, _ = gdval.is_valid_wkt(wkt)
        assert not is_valid


def test_is_valid_geojson_with_valid_input():

    valid_geojson1 = """{ "type": "Point", "coordinates": [125.6, 10.1] }"""

    logger = logging.getLogger(__name__)

    valid_geojson_strings = [valid_geojson1]

    gdval = GeoDCAT_AP_Location_Validator(logger)
    for geojson in valid_geojson_strings:
        is_valid, _ = gdval.is_valid_geojson(geojson)
        assert is_valid


def test_is_valid_geojson_with_invalid_input():

    invalid_geojson1 = 'POINT (30 10)'

    logger = logging.getLogger(__name__)

    valid_geojson_strings = [invalid_geojson1]

    gdval = GeoDCAT_AP_Location_Validator(logger)
    for geojson in valid_geojson_strings:
        is_valid, _ = gdval.is_valid_geojson(geojson)
        assert not is_valid