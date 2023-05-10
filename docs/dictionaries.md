# Neurobagel Data Dictionaries

The Neurobagel annotator creates a BIDS compatible data dictionary
and augments the information that BIDS recommends with 
unambiguous semantic tags.

Below we'll outline several special cases using the following example `participants.tsv` file:

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
    "purl": "http://purl.obolibrary.org/obo/",
    "snomed": "http://purl.bioontology.org/ontology/SNOMEDCT/",
    "cogatlas": "https://www.cognitiveatlas.org/task/id/"
  }
}
```

## Participant identifier

Term from the Neurobagel vocabulary.

```json hl_lines="6-7"
{
  "participant_id": {
    "Description": "A participant ID",
    "Annotations": {
      "IsAbout": {
        "TermURL": "nb:ParticipantID",
        "Label": "Subject Unique Identifier"
      }
    }
  }
}

```

!!! note
    `participant_id` is a reserved name in BIDS and BIDS data dictionaries
    therefore typically don't annotate this column. Neurobagel supports
    multiple subject ID columns for situations where a study is using more than
    one ID scheme.

## Session identifier

Term from the Neurobagel vocabulary.

```json hl_lines="6-7"
{
  "session_id": {
    "Description": "A session ID",
    "Annotations": {
      "IsAbout": {
        "TermURL": "nb:SessionID",
        "Label": "Run Identifier"
      }
    }
  }
}

```

!!! note
    Unlike the BIDS specification, Neurobagel supports a `participants.tsv`
    file with a `session_id` field.

## Diagnosis

Terms from the [SNOMED-CT ontology](https://browser.ihtsdotools.org/) for clinical diagnosis.
Terms from the National Cancer Institute Thesaurus for healthy control status.

```json hl_lines="10-11 15-16 19-20"
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
          "TermURL": "purl:NCIT_C94342",
          "Label": "Healthy Control"
        }
      }
    }
  }
}
```

The `IsAbout` relation uses a term from the Neurobagel namespace because
`"Diagnosis"` is a standardized term.

## Sex

Terms are from the SNOMED-CT ontology.

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

## Age
Neurobagel has a common data element for `"Age"` which describes a continuous column. To ensure age values are represented as floats in Neurobagel graphs, Neurobagel encodes the relevant "heuristic" describing the value format of a given age column. This heuristic, stored in the `Transformation` annotation, corresponds internally to a specific transformation that is used to convert the values to float ages.

Possible heuristics are: `float`, `int`, `euro`, `bounded`, `range`, `iso8601`

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
        "TermURL": "nb:euro",
        "Label": "European value decimals"
      }
    }
  }
}
```

## Assessment tool

For assessment tools like cognitive tests or rating scales, 
Neurobagel encodes whether the tool was successfully completed.
Because assessment tools often have several subscales or items 
that can be stored as separate columns in the tabular `participant.tsv` file,
each assessment tool column gets at least two annotations:

- one to classify it as `IsAbout` the generic category of assessment tools
- one to classify it as `PartOf` the specific assessment tool

An additional annotation `MissingValues` can be used to specify value(s) in an assessment tool column which represent that the participant is missing a value/response for that subscale, when instances of missing values are present.

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
we then combine all of the columns that were classified as `PartOf` that specific tool
and then apply a simple `all()` heuristic to check that none of the columns
contain any `MissingValues`.

For the above example, this would be:

| particpant_id | updrs_1 | updrs_2 |
|---------------|---------|---------|
| sub-01        | 2       |         |
| sub-02        | 1       | 1       |

Therefore: 

| particpant_id | updrs_available |
|---------------|-----------------|
| sub-01        | False           |
| sub-02        | True            |

