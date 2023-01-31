# Neurobagel Data Dictionaries

The neurobagel annotator creates a BIDS compatible data dictionary
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
    "bg": "https://terms.neurobagel.org/",
    "purl": "http://purl.obolibrary.org/obo/",
    "snomed": "http://purl.bioontology.org/ontology/SNOMEDCT/",
    "cogAtlas": "https://www.cognitiveatlas.org/task/id/"
  }
}
```

## Participant identifier

Term from National Cancer Institute Thesaurus

```json hl_lines="5-6"
{
  "participant_id": {
    "Annotations": {
      "IsAbout": {
        "TermURL": "purl:NCIT_C69256",
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

Term from National Cancer Institute Thesaurus

```json hl_lines="5-6"
{
  "session_id": {
    "Annotations": {
      "IsAbout": {
        "TermURL": "purl:NCIT_C117058",
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

```json hl_lines="5-6 10-11 14-15"
{
  "group": {
    "Annotations": {
      "IsAbout": {
        "TermURL": "bg:diagnosis",
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

The `IsAbout` relation uses a term from the neurobagel (`bg`) namespace because
`"Diagnosis"` is a standardized term.

## Sex

Terms are from the BIDS recommended namespace.

```json
{
    "sex": {
    "Annotations": {
      "IsAbout": {
        "TermURL": "bg:sex",
        "Label": "Sex"
      },
      "Levels": {
        "M": {
          "TermURL": "bids:male",
          "Label": "Male"
        },
        "F": {
          "TermURL": "bids:female",
          "Label": "Female"
        }
      }
    }
  }
}
```

The `IsAbout` relation uses a Neurobagel (`bg`) scoped term for `sex` because 
this is a Neurobagel common data element.

## Assessment tool

For assessment tools like cognitive tests or rating scales, 
Neurobagel encodes whether the tool was successfully completed.
Because assessment tools often have several subscales or items 
that can be stored in the tabular `participant.tsv` file,
each assessment tool column gets two tags:

- one to classify it as `IsAbout` the generic category of assessment tools
- one to classify it as `PartOf` the specific assessment tool

```json hl_lines="4 8 24"
{
  "updrs_1": {
    "Annotations": {
      "IsAbout": {
        "TermURL": "bg:assessment",
        "Label": "Assessment tool"
      },
      "IsPartOf": {
        "TermURL": "cogAtlas:tsk_4a57abb949ece",
        "Label": "Unified Parkinson's Disease Rating Scale"
      }
    }
  },
  "updrs_2": {
    "Annotations": {
      "IsAbout": {
        "TermURL": "bg:assessment",
        "Label": "Assessment tool"
      },
      "IsPartOf": {
        "TermURL": "cogAtlas:tsk_4a57abb949ece",
        "Label": "Unified Parkinson's Disease Rating Scale"
      },
      "MissingValues": [""]
    }
  }
}
```

To determine whether a specific assessment tool is available for a given participant,
we then combine all of the columns that were classified as `PartOf` the specific tool
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

