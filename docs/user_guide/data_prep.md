# Preparing the phenotypic data

??? tip "Looking for more general guidelines on how to organize your dataset?"

    We recommend also checking out [Nipoppy](https://nipoppy.readthedocs.io/), a protocol for standardized organization and processing of clinical-neuroimaging datasets that extends [BIDS](https://bids-specification.readthedocs.io/en/stable/). 
    Neurobagel tools are designed to be compatible with data organized according to the Nipoppy specification, although you do not need to use Nipoppy in order to use Neurobagel.

To use the Neurobagel annotation tool,
you must prepare the tabular data for your dataset as a single, tab-separated values file (`.tsv`).

Within Neurobagel, tabular (or phenotypic) data  refers to any demographic, clinical/behavioural, cognitive, or other non-imaging-derived data of participants
which are typically stored in a tabular format.

## Requirements for the phenotypic TSV

!!! warning "If you're unfamiliar with TSV files or unsure how to format them correctly"
    Please first consult our [TSV](../glossary.md#tsv) glossary section for information on creating valid TSV files.

In a valid phenotypic TSV file for Neurobagel, rows identify each participant (or participant-session in a longitudinal dataset), and columns describe properties of participants (age, sex, diagnosis, etc.). 

Each row **MUST** describe only one participant/session, and each participant/session **MUST** be described by only one row.

The TSV **MUST** contain:

- A minimum of 2 columns
- At least 1 column containing subject identifiers. If no session information is present, then subject IDs must be unique per row. If both subject and session ID columns are present, then the combinations of IDs must be unique per row.

    !!! note "Only one subject ID column can be annotated"
        Neurobagel currently does not support linking multiple IDs to a single subject. 
        If your TSV file includes more than one subject ID column (e.g., study ID, hospital ID),
        note that you will need to choose one column to serve as the primary subject ID during annotation.

- At least 1 column that describes demographic or other phenotypic information about participants


The TSV **MAY** contain:

- At least 1 column containing session identifiers (e.g., if the dataset is longitudinal)
  
    !!! note "Only one session ID column can be annotated"
        Neurobagel currently does not support linking multiple IDs to a single session.
        If your TSV file includes more than one session ID column (e.g., visit number, scan ID),
        note that you will need to choose one column to serve as the primary session ID during annotation.

The TSV **MUST NOT** contain:

- Missing values in the columns you intend to annotate as the primary subject ID or session ID (if available)

For all phenotypic variables currently modeled by Neurobagel, see the [data dictionary section](../data_models/dictionaries.md).

### If your dataset has imaging (BIDS) data

In addition to phenotypic characteristics of subjects described in a TSV, Neurobagel can optionally also harmonize information about subjects' imaging data from a corresponding [BIDS](https://bids-specification.readthedocs.io/en/stable/) dataset.

If you wish to include subjects' BIDS imaging data as part of their representation in Neurobagel,
your phenotypic TSV **MUST** meet the following requirements **in addition** to the ones listed above:

- At least 1 column in the TSV contains subject IDs that 
  match the names of the [BIDS subject subdirectories](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#filesystem-structure), 
  **AND** this must be the column you annotate as the primary subject ID

    !!! note "Subject IDs are case-sensitive"
        Subject IDs in the phenotypic TSV must match corresponding BIDS subject IDs exactly 
        for Neurobagel to correctly link phenotypic and BIDS information. 
        For example, a BIDS ID of `sub-MNI001` would _not_ be matched to subject IDs `sub-mni001` or `mni001` in a phenotypic TSV.

- All BIDS subject IDs are found in the phenotypic TSV, 
  even for subjects with imaging data only. 
  Columns may be left empty for missing phenotypic values. 
    - Datasets in which subjects are present in the BIDS dataset but not in the phenotypic TSV are not supported. 
    However, subjects with phenotypic data only (no BIDS data) are allowed.
    <!--- TODO: Consider removing below bullet point as it seems unnecessary. -->
    - If this condition is not met, you will encounter an error when [running the Neurobagel CLI](cli.md) on your dataset to generate Neurobagel graph-ready files, 
    indicating that your BIDS directory contains subjects not found in your phenotypic file.

If your dataset is longitudinal, the session IDs in the phenotypic TSV **MAY** match the BIDS session IDs, but this is not required.

## Examples of valid phenotypic TSVs

Depending on your dataset, your tabular data may look like one of the following:

### A BIDS `participants.tsv` file

If you have a [BIDS compliant `participants.tsv`](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#participants-file) that contains 
all the demographic and clinical/behavioural information for participants, 
you can annotate this file with Neurobagel's annotation tool
to create a data dictionary for the file.

Example TSV:

| participant_id | age | sex    | tools  |
| -------------- | --- | ------ | ------ |
| sub-01         | 22  | female | WASI-2 |
| sub-02         | 28  | male   | Stroop |
| ...            |     |        |        |


### A longitudinal data file
If you have longitudinal tabular data (e.g. age collected at multiple sessions/visits), 
then the information for all sessions should be combined into a single TSV. 
Each row must describe a unique combination of subject and session.

Example TSV:

| participant_id | session_id | age | tools  |
| -------------- | ---------- | --- | ------ |
| sub-01         | ses-01     | 22  | WASI-2 |
| sub-01         | ses-02     | 23  |        | 
| sub-02         | ses-01     | 28  | Stroop |
| ...            |            |     |        |

!!! tip

    A `participants.tsv` file with multiple sessions is not BIDS compliant. 
    If you want to store multi-session phenotypic data in a BIDS dataset, 
    you could do so in the `phenotype/` subdirectory 
    (see also the BIDS specification section on [Longitudinal and multi-site studies](https://bids-specification.readthedocs.io/en/stable/06-longitudinal-and-multi-site-studies.html#longitudinal-and-multi-site-studies)).

### Multiple participant or session identifier columns

In some cases, there may be a need for more than one set of IDs
for participants and/or sessions.

For example, if a participant was first enrolled in a behavioural study
with one type of ID,
and then later joined an imaging study under a different ID.
In this case, both types of participant IDs should be recorded in the tabular file.

The only requirement is that **the combination of all ID values for a row is unique**.

!!! Warning "Neurobagel currently supports only one subject ID and one session ID"

    Neurobagel currently does not support annotating multiple subject or session ID columns in the same TSV file. 
    If you have multiple subject or session IDs, you must choose one to use as the primary ID.
    Additional subject/session ID columns can still be included in the TSV but will be ignored by Neurobagel.

Example **invalid** TSV:

| participant_id | alternative_participant_id | ... |
| -------------- | -------------------------- | --- |
| sub-01         | SID-1234                   |     |
| sub-01         | SID-2222                   |     |
| sub-02         | SID-1234                   |     |

The same rules apply when multiple session IDs are present.

Example **valid** TSV:

| participant_id | alt_participant_id | session_id | alt_session_id | age | ... |
| -------------- | ------------------ | ---------- | -------------- | --- | --- |
| sub-01         | SID-1234           | ses-01     | visit-1        | 22  |     |
| sub-01         | SID-1234           | ses-02     | visit-2        | 23  |     |
| sub-02         | SID-2222           | ses-01     | visit-1        | 28  |     |
| ...            |                    |            |                |     |     |
