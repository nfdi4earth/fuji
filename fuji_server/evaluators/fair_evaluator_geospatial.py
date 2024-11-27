# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

from fuji_server.evaluators.fair_evaluator import FAIREvaluator
from fuji_server.models.geospatial import Geospatial
from fuji_server.models.geospatial_output import GeospatialOutput


class FAIREvaluatorGeospatial(FAIREvaluator):
    """
    A class to evaluate all metrics related to geospatial metadata.
    Basically, this is related to entities described by GeoDCAT-AP.
    ...

    Methods
    -------
    evaluate()
        This method evaluates all metrics that contain tests related to
        geospatial metadata.
    """

    def __init__(self, fuji_instance):
        FAIREvaluator.__init__(self, fuji_instance)
        # although 'set_metric' is able to get a list as input
        # it is not able to handle multiple existing metrics
        # and will simple choose the first, that really exists
        # For now, we have to:
        #   1. set all possbile metrics in the constructor
        #   2. reset them before the evaluation of each test, see `evaluate()`
        # ToDo: implement a better solution, as this works but is kind of hacky
        self.set_metric(["FsF-I3-01M", "FsF-R1-01MD"])

        self.metric_test_map = {  # overall map
            "testGeospatialServiceCategory": ["FsF-I3-01M-3"],
            "testGeospatialServiceType": ["FsF-I3-01M-4"],
            "testGeospatialServiceProtocol": ["FsF-I3-01M-5"],
            "testDebug": ["FsF-R1-01MD-5"],
        }
        self.is_actionable = False

    def testGeospatialServiceCategory(self):
        agnostic_test_name = "testGeospatialServiceCategory"
        test_status = False
        test_defined = False
        for test_id in self.metric_test_map[agnostic_test_name]:
            if self.isTestDefined(test_id):
                test_defined = True
                break
        if test_defined:
            test_score = self.getTestConfigScore(test_id)
            # TODO implement

        return test_status

    def testGeospatialServiceType(self):
        agnostic_test_name = "testGeospatialServiceType"
        test_status = False
        test_defined = False
        for test_id in self.metric_test_map[agnostic_test_name]:
            if self.isTestDefined(test_id):
                test_defined = True
                break
        if test_defined:
            test_score = self.getTestConfigScore(test_id)
            # TODO implement

        return test_status

    def testGeospatialServiceProtocol(self):
        agnostic_test_name = "testGeospatialServiceProtocol"
        test_status = False
        test_defined = False
        for test_id in self.metric_test_map[agnostic_test_name]:
            if self.isTestDefined(test_id):
                test_defined = True
                break
        if test_defined:
            test_score = self.getTestConfigScore(test_id)
            # TODO implement

        return test_status

    # Overwrite the method to print the overarching metric
    # for debugging purposes
    # ToDo: remove this method, when the debugging is done
    def isTestDefined(self, testid):
        result = super().isTestDefined(testid)
        print(f"testid: {testid}")
        print(f"overarching metric: {self.metric_identifier}")
        print(f"isTestDefined: {result}")
        return result

    # This method is only used to debug if this class is able to handle
    # tests from multiple metrics
    # ToDo: remove this method, when the debugging is done
    def testDebug(self):
        agnostic_test_name = "testDebug"
        test_status = False
        test_defined = False
        for test_id in self.metric_test_map[agnostic_test_name]:
            if self.isTestDefined(test_id):
                test_defined = True
                break
        if test_defined:
            test_score = self.getTestConfigScore(test_id)
            # TODO implement

        return test_status

    def evaluate(self):
        self.output = GeospatialOutput()

        self.result = Geospatial(
            id=self.metric_number,
            metric_identifier=self.metric_identifier,
            metric_name=self.metric_name,
        )

        geospatial_status = "fail"

        # set overarching metric
        self.set_metric(["FsF-I3-01M"])
        if self.testGeospatialServiceCategory():
            geospatial_status = "pass"
        if self.testGeospatialServiceProtocol():
            geospatial_status = "pass"
        if self.testGeospatialServiceType():
            geospatial_status = "pass"

        # set overarching metric
        self.set_metric(["FsF-R1-01MD"])
        if self.testDebug():
            geospatial_status = "pass"

        self.result.test_status = geospatial_status
        self.result.output = self.output
        self.result.metric_tests = self.metric_tests
        self.result.score = self.score
        self.result.maturity = self.maturity

    def extract_epsg_code(url):
        # Split the URL using '/' as the delimiter and get the last part
        epsg_code = url.split("/")[-1]
        return epsg_code

    def check_epsg_in_register(epsg_code):
        # Define the URL for the EPSG CRS register with the EPSG code
        url = f"https://www.opengis.net/def/crs/EPSG/0/{epsg_code}"

        try:
            # Send a GET request to the URL
            response = requests.get(url)

            # If the response status code is 200, the EPSG code exists in the register
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException as e:
            # Handle errors in case of a failed request
            print(f"An error occurred: {e}")
            return False
