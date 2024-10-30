# Variables harmonized by Neurobagel

Neurobagel semantically harmonizes a number of variables used to describe different data and metadata for a study participant.

The following list summarizes the variables that can currently be modeled and queried using Neurobagel, at the level of a single subject session.

**We are actively working to expand our subject data model, and welcome [feedback](http://127.0.0.1:8000/getting_help/) on any other variables you would like to be able to query.**

## Phenotypic
For more information on how phenotypic attributes are modeled, see the page on [Neurobagel data dictionaries](dictionaries.md).

- Age
- Sex
- Diagnosis
- Availability of scores on a particular assessment

## Imaging

### Raw
- Available MRI acquisition sequences, following the [BIDS specification](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/magnetic-resonance-imaging-data.html#magnetic-resonance-imaging)

### Processed
- Completed processing pipelines, following the [Nipoppy specification](https://nipoppy.readthedocs.io/en/latest/user_guide/tracking.html)
