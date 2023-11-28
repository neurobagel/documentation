### Federation API

:   The neurobagel federation API (also f-API in the documentation)
    is a standalone service that allows query users to send a single
    query and have it automatically send to many neurobagel node APIs
    (n-API) without having to know where these node APIs are located.
    The f-API takes care of keeping an up to date list of available 
    n-APIs, federating queries, retrieving and combining results, 
    and returning them to the user.

    The f-API is designed to very closely resemble the behaviour and
    the endpoints of a n-API so that services can be built that are
    able to work either directly with a single n-API or with an f-API.

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

### Node API

:   In neurobagel we refer to a node as a locally deployed service
    that holds information about data for one data owner who controls
    and manages the node. A node has two core components:

    - a graph backend to store the harmonised data for querying
    - a RESTful **node API** (n-API) that exposes query endpoints for
    users or programs to send queries and retrieve results

    One important purpose of the n-API is to act as a barrier
    between the user and the graph backend so that the user cannot
    execute arbitrary queries on the graph and that the data owner
    can control how detailed the query responses should be.




