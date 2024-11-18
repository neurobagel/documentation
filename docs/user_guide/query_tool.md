# The Neurobagel Query Tool

Neurobagel's query tool is a web interface for searching across a Neurobagel graph based on various subject clinical-demographic and imaging parameters.

The query tool is a React application, developed in [TypeScript](https://www.typescriptlang.org/) using a variety of tools including [Vite](https://vitejs.dev/), [Cypress](https://www.cypress.io/), and [MUI](https://mui.com/).

## Quickstart
{%
   include-markdown "https://raw.githubusercontent.com/neurobagel/query-tool/main/README.md"
   start="## Quickstart"
   end="You can refer to [the neurobagel documentation](https://neurobagel.org/query_tool/#downloading-query-results) to see what the outputs of the query tool look like"
   rewrite-relative-urls=false
%}

### Downloading query results

For a given query, the query tool offers two kinds of TSV files for results that users can download. 
At least one dataset matching the query must be selected in the interface in order to download the query results.

#### Dataset-level results

The dataset-level results TSV describes the datasets that contain subjects matching the user's query.
This TSV contains the following columns:

- `DatasetID`: unique identifier (UUID) for dataset in the graph. 
Note that this ID is not guaranteed to be persistent across versions of a graph/across graphs, but will always be identical across a pair of query tool result files. 
_This column can be used as the key to join the dataset-level and participant-level results TSVs for a given query result, if needed._
- `DatasetName`: human readable name of the dataset
- `PortalURI`: URL to a website or page about the dataset, if available
- `NumMatchingSubjects`: (aggregate variable) number of subjects matching the query within the dataset
- `AvailableImageModalites`: (aggregate variable) list of unique imaging modalities available for the dataset

Example:

{{ read_table('./repos/neurobagel_examples/query-tool-results/dataset-level-results.tsv') }}

#### Participant-level results

The participant-level results TSV contains the available harmonized participant attributes for subject sessions matching the query in each (selected) matching dataset.
Each row in the TSV corresponds to a single matching subject _session_.

This TSV contains the following columns:

- `DatasetID`: unique identifier (UUID) for dataset in the graph. 
Note that this ID is not guaranteed to be persistent across versions of a graph/across graphs, but will always be identical across a pair of query tool result files. 
_This column can be used as the key to join the dataset-level and participant-level results TSVs for a given query result, if needed._
- `SubjectID`: subject label
- `SessionID`: the label of the session
- `SessionType`: either `ImagingSession` or `PhenotypicSession`
- `Age`: subject age, if available
- `Sex`: subject sex, if available
- `Diagnosis`: list of diagnoses of subject, if available
- `Assessment` : list of assessments completed by subject, if available
- `SessionFilePath`: the path of the session directory (for imaging sessions) either relative to the dataset root (for datasets available through DataLad) or relative to the root of the filesystem where the dataset is stored
- `NumPhenotypicSessions`: (aggregate variable) total number of **phenotypic** sessions that match the query for a subject
- `NumImagingSessions`: (aggregate variable) total number of **imaging** sessions that match the query for a subject
This number will be the same across rows corresponding to the same subject.
- `Modality`: imaging modalities acquired in the session, if available

Example:

{{ read_table('./repos/neurobagel_examples/query-tool-results/participant-level-results.tsv') }}

#### `protected` participant-level results in aggregate mode

If the values for all columns except for `DatasetID` and `SessionPath` in the participant-level results tsv are set to `protected`, this indicates the graph being queried has been configured (via its corresponding Neurobagel node API) to return only aggregate information about matches (due to data privacy reasons). 
This configuration can be modified by setting the `NB_RETURN_AGG` environment variable to `false` (the value is by default `true`). 
See related section of the documentation [here](config.md#environment-variables).

Example:

{{ read_table('./repos/neurobagel_examples/query-tool-results/participant-level-results-agg.tsv') }}

## Testing
{%
   include-markdown "https://raw.githubusercontent.com/neurobagel/query-tool/main/README.md"
   start="## Testing"
%}
