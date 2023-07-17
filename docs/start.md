# Ecosystem

The Neurobagel ecosystem comprises four primary tools:

- The **annotation tool** [:simple-github:](https://github.com/neurobagel/annotation_tool) ([annotate.neurobagel.org](https://annotate.neurobagel.org))
    - to create harmonized annotations of phenotypic variables
    - intended for use by researchers and domain experts
    - static site, deployed on GitHub Pages
- The **command-line interface** [:simple-github:](https://github.com/neurobagel/bagel-cli)
    - to extract subject-specific metadata from annotated phenotypic and BIDS data
    - intended for data managers to create graph-ready harmonized data
- The **knowledge graph store** and **API** [:simple-github:](https://github.com/neurobagel/api) ([api.neurobagel.org](https://api.neurobagel.org))
    - to store and query extracted metadata using [RDF](https://www.w3.org/RDF/) and the [SPARQL query language](https://www.w3.org/TR/rdf-sparql-query/)
    - intended for research/data platform owners and for isolated deployments
- The **query tool** [:simple-github:](https://github.com/neurobagel/query-tool) ([query.neurobagel.org](https://query.neurobagel.org))
    - to search across datasets and obtain metadata for subjects based on harmonized subject-level attributes
    - intended to help researchers and scientific data users find cohorts
    - static site, deployed on GitHub Pages


??? Todo

    Add Neurobagel figure for overview.

## Getting started

If you have a dataset you wish to annotate using Neurobagel, see [Annotating a dataset](annotation_tool.md).

If you are a sysadmin or researcher seeking to deploy the Neurobagel software stack locally, see [Setting up a graph](infrastructure.md).

If you want to search for participants in the Neurobagel graph, see [Running cohort queries](query_tool.md).