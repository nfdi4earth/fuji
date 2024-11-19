#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

import json
import os

import requests

# That is how a request may look like (from the OpenAPI API)
# curl -X POST "http://localhost:1071/fuji/api/v1/evaluate" -H  "accept: application/json" -H  "Authorization: Basic bWFydmVsOndvbmRlcndvbWFu" -H  "Content-Type: application/json" -d "{\"object_identifier\":\"https://archive.materialscloud.org/record/2021.146\",\"test_debug\":true,\"use_datacite\":true}"

results_folder = "./results/"
# pids = ["https://archive.materialscloud.org/record/2021.146"]

# or load pids from a file with one pid per line, which you have to generate beforehand
# with open('dois.txt', 'r') as fileo:
#    pids = fileo.readlines()

fuji_api_url = "http://localhost:1071/fuji/api/v1/evaluate"
# the Authorization key you get from your running OpenAPI API instance
headers = {
    "accept": "application/json",
    "Authorization": "Basic bWFydmVsOndvbmRlcndvbWFu",
    "Content-Type": "application/json",
}
req_dict = {
    "object_identifier": "https://klimakonform-dmp.geo.tu-dresden.de/dataset/kk-gebiet-tagliche-mdk-projektion-bias-corrected",
    "test_debug": True,
    "metadata_service_endpoint": "http://ws.pangaea.de/oai/provider",
    "metadata_service_type": "oai_pmh",
    "use_datacite": True,
    "use_github": False,
    "metric_version": "metrics_v0.5geodcat"
 }


req_dict_bad = {
    "object_identifier": "https://spatialdata.gov.scot/geonetwork/api/collections/main/items/fa510351-8e30-4147-b984-862be84a6f90?f=dcat",
    "test_debug": True,
    "metadata_service_endpoint": "http://ws.pangaea.de/oai/provider",
    "metadata_service_type": "oai_pmh",
    "use_datacite": True,
    "use_github": False,
    "metric_version": "metrics_v0.5geodcat"
} 

# Store one file per pid for later report creation
req = requests.post(fuji_api_url, json=req_dict_bad, headers=headers)

rs_json = req.json()
print(rs_json)

res_filename_path = os.path.join(results_folder, "res.json")

with open(res_filename_path, "w", encoding="utf-8") as fileo:    
    json.dump(rs_json, fileo, ensure_ascii=False)
