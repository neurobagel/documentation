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

### Services

The Neurobagel Docker Compose recipe includes several services
and coordinates them to work together:

(In parentheses are the names of services within the Docker Compose stack)

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

### Default ports of services

??? warning "Don't publicly expose service ports on a production server"

    We're providing the default ports as a reference for local deployment, testing, and for scenarios
    where you do not want to use the
    [provided reverse proxy deployment recipes](#proxy-server).
    
    Where possible, we **strongly recommend** that you avoid opening service ports to a public network
    and instead use our
    [reverse proxy deployment recipe](#proxy-server).

Neurobagel node services run inside Docker containers. Each service listens on an *internal port* within its container and
exposes a *host port* that makes it accessible from the host machine. Below, we list the default *host ports* for each service
when running in a fresh deployment,
along with the [environment variables](#environment-variables-reference) that can be used to configure them.

- `api` (the node API)
    - environment variable: `NB_NAPI_PORT_HOST`
    - default host port: `8000`
- `federation` (the federation API)
    - environment variable: `NB_FAPI_PORT_HOST`
    - default host port: `8080`
- `query_tool` (the graphical query web interface)
    - environment variable: `NB_QUERY_PORT_HOST`
    - default host port: `3000`
- `graph` (the internal graph database)
    - environment variable: `NB_GRAPH_PORT_HOST`
    - default host port: `7200`

## Production deployment

### Deployment profiles

Neurobagel offers different deployment profiles that allow you to launch
specific combinations of services (listed below), depending on your use case.

- [`proxy server`](#proxy-server): Deploys pre-configured, containerized
    reverse-proxy services that will automatically set up routes
    to your Neurobagel services under your desired URLs.

    ??? info "You can also use an existing proxy server"

        Our deployment instructions assume that there is no existing proxy server set up
        on the machine that will host your Neurobagel services.
        If you already have a proxy server setup, 
        follow the slightly modified steps described in [deploying with an existing proxy server](#deploying-with-an-existing-proxy-server).
        
        In this case, you can ignore the `proxy` deployment recipe.
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

### Common setup for all deployment profiles

!!! info "Do these steps first for each deployment profile you set up"

    Each production deployment profile requires a fresh deployment recipe and begins with the same initial steps.
    Complete these steps before following the profile-specific setup instructions.

#### Clone the recipe repository

Make a fresh clone of the `recipes` repository in a location of your choice.

```bash
git clone https://github.com/neurobagel/recipes.git my-new-deployment
```

Change `my-new-deployment` to a directory name you will recognize in the future.
Then navigate into this directory for the remaining steps.

```bash
cd my-new-deployment
```

#### Copy the template files

The recipe repository comes with templates of the `.env` and
`local_nb_nodes.json` files. Copy and rename these templates, but do not edit
the templates themselves.

```bash
cp template.env .env
cp local_nb_nodes.template.json local_nb_nodes.json
```

### Proxy server

To make your Neurobagel node services (node API, query tool, etc.) accessible via custom URLs
(e.g. `https://www.myfirstnode.org/query`) rather than a server IP address and port
(e.g. `http://192.168.0.1:3000`) as shown in in the [getting started guide](getting_started.md),
you will need to set up a reverse proxy such as [NGINX](https://nginx.org/en/docs/beginners_guide.html) or
[Caddy](https://caddyserver.com/docs/quick-starts/reverse-proxy).
(e.g. `http://192.168.0.1:3000`),
Neurobagel provides a recipe for you to easily set up an [NGINX](https://nginx.org/en/docs/beginners_guide.html) reverse proxy alongside your Neurobagel services.

    Make sure that:

    - you have access to the domain you want to host your services at,
    so that you can create a DNS entry that points at the webserver
    that will host your Neurobagel services.
    - your web server firewall allows incoming connections
    on ports 80 (HTTP) and 443 (HTTPS).
    [Both are necessary](https://letsencrypt.org/docs/integration-guide/#firewall-configuration)
    to complete the SSL certificate challenge and offer HTTPS connections.

#### Set proxy network name

!!! note "Start from a [fresh setup](#common-setup-for-all-deployment-profiles)!"

Open the `.env` file in you favourite text editor and uncomment the following line:

```bash
# Uncomment to manually set the name of the proxy docker network
# PROXY_NETWORK_NAME=NB_proxynet
```

If you change the name of the proxy network, make sure to remember it
as you will have to use the same name in your other deployments so that
your deployed services and the proxy server can see each other.

#### Launch the proxy server

Launch the proxy server using the corresponding deployment recipe:

```bash
docker compose -f docker-compose.proxy.yml up -d
```

You should now see the `nginx` and `nginx-acme` services running:

```bash
docker ps
```

### Node

!!! note "Start from a [fresh setup](#common-setup-for-all-deployment-profiles)!"

#### Set graph username and secrets

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

    ??? info "Graph store passwords are not meant for node users!"
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
check the [Environment variable reference](#environment-variables-reference)

#### Set node proxy network

In the `.env` file uncomment the following line
and set it to the name of [your proxy network](#set-proxy-network-name):

```bash
# Uncomment to manually set the name of the proxy docker network
# PROXY_NETWORK_NAME=NB_proxynet
```

??? note "Make sure to use the same proxy network name"

    The `PROXY_NETWORK_NAME` `.env` variable must be set to exactly the same
    name for all services that connect to your [proxy server](#proxy-server).
    This is also why you have to launch the proxy server first.

    You can use
    [`docker network ls`](https://docs.docker.com/reference/cli/docker/network/ls/)
    and 
    [`docker network inspect <network_name>`](https://docs.docker.com/reference/cli/docker/network/inspect/)
    to review your docker networks.

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

Set the `COMPOSE_PROFILES` variable in the `.env` file to
[the `node` profile](#deployment-profiles). This is the default value.

```bash
COMPOSE_PROFILES=node
```

#### Set node subdirectory path

!!! info "This is an optional step"

You may want to have your node API respond on a subdirectory of your domain (e.g. `myinstitute.org/node-api`).
This is especially useful if you want to serve several nodes (or services)
on the same domain, because you can set a different subdirectory for each
(e.g. `myinstitute.org/node1`, `myinstitute.org/node2`, ...).

To do so, uncomment and set the following line in the `.env` file:

```bash
NB_NAPI_BASE_PATH="/node-api"
```

#### Launch node

Save the changes to your `.env` file and launch your node:

```bash
docker compose -f docker-compose.prod.yml up -d
```

??? info "Make sure the proxy service is already running"

    The default `node` deployment recipe requires that you have already
    [deployed the proxy server](#proxy-server).

### Portal

!!! note "Start from a [fresh setup](#common-setup-for-all-deployment-profiles)!"

#### Set nodes to federate over

You configure the URLs and display names of the **node APIs** of any
nodes you want your portal to federate over
by editing the `local_nb_nodes.json` file.

Each node to be federated over is defined using a dictionary with two key-value pairs:

```json
{
"NodeName": "<DISPLAY NAME OF NODE>",
"ApiURL": "<URL OF NODE API>"
}
```


!!! warning "`ApiURL` must include the protocol (`http://` or `https://`)"

??? info "Public Neurobagel nodes do not need to be included"

        We maintain a list of publicly accessible Neurobagel nodes 
    [here](https://github.com/neurobagel/menu/blob/main/node_directory/neurobagel_public_nodes.json).
    By default, every new f-API will look up this list
    on startup and include it in its internal list of nodes to
    federate over (this can be disabled using the environment variable [`NB_FEDERATE_REMOTE_PUBLIC_NODES`](#environment-variables-reference)).
    This means that **you do not have to manually add these public nodes** to your `local_nb_nodes.json` file.

??? warning "Do not use `localhost`/`127.0.0.1` in `local_nb_nodes.json`"

    Even if the local node API(s) you are federating over are running 
    on the same host machine as your federation API, 
    you cannot use `localhost` for the `ApiURL` and must instead provide a network-accessible URL, IP address, or container name.
    For an example, see the configuration for the node called `"My Institute"` above.

??? failure "Be careful to not use your federation API's own address for `ApiURL`!"

    This will cause an infinite request loop that will likely overload your service, as an f-API will be repeatedly making requests to itself.

#### Set portal proxy network

In the `.env` file uncomment the following line
and set it to the name of [your proxy network](#set-proxy-network-name):

```bash
# Uncomment to manually set the name of the proxy docker network
# PROXY_NETWORK_NAME=NB_proxynet
```

??? note "Make sure to use the same proxy network name"

    The `PROXY_NETWORK_NAME` `.env` variable must be set to exactly the same
    name for all services that connect to your [proxy server](#proxy-server).
    This is also why you have to launch the proxy server first.

    You can use
    [`docker network ls`](https://docs.docker.com/reference/cli/docker/network/ls/)
    and 
    [`docker network inspect <network_name>`](https://docs.docker.com/reference/cli/docker/network/inspect/)
    to review your docker networks.

#### Set portal domain

If you want to serve both the web query tool and the federation API
service under the same domain, you only need uncomment and set the
`NB_DEPLOY_DOMAIN` variable in the `.env` file:

```bash
NB_DEPLOY_DOMAIN="mydomain.org"
```

You can **optionally** override this value for each service by setting
a different domain in the

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

To do so, uncomment and set the corresponding variable in the `.env` file:

- `NB_QUERY_APP_BASE_PATH` for the query tool
- `NB_FAPI_BASE_PATH` for the federation API

#### Set portal deployment profile

Set the `COMPOSE_PROFILES` variable in the `.env` file to
[the `portal` profile](#deployment-profiles).

```bash
COMPOSE_PROFILES=portal
```

#### Launch portal

```bash
docker compose -f docker-compose.prod.yml up -d
```

## Deploying with an existing proxy server

If you already have a proxy server setup on your machine
and prefer to keep using it, you need to make a few adjustments to the
standard deployment recipes described above.

!!! warning "Do not follow this section if you are using Neurobagel's [containerized proxy server](#proxy-server)"

    If you are unfamiliar with managing and
    maintaining a bare-metal reverse proxy, you should use the
    [containerized proxy server](#proxy-server) provided with Neurobagel deployment recipes instead.
    
    We document how to run Neurobagel with an existing reverse proxy to help
    facilitate integration into established server setups. This type of deployment
    needs a good deal more manual configuration and maintenance.

!!! warning **Do not** launch the [`proxy` deployment profile](#proxy-server)"

    If you want to use your existing reverse proxy setup,
    make sure to not launch the [`proxy` deployment template](#proxy-server)
    provided by Neurobagel, or shut it down if you have already launched it.

### Follow the default setup

Deploying with an existing proxy server is very similar to using the default
deployment templates and requires only minimal changes. Begin by following
the default setup instructions for your [desired deployment profile](#deployment-profiles):

- For a `node` deployment follow the [node setup](#node)
- For a `portal` deployment follow the [portal setup](#portal)

!!! note "Do not launch the default deployment template"

    Skip the launch step of the default deployment instructions. Deploying
    behind an existing proxy server requires a different docker compose file.
    Trying to launch a default deployment template without the
    [default proxy service](#proxy-server) running will most likely fail.

### Set service host ports

??? info "Differences from the default deployment recipe"

    Unlike the default production Docker Compose file the deployment recipe for an
    existing proxy

    - **does not** expect an existing proxy Docker network to connect with
    - **does** export the service ports to the host machine,
        so you can configure your existing proxy server
        to reach each service on their port at the loopback address (i.e. `localhost`).

Neurobagel services have [default ports](#default-ports-of-services)
that they will try to bind to on the host. In most cases, you will want to
change these ports to avoid conflicts with existing services. To do so,
open then `.env` file and uncomment and set `NB_<XYZ>_PORT_HOST` variables
for your services. Refer to the [default ports](#default-ports-of-services)
for a list of the variable names.

### Configure your existing reverse proxy

You must manually configure the routing rules in your reverse proxy
and provision the necessary SSL certificates for HTTPS. That means,
for each service you deploy, you must:

- ensure that your reverse proxy is correctly configured to route incoming
    request to this service
- obtain, store, and update SSL certificates for each domain you use to host
    your services.

Please refer to the documentation of your existing reverse proxy server on
how to do this.

### Launch services behind an existing proxy

Ensure that you have correctly followed the setup instructions for your desired
[deployment profile](#deployment-profiles). Then launch your services using the
`docker-compose.noproxy.prod.yml` compose file:

```bash
docker compose -f docker-compose.noproxy.prod.yml up -d
```

## Environment variables reference

Below are all the possible Neurobagel environment variables that can be set in `.env`.

{{ read_table('./repos/recipes/docs/neurobagel_environment_variables.tsv') }}

??? warning "Ensure that shell variables do not clash with `.env` file"

    If the shell you run `docker compose` from already has any 
    shell variable of the same name set, 
    the shell variable will take precedence over the configuration
    of `.env`!
    In this case, make sure to `unset` the local variable first.

    For more information, see [Docker's environment variable precedence](https://docs.docker.com/compose/environment-variables/envvars-precedence/).

!!! tip
    Double check that any environment variables you have customized in `.env` are resolved with your expected values using the command `docker compose config`.