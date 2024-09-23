# Preparing the phenotypic data

!!! tip "Looking for more general guidelines on how to organize your dataset?"

    We recommend also checking out [Nipoppy](https://nipoppy.readthedocs.io/), a protocol for standardized organization and processing of clinical-neuroimaging datasets that extends [BIDS](https://bids-specification.readthedocs.io/en/stable/). 
    Neurobagel tools are designed to be compatible with data organized according to the Nipoppy specification, although you do not need to use Nipoppy in order to use Neurobagel.

To use the Neurobagel annotation tool, 
please prepare the tabular data for your dataset as a single, tab-separated file (`.tsv`).

!!! note
    In the Neurobagel context, _tabular_ or _phenotypic_ data for a dataset refers to any demographic,
    clinical/behavioural, cognitive, or other non-imaging-derived data of participants 
    which are typically stored in a tabular file format.

## General requirements for the phenotypic TSV

### All datasets

A valid dataset for Neurobagel **MUST** include a TSV file that describes participant attributes.

The TSV: 

- MUST contain a minimum of two columns
- MUST contain at least one column with subject IDs

    ??? note "Only one subject ID column can be annotated"
        Neurobagel currently does not support annotating multiple subject ID columns 
        so you must choose one as the primary ID during annotation

- MUST contain at least one additional column that describes demographic or other phenotypic information
- MAY contain a column with session IDs if the dataset is longitudinal.

    ??? note "Only one session ID column can be annotated"
        Neurobagel currently does not support annotating multiple session ID columns 
        so you must choose one as the primary ID during annotation
  
- MUST NOT contain any missing values in the subject ID and session ID (if available) column
- MUST have unique values in the subject ID column OR in the combination of subject ID and session ID columns

for variables currently modeled by Neurobagel, see the [data dictionary section](dictionaries.md).

### Datasets with imaging (BIDS) data

If a dataset has imaging data in [BIDS](https://bids-specification.readthedocs.io/en/stable/) format, 
Neurobagel **additionally** requires that:

- At least one column in the phenotypic TSV contains subject IDs that 
  match the names of [BIDS subject subdirectories](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#filesystem-structure). 
  If this condition is not met, you will encounter an error 
  when [running the Neurobagel CLI](cli.md) on your dataset to generate Neurobagel graph-ready files, 
  indicating that your BIDS directory contains subjects not found in your phenotypic file.

    !!! note
        Subject IDs are case-sensitive and must match BIDS subject IDs exactly 
        for Neurobagel to be able to link phenotypic and BIDS information. 
        e.g., a BIDS ID of `sub-MNI001` is not the same as subject IDs `sub-mni001` or `mni001` 
        in a phenotypic TSV and would not be linked by Neurobagel.

- All BIDS subjects are included in the phenotypic TSV, 
  even if they only have BIDS imaging information. 
  Neurobagel does not allow for datasets where subjects have BIDS 
  data but are not represented in the phenotypic TSV 
  (however, subjects who have phenotypic data but no BIDS data are allowed).
- If the dataset is longitudinal, the session IDs in the phenotypic TSV 
  MAY match the session IDs in the BIDS dataset, but don't have to. 
  If matching session IDs are present in the phenotypic TSV and the BIDS dataset, neurobagel will interpret
  this to mean that the phenotypic data is associated with the corresponding BIDS session.
  If phenotypic and BIDS session IDs do not match, Neurobagel will treat them as distinct sessions.

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
    Neurobagel does not support multiple subject or session IDs in the same TSV file. 
    If you have multiple subject or session IDs, you must choose one to use as the primary ID 
    and include the others as additional columns.
    

    We are planning to support multiple IDs in the future. 

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


