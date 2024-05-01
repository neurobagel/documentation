# Updating a harmonized dataset

## Following a change in my _dataset_

When using Neurobagel tools on a dataset that is still undergoing data collection, you may need to update the Neurobagel annotations and/or graph-ready data for the dataset when you want to add new subjects or measurements or to correct mistakes in prior data versions.

For any of the below types of changes, you will need to regenerate a graph-ready `.jsonld` file for the dataset which reflects the change.

### If the phenotypic (tabular) data have changed
If new variables have been added to the dataset such that there are new columns in the phenotypic TSV you previously annotated using Neurobagel's annotation tool, you will need to:  

1. **Generate an updated data dictionary** by annotating the new variables in your TSV following the [annotation workflow](annotation_tool.md)

2. **Generate a new graph-ready data file** for the dataset by [re-running the CLI](cli.md) on your updated TSV and data dictionary

### If only the imaging data have changed
If the BIDS data for a dataset have changed without changes in the corresponding phenotypic TSV (e.g., if new modalities or scans have been acquired for a subject), you have two options:

- If you still have access to the dataset's phenotypic JSONLD generated from the `pheno` command of the `bagel-cli` (step 1), you may choose to [rerun only the `bids` CLI command](cli.md) on the updated BIDS directory. 
This will generate a new graph-ready data file with updated imaging metadata of subjects.

OR

- [Rerun the CLI entirely (`pheno` and `bids` steps)](cli.md) to generate a new graph-ready data file for the dataset.

_When in doubt, rerun both CLI commands._

### If only the subjects have changed
If subjects have been added to or removed from the dataset but the phenotypic TSV is otherwise unchanged (i.e., only new or removed rows, without changes to the available variables), you will need to:

- **Generate a new graph-ready data file** for the dataset by [re-running the CLI](cli.md) (`pheno` and `bids` steps) on your updated TSV and existing data dictionary

## Following a change in the _Neurobagel data model_

As Neurobagel continues developing the data model, new tool releases may introduce breaking changes to the data model for subject-level information in a `.jsonld` graph data file. 
Breaking changes will be highlighted in the release notes.

_If you have already created `.jsonld` files for a Neurobagel graph database_ but want to update your graph data to the latest Neurobagel data model following such a change, you can easily do so by [rerunning the CLI](cli.md) on the existing data dictionaries and phenotypic TSVs for the dataset(s) in the graph.
This will ensure that if you use the latest version of the Neurobagel CLI to process new datasets (i.e., generate new `.jsonld` files) for your database, the resulting data will not have conflicts with existing data in the graph.

Note that if upgrading to a newer version of the data model, **you should regenerate the `.jsonld` files for _all_ datasets in your existing graph**.

## Updating the graph database
To allow easy (re-)uploading of the updated `.jsonld` for your dataset(s) to a graph database, make a copy of it in a [central directory on your research data fileserver for storing local Neurobagel `jsonld` datasets](config.md). 
Then, follow the steps for [uploading/updating a dataset in the graph database](infrastructure.md#uploading-data-to-the-graph) (needs to be completed by user with database write access).
