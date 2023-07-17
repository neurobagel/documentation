# The Neurobagel API

The Neurobagel API, hosted at [https://api.neurobagel.org/]([https://api.neurobagel.org/]), 
is a REST API that interfaces with Neurobagel's own running knowledge graph instance. 
The API formulates SPARQL queries to the graph from a set of user-defined parameters and 
processes returned query results into a user-friendly format.

Neurobagel's query tool ([https://query.neurobagel.org](https://query.neurobagel.org)) queries the Neurobagel graph by sending requests to the API. 
However, HTTP requests can also be sent directly to the Neurobagel API. 
An independent local or institutional deployment of the API is also possible to interface with a local or restricted graph (see section on [setting up a graph](infrastructure.md)).

## Quickstart
Queries of the knowledge graph can be submitted via direct requests to the API using the `https://api.neurobagel.org/query/` endpoint. 
Specific query parameters are defined using key-value pairs in the URL following `/query/`.

**Example: "I want to query for only female participants in the graph."**

The URL for such a query would be `https://api.neurobagel.org/query/?sex=snomed:248152002`, where `snomed:248152002` is a controlled term from the SNOMED CT vocabulary corresponding to female sex.

### Example using a curl request
```bash
# To query for female participants in the graph

curl -X 'GET' \
  'http://localhost:8000/query/?sex=snomed:248152002' \
  -H 'accept: application/json'

# or
curl -L http://localhost:8000/query/?sex=snomed:248152002
```

## Using the interactive API docs
Interactive documentation for the API (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)) is available at [https://api.neurobagel.org/docs]([https://api.neurobagel.org/docs]) and can also be used to run queries against the graph.

!!! note
    For convenience, navigating to [https://api.neurobagel.org/]([https://api.neurobagel.org/]) in the browser will automatically redirect you to the docs.

To send a request to the API from the docs interface, expand the `query` endpoint tab with the :fontawesome-solid-chevron-down: icon to view the parameters that can be set, 
and click "Try it out" and then "Execute" to execute a query.

!!! note
    Due to limitations of Swagger UI in displaying very large HTTP response bodies, 
    queries with very few parameters sent using the interactive docs UI may be very slow or time out. 
    If this is the case, try using a `curl` request or the query tool instead.
