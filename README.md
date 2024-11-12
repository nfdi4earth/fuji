### F-UJI Tool Adjustment

#### Necessary Steps:

1. [**Metadata Harvester**](https://github.com/pangaea-data-publisher/fuji/blob/master/fuji_server/harvester/metadata_harvester.py)

- This is where the metadata is harvested.
- Problem: Only basic properties are harvested here. A later test on GeoDCAT would logically only work if we harvest corresponding properties.
- These are then stored in the [FAIRCheck object](https://github.com/pangaea-data-publisher/fuji/blob/ba289b056632af125e56c43761636f1e70d391f4/fuji_server/controllers/fair_check.py#L62)

Implementations:
- The Metadata Harvester uses several helper classes to collect metadata (in */fuji_server/harvester/helper/*)
- There is a class [MetaDataCollectorRdf](https://github.com/pangaea-data-publisher/fuji/blob/master/fuji_server/helper/metadata_collector_rdf.py), which tries to generate an RDF graph from the available interfaces and read metadata. Here, the DCAT properties are also read => see [method here](https://github.com/pangaea-data-publisher/fuji/blob/ba289b056632af125e56c43761636f1e70d391f4/fuji_server/helper/metadata_collector_rdf.py#L1109)
- I have implemented another method *fuji_server.helper.MetaDataCollectorRdf.get_geodcat_metadata()* that reads the properties relevant for GeoDCAT-AP
- Additionally, the method *fuji_server.helper.MetaDataCollectorRdf.get_metadata_from_graph()* had to be adjusted so that GeoDCAT properties are read when the corresponding namespace ([http://data.europe.eu/930/](http://data.europe.eu/930/)) is present
- After collecting the metadata using the helper classes in [Metadata Harvester](https://github.com/pangaea-data-publisher/fuji/blob/master/fuji_server/harvester/metadata_harvester.py), these are passed to a method [*fuji_server.harvester.MetadataHarvester.merge_metadata*](https://github.com/pangaea-data-publisher/fuji/blob/ba289b056632af125e56c43761636f1e70d391f4/fuji_server/harvester/metadata_harvester.py#L139) and the metadata harvested from different sources are fused (these fused metadata are later passed [here](https://github.com/pangaea-data-publisher/fuji/blob/ba289b056632af125e56c43761636f1e70d391f4/fuji_server/controllers/fair_check.py#L435) to the FAIRCheck object). This method also needs to be adjusted to retain the GeoDCAT properties in the fused metadata. I added a geospatial_properties attribute to the MetadataHarvester class, in which the properties are stored
- ⚠️ Only the properties that are also listed in [*fuji_server.helper.metadata_mapper.REFERENCE_METADATA_LIST*](https://github.com/pangaea-data-publisher/fuji/blob/master/fuji_server/helper/metadata_mapper.py) are considered here ([see this line](https://github.com/pangaea-data-publisher/fuji/blob/ba289b056632af125e56c43761636f1e70d391f4/fuji_server/harvester/metadata_harvester.py#L161)) => Therefore, I have listed some GeoDCAT relevant properties here
- #TODO: automatically read the *MetadataHarvester.geospatial_properties* based on the properties from the mapping file, instead of hardcoding properties in *merge_metadata()*

2. **Evaluation:**

- After the GeoDCAT properties have been harvested, the evaluation can now be modified
- Necessary for this is:
  - Creation of a new metric in one of the config files in *fuji_server/yaml/*
    - [According to the documentation](https://github.com/pangaea-data-publisher/fuji/tree/master?tab=readme-ov-file#adding-support-for-new-metrics), one of the existing files should be used as a template
    - In *fuji_server.helper.metric_helper.MetricHelper*, the metrics are read from the yaml file. For this, it is checked relatively restrictively via regex whether the metric names correspond to the required patterns => I have had the best experiences with adding additional tests to existing metrics
    - I created a copy of [metrics_v0.5.yaml](https://github.com/pangaea-data-publisher/fuji/blob/master/fuji_server/yaml/metrics_v0.5.yaml) and added an additional test ***FsF-F2-01M-4*** for the metric ***FsF-F2-01M*** (Descriptive Core Metadata) that checks for the presence of GeoDCAT properties (here, the properties to be checked must be named exactly as in the [mapping file](https://github.com/pangaea-data-publisher/fuji/blob/master/fuji_server/helper/metadata_mapper.py)).
  - The metric ***FsF-F2-01M*** is implemented in [*fuji_server.evaluators.fair_evaluator_minimal_metadata.FAIREvaluatorCoreMetadata*](https://github.com/pangaea-data-publisher/fuji/blob/ba289b056632af125e56c43761636f1e70d391f4/fuji_server/evaluators/fair_evaluator_minimal_metadata.py#L12). Since I added the test in the yaml for this metric, the implementations for the new test are also here
    - In the __*init()*__ function, the corresponding metrics/tests must be listed here.
    - The test ***FsF-F2-01M-3*** is implemented in [*fuji_server.evaluators.fair_evaluator_minimal_metadata.FAIREvaluatorCoreMetadata.testCoreDescriptiveMetadataAvailable()*](https://github.com/pangaea-data-publisher/fuji/blob/ba289b056632af125e56c43761636f1e70d391f4/fuji_server/evaluators/fair_evaluator_minimal_metadata.py#L95). I modified this method so that ***FsF-F2-01M-4** (test for GeoDCAT properties)* is also applied.
  - For a more sustainable implementation, it would probably be recommended to create a separate evaluation class in *fuji_server/evaluator/* instead of modifying the existing class

#### Test Execution of the Evaluator:

```bash
curl -X POST http://localhost:1071/fuji/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "object_identifier": "https://klimakonform-dmp.geo.tu-dresden.de/dataset/kk-gebiet-tagliche-mdk-projektion-bias-corrected",
    "test_debug": true,
    "metadata_service_endpoint": "http://ws.pangaea.de/oai/provider",
    "metadata_service_type": "oai_pmh",
    "use_datacite": true,
    "use_github": false,
    "metric_version": "metrics_v0.6geo"
  }'
```
