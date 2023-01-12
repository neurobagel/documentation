# Welcome to Neurobagel

## Preparing the data

To use the Neurobagel Annotation tool, 
please prepare your tabular data as a single file.

Here are some examples:

### A BIDS participants.tsv file

If you have a BIDS compliant participants.tsv file that contains 
all of your demographic information, 
then you can annotate this file with the Neurobagel Annotator
to create a new data dictionary. 

For example:

| participant_id | age | sex    | tools  |
| -------------- | --- | ------ | ------ |
| sub-01         | 22  | female | WASI-2 |
| sub-02         | 28  | male   | Stroop |
| ...            |     |        |        |


### A multi-session file
If you have multi-session tabular data (e.g. different ages for different sessions),
then you should combine all information into a single tabular file.

!!! note

    A participants.tsv file with multiple sessions is not BIDS compliant.
    If you want to store a multi-session file in a BIDS dataset,
    you could do so in the `/pheno` subdirector.


For example:


| participant_id | session_id | age | tools  |
| -------------- | ---------- | --- | ------ |
| sub-01         | ses-01     | 22  | WASI-2 |
| sub-01         | ses-02     | 23  |        | 
| sub-02         | ses-01     | 28  | Stroop |
| ...            |            |     |        |

### Multiple participant or session IDs
In some cases there may be a need for more than one set of IDs 
for participants and/or sessions.
For example if a participant was first enrolled in a behavioural study
with one type of IDs 
and later joined an imaging study with different IDs.
In such a case, you should include both participant IDs in the tabular file.
The only requirement is that the combination of IDs has to be unique.

For example, this would **not be allowed**:

| participant_id | alternative_participant_id | ... |
| -------------- | -------------------------- | --- |
| sub-01         | SID-1234                   |     |
| sub-01         | SID-2222                   |     |
| sub-02         | SID-1234                   |     |

The same rules apply to session IDs. 

For example:

| participant_id | alt_participant_id | session_id | alt_session_id | age | ... |
| -------------- | ------------------ | ---------- | -------------- | --- | --- |
| sub-01         | SID-1234           | ses-01     | visit-1        | 22  |     |
| sub-01         | SID-1234           | ses-02     | visit-2        | 23  |     |
| sub-02         | SID-2222           | ses-01     | visit-1        | 28  |     |
| ...            |                    |            |                |     |     |
