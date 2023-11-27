## When to use local query federation
There are two main reasons to deploy local query federation:

- **Case 1**: one-way federation. You have (at least) one [local neurobagel
node](infrastructure.md) and you want your users to be able to search
the data in the local node alongside all the publicly
visible data in the neurobagel network.
- **Case 2**: internal federation. You have two or more local neurobagel
nodes (e.g. for data from different groups in your institute)
and you want your local users to search across all of them.

![Local federation scenarios](imgs/local_federation_architecture.jpg)

Note that these cases are not mutually exclusive. 
Any local neurobagel nodes you deploy will only be visible to users
inside of your local network (internal federation).

## When not to use local query federation
Query federation is not necessary, if you:

- **only want to query public neurobagel nodes**:
  Existing public nodes in the neurobagel network are accessible
  to everyone via our public query tool (e.g. on [query.neurobagel.org](https://query.neurobagel.org/))
  and you can choose to also make them available to your local deployment
  through one-way federation.
- **you only want to search a single neurobagel node**:
  If you only have one local node that you want to query,
  it is easier to directly query the node-API of this node.
  In that case, all you have to do is follow the [deployment instructions
  for a neurobagel node](infrastructure.md) and you are good to go.

## Setting up for local federation
Federated graph queries in neurobagel are provided by the federation API (`f-API`) service.
The neurobagel `f-API` takes a single user query and then sends it to every
neurobagel node API (`n-API`) it is aware of, collects and combinesthe responses,
and sends them back to the user as a single answer.

!!! note

    Make sure you have at least one [local `n-API` configured and running](infrastructure.md)
    before you set up local federation. If you do not have any local
    `n-APIs` to federate over, you can just use our public query tool directly at [query.neurobagel.org](https://query.neurobagel.org/).

In your command line, create and navigate to a new directory where you will keep the configuration
files for your new `f-API`. In this directory, create two files:

### `fed.env` environment file 

Create a text file called `fed.env` to hold environment variables needed for the `f-API` deployment. 
Let's assume there are two local nodes already running on different servers of your institutional network, and you want to set up federation across both nodes:

- a node named `"node_archive"` running on your local computer on port `8000` and 
- a node named `"node_recruitment"` running on a different computer with the local IP `192.168.0.1`, listening on the default http port `80`. 
In your `fed.env` file you would configure this as follows:

``` {.bash .annotate}
# Configuration for f-API
# List of known local node APIs: (node_URL, node_NAME)
LOCAL_NB_NODES=(http://localhost:8000, node_archive) (http://192.168.0.1, node_recruitment)
# Define the port that the f-API will run on INSIDE the docker container (default 8000)
NB_API_PORT=8000
# Define the port that the f-API will be exposed on to the host computer (and likely the outside network)
NB_API_PORT_HOST=8080
# Chose the docker image tag of the f-API (default latest)
NB_API_TAG=latest

# Configuration for query tool
# Define the URL of the f-API as it will appear to a user
API_QUERY_URL=http://localhost:8080 # (1)!
# Chose the docker image tag of the query tool (default latest)
NB_QUERY_TAG=latest
# Chose the port that the query tool will be exposed on the host and likely the network (default 3000)
NB_QUERY_PORT_HOST=3000
```

1.  When a user users the graphical query tool to query your
    f-API, these requests will be sent from the users machine,
    not from the machine hosting the query tool.

    Make sure you set the `API_QUERY_URL` in your `fed.env`
    as it will appear to a user on their own machine 
    - otherwise the request will fail..

Each node to be federated over is described in the variable `LOCAL_NB_NODES` by a comma-delimited tuple of the form `(node_URL, node_NAME)`.

You can add one or more local nodes to the list of nodes known to your `f-API` in this way.
Just adjust the above code snippet according to your own deployment, and store it in a file called `fed.env`.


### `docker-compose.yml` docker config file

Create a second file called `docker-compose.yml`. 
This file describes the required services, ports and paths
to launch the `f-API` together with a connected query tool.

!!! danger "Make sure you have a recent version of docker compose installed"

    Some Linux distributions come with outdated versions of `docker` and 
    `docker compose` installed. Please make sure you install `docker` 
    as described in the [official documentation](https://docs.docker.com/engine/install/).

Copy the following snippet into your `docker-compose.yml` file.
You should not have to change anything about this file.
All local configuration changes are done in the `fed.env` file.

``` {.yaml .annotate}
version: "3.8"

services:
  federation:
    image: "neurobagel/federation_api:${NB_API_TAG:-latest}"
    ports:
      - "${NB_API_PORT_HOST:-8000}:${NB_API_PORT:-8000}"
    environment:
      - LOCAL_NB_NODES=${LOCAL_NB_NODES} # (1)!
      - NB_API_PORT=${NB_API_PORT:-8000}
  query:
    image: "neurobagel/query_tool:${NB_QUERY_TAG:-latest}"
    ports:
      - "${NB_QUERY_PORT_HOST:-3000}:3000"
    environment:
      - API_QUERY_URL=${API_QUERY_URL:-http://localhost:8000/}
```

1.  We maintain a list of public neurobagel nodes 
    [here](https://github.com/neurobagel/menu/blob/main/node_directory/neurobagel_public_nodes.json).
    By default every new `f-API` will lookup this list
    on startup and include it in the list of nodes to
    federate over.
    This also means that you do not have to manually
    configure public nodes, i.e. you **do not have to explicitly add them** to the `LOCAL_NB_NODES` variable) in your `fed.env` file.


## Launch f-API and query tool
Once you have created your `fed.env` and `docker-compose.yml` files
as described above, you can simply launch the services by running

`docker compose --env-file fed.env up -d`

from the same directory.