# Preparing the phenotypic data

??? tip "Looking for more general guidelines on how to organize your dataset?"

    We recommend also checking out [Nipoppy](https://nipoppy.readthedocs.io/), a protocol for standardized organization and processing of clinical-neuroimaging datasets that extends [BIDS](https://bids-specification.readthedocs.io/en/stable/). 
    Neurobagel tools are designed to be compatible with data organized according to the Nipoppy specification, although you do not need to use Nipoppy in order to use Neurobagel.

To use the Neurobagel annotation tool,
you must prepare the tabular data for your dataset as a single tab-separated values (`.tsv`) file.

Within Neurobagel, tabular (or phenotypic) data  refers to any demographic, clinical/behavioural, cognitive, or other non-imaging-derived data of participants
which are typically stored in a tabular format.

## Requirements for the phenotypic TSV

!!! warning "If you're unfamiliar with TSV files or unsure how to format them correctly"
    Please first consult our [TSV glossary section](../glossary.md#tsv) for information on creating valid TSV files.

In a valid phenotypic TSV file for Neurobagel, rows identify each participant (or participant-session in a longitudinal dataset), and columns describe properties of participants (age, sex, diagnosis, etc.). 

Each row **MUST** describe only one participant/session, and each participant/session **MUST** be described by only one row.

The TSV **MUST** contain:

- A minimum of 2 columns
- At least 1 column containing subject identifiers (IDs). Subject IDs must be unique per row.
    - If both subject and session ID columns are present, then the combinations of IDs must be unique per row.

    !!! note "Only one subject ID column can be annotated"
        Neurobagel currently does not support linking multiple IDs to a single subject. 
        If your TSV file includes multiple subject ID columns (e.g., study ID, hospital ID),
        you will choose one column to serve as the primary subject ID during annotation.

- At least 1 column that describes demographic or other phenotypic information


The TSV **MAY** contain:

- At least 1 column containing session identifiers (e.g., if the dataset is longitudinal)
  
    !!! note "Only one session ID column can be annotated"
        Neurobagel currently does not support linking multiple IDs to a single session.
        If your TSV file includes multiple session ID columns (e.g., visit number, scan ID),
        you will choose one column to serve as the primary session ID during annotation.

The TSV **MUST NOT** contain:

- Missing values in the columns you intend to annotate as the primary subject ID or session ID (if available)

For all phenotypic variables currently modeled by Neurobagel, see [here](../data_models/dictionaries.md).

### If your dataset has imaging (BIDS) data

In addition to phenotypic characteristics of subjects, Neurobagel can also harmonize information about subjects' imaging data from a corresponding [BIDS](https://bids-specification.readthedocs.io/en/stable/) dataset (see also [Preparing imaging data](preparing_imaging_data.md)).

To include subjects' BIDS imaging data as part of their representation in Neurobagel,
your phenotypic TSV **MUST** meet the following requirements **in addition** to the ones listed above:

- At least 1 column in the phenotypic TSV contains subject IDs that 
  exactly match the subject IDs in your [BIDS metadata table](preparing_imaging_data.md) 
  (by default, these should be [BIDS subject IDs](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#filesystem-structure) in the form `sub-<label>`), 
  **AND** this must be the column you annotate as the primary subject ID

    !!! note "Subject IDs are case-sensitive"
        Subject IDs in the phenotypic TSV must match corresponding BIDS subject IDs exactly 
        for Neurobagel to correctly link phenotypic and BIDS information. 
        For example, a BIDS ID of `sub-MNI001` would _not_ be matched to subject IDs `sub-mni001` or `mni001` in a phenotypic TSV.

- All BIDS subject IDs must appear in the phenotypic TSV, 
  even if the subject only has imaging data (columns can be left empty for missing phenotypic values) 
    - Datasets that include subjects in the BIDS dataset but not in the phenotypic TSV are not supported. 
    However, subjects with phenotypic data only (no BIDS data) are allowed.

If your dataset is longitudinal, the session IDs in the phenotypic TSV **MAY** match the BIDS session IDs, but this is not required.

## Examples of valid phenotypic TSVs

Depending on your dataset, your tabular data may look like one of the following:

### A BIDS `participants.tsv` file

If you have a [BIDS compliant `participants.tsv`](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#participants-file) that contains 
all the demographic and clinical/behavioural information for participants, 
you can annotate this file with Neurobagel's annotation tool
to create a data dictionary for the file.

Example TSV:

participant_id | age | sex | tools
---- | ---- | ---- | ----
sub-01 | 22 | female | WASI-2
sub-02  | 28 | male | Stroop
... | ... | ... | ... |


### A longitudinal data file
If you have longitudinal tabular data (e.g. age collected at multiple sessions/visits), 
then the information for all sessions should be combined into a single TSV. 
Each row must describe a unique combination of subject and session.

Example TSV:

participant_id | session_id | age | tools
---- | ---- | ---- | ----
sub-01 | ses-01 | 22 | WASI-2
sub-01 | ses-02 | 23 |
sub-02 | ses-01 | 28 | Stroop
... | ... | ... | ...

!!! tip

    A `participants.tsv` file with multiple sessions is not BIDS compliant. 
    If you want to store multi-session phenotypic data in a BIDS dataset, 
    you could do so in the `phenotype/` subdirectory 
    (see also the BIDS specification section on [Longitudinal and multi-site studies](https://bids-specification.readthedocs.io/en/stable/06-longitudinal-and-multi-site-studies.html#longitudinal-and-multi-site-studies)).

### Multiple participant or session ID columns

In some cases, there may be a need for more than one set of IDs
for participants and/or sessions.

For example, if a participant was first enrolled in a behavioural study
with one type of ID,
and then later joined an imaging study under a different ID, 
both types of participant IDs may be recorded in the tabular file.

For Neurobagel, the only requirement is that **the combination of all ID values for a row is unique**.

!!! Warning "Only one subject ID and session ID column can be annotated for Neurobagel"

    If your TSV file contains multiple subject or session ID columns, you will select one to use as the primary ID during annotation.
    The remaining subject/session ID columns will be ignored by Neurobagel.

Example **invalid** TSV:

participant_id | alternative_participant_id | ...
---- | ---- | ----
sub-01 | SID-1234 | ...
sub-01 | SID-2222 | ...
sub-02 | SID-1234 | ...

The same rules apply when multiple session IDs are present.

Example **valid** TSV:

participant_id | alt_participant_id | session_id | alt_session_id | age | ...
---- | ---- | ---- | ---- | ---- | ----
sub-01 | SID-1234 | ses-01 | visit-1 | 22 | ...
sub-01 | SID-1234 | ses-02 | visit-2 | 23 | ...
sub-02 | SID-2222 | ses-01 | visit-1 | 28 | ...
... | ... | ... | ... | ... | ...
