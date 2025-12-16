To generate harmonized data using Neurobagel, you must prepare a dataset description file.
This is a [JSON](https://www.w3schools.com/whatis/whatis_json.asp) file, based on the [`dataset_description.json`](https://bids-specification.readthedocs.io/en/stable/modality-agnostic-files/dataset-description.html#dataset-description) from [BIDS](https://bids-specification.readthedocs.io/en/stable/), that includes information about both the dataset and how to access the data.

Dataset information from this file will be displayed to a user when they discover your dataset in the Neurobagel query tool.

## If your dataset is in BIDS

The Neurobagel dataset description shares a subset of keys in common with the BIDS `dataset_description.json`,
but supports additional optional keys related to dataset access information (see [Dataset description fields](#dataset-description-fields)).

Your existing valid BIDS `dataset_description.json` can be directly used for Neurobagel without modification. 
However, we strongly recommend adding the Neurobagel-supported keys (highlighted below) to improve dataset [FAIRness](https://www.go-fair.org/fair-principles/) and dataset discoverability in Neurobagel:

``` { .json hl_lines="6-10" title="Neurobagel dataset description template" }
{
    "Name": "My Dataset",
	"Authors": [],
	"ReferencesAndLinks": [],
	"Keywords": [],
	"RepositoryURL": "",
	"AccessInstructions": "",
	"AccessType": "",
	"AccessEmail": "",
	"AccessLink": ""
}
```

!!! tip
    BIDS allows additional keys in `dataset_description.json`; these will be safely ignored by the BIDS validator.

!!! warning "The Neurobagel dataset description template is NOT a valid BIDS dataset_description.json!"
    Do not overwrite an existing BIDS `dataset_description.json` with the template above—only add Neurobagel-supported keys as needed.

    While any valid BIDS `dataset_description.json` is valid as a Neurobagel dataset description file (which only requires the `Name` key), 
    the converse is not true because Neurobagel does not require the `BIDSVersion` key mandatory in a BIDS `dataset_description.json`.
    If you are creating a single `dataset_description.json` for both BIDS and Neurobagel, be sure to also consult the [BIDS schema](https://bids-specification.readthedocs.io/en/stable/modality-agnostic-files/dataset-description.html#dataset-description) for this file.

## If your dataset is not in BIDS

Below is an editable and copy-pasteable template for your dataset description JSON.
For more information on each field, see [Dataset description fields](#dataset-description-fields).

!!! tip "Tips"
    - Click the underlined fields to edit the placeholder values.
    - Fields wrapped in square brackets `[]` expect a list of comma-separated strings, e.g. `["Item 1", "Item 2"]`.
    - To leave any fields empty, delete the placeholder value.

```madlibs
json
~~~
{
	"Name": "___DATASET NAME___",
	"Authors": [___AUTHORS___],
	"ReferencesAndLinks": [___LINKS___],
	"Keywords": [___KEYWORDS___],
	"RepositoryURL": "___URL___",
	"AccessInstructions": "___INSTRUCTIONS___",
	"AccessType": "___TYPE___",
	"AccessEmail": "___EMAIL___",
	"AccessLink": "___URL___"
}
```

Save the contents in a file with the extension `.json`. 
We recommend using an informative file name like `DATASETNAME_description.json`.

## Dataset description fields

Neurobagel recognizes the following fields in the dataset description JSON file. Extra keys are ignored. * indicates a key adopted from the BIDS [`dataset_description.json`](https://bids-specification.readthedocs.io/en/stable/modality-agnostic-files/dataset-description.html).

Key name | Requirement level | Data type | Description
---- | ---- | ---- | ----
Name* | REQUIRED | string | Name of the dataset. This name will be displayed when users discover the dataset in a Neurobagel query.
Authors* | RECOMMENDED | list of strings | List of individuals who contributed to the creation/curation of the dataset.
ReferencesAndLinks* | RECOMMENDED | list of strings | List of links or references that contain information on the dataset.
Keywords* | RECOMMENDED | list of strings | List of keywords describing the content or subject matter of the dataset.
RepositoryURL | RECOMMENDED | string | URL to a repository where the dataset can be downloaded or retrieved from (e.g., DataLad, Zenodo, GitHub).
AccessInstructions | RECOMMENDED | string | Description of how to access the data.
AccessType | RECOMMENDED | string, one of: `"public"`, `"registered"`, `"restricted"` | Level of requirements for dataset access. `public`: Immediately accessible without registration, authentication, or approval. `registered`: Requires authentication or agreement to basic terms of use, but no formal application or review. `restricted`: Formal approval or review of application/request required before access is granted.
AccessEmail | RECOMMENDED | string (email) | Primary email for access requests.
AccessLink | RECOMMENDED | string | Primary link for access requests or information.

## Example
<!-- TODO: Update link once neurobagel_examples PR is merged! -->
```json
--8<-- "https://raw.githubusercontent.com/neurobagel/neurobagel_examples/refs/heads/add-example-dataset-description/data-upload/synthetic_dataset_description.json"
```