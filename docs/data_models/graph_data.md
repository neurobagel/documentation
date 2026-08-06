# Neurobagel graph data files

## Overview

Using the Neurobagel CLI (see also the [section on the CLI](../user_guide/cli.md)),
a Neurobagel data dictionary (`.json`) for a dataset can be processed together
with the corresponding tabular data (`.tsv`) and BIDS dataset (if available)
to generate subject-level [linked data](https://www.w3.org/wiki/LinkedData)
that can be encoded in a knowledge graph.
The Neurobagel graph-ready data are stored in [JSON-LD](https://json-ld.org/) format (`.jsonld`),
and include a representation of each subject's harmonized phenotypic properties and imaging metadata.

Another way to think about the difference between a Neurobagel data dictionary and a graph-ready `.jsonld` data file is this:
_more than one dataset can theoretically have the same data dictionary_ (if the tabular data include the same columns and unique column values),
but _the `.jsonld` file for each dataset is unique_ as long as the actual data of subjects differs across datasets.

## Example `.jsonld` files

Depending on whether a dataset annotated using Neurobagel includes BIDS imaging data,
the `.jsonld` data for the dataset may or may not include imaging metadata of subjects (extracted automatically with the CLI).

- [Example `.jsonld` containing only phenotypic data](https://github.com/neurobagel/neurobagel_examples/blob/main/data-upload/example_synthetic.jsonld)
- [Example `.jsonld` containing phenotypic and raw imaging (BIDS) data](https://github.com/neurobagel/neurobagel_examples/blob/main/data-upload/pheno-bids-output/example_synthetic_pheno-bids.jsonld)
- [Example `.jsonld` containing phenotypic and imaging derivative data](https://github.com/neurobagel/neurobagel_examples/blob/main/data-upload/pheno-derivatives-output/example_synthetic_pheno-derivatives.jsonld)
- [Example `.jsonld` containing phenotypic, raw imaging (BIDS), and imaging derivative data](https://github.com/neurobagel/neurobagel_examples/blob/main/data-upload/pheno-bids-derivatives-output/example_synthetic_pheno-bids-derivatives.jsonld)

??? info "More info on example dataset"
    The above `.jsonld` files represent an example dataset used for testing which includes the following:

    | Data | Link |
    | ----- | ----- |
    | Phenotypic TSV | [:octicons-link-external-16:](https://github.com/neurobagel/neurobagel_examples/blob/main/data-upload/example_synthetic.tsv)  |
    | Neurobagel data dictionary | [:octicons-link-external-16:](https://github.com/neurobagel/neurobagel_examples/blob/main/data-upload/example_synthetic.json) |
    | BIDS dataset | [:octicons-link-external-16:](https://github.com/bids-standard/bids-examples/tree/master/synthetic) |
