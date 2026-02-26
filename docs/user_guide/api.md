# The Neurobagel API

## Introduction

Neurobagel has two flavours of APIs that can be deployed: **node API** and **federation API**.

- A [Neurobagel node API (n-API)](https://github.com/neurobagel/api) formulates SPARQL queries
  based on a set of user-defined parameters to a single connected graph database,
  and processes returned query results into a user-friendly format.
- A [Neurobagel federation API (f-API)](https://github.com/neurobagel/federation-api)
  lets the user sends a single query to _each_ node API it is aware of,
  and collects and combines the decentralized responses into a single set of query results.

Neurobagel's query tool provides a GUI for querying one or more Neurobagel graphs by sending requests to a Neurobagel _federation API_ instance.
However, HTTP requests can also be sent directly to any publicly accessible Neurobagel API (node or federation).

## Public Neurobagel APIs

In addition to supporting independent local/institutional deployments (i.e., instances) of the Neurobagel API,
which can interface with a local or restricted graph,
Neurobagel also hosts its own public instances of a node API and a federation API.

[https://api.neurobagel.org/](https://api.neurobagel.org/) is a public,
Neurobagel-hosted node API that interfaces with Neurobagel's own running graph instance
containing harmonized datasets from the [OpenNeuro](https://openneuro.org/) platform.

## Sending a request to a Neurobagel API directly

Cohort queries of a specific Neurobagel graph database can be submitted via direct requests to the corresponding node API using the `/query` endpoint, e.g. `https://api.neurobagel.org/query`.
Specific query parameters are defined using key-value pairs in the URL following `/query`.

**Example: "I want to query for only female participants in the OpenNeuro graph."**

The URL for such a query would be `https://api.neurobagel.org/query?sex=snomed:248152002`,
where `snomed:248152002` is a controlled term from the SNOMED CT vocabulary corresponding to female sex.

### Example using a curl request

```bash
# To query for female participants in the graph

curl -X 'GET' \
  'https://api.neurobagel.org/query?sex=snomed:248152002' \
  -H 'accept: application/json'

# or
curl -L https://api.neurobagel.org/query?sex=snomed:248152002
```

!!! warning "Avoid trailing slashes in API endpoint URLs"

    Neurobagel APIs have strict requirements regarding trailing slashes.
    When sending `curl` requests to an instance of a Neurobagel API, ensure that you do not include trailing slashes in endpoint URLs.
    For example, requests to `https://api.neurobagel.org/query` will work, but `https://api.neurobagel.org/query/` will not.

## Using the interactive Neurobagel API docs

Interactive documentation for a Neurobagel API (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui))
is available at the `/docs` endpoint (e.g., [https://api.neurobagel.org/docs](https://api.neurobagel.org/docs))
and can also be used to run queries against the graph.

!!! note
    For convenience, navigating to [https://api.neurobagel.org/](https://api.neurobagel.org/) in the browser will automatically redirect you to the docs.

To send a request to the API from the docs interface, expand the `query` endpoint tab with the :fontawesome-solid-chevron-down: icon to view the parameters that can be set,
and click "Try it out" and then "Execute" to execute a query.

!!! note
    Due to limitations of Swagger UI in displaying very large HTTP response bodies,
    queries with very few parameters sent using the interactive docs UI may be very slow or time out.
    If this is the case, try using a `curl` request or the query tool instead.
