### Controlled term

:   A controlled term has a 

    - a clear definition
    - a unique and persistent identifier
    - that exists in a curated list of terms like a vocabulary, taxonomy or ontology

    An example is the controlled term for 
    ["Parkinson's disease" from the ICD-11 taxonomy](https://icd.who.int/browse11/l-m/en#/http://id.who.int/icd/entity/296066191)
    with the unique code `8A00.0`.

### Controlled vocabulary, taxonomy, ontology

:    A **controlled vocabulary** is a collection of controlled terms that
     are often all about one specific topic. The main benefit of a 
     controlled vocabulary is that it provides unambiguous terms with
     clear definitions that people can agree to use to describe their
     information - removing the need to align variable names and value
     formats between datasets and enabling interoperability. 
     
     For example, most websites use the [schema.org](https://schema.org/)
     vocabulary to describe things like 
     [products](https://schema.org/Product) to purchase, 
     [events](https://schema.org/Event) to book, 
     [recipes](https://schema.org/Recipe) to cook etc.
     in a consistent way that can be understood by 
     the search spiders of big search engines.
     
     Creating a controlled vocabulary is a laborious task 
     that involves deep subject matter expertise, often from many experts, 
     and need to be maintained to remain relevant.
     You should therefore almost always **reuse** an existing vocabulary
     rather than creating your own. 
     
     A **taxonomy** is a more specific form of a controlled vocabulary 
     that organizes terms into hierarchical relationships. For example
     a [Recipe](https://schema.org/Recipe) in schema.org is a subtype of
     a HowTo which itself is a subtype of a CreativeWork. This hierarchy 
     let's you do things like search for "CreativeWork" and also find
     "Recipe", even if you have never made this link directly.
     
     An **ontology** is an even more specific form of a taxonomy 
     where terms can have very complex relationships with each other
     that include logical constraints. In an Ontology you could for example
     express that for someone to be a "sister" to someone else, 
     both the subject and the object of the relationship have to be "human",
     only the subject of the relation has to be "female", and both have to 
     have at least one parent in common. These complex expressions are very
     labour intensive to create but can provide also very 
     rich ways of validating and even inferring information.

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