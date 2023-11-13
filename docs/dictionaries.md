# Neurobagel data dictionaries

## Overview
When you annotate a phenotypic TSV using the Neurobagel annotation tool 
(see also the [section on the annotation tool](annotation_tool.md)),
your annotations are automatically stored in a JSON data dictionary.
A Neurobagel data dictionary essentially describes the meaning and properties of columns and column values
using standardized vocabularies.

!!! example
    A comprehensive example data dictionary containing all currently supported phenotypic attributes and annotations can be found [here](https://github.com/neurobagel/neurobagel_examples/blob/main/data-upload/example_synthetic.json) (corresponding [phenotypic .tsv](https://github.com/neurobagel/neurobagel_examples/blob/main/data-upload/example_synthetic.tsv)).

Importantly, Neurobagel uses a structure for these data dictionaries that is compatible 
with and expands on 
[BIDS `participant.json` data dictionaries](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#participants-file). 

!!! info
    The specification for how a Neurobagel data dictionary is structured
    is also called a schema. 
    Because Neurobagel data dictionaries are stored as `.json` files,
    we use the [`jsonschema` schema language](https://json-schema.org/) 
    to write the specification.

Neurobagel data dictionaries uniquely include an `Annotations` attribute 
for each column entry to store user-provided semantic annotations.

Here is an example BIDS data dictionary (`participants.json`):

```json
{
  "age": {
    "Description": "age of the participant",
    "Units": "years"
  },
  "sex": {
    "Description": "sex of the participant as reported by the participant",
    "Levels": {
      "M": "male",
      "F": "female"
    }
  }
}
```

And here is the same data dictionary augmented with Neurobagel annotations:

```json hl_lines="5-14 22-41"
{
  "age": {
    "Description": "age of the participant",
    "Units": "years",
    "Annotations": {
      "IsAbout": {
        "TermURL": "http://neurobagel.org/vocab/Age",
        "Label": "Age"
      },
      "Transformation": {
        "TermURL": "http://neurobagel.org/vocab/int",
        "Label": "Integer"
      }
    }
  },
  "sex": {
    "Description": "sex of the participant as reported by the participant",
    "Levels": {
      "M": "male",
      "F": "female"
    },
    "Annotations": {
      "IsAbout": {
        "TermURL": "http://neurobagel.org/vocab/Sex",
        "Label": "Sex"
      },
      "Levels": {
        "M": {
          "TermURL": "http://purl.bioontology.org/ontology/SNOMEDCT/248153007",
          "Label": "Male"
        },
        "F": {
          "TermURL": "http://purl.bioontology.org/ontology/SNOMEDCT/248152002",
          "Label": "Female"
        }
      },
      "MissingValues": [
        "",
        " "
      ]
    }
  }
}
```

A custom Neurobagel namespace (URI: `http://neurobagel.org/vocab/`) is currently used for controlled terms that represent attribute classes modelled by Neurobagel, such as `"Age"` and `"Sex"`, even though these terms may have equivalents in other vocabularies used for annotation. For example, the following terms from the Neurobagel annotations above are conceptually equivalent to terms from the SNOMED CT namespace:

| Neurobagel namespace term       | Equivalent external controlled vocabulary term                     |
|---------------------------------|---------------------------------------------------------|
| http://neurobagel.org/vocab/Age | http://purl.bioontology.org/ontology/SNOMEDCT/397669002 |
| http://neurobagel.org/vocab/Sex | http://purl.bioontology.org/ontology/SNOMEDCT/184100006 |

## Phenotypic attributes

The Neurobagel annotation tool generates a data dictionary entry for a given column 
by augmenting the information recommended by BIDS with unambiguous semantic tags.

Below we'll outline several example annotations using the following example `participants.tsv` file:

| participant_id | session_id | group | age | sex | updrs_1 | updrs_2 |
|----------------|------------|-------|-----|-----|---------|---------|
| sub-01         | ses-01     | PAT   | 25  | M   | 2       |         |
| sub-01         | ses-02     | PAT   | 26  | M   | 3       | 5       |
| sub-02         | ses-01     | CTL   | 28  | F   | 1       | 1       |
| sub-02         | ses-02     | CTL   | 29  | F   | 1       | 1       |

Controlled terms in the below examples are shortened using the RDF prefix/context
syntax for [json-ld](https://w3c.github.io/json-ld-syntax/#the-context):

```json
{
  "@context": {
    "nb": "http://neurobagel.org/vocab/",
    "ncit": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#",
    "nidm": "http://purl.org/nidash/nidm#",
    "snomed": "http://purl.bioontology.org/ontology/SNOMEDCT/",
    "cogatlas": "https://www.cognitiveatlas.org/task/id/"
  }
}
```

### Participant identifier

Term from the Neurobagel vocabulary.

```json hl_lines="6-7 9"
{
  "participant_id": {
    "Description": "A participant ID",
    "Annotations": {
      "IsAbout": {
        "TermURL": "nb:ParticipantID",
        "Label": "Subject Unique Identifier"
      },
      "Identifies": "participant"
    }
  }
}

```

!!! note
    `participant_id` is a reserved name in BIDS and BIDS data dictionaries
    therefore typically don't annotate this column. Neurobagel supports
    multiple subject ID columns for situations where a study is using more than
    one ID scheme.

!!! note
    The `Identifies` annotation key is currently required to validate annotations for columns about unique 
    observation identifiers  (e.g., participant or session IDs). The `"Identifies"` key should only be used for these
    columns and its value should be an informative string value describing the type/level of observation 
    identified. This required key is currently only used for validation and its value will not be processed by
    Neurobagel.
    (e.g., participant or session IDs), and should have an informative string value 
    describing the type/level of observation identified.

### Session identifier

Term from the Neurobagel vocabulary.

```json hl_lines="6-7 9"
{
  "session_id": {
    "Description": "A session ID",
    "Annotations": {
      "IsAbout": {
        "TermURL": "nb:SessionID",
        "Label": "Run Identifier"
      },
      "Identifies": "session"
    }
  }
}

```

!!! note
    Unlike the BIDS specification, Neurobagel supports a `participants.tsv`
    file with a `session_id` field.

### Diagnosis

Terms from the [SNOMED-CT ontology](https://browser.ihtsdotools.org/) for clinical diagnosis.
Terms from the National Cancer Institute Thesaurus for healthy control status.

```json hl_lines="10-11 13 15-16 19-20"
{
  "group": {
    "Description": "Group variable",
    "Levels": {
      "PD": "Parkinson's patient",
      "CTRL": "Control subject",
    },
    "Annotations": {
      "IsAbout": {
        "TermURL": "nb:Diagnosis",
        "Label": "Diagnosis"
      },
      "Levels": {
        "PD": {
          "TermURL": "snomed:49049000",
          "Label": "Parkinson's disease"
        },
        "CTRL": {
          "TermURL": "ncit:C94342",
          "Label": "Healthy Control"
        }
      }
    }
  }
}
```

The `IsAbout` relation uses a term from the Neurobagel namespace because
`"Diagnosis"` is a standardized term.

!!! note
    Columns with categorical values (e.g., study groups, diagnoses, sex)
    require a `Levels` key in their Neurobagel annotation. 
    The Neurobagel "Levels" key is modeled after the BIDS "Levels" key for human readable descriptions.

### Sex

Terms are from the SNOMED-CT ontology, which has controlled terms aligning with BIDS `participants.tsv` descriptions for sex.  Below are the SNOMED terms for the sex values allowed by BIDS: 

| Sex    | Controlled term                                                 |
| ------ | --------------------------------------------------------------- |
| Male   | http://purl.bioontology.org/ontology/SNOMEDCT/248153007         |
| Female | http://purl.bioontology.org/ontology/SNOMEDCT/248152002         |
| Other  | http://purl.bioontology.org/ontology/SNOMEDCT/32570681000036106 |

Here is what a sex annotation looks like in practice:

```json
{
  "sex": {
    "Description": "Sex variable",
    "Levels": {
      "M": "Male",
      "F": "Female"
    },
    "Annotations": {
      "IsAbout": {
        "TermURL": "nb:Sex",
        "Label": "Sex"
      },
      "Levels": {
        "M": {
          "TermURL": "snomed:248153007",
          "Label": "Male"
        },
        "F": {
          "TermURL": "snomed:248152002",
          "Label": "Female"
        }
      }
    }
  }
}
```

The `IsAbout` relation uses a Neurobagel scoped term for `"Sex"` because 
this is a Neurobagel common data element.

### Age
Neurobagel has a common data element for `"Age"` describing a continuous column. 
To ensure age values are represented as floats in Neurobagel graphs, 
Neurobagel encodes the relevant "heuristic" describing the value format for a given age column. 
This heuristic, stored in the `Transformation` annotation (required for continuous columns describing age), 
maps internally to a specific transformation that is used to convert the values to floats.

Possible heuristics: 

| TermURL | Label | Example |
| ----- | ----- | ----- |
| `nb:FromFloat` | float value | `31.5`
| `nb:FromInt` | integer value | `31`
| `nb:FromEuro` | european decimal value | `31,5`
| `nb:FromBounded` | bounded value | `30+`
| `nb:FromISO8061` | period of time defined according to the ISO8601 standard | `31Y6M`


```json hl_lines="9-12"
{
  "age": {
    "Description": "Participant age",
    "Annotations": {
      "IsAbout": {
        "TermURL": "nb:Age",
        "Label": "Chronological age"
      },
      "Transformation": {
        "TermURL": "nb:FromEuro",
        "Label": "European value decimals"
      }
    }
  }
}
```

### Assessment tool

For assessment tools like cognitive tests or rating scales, 
Neurobagel encodes whether a subject has a value/score for _at least one_ item or subscale of the assessment.
Because assessment tools often have several subscales or items 
that can be stored as separate columns in the tabular `participant.tsv` file,
each assessment tool column receives **a minimum** of two annotations:

- one to classify that the column `IsAbout` the generic category of assessment tools
- one to classify that the column `IsPartOf` the specific assessment tool

An optional additional annotation `MissingValues` can be used to specify value(s) 
in an assessment tool column which represent that the participant is missing a value/response for that subscale,
when instances of missing values are present (see also section [Missing values](#missing-values)).

```json hl_lines="5 9 26"
{
  "updrs_1": {
    "Description": "item 1 scores for UPDRS",
    "Annotations": {
      "IsAbout": {
        "TermURL": "nb:Assessment",
        "Label": "Assessment tool"
      },
      "IsPartOf": {
        "TermURL": "cogatlas:tsk_4a57abb949ece",
        "Label": "Unified Parkinson's Disease Rating Scale"
      }
    }
  },
  "updrs_2": {
    "Description": "item 2 scores for UPDRS",
    "Annotations": {
      "IsAbout": {
        "TermURL": "nb:Assessment",
        "Label": "Assessment tool"
      },
      "IsPartOf": {
        "TermURL": "cogatlas:tsk_4a57abb949ece",
        "Label": "Unified Parkinson's Disease Rating Scale"
      },
      "MissingValues": [""]
    }
  }
}
```

To determine whether a specific assessment tool is available for a given participant,
we then consider all of the columns that were classified as `IsPartOf` that specific tool
and then apply a simple `any()` heuristic to check that at least one column does not
contain any `MissingValues`.

For the above example, this would be:

| particpant_id | updrs_1 | updrs_2 |
|---------------|---------|---------|
| sub-01        | 2       |         |
| sub-02        | 1       | 1       |
| sub-03        |         |         |

Therefore: 

| particpant_id | updrs_available |
|---------------|-----------------|
| sub-01        | True           |
| sub-02        | True            |
| sub-03        | False           |

## Missing values
Missing values are allowed for any phenotypic variable (column) that does not describe a participant or session identifier (e.g., columns like `participant_id` or `session_id`). 
In a Neurobagel data dictionary, missing values for a given column are listed under the `"MissingValues"` annotation for the column (see the [Assessment tool](#assessment-tool) section
or the [comprehensive example data dictionary](https://github.com/neurobagel/neurobagel_examples/blob/main/data-upload/example_synthetic.json) for examples).
