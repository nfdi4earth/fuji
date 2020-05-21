import connexion
from fuji_server.controllers.fair_check import FAIRCheck
from fuji_server.models.body import Body  # noqa: E501
from fuji_server.models.fair_results import FAIRResults  # noqa: E501


def assess_by_id(body):  # noqa: E501
    """assess_by_id

    Evaluate FAIRness of a data object based on its identifier # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: FAIRResults
    """

    if connexion.request.is_json:
        results = []
        body = Body.from_dict(connexion.request.get_json())  # noqa: E501
        identifier=body.object_identifier
        oai_pmh = body.oaipmh_provider
        debug = body.test_debug
        ft = FAIRCheck(uid=identifier,oai=oai_pmh,test_debug=debug)

        uid_result, pid_result = ft.check_unique_persistent()
        core_metadata_result = ft.check_minimal_metatadata()
        content_identifier_included_result = ft.check_content_identifier_included()
        #check_searchable_result = ft.check_searchable()
        license_result = ft.check_license()
        relatedresources_result = ft.check_relatedresources()
        ft.test_re3data()  # TEST ONLY!!

        results.append(uid_result)
        results.append(pid_result)
        results.append(core_metadata_result)
        results.append(content_identifier_included_result)
        results.append(relatedresources_result)
        results.append(license_result)


    return results

