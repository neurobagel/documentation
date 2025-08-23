# Preparing the imaging metadata as a table

To make your dataset's neuroimaging metadata queryable using Neurobagel, you must provide a `.tsv` file that lists each subject's available NIfTI imaging files and modality information following [BIDS](https://bids-specification.readthedocs.io/en/stable/) naming conventions. 
We refer to this as a BIDS metadata table.

The expected format of the table is illustrated in the example below:

sub | ses | suffix | path
---- | ---- | ---- | ----
sub-01 | ses-01 | T1w | /data/bids-examples/synthetic/sub-01/ses-01/anat/sub-01_ses-01_T1w.nii
sub-01 | ses-01 | bold | /data/bids-examples/synthetic/sub-01/ses-01/func/sub-01_ses-01_task-rest_bold.nii
sub-02 | ses-01 | T1w | /data/bids-examples/synthetic/sub-02/ses-01/anat/sub-02_ses-01_T1w.nii
sub-02 | ses-01 | bold | /data/bids-examples/synthetic/sub-02/ses-01/func/sub-02_ses-01_task-rest_bold.nii
... | ... | ... | ... | ...

### Automatically generating a BIDS metadata table

If your dataset is already in [BIDS](https://bids-specification.readthedocs.io/en/stable/), run the Neurobagel CLI's [`bids2tsv`](cli.md#0-generate-a-bids-metadata-table) command to automatically generate a metadata table in the format above from your BIDS dataset directory.

### About the BIDS metadata table
The table must include at least four columns named exactly `sub`, `ses`, `suffix`, and `path` (adapted from [BIDS](https://bids-specification.readthedocs.io/en/stable/) entities). 
Additional columns are allowed but will be ignored by Neurobagel.

Each row of the table indexes a single NIfTI (`.nii` or `.nii.gz`) file with the following metadata:

- `sub` (required)
    - Subject ID in the format `sub-<label>`
    - Example: `sub-PD123`
- `ses` (optional)
    - Session ID in the format `ses-<label>`, if applicable
    - Example: `ses-01`
- `suffix` (required)
    - BIDS suffix corresponding to the image modality (or sequence) of the NIfTI file 
    - For more information, see the "Modality specific files" section of the [BIDS specification](https://bids-specification.readthedocs.io/en/stable/) or consult this [master list](https://github.com/bids-standard/bids-specification/blob/master/src/schema/objects/suffixes.yaml) of recognized BIDS image suffixes
    - Example: `T1w`
- `path` (required)
    - Absolute path to the NIfTI file, ending with the extension `.nii` or `.nii.gz`
    - Example: `/data/pd/qpn/sub-PD123/ses-01/anat/sub-PD123_ses-01_T1w.nii.gz`
