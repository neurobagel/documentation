# Updating a harmonized dataset

When using Neurobagel tools on a dataset that is still undergoing data collection, you may need to update the Neurobagel annotations and/or graph-ready data for the dataset when you want to add new subjects or measurements or to correct mistakes in prior data versions.

For any of the below types of changes, you will need to regenerate a graph-ready `.jsonld` file for the dataset which reflects the change.

## If the phenotypic (tabular) data have changed
If new variables have been added to the dataset such that there are new columns in the phenotypic TSV you previously annotated using Neurobagel's annotation tool, you will need to:  

1. **Generate an updated data dictionary** by annotating the new variables in your TSV following the [annotation workflow](annotation_tool.md)

2. **Generate a new graph-ready data file** for the dataset by [re-running the CLI](cli.md) on your updated TSV and data dictionary

## If only the imaging data have changed
If the BIDS data for a dataset have changed without changes in the corresponding phenotypic TSV (e.g., if new modalities or scans have been acquired for a subject), you have two options:

a. If you still have access to the dataset's phenotypic JSONLD generated from the `pheno` command of the `bagel-cli` (step 1), you may choose to [rerun only the `bids` CLI command](cli.md) on the updated BIDS directory. 
This will generate a new graph-ready data file with updated imaging metadata of subjects.

b. [Rerun the CLI entirely (`pheno` and `bids` steps)](cli.md) to generate a new graph-ready data file for the dataset.

_When in doubt, go with option b._

## If only the subjects have changed
If subjects have been added to or removed from the dataset, but the phenotypic TSV otherwise has been unchanged (e.g., only new or removed rows), you will need to:

1. **Generate a new graph-ready data file** for the dataset by [re-running the CLI](cli.md) (`pheno` and `bids` steps) on your updated TSV and existing data dictionary

## Updating the graph database
To allow easy (re-)uploading of the updated `.jsonld` for your dataset to a graph database, make a copy of it in a [central directory on your research data fileserver for storing local Neurobagel `jsonld` datasets](infrastructure.md#where-to-store-neurobagel-graph-ready-data). 
Then, follow the steps for [uploading/updating a dataset in the graph database](infrastructure.md#uploading-data-to-the-graph) (needs to be completed by user with database write access).
