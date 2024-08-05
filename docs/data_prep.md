# Preparing the phenotypic data

To use the Neurobagel annotation tool, 
please prepare the tabular data for your dataset as a single, tab-separated file (`.tsv`).

!!! note
    In the Neurobagel context, _tabular_ or _phenotypic_ data for a dataset refers to any demographic,
    clinical/behavioural, cognitive, or other non-imaging-derived data of participants 
    which are typically stored in a tabular file format.

## General requirements for the phenotypic TSV

### All datasets

A valid dataset for Neurobagel **must** include a TSV file that describes participant attributes. 
The TSV must contain a minimum of two columns: at least one column must contain subject IDs, 
and at least one column must describe demographic or other phenotypic information 
(for variables currently modeled by Neurobagel, see the [data dictionary section](dictionaries.md)).

### Datasets with imaging (BIDS) data

If a dataset has imaging data in [BIDS](https://bids-specification.readthedocs.io/en/stable/) format, 
Neurobagel **additionally** requires that:

- At least one column in the phenotypic TSV contains subject IDs that match the names of [BIDS subject subdirectories](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#filesystem-structure). 
Note that subject IDs are case-sensitive.
- The subjects in the phenotypic TSV must be the same or a superset of subjects found in the BIDS directory. Neurobagel does not currently allow for datasets where subjects have BIDS data but are not represented in the phenotypic TSV.

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
