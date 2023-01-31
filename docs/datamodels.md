# Neurobagel Datamodels

## Data Dictionaries

When you annotate a demographic `.csv` file with the Neurobagel Annotation tool,
your annotations are stored in a data dictionary.
Neurobagel uses a structure for these data dictionaries that is compatible 
with and expands on the 
[BIDS `participant.json` data dictionaries](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#participants-file). 

!!! info
    The specification for how a Neurobagel data dictionary is structured
    is also called a schema. 
    Because Neurobagel data dictionaries are stored as `.json` files,
    we use the [`jsonschema` schema language](https://json-schema.org/) 
    to write the specification.

The Neurobagel data dictionaries add a new `Annotations` attribute 
to each column entry to store the semantic annotations.

Here is an example of a BIDS data dictionary:

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

And here is the same example with Neurobagel annotations added:

```json hl_lines="5-14 22-41"
{
  "age": {
    "Description": "age of the participant",
    "Units": "years",
    "Annotations": {
      "IsAbout": {
        "TermURL": "http://purl.obolibrary.org/obo/NCIT_C25150",
        "Label": "Age"
      },
      "Unit": {
        "TermURL": "xsd:integer",
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
        "TermURL": "http://purl.obolibrary.org/obo/NCIT_C28421",
        "Label": "Sex"
      },
      "Levels": {
        "M": {
          "TermURL": "http://purl.obolibrary.org/obo/NCIT_C20197",
          "Label": "Male"
        },
        "F": {
          "TermURL": "http://purl.obolibrary.org/obo/NCIT_C16576",
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

### Special attributes

