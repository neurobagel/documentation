This glossary compiles some key terms used in the Neurobagel documentation and defines them in the context of the Neurobagel ecosystem.

### Data dictionary

:   A JSON file that describes the information contained in columns from a tabular data file,
    along with the meaning and properties (format of numerical data, unique “levels”
    of categorical data, etc.) of values in each column. In the context of Neurobagel,
    the meanings of columns and column values are encoded using terms from standardised vocabularies.

### Data model

**Used interchangeably with**: data schema

:   A structure that has been designed with the
    purpose to represent a specific kind of information.
    A data model is made up of generic types or classes that are relevant
    to the data model designers (for Neurobagel, examples include "Research Participant"
    and "Neuroimaging Dataset"), the properties these types can
    have (e.g., "Age in years", "Dataset name"), and the
    relationships that can exist between them (e.g., "is part of").
    The goal of a data model is to give information a structure
    so that we can write programs that can consume the information.

    The Neurobagel data model is designed to represent the kind
    of information that is important to support the most relevant
    cohort definition queries, and thus models types, properties,
    and relationships that are important for this purpose.
    It is not a static thing, and we constantly add new things to
    the data model as we support new use cases that rely on this
    information.

### Controlled term

:   A unique identifier or code for a concept that is described in a controlled vocabulary.

    A controlled term has a

    - a clear definition
    - a unique and persistent identifier
    - from a specific curated list of terms like a vocabulary, taxonomy or ontology

    An example is the controlled term for
    ["Parkinson's disease" from the ICD-11 taxonomy](https://icd.who.int/browse11/l-m/en#/http://id.who.int/icd/entity/296066191)
    with the unique code `8A00.0`.

### Controlled vocabulary

**Used interchangeably with**: taxonomy, and ontology

:   A **controlled vocabulary** is a collection of controlled terms that
    are often all about one specific topic. The main benefit of a
    controlled vocabulary is that it provides unambiguous terms with
    clear definitions that people have agreed to use to describe their
    information - removing the need to align variable names and value
    formats between datasets and enabling interoperability.

    For example, most websites use the [schema.org](https://schema.org/)
    vocabulary to describe things like
    [products](https://schema.org/Product) to purchase,
    [events](https://schema.org/Event) to book,
    [recipes](https://schema.org/Recipe) to cook etc.
    in a consistent way that can be understood by
    the search spiders of big search engines.

??? Note "Reusing controlled vocabularies"
    Creating a controlled vocabulary is a laborious task
    that involves deep subject matter expertise, often from many experts,
    and needs to be maintained to remain relevant.
    You should therefore almost always **reuse** an existing vocabulary
    rather than creating your own.

    A **taxonomy** is a more specific form of a controlled vocabulary
    that organizes terms into hierarchical relationships. For example,
    a ["Recipe"](https://schema.org/Recipe) in schema.org is a subtype of
    a "HowTo" which itself is a subtype of a "CreativeWork". This hierarchy
    let's you do things like search for "CreativeWork" and also find
    "Recipe", even if you have never made this link directly.

    An **ontology** is an even more specific form of a taxonomy
    where terms can have very complex relationships with each other
    that include logical constraints. In an ontology, you could for example
    express that for someone to be a "sister" to someone else,
    both the subject and the object of the relationship have to be "human",
    only the subject of the relation has to be "female", and both have to
    have at least one parent in common. These complex expressions are very
    labour intensive to create but can provide also very
    rich ways of validating and even inferring information.

### Graph database

**Used interchangeably with**: knowledge graph store, graph store, graph

:   A type of database, in the same way that a relational databases is a type of database.
    The main distinguishing feature of graph databases is that they
    represent entities as nodes in a graph,
    and relationships between entities as edges between these nodes.
    This data model makes it easy to easily add new information
    by drawing a new edge between two nodes.

??? note
    A single Neurobagel graph database can contain harmonised information about multiple datasets and their respective subjects. Each subject is represented by a node, and their harmonised phenotypic and imaging data characteristics are described using controlled terms connected to the subject node via a series of edges that individually encode the type of attribute described by the controlled term.

    Neurobagel uses the RDF graph data model, see also [https://en.wikipedia.org/wiki/Graph_database](https://en.wikipedia.org/wiki/Graph_database).

### Annotation

:   In the context of Neurobagel, annotation refers to the process
    of describing tabular demographic, cognitive, and/or clinical (phenotypic) data for a dataset
    with terms from controlled vocabularies to create machine
    understandable data dictionaries for the data. You can learn
    more about this process in our [documentation](user_guide/annotation_tool.md).

### Aggregated results

:   If the owner of a Neurobagel node decides that query responses
    should not include information at the level of individual
    participants, they can configure their node to only return
    aggregated results. In this mode, the node will aggregate
    all participants that match a query at the dataset level
    and only respond with counts of matching participants.

### Data owner

:   A person or an institute
    who is responsible in the data governance sense
    for one or many datasets. In the context of Neurobagel, one data owner can have one or
    more Neurobagel nodes, but every Neurobagel node can only
    have one data owner who is responsible for all of the data
    stored inside the node.

### Federation API

**Used interchangeably with**: f-API
:   A standalone service that allows query users to send a single
    query and have it automatically sent to many Neurobagel node APIs
    (n-API) without having to know where these node APIs are located.
    The f-API takes care of keeping an up to date list of available
    n-APIs, federating queries, retrieving and combining results,
    and returning them to the user.

    Designed to very closely resemble the behaviour and
    the endpoints of a n-API so that services can be built that are
    able to work either directly with a single n-API or with an f-API.

### Node API

**Used interchangeably with**: n-API
:   A Neurobagel "node" is a locally deployed service
    that holds information about data for one data owner who controls
    and manages the node. A node has two core components:

    - a graph backend to store the harmonised data for querying
    - a RESTful **node API** that exposes query endpoints for
    users or programs to send queries and retrieve results

    One important purpose of the n-API is to act as a barrier
    between the user and the graph backend so that the user cannot
    execute arbitrary queries on the graph, and the data owner
    can control how detailed the query responses should be.

### Tabular data

**Used interchangeably with**: phenotypic data

:   Tabular text files (e.g., .tsv or .csv) that contain information about
    participants such as their demographic information or data from
    cognitive or clinical assessments they have completed.
    We often refer to this information as phenotypic data
    because they describe observable characteristics of the participant.

### TSV

:   A Tab-Separated Values (TSV) file has the `.tsv` extension and is a [plain text](https://www.howtogeek.com/465420/what-is-plain-text/) file structured as a table,
    where values belonging to different columns are separated by a single tab character (`\t`).
    Each column represents a field of interest, and each row represents a single datapoint.
    The first line of the file (the header) contains the names of each column.

    A valid TSV should also follow some common formatting guidelines:

    - Each line must contain the same number of tab-separated fields (columns), even if some are empty
    - Column names must be unique (no duplicates)
    - Do not include completely blank rows or columns
    - Avoid leading or trailing spaces in column names and values

    Most spreadsheet software (e.g., Microsoft Excel, Google Sheets) will allow you to save a file as TSV ([this webpage](https://www.geeksforgeeks.org/techtips/what-is-a-tsv-file/) has guides on creating TSVs in common applications),
    but it is your responsibility to ensure that the file is well-structured according to TSV formatting conventions.
