# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

from fuji_server.helper.geodcatap_location_validator import GeoDCAT_AP_Location_Validator
import logging

def test_validate_valid_wkt():

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