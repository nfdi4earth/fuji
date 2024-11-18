#!/usr/bin/env python
# -*- coding: utf-8 -*-


# SPDX-FileCopyrightText: 2020 PANGAEA (https://www.pangaea.de/)
#
# SPDX-License-Identifier: MIT

import json
import os

import requests

# That is how a request may look like (from the OpenAPI API)
# curl -X POST "http://localhost:1071/fuji/api/v1/evaluate" -H  "accept: application/json" -H  "Authorization: Basic bWFydmVsOndvbmRlcndvbWFu" -H  "Content-Type: application/json" -d "{\"object_identifier\":\"https://archive.materialscloud.org/record/2021.146\",\"test_debug\":true,\"use_datacite\":true}"

results_folder = "."
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



# Store one file per pid for later report creation
req = requests.post(fuji_api_url, json=req_dict, headers=headers)

rs_json = req.json()
print(rs_json)

res_filename = "fuji_response.json"  # depending on the pid you may want to change this
res_filename_path = os.path.join(results_folder, res_filename)

with open(res_filename_path, "w", encoding="utf-8") as fileo:
  json.dump(rs_json, fileo, ensure_ascii=False)
  print(f"Results stored in {res_filename_path}")
