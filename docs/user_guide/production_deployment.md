The [getting started](getting_started.md) section
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

## Setting up a production deployment

### Deployment profiles

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
    e.g. to federate over nodes that are not in the list of public Neurobagel nodes.
       - `federation`
       - `query_federation`
- [`proxy`](#proxy-server): Deploys pre-configured, containerized
    reverse-proxy services that will automatically set up routes
    to your Neurobagel services under your desired URLs.

    ??? info "You can also use an existing proxy server"

        Our deployment instructions assume that there is no existing proxy server set up
        on the machine that will host your Neurobagel services.
        If you already have a proxy server setup, 
        follow the slightly modified steps described in [deploying with an existing proxy server](#deploying-with-an-existing-proxy-server).
        
        In this case, you can ignore the `proxy` deployment recipe.

### Common setup for all deployment profiles

!!! warning "Do these steps first for each deployment profile you set up"

    Each production deployment profile requires a fresh deployment recipe and begins with the same initial steps.
    Complete these steps before following the profile-specific setup instructions.

#### Clone the recipe repository

Make a fresh clone of the `recipes` repository in a location of your choice.

```bash
git clone https://github.com/neurobagel/recipes.git recipes
```

Change `my-new-deployment` to a directory name you will recognize in the future.
Then navigate into this directory for the remaining steps.

```bash
cd recipes
```

#### Copy the template configuration files

The recipe repository includes templates of files for configuring your deployment: `.env` and  
`local_nb_nodes.json`. Copy and rename these templates, but do not edit
the templates themselves.

```bash
cp template.env .env
cp local_nb_nodes.template.json local_nb_nodes.json
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

#### Set graph store credentials

!!! danger "This is a security relevant section!"

The graph store (GraphDB instance) in a Neurobagel node
is secured with password-based access and includes two users:
an `admin` superuser and a regular database user,
both of which are automatically configured by the Neurobagel deployment recipe.
Passwords for both users are defined via files in the `./secrets` directory
of the recipes repository, while the regular database username is set
through an environment variable in `.env` file.

??? warning "Changing user credentials after the first launch requires a hard reset"

    If you've previously launched a Neurobagel deployment (Docker Compose stack),
    you'll need to
    [reset your graph store](maintaining.md#resetting-your-graphdb-instance)
    for any changes you have made to user credentials to take effect. 
    Any other configuration changes you've already made
    will be applied when you re-launch your node.

1. In your `.env`, **set a custom username and database name for your graph store** by editing the following variables:
    - `NB_GRAPH_USERNAME`
    - `NB_GRAPH_DB`

2. In the ([`./secrets`](https://github.com/neurobagel/recipes/tree/main/secrets) directory, **change the default passwords** by replacing the contents of the file `NB_GRAPH_ADMIN_PASSWORD.txt` for the `admin` superuser, and the file `NB_GRAPH_PASSWORD.txt` for the graph database user (corresponding to `NB_GRAPH_USERNAME`).
    - To generate a random password in the terminal, you can use:

      ```bash
      openssl rand -hex 16
      ```

    - (Optional) You can change the directory where your password files are stored by editing the `NB_GRAPH_SECRETS_PATH` variable in `.env`.

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
  
#### Set node response granularity

!!! danger "This is a security relevant section!"

Review and change as needed the following variables in `.env`
based on your data sharing requirements:

- `NB_RETURN_AGG`: whether to return aggregate counts only, instead of subject-level records
- `NB_MIN_CELL_SIZE`: minimum matching subject threshold for dataset visibility in queries

For more details on all available environment variables,
check the [Environment variable reference](maintaining.md#environment-variables-reference)

#### Set node domain

In your `.env` file,
uncomment the variable `NB_NAPI_DOMAIN` and set it to the domain
(including any subdomain) that you want to use for your node API
(the web-accessible part of your node).

```bash
NB_NAPI_DOMAIN=node.mydomain.org
```

!!! warning "Do not include the protocol (`http://` or `https://`) in the domain name"

#### Set node deployment profile

In your `.env` file, ensure that `COMPOSE_PROFILES` is set to
the [`node` profile](#deployment-profiles). This is the default value.

```bash
COMPOSE_PROFILES=node
```

#### Set node subdirectory path

!!! info "This is an optional step"

To host your node API on a subdirectory of your domain (e.g. `mydomain.org/node`),
uncomment and set `NB_NAPI_BASE_PATH`
to the desired subdirectory path in the `.env` file.

```bash
NB_NAPI_BASE_PATH="/node"
```

This is useful if you want to serve several nodes (or services)  
on the same domain, because you can use a different subdirectory for each  
(e.g. `myinstitute.org/node1`, `myinstitute.org/node2`, ...).

#### Launch node

Save the changes to your `.env` file and launch your node:

```bash
docker compose -f docker-compose.prod.yml up -d
```

??? info "Make sure the proxy service is already running"

    The default `node` deployment recipe requires that you have already
    [deployed the proxy server](#proxy-server).

### Portal

!!! note "Start from a [fresh deployment recipe](#common-setup-for-all-deployment-profiles)!"

To host your own query portal that federates over a set of nodes,
use your `local_nb_nodes.json` to configure the nodes of interest.

Each node to be federated over is defined using a dictionary with two required keys:

- `NodeName`: Display name of the node, which will be shown in the query portal
- `ApiURL`: URL of the **node API** for the node

`local_nb_nodes.json`:

    [
        {
            "NodeName": "Parkinson's Disease Data - Site 1",
            "ApiURL": "https://mydomain.org/site1"
        },
        {
            "NodeName": "Parkinson's Disease Data - Site 2",
            "ApiURL": "https://mydomain.org/site2"
        }
    ]

!!! warning "`ApiURL` must include the protocol (`http://` or `https://`)"

??? info "Public Neurobagel nodes do not need to be included"

        We maintain a list of publicly accessible Neurobagel nodes 
    [here](https://github.com/neurobagel/menu/blob/main/node_directory/neurobagel_public_nodes.json).
    By default, every new f-API will look up this list
    on startup and include it in its internal list of nodes to
    federate over (this can be disabled using the environment variable [`NB_FEDERATE_REMOTE_PUBLIC_NODES`](#environment-variables-reference)).
    This means that **you do not have to manually add these public nodes** to your `local_nb_nodes.json` file.

    federate over (this can be disabled using the environment variable [`NB_FEDERATE_REMOTE_PUBLIC_NODES`](maintaining.md#environment-variables-reference)).

    This will cause an infinite request loop that will likely overload your service, as an f-API will be repeatedly making requests to itself.

#### Set portal domains

Uncomment and set the domain name for both
the web query tool and the federation API in your `.env` file.

- `NB_QUERY_DOMAIN` variable for the query tool
- `NB_FAPI_DOMAIN` variable for the federation API

!!! warning "Do not include the protocol (`http://` or `https://`) in the domain name"

#### Set portal subdirectory path

!!! info "This is an optional step"

You may want to have one or several of your portal services
respond on a subdirectory of your domain (e.g. `myinstitute.org/federate`).
This is especially useful if you want to serve several services
on the same domain, because you can set a different subdirectory for each
(e.g. `myinstitute.org/federate`, `myinstitute.org/query`, ...).

To host one or more of your portal services on a subdirectory
of your domain (e.g. `mydomain.org/federate`),
uncomment and set the following variable(s) to the desired
subdirectory path(s) in the `.env` file:

- `NB_QUERY_APP_BASE_PATH` for the query tool
- `NB_FAPI_BASE_PATH` for the federation API

This is useful if you want to serve the services on the same domain,
because you can use a different subdirectory for each  
(e.g. `mydomain.org/federate`, `mydomain.org/query`).

#### Set `portal` deployment profile

In your .env file, set `COMPOSE_PROFILES` to
the [`portal` profile](#deployment-profiles).

```bash
COMPOSE_PROFILES=portal
```

#### Launch portal

```bash
docker compose -f docker-compose.prod.yml up -d
```
