# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

import feedparser

from fuji_server.helper.metadata_provider import MetadataProvider
from fuji_server.helper.request_helper import AcceptTypes, RequestHelper


class RSSAtomMetadataProvider(MetadataProvider):
    """A metadata provider class to provide the metadata from GeoRSS ATOM

    ...

    Methods
    -------
    getMetadataStandards()
        Method will return the metadata standards in the namespaces
    getMetadata(queryString)
        Method that will return schemas of GeoRSS Atom
    getNamespaces()
        Method to get namespaces

    """

    rss_namespaces = {"atom": "http://www.w3.org/2005/Atom", "georss": "http://www.georss.org/georss/"}

    def getMetadata(self):
        # http://ws.pangaea.de/oai/provider?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:pangaea.de:doi:10.1594/PANGAEA.66871
        # The nature of a resource identifier is outside the scope of the OAI-PMH.
        # To facilitate access to the resource associated with harvested metadata, repositories should use an element in
        # #metadata records to establish a linkage between the record (and the identifier of its item) and the identifier
        # URL, URN, DOI, etc.) of the associated resource.
        # #The mandatory Dublin Core format provides the identifier element that should be used for this purpose
        return None

    def getMetadataStandards(self):
        """Method to get the metadata schema from the GeoRSS Atom namespaces

        Returns
        -------
        dict
            A dictionary of schemas in GeoRSS Atom
        """
        schemas = {}

        try:
            requestHelper = RequestHelper(self.endpoint, self.logger)
            requestHelper.setAcceptType(AcceptTypes.default)
            neg_source, rss_response = requestHelper.content_negotiate("FsF-F2-01M")
            if requestHelper.response_content is not None:
                feed = feedparser.parse(requestHelper.response_content)
            # print(feed.namespaces)
            for namespace_pre, namespace_uri in feed.namespaces.items():
                if namespace_uri not in self.namespaces:
                    self.namespaces.append(str(namespace_uri))
                    schemas[str(namespace_pre)] = str(namespace_uri)
        except Exception as e:
            print("RSS Error ", e)
            self.logger.info(
                f"{self.metric_id} : Could not parse response retrieved from RSS/Atom Feed endpoint -: {e!s}"
            )

        return schemas

    def getNamespaces(self):
        return self.namespaces
