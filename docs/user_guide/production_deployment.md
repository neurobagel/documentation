The [Getting started](getting_started.md) page
is designed for quick local testing with minimal configuration.
For a production deployment intended for external users,
you should customize the settings to fit your specific needs.

To help you with this,
the Neurobagel [`recipes` repository](https://github.com/neurobagel/recipes)
includes dedicated production deployment recipes that should
cover the most common use cases.

!!! info "Start with a fresh recipe for each deployment"

    Make a fresh clone of the
    [`recipes` repository](https://github.com/neurobagel/recipes) for each
    deployment you want to launch.

    For example, hosting multiple Neurobagel [nodes](#node),
    or a single [node](#node) alongside a [containerized proxy server](#proxy-server),
    means creating a separate clone of the `recipes` repo for each node or proxy server.
    This will make it easier to update and maintain each deployment.

## Deployable services

All Neurobagel services are [containerized](https://www.docker.com/resources/what-container/).
The production deployment recipes use [Docker Compose profiles](https://docs.docker.com/compose/how-tos/profiles/)
to group related services and allow them to be launched together.

Neurobagel services that are included in the Docker Compose deployment recipes:

- **[Neurobagel node API/n-API](api.md)** (`api`): The API that communicates with a single graph store and determines
    how detailed the response to a query should be from that graph.
- **Graph store** (`graph`): A third-party RDF store that stores Neurobagel-harmonized data to be queried. At the moment our recipe uses the free tier
    of [GraphDB](https://db-engines.com/en/system/GraphDB) for this.
- **Neurobagel federation/f-API** (`federation`): A special API that can federate over one or more
    Neurobagel nodes to provide a single point of access to multiple distributed databases.
    By default it will federate over all public nodes and any local nodes you specify.
- **[Neurobagel query tool](query_tool.md)** (`query_federation`): A web app that provides a graphical interface for users to query a
    federation API and view the results from one or more nodes. Because the query tool is a static app and is run locally
    in the user's browser, this service simply hosts the app.

Two additional, third-party services are part of production deployment recipes:

- **[NGINX reverse proxy](https://nginx.org/en/)** (`nginx-proxy`):
    A [containerized version](https://github.com/nginx-proxy/nginx-proxy)
    of the popular proxy server that lets you serve your Neurobagel services
    under custom URLs, handling routes automatically.
- **Automatic SSL certificate service** (`acme-companion`):
    A [containerized companion tool](https://github.com/nginx-proxy/acme-companion)
    for nginx that automatically provisions SSL certificates for the routes
    created by `nginx` so users can communicate with your services
    via encrypted HTTPS connections.

## Deployment profiles

Neurobagel offers different deployment profiles that allow you to launch
specific combinations of services (listed below), depending on your use case.

- [`node`](#node): Deploys an individual Neurobagel node.
    A Neurobagel node includes an internal graph database and a node API
    that handles all incoming queries and talks to the graph database.
    You can run several nodes on the same machine.
    - `api`
    - `graph`

- [`portal`](#portal): Deploys the federation engine and a connected web query interface.
    Use this profile only if you need to host your own federated query tool,
    e.g. to federate over nodes that are not in the
    [list of public Neurobagel nodes](https://github.com/neurobagel/menu/blob/main/node_directory/neurobagel_public_nodes.json).
       - `federation`
       - `query_federation`
- [`proxy`](#proxy-server): Deploys pre-configured, containerized
    reverse-proxy services that will automatically set up routes
    to your Neurobagel services under your desired URLs.

    ??? info "You can also use an existing proxy server"

        Our deployment instructions assume that there is no existing proxy server set up
        on the machine that will host your Neurobagel services.
        If you already have a proxy server setup,
        follow the slightly modified steps described in [deploying with an existing proxy server](production_deployment_with_own_proxy.md).

        In this case, you can ignore the `proxy` deployment recipe.

## Setting up a production deployment

### Requirements

In addition to the Docker and Docker Compose requirements outlined on the [Getting started page](getting_started.md#docker-and-docker-compose),
the Neurobagel configuration wizard for a production deployment requires **Python 3.10 or later** on the host machine.

### Install the Neurobagel configuration wizard

`configure-nb` is a tool that simplifies Neurobagel deployment configuration, and can be installed from [PyPI](https://pypi.org/project/configure-nb/) using `pip`.

Install the `configure-nb` package:

```bash
pip install configure-nb
```

### Common setup for all deployment profiles

!!! warning "Do these steps first for each deployment profile you set up"

    Each production deployment profile requires a fresh deployment recipe and begins with the same initial steps.
    Complete these steps before following the profile-specific setup instructions.

#### Clone the recipe repository

Make a fresh clone of the `recipes` repository in a location of your choice.

```bash
git clone https://github.com/neurobagel/recipes.git recipes
```

!!! tip "Consider changing `recipes` to a name you will recognize in the future"

Then navigate into this directory for the remaining steps.

```bash
cd recipes
```

### Proxy server

??? warning "Skip if you already have a reverse proxy server"

    If you already have a reverse proxy server set up and want to continue using
    it, **do not follow this section** and instead continue with our guide
    on [production deployment with an existing proxy server](production_deployment_with_own_proxy.md).
??? warning "Always launch the proxy server first"

    Our reverse proxy recipe is set up to automatically configure routes to the
    Neurobagel services you launch. In order to do that, the proxy server must
    already be running when you launch a new Neurobagel service.
    If you have already launched Neurobagel services
    (e.g. [node](#node) or [portal](#portal)),
    shut them down again,
    launch the proxy server, and then relaunch the services.

!!! info "Start from a [fresh deployment recipe](#common-setup-for-all-deployment-profiles)!"

To host your Neurobagel [node services](#deployable-services) under a custom URL
(e.g. `https://www.myfirstnode.org/query`) rather than a server IP address and port
(e.g. `http://192.168.0.1:3000`), we provide a recipe for you to easily set up an
[NGINX](https://nginx.org/en/docs/beginners_guide.html) reverse proxy
alongside your Neurobagel services.

Make sure that:

- you have access to the domain you want to host your services at,
so that you can create a DNS entry that points at the machine
that will host your Neurobagel services.
- your machine firewall allows incoming connections
on ports 80 (HTTP) and 443 (HTTPS).
[Both are necessary](https://letsencrypt.org/docs/integration-guide/#firewall-configuration)
to enable HTTPS connections.

Launch the proxy server using the corresponding deployment recipe:

```bash
docker compose -f docker-compose.proxy.yml up -d
```

You should now see the `nginx-proxy` and `acme-companion` services running:

```bash
docker ps
```

### Node

!!! note "Start from a [fresh deployment recipe](#common-setup-for-all-deployment-profiles)!"

??? info "Make sure the proxy service is already running"

    The default `portal` deployment recipe requires that you have already
    [deployed the proxy server](#proxy-server).

#### Create node INI config file

In your deployment recipe directory, create a file called [`nb_config.ini`](../glossary.md#neurobagel-configuration-file).
This file will store the environment variables used to configure the services in your deployment.

Here is an example minimal `nb_config.ini` for a **node** deployment:

```ini title="nb_config.ini"
[compose]
COMPOSE_PROFILES=node #(1)!

[service:graph]
LOCAL_GRAPH_DATA=./data

[service:node-api]
NB_RETURN_AGG=true
NB_MIN_CELL_SIZE=0
NB_NAPI_DOMAIN=mydomain.org
NB_NAPI_BASE_PATH=/node
```

1. `COMPOSE_PROFILES` must be set to `node` for a [node deployment](#deployment-profiles).

!!! warning "Do not wrap values in quotations (`''` or `""`) - they will be treated as literal characters"

!!! info
    For more details on all available environment variables,
    see the [Environment variable reference](maintaining.md#environment-variables-reference).

The following sections describe the node configuration options in more detail.

#### Set graph store credentials

!!! danger "This is a security relevant section!"

??? warning "Changing passwords after the first launch requires a hard reset"

    If you've previously launched a Neurobagel deployment (Docker Compose stack),
    you'll need to
    [reset your graph store](maintaining.md#resetting-your-graphdb-instance)
    for any changes you have made to user credentials to take effect.
    Any other configuration changes you've already made
    will be applied when you re-launch your node.

The graph store (GraphDB instance) in a Neurobagel node
is secured with password-based access and includes two users:
an `admin` superuser and a  regular database user.
The Neurobagel deployment recipes automatically creates both these users.

In the [`./secrets`](https://github.com/neurobagel/recipes/tree/main/secrets) subdirectory,
change the default passwords for these users:

- Replace the contents of `NB_GRAPH_ADMIN_PASSWORD.txt` to set the password for the `admin` superuser
- Replace the contents of `NB_GRAPH_PASSWORD.txt` to set the password for the graph database user

??? tip "Want to generate a random password in the terminal?"
    To generate a random password in the terminal, you can use:

    ```bash
    openssl rand -hex 16
    ```

(Optional) To change the directory where your password files are stored, use the `NB_GRAPH_SECRETS_PATH` variable:
```ini title="nb_config.ini" hl_lines="6"
[compose]
COMPOSE_PROFILES=node

[service:graph]
LOCAL_GRAPH_DATA=./data
NB_GRAPH_SECRETS_PATH=./secrets

[service:node-api]
NB_RETURN_AGG=true
NB_MIN_CELL_SIZE=0
NB_NAPI_DOMAIN=mydomain.org
NB_NAPI_BASE_PATH=/node
```

??? info "Graph store passwords are only for administrator use!"
    The `admin` user and graph database user credentials are intended solely for internal use by the deployment recipe scripts that automatically set up and update the graph store,
    or for a node administrator to interact directly with the graph store.
    These credentials also secure internal communication between your graph store and its node API,
    ensuring that node users cannot query your graph directly.
    GraphDB user credentials are not intended for use by a general node query user.

??? info "Passwords are handled as Docker secrets"

    The contents of `NB_GRAPH_ADMIN_PASSWORD.txt` and `NB_GRAPH_PASSWORD.txt` are passed to Neurobagel containers as [Docker secrets](https://docs.docker.com/reference/compose-file/secrets/).
    This ensures that your passwords are not exposed in the container logs or in the `docker-compose.yml` file.

    Do not share your password files with others.

#### Add data to the node

By default, the deployment recipe will automatically upload all JSONLD files found in [`./data`](https://github.com/neurobagel/recipes/tree/main/data)
inside your deployment recipe directory to the graph store.

To add the dataset JSONLD files for your node, either:

- place them in the `./data` subdirectory (replacing the example JSONLD file), **or**
- define a custom path to your JSONLD files using the variable `LOCAL_GRAPH_DATA`:

    ```ini title="nb_config.ini" hl_lines="5"
    [compose]
    COMPOSE_PROFILES=node

    [service:graph]
    LOCAL_GRAPH_DATA=./data

    [service:node-api]
    NB_RETURN_AGG=true
    NB_MIN_CELL_SIZE=0
    NB_NAPI_DOMAIN=mydomain.org
    NB_NAPI_BASE_PATH=/node
    ```

#### Set node response granularity

!!! danger "This is a security relevant section!"

Based on your data sharing requirements, set the following variables to control
the level of detail returned in query results from your node:

- `NB_RETURN_AGG`: whether to return aggregate counts only, instead of subject-level records
- `NB_MIN_CELL_SIZE`: minimum matching subject threshold for dataset visibility in queries

```ini title="nb_config.ini" hl_lines="8-9"
[compose]
COMPOSE_PROFILES=node

[service:graph]
LOCAL_GRAPH_DATA=./data

[service:node-api]
NB_RETURN_AGG=true
NB_MIN_CELL_SIZE=0
NB_NAPI_DOMAIN=mydomain.org
NB_NAPI_BASE_PATH=/node
```

#### Set node domain and subpath

Set `NB_NAPI_DOMAIN` to the domain name
(including any subdomain) you will use for your node API
(the web-accessible part of your node).

Optionally, set `NB_NAPI_BASE_PATH` to host your node API on a subpath of your domain.
This is useful when hosting multiple nodes or services on the same domain, because you can use a different subpath for each
(e.g. `mydomain.org/node1`, `mydomain.org/node2`, ...).

```ini title="nb_config.ini" hl_lines="10-11"
[compose]
COMPOSE_PROFILES=node

[service:graph]
LOCAL_GRAPH_DATA=./data

[service:node-api]
NB_RETURN_AGG=true
NB_MIN_CELL_SIZE=0
NB_NAPI_DOMAIN=mydomain.org
NB_NAPI_BASE_PATH=/node #(1)!
```

1. `NB_NAPI_BASE_PATH` is optional and can be omitted if you are not using a subpath.

!!! warning "Domain names must not include a protocol (`http://` or `https://`)"
!!! warning "Custom subpaths must include a leading slash `/`"

#### Generate node configuration

Run `configure-nb` to generate the runtime configuration file for your deployment
from the `nb_config.ini` file you created.

```bash
configure-nb
```

You should now have a `.env` file in your deployment recipe directory.

#### Launch node

Launch your node using Docker Compose.

```bash
docker compose -f docker-compose.prod.yml up -d
```

### Portal

!!! note "Start from a [fresh deployment recipe](#common-setup-for-all-deployment-profiles)!"

??? info "Make sure the proxy server is already running"

    The default `portal` deployment recipe requires that you have already
    [deployed the proxy server](#proxy-server).

#### Create portal INI config file

In your deployment recipe directory, create a file called [`nb_config.ini`](../glossary.md#neurobagel-configuration-file).
This file will store the environment variables used to configure the services in your deployment.

Here is an example minimal `nb_config.ini` for a **portal** deployment:

```ini title="nb_config.ini"
[compose]
COMPOSE_PROFILES=portal #(1)!

[node:1]
NAME=Parkinson's Disease Data - Site 1
API_URL=https://mydomain.org/site1

[node:2]
NAME=Parkinson's Disease Data - Site 2
API_URL=https://mydomain.org/site2

[service:federation-api]
NB_FAPI_DOMAIN=mydomain.org
NB_FAPI_BASE_PATH=/federate

[service:query]
NB_QUERY_DOMAIN=mydomain.org
NB_QUERY_APP_BASE_PATH=/
```

1. `COMPOSE_PROFILES` must be set to `portal` for a [portal deployment](#deployment-profiles).

!!! warning "Do not wrap values in quotations (`''` or `""`) - they will be treated as literal characters"

!!! info
    For more details on all available environment variables,
    see the [Environment variable reference](maintaining.md#environment-variables-reference).

The following sections describe the portal configuration options in more detail.

#### Set nodes to federate

```ini title="nb_config.ini" hl_lines="4-10"
[compose]
COMPOSE_PROFILES=portal

[node:1]
NAME=Parkinson's Disease Data - Site 1
API_URL=https://mydomain.org/site1

[node:2]
NAME=Parkinson's Disease Data - Site 2
API_URL=https://mydomain.org/site2

[service:federation-api]
NB_FAPI_DOMAIN=mydomain.org
NB_FAPI_BASE_PATH=/federate

[service:query]
NB_QUERY_DOMAIN=mydomain.org
NB_QUERY_APP_BASE_PATH=/query
```

A portal deployment federates queries across a custom set of nodes that you define.
Each node of interest is defined using a federation node configuration section following the format:

```ini
[node:<ID>]
NAME=<NODE DISPLAY NAME (SHOWN IN THE QUERY PORTAL)>
API_URL=<URL OF THE NODE API>
```

Federation node configuration section headers must start with the prefix `node:`.
`<ID>` is an arbitrary internal identifier used only to ensure section names are unique.
For simplicity, we recommend using numeric IDs such as `[node:1]`, `[node:2]`, etc.

!!! warning "`API_URL` must include the protocol (`http://` or `https://`)"

??? info "Public Neurobagel nodes do not need to be included"

    We maintain a list of publicly accessible Neurobagel nodes
    [here](https://github.com/neurobagel/menu/blob/main/node_directory/neurobagel_public_nodes.json).
    By default, every new f-API will look up this list
    on startup and include it in its internal list of nodes to
    federate over
    (this can be disabled by setting the variable [`NB_FEDERATE_REMOTE_PUBLIC_NODES`](maintaining.md#environment-variables-reference) in `nb_config.ini`).
    This means that you do not have to manually define these public nodes in `nb_config.ini`.

!!! danger "Do not include URLs of federation APIs"

    Make sure you do not include your own f-API in the list of nodes to
    federate over.
    This will cause an infinite request loop that will likely overload your service,
    as an f-API will be repeatedly making requests to itself.

#### Set portal domains and subpaths

Set `NB_FAPI_DOMAIN` and `NB_QUERY_DOMAIN` to the domain names you will use for your federation API and web query tool, respectively.

Optionally, set `NB_FAPI_BASE_PATH` and/or `NB_QUERY_APP_BASE_PATH` to host your federation API and/or
web query tool on a subpath of your domain.
This is useful when hosting multiple services on the same domain, because you can use a different subpath for each
(e.g. `mydomain.org/federate`, `mydomain.org/query`, ...).

```ini title="nb_config.ini" hl_lines="13-14 17-18"
[compose]
COMPOSE_PROFILES=portal

[node:1]
NAME=Parkinson's Disease Data - Site 1
API_URL=https://mydomain.org/site1

[node:2]
NAME=Parkinson's Disease Data - Site 2
API_URL=https://mydomain.org/site2

[service:federation-api]
NB_FAPI_DOMAIN=mydomain.org
NB_FAPI_BASE_PATH=/federate #(1)!

[service:query]
NB_QUERY_DOMAIN=mydomain.org
NB_QUERY_APP_BASE_PATH=/query #(2)!
```

1. `NB_FAPI_BASE_PATH` is optional and can be omitted if you are not using a subpath.
2. `NB_QUERY_APP_BASE_PATH` is optional and can be omitted if you are not using a subpath.

!!! warning "Domain names must not include a protocol (`http://` or `https://`)"

!!! warning "Custom subpaths must include a leading slash `/`"

#### Generate portal runtime config

Run `configure-nb` to generate the runtime configuration files for your deployment
from the `nb_config.ini` file you created.

```bash
configure-nb
```

You should now have two additional files in your deployment recipe directory: `.env` and `local_nb_nodes.json`.

#### Launch portal

Launch your portal using Docker Compose.

```bash
docker compose -f docker-compose.prod.yml up -d
```

## Making your node publicly discoverable

The public Neurobagel query tool ([https://query.neurobagel.org](https://query.neurobagel.org))
provides query federation to all publicly accessible Neurobagel nodes.

To make your node queryable at [https://query.neurobagel.org](https://query.neurobagel.org), it simply needs to be added to our [public federation index](https://github.com/neurobagel/menu/blob/main/node_directory/neurobagel_public_nodes.json) on GitHub.

### If you have a GitHub Account

1. [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) the [neurobagel/menu](https://github.com/neurobagel/menu) repository.

2. Add your node name and node API URL to the [public federation index JSON file](https://github.com/neurobagel/menu/blob/main/node_directory/neurobagel_public_nodes.json), using the following format:

    ```json
    {
        "NodeName": "NAME OF YOUR NODE",
        "ApiURL": "https://URL-OF-YOUR-NODE-API"
    }
    ```

    `NodeName` defines the display name of your node as it will appear the Neurobagel query tool.

3. [Open a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) in the neurobagel/menu repository.

### If you do not have a GitHub Account

Join the [Neurobagel Discord server](https://discord.gg/BEXXgt3hXk) and message `@neurobagel/dev` with your node information, so that a maintainer can add your node to the public federation index.
