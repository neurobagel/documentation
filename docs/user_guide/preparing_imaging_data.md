# Preparing the imaging metadata as a table

To be able to query information about available neuroimaging data in your dataset, you must provide Neurobagel with a `.tsv` file containing your dataset's neuroimaging metadata.
We refer to this as a BIDS metadata table.

If your dataset is already in [BIDS](https://bids-specification.readthedocs.io/en/stable/), the Neurobagel CLI provides a [`bids2tsv`](cli.md#generate-a-bids-metadata-table) command that will automatically generate this table for you.

The BIDS metadata table lists each subject's available imaging files and modality information, using [BIDS](https://bids-specification.readthedocs.io/en/stable/) naming conventions, in the format shown below.

## Example BIDS metadata table
| sub | ses | suffix | path |
| ---- | ---- | ---- | ---- |
| sub-01 | ses-01 | T1w | /data/bids-examples/synthetic/sub-01/ses-01/anat/sub-01_ses-01_T1w.nii |
| sub-01 | ses-01 | bold | /data/bids-examples/synthetic/sub-01/ses-01/func/sub-01_ses-01_task-rest_bold.nii |
| sub-02 | ses-01 | T1w | /data/bids-examples/synthetic/sub-02/ses-01/anat/sub-02_ses-01_T1w.nii |
| sub-02 | ses-01 | bold | /data/bids-examples/synthetic/sub-02/ses-01/func/sub-02_ses-01_task-rest_bold.nii |
| ... | ... | ... | ... |


## About the BIDS metadata table
The table must include at least four columns named exactly `sub`, `ses`, `suffix`, and `path` (adapted from [BIDS](https://bids-specification.readthedocs.io/en/stable/) entities).
Additional columns are allowed but will be ignored by Neurobagel.

Each row of the table indexes a single image file with the following metadata:

- `sub` (required)
    - Subject ID
    - Example: `sub-PD123`
- `ses` (optional)
    - Session ID, if applicable
    - Example: `ses-01`
- `suffix` (required)
    - BIDS suffix corresponding to the modality (or sequence) of the image file
    - See also [Supported BIDS imaging modalities](#supported-bids-imaging-modalities)
    - Example: `T1w`
- `path` (required)
    - Path to the image file
    - Example: `/data/pd/qpn/sub-PD123/ses-01/anat/sub-PD123_ses-01_T1w.nii.gz`


## Supported BIDS imaging modalities

Neurobagel currently supports a subset of MRI modalities included in the [BIDS specification](https://bids-specification.readthedocs.io/en/stable/),
but we plan to expand this list for closer alignment with BIDS in the future.

Supported modalities are listed below using their BIDS suffixes:

- `dwi`
- `T1w`
- `T2w`
- `bold`
- `asl`
- `eeg`
- `meg`
- `pet`

!!! info
    For more information, see also the "Modality specific files" section of the [BIDS specification](https://bids-specification.readthedocs.io/en/stable/)
    or consult this [master list](https://github.com/bids-standard/bids-specification/blob/master/src/schema/objects/suffixes.yaml) of image suffixes supported by BIDS.
