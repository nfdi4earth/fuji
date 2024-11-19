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
        self.set_metric(["FsF-I3-01M"])
        self.metric_test_map = {  # overall map
            "testGeospatialServiceCategory": ["FsF-I3-01M-3"],
            "testGeospatialServiceType": ["FsF-I3-01M-4"],
            "testGeospatialServiceProtocol": ["FsF-I3-01M-5"],
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

    def evaluate(self):
        self.output = GeospatialOutput()

        self.result = Geospatial(
            id=self.metric_number,
            metric_identifier=self.metric_identifier,
            metric_name=self.metric_name,
        )

        geospatial_status = "fail"
        if self.testGeospatialServiceType():
            geospatial_status = "pass"
        if self.testGeospatialServiceProtocol():
            geospatial_status = "pass"
        if self.testGeospatialServiceProtocol():
            geospatial_status = "pass"

        self.result.test_status = geospatial_status
        self.result.output = self.output
        self.result.metric_tests = self.metric_tests
        self.result.score = self.score
        self.result.maturity = self.maturity
