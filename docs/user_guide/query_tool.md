# The Neurobagel Query Tool

Neurobagel's query tool is a web interface for searching across a Neurobagel graph based on various subject clinical-demographic and imaging parameters.

The query tool is a React application, developed in [TypeScript](https://www.typescriptlang.org/) using a variety of tools including [Vite](https://vitejs.dev/), [Cypress](https://www.cypress.io/), and [MUI](https://mui.com/).

## Quickstart
{%
   include-markdown "https://raw.githubusercontent.com/neurobagel/query-tool/main/README.md"
   start="## Quickstart"
   end="The query tool offers two different TSV files for results"
   rewrite-relative-urls=false
%}

### Downloading query results

For a given query, there are two formats of query results that users can download as a TSV file.
At least one dataset matching the query must be selected in the results panel in order to download the query results.

#### Harmonized TSV data with descriptive labels

The default TSV available for download describes the available harmonized attributes and metadata for subjects matching the query, from the (selected) matching datasets. 
Harmonized data are provided as standardized vocabulary-derived labels for readability.

Each row corresponds to a single matching subject session, except for [datasets configured to only return aggregate results](#protected-subject-level-results-for-aggregate-datasets).

??? abstract "Example query result TSV"
    {{ read_table('./repos/neurobagel_examples/query-tool-results/neurobagel-query-results.tsv') }}

Columns in the TSV are described below:
* = required values

| Column name | Description |
| ---- | ---- |
| DatasetName * | name of the dataset |
| PortalURI | URL to a website or page about the dataset |
| NumMatchingSubjects * | _(dataset-level)_ total number of subjects matching the query in the dataset |
| SubjectID * | subject label |
| SessionID * | session label |
| ImagingSessionPath | _(imaging sessions only)_ path to the session directory, or subject directory if only one session exists. Either an absolute path from the filesystem root where the dataset is stored, or a relative path from the dataset root for DataLad datasets. |
| SessionType * | type of data acquired in the session, either `ImagingSession` or `PhenotypicSession`. Represents the nature of data being described, without denoting specific time or visits. e.g., A session in which both imaging and non-imaging data were acquired would be represented by separate rows, one per type. |
| Age | subject age |
| Sex | subject sex |
| Diagnosis | list of diagnoses for subject |
| Assessment | list of assessments completed by subject |
| NumMatchingPhenotypicSessions * | _(subject-level)_ total number of phenotypic sessions for the subject which match the query |
| NumMatchingImagingSessions * | _(subject-level)_ total number of imaging sessions for the subject which match the query |
| SessionImagingModalities | _(imaging sessions only)_ imaging modalities acquired in the session |
| SessionCompletedPipelines | _(imaging sessions only)_ processing pipelines completed for the session |
| DatasetImagingModalities | _(dataset-level)_ imaging modalities acquired in at least one session in the dataset |
| DatasetPipelines | _(dataset-level)_ processing pipelines completed for at least one session in the dataset |

#### Harmonized TSV data with URIs

A machine-optimized version of the query results, containing [URIs](https://www.ontotext.com/knowledgehub/fundamentals/linked-data-linked-open-data/) instead of descriptive labels for harmonized attributes and metadata of matching subjects, is also available for download as a TSV.

Each row corresponds to a single matching subject session, except for [datasets configured to only return aggregate results](#protected-subject-level-results-for-aggregate-datasets).

??? abstract "Example query result TSV"
    {{ read_table('./repos/neurobagel_examples/query-tool-results/neurobagel-query-results-with-URIs.tsv') }}

This file contains the same columns and data as the [descriptive query results TSV](#harmonized-tsv-data-with-descriptive-labels). 
However, the harmonized terms in the following columns are provided in their raw URI form instead of as descriptive labels:

| Column name |
| ----- |
| SessionType |
| Sex |
| Diagnosis |
| Assessment |
| SessionImagingModalities |
| SessionCompletedPipelines |
| DatasetImagingModalities |
| DatasetPipelines |

#### `protected` subject-level results for aggregate datasets

!!! example
    For examples of aggregated matching dataset results, see the last rows of the example query result TSV in the previous two sections.

A row in a query result TSV may show `protected` for all columns except for `DatasetName`, `PortalURI`, and other dataset-level columns. This means the source graph database (node) has been configured (via its corresponding Neurobagel node API) to return only aggregate information about matching subjects e.g., for data privacy reasons.

More information on this configuration setting, called `NB_RETURN_AGG`, and how to change it for a node can be found [here](config.md#environment-variables).

## Testing
{%
   include-markdown "https://raw.githubusercontent.com/neurobagel/query-tool/main/README.md"
   start="## Testing"
%}
