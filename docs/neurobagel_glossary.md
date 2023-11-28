### Annotation

:   In the context of neurobagel, annotation refers to the process
    of describing tabular demographic or phenotypic datasets
    with terms from controlled vocabularies to create machine 
    understandable data dictionaries for data. You can learn
    more about this process in our [documentation](annotation_tool.md).

### Aggregated results

:   If the owner of a neurobagel node decides that query responses
    should not include information at the level of individual 
    participants, they can configure their node to only return
    aggregated results. In this mode, the node will aggregate
    all participants that match a query at the dataset level
    and only respond with counts of matching participants.

### Data owner

:   A data owner for neurobagel is a person or an institute
    who is responsible in the data governance sense 
    for one or many datasets. One data owner can have one or
    more neurobagel nodes, but every neurobagel node can only
    have one data owner who is responsible for all of the data
    stored inside the node. 

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

### Tabular or phenotypic data

:   



