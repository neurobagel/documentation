### Controlled term

:   A controlled term has a 

    - a clear definition
    - a unique and persistent identifier
    - that exists in a curated list of terms like a vocabulary, taxonomy or ontology

    An example is the controlled term for 
    ["Parkinson's disease" from the ICD-11 taxonomy](https://icd.who.int/browse11/l-m/en#/http://id.who.int/icd/entity/296066191)
    with the unique code `8A00.0`.

### Data model

:   A data model is a structure that has been designed with the 
    purpose to represent a specific kind of information. 
    It is made up of generic types or classes that are relevant
    to the data model designers (for example "Research Participant"
    and "Neuroimaging Dataset"), the properties these types can
    have (for example "Age in years" and "Dataset name"), and the 
    relationships that can exist between them (for example "is Part of").
    The goal of a data model is to give information a structure
    so that we can write programs that can consume the information.

    The neurobagel data model is designed to represent the kind
    of information that is important to support the most relevant
    cohort definition queries, and thus models types, properties,
    and relationships that are important for this purpose.
    It is not a static thing, and we constantly add new things to 
    the data model as we support new use cases that rely on this
    information.


### Graph database

:   Graph databases are a type of database such as relational databases.
    The main distinguishing feature of graph databases is that they 
    represent entities as nodes in a graph, 
    and relationships between entities as edges between these nodes.
    This data model makes it easy to easily add new information
    by drawing a new edge between two nodes.

    Graph databases come in two general flavours: 
    linked property graphs (LPG),
    and Resource Description Framework (RDF) graphs. 
    Neurobagel uses RDF graphs because RDF is an open standard
    maintained by the W3C.