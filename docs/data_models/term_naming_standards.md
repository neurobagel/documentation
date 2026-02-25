# Neurobagel standards for controlled term naming

## Naming conventions
### Namespace prefixes

- Names should be all lowercase (e.g., `nidm`, `snomed`)

### Properties (graph "edges")

- Names should adhere to camelCase (uses capitalized words except for the first word/letter)
- Should be a compound of:
    - a verb relevant to the property (e.g., **has**Age, **is**SubjectGroup)
    - the [range](https://www.w3.org/TR/owl-ref/#range-def) of the property, (e.g.,has**Diagnosis** points to a Diagnosis object)

What this might look like in semantic triples:

```
<Subject> <nb:hasDiagnosis> <snomed:1234>
<snomed:1234> <rdf:type> <nb:Diagnosis>
```

### Classes or resources (graph "nodes")

- Names should adhere to PascalCase (each word capitalized)
- Where possible, simplify to a single word (e.g., `Diagnosis`, `Dataset`, `Sex`)

!!! note

    Generally, we own the terms for properties and classes (e.g., Diagnosis, Assessment) but not the resources representing _instances_ of classes such as specific diagnosis, sex, or assessment values (these are reused from existing vocabularies).

    In cases where we reuse a term for a class that comes from an existing controlled vocabulary, and that vocabulary follows a different naming convention (e.g., all lowercase), we should follow the existing naming convention.

## Currently used namespaces

| Prefix | IRI | Types of terms |
| ----- | ----- | ----- |
| `nb` | http://neurobagel.org/vocab/ | Neurobagel-"owned" properties and classes |
| `snomed` | http://purl.bioontology.org/ontology/SNOMEDCT/ | diagnoses, sex, and assessments or instruments |
| `ncit` | http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl# | group designation (e.g., healthy control) |
| `nidm` | http://purl.org/nidash/nidm# | imaging modalities |
| `np` | https://github.com/nipoppy/pipeline-catalog/tree/main/processing/ | processing pipeline and derivative metadata |


## What if an `nb` term already exists in another controlled vocabulary?
If there is an equivalent controlled term to one we are defining in a different namespace,
we document this and express their equivalence using `owl:sameAs`.

Example:
If our term is `nb:Subject` and `nidm:Subject` is conceptually equivalent:

```
<nb:12345> a <nb:Subject>
<nb:Subject> a <rdfs:Resource>;
	<owl:sameAs> <nidm:Subject>
```

## Other general guidelines

- Each property (edge) should use a single namespace for the resources it corresponds to
- Where possible, hardcode or refer to identifiers and not human-readable labels
