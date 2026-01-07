The [getting started](getting_started.md) section is designed to be easily deployed
with a single command and without deep configuration to make local testing easier.
For a production deployment intended for external users,
you will want to customize the settings to fit your specific needs.

To help you with this,
our [`recipes` repository](https://github.com/neurobagel/recipes)
includes dedicated production deployment templates that should
cover the most common scenarios.

!!! info "Start with a fresh template for each deployment"

    Make sure to clone a fresh copy of the 
    [`recipes` repository](https://github.com/neurobagel/recipes) for each
    deployment you want to make. 
    
    For example if you are hosting several [nodes](#node),
    or if you launch the [containerized proxy server](#proxy) and a [single node](#node),
    make one local clone of the `recipes` repo for each of them.
    This will make it easier to update and maintain each deployment.

## Deployable services and profiles

The production deployment templates group services into
[docker compose profiles](https://docs.docker.com/compose/how-tos/profiles/)
that allow you to launch related services together.

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

Two additional, third-party services are part of production deployment templates:

- **[NGINX reverse proxy](https://nginx.org/en/)** (`nginx`):
    A [containerized version](https://github.com/nginx-proxy/nginx-proxy)
    of the popular proxy server that automatically create routes to
    your Neurobagel services.
- **Automatic SSL certificate service** (`nginx-acme`):
    A [containerized companion tool](https://github.com/nginx-proxy/acme-companion)
    for nginx that automatically provisions SSL certificates for the routes
    created by `nginx` so users can communicate with your services
    via encrypted HTTPS connections.

### Default ports of services

??? warning "Don't publicly expose service ports on a production server"

    We're providing the default ports as a reference for local deployment, testing, and for scenarios
    where you do not want to use the
    [provided reverse proxy deployment recipes](#behind-a-reverse-proxy).
    
    Where possible, we **strongly recommend** that you avoid opening service ports to a public network
    and instead use our
    [reverse proxy deployment recipe](#behind-a-reverse-proxy).

Neurobagel node services run inside Docker containers. Each service listens on an *internal port* within its container and
exposes a *host port* that makes it accessible from the host machine. Below, we list the default *host ports* for each service
when running in a fresh deployment following our [getting started guide](getting_started.md),
along with the [environment variables](#environment-variables) that can be used to configure them.

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

### Profiles

Neurobagel offers different deployment profiles that allow you to spin up
specific combinations of services (listed below), depending on your use case.

- [`proxy server`](#proxy-server): Deploys pre-configured, containerized
    reverse-proxy services that will automatically create the desired routes
    to your Neurobagel services.

    !!! info "You can also use an existing proxy server"

        Our deployment templates assume that you do not yet have a proxy server set up
        on the machine where you will be hosting your Neurobagel services.
        If you do already have a proxy server setup using a different method,
        you can adjust the default deployment with some minor changes documented in the
        section on [deploying with a bare metal proxy server](#own-proxy).
        
        In this case, you can ignore the `proxy server` deployment template.

- [`node`](#node): Deploys an individual Neurobagel node. You can run several
    Neurobagel nodes on the same machine.
       - `api`
       - `graph`

- [`portal`](#portal): Deploys the federation engine and a connected web query interface.
    Chose this profile if you want to host your own federated query e.g. for a list of nodes that
    are not included in the list of publicly accessible Neurobagel nodes.
       - `federation`
       - `query_tool`

### Preparations

!!! info "Always do these steps first"

    All three production deployment profiles begin with the same initial steps.
    Make sure to complete them before following the profile specific setup instructions:

1. Make a fresh clone of the recipe repository in a location of your choice.

    ```bash
    git clone https://github.com/neurobagel/recipes.git my-new-deployment
    ```

    Change `my-new-deployment` to a directory name you will recognize in the future.

    ```bash
    cd my-new-deployment
    ```

2. Copy and edit the `template.env` file

    ```bash
    cp template.env .env
    ```

### Proxy server

To make your Neurobagel node services (node API, query tool, etc.) accessible via custom URLs
(e.g. `https://www.myfirstnode.org/query`) rather than a server IP address and port
(e.g. `http://192.168.0.1:3000`) as shown in in the [getting started guide](getting_started.md),
you will need to set up a reverse proxy such as [NGINX](https://nginx.org/en/docs/beginners_guide.html) or
[Caddy](https://caddyserver.com/docs/quick-starts/reverse-proxy).
This will route incoming requests for custom URLs to the Neurobagel services deployed on your server.

!!! info "Before you begin"

    Make sure that:

    - you have access to the domain you want to host your services at,
    so that you can create a DNS entry that points at the webserver
    that will host your Neurobagel services.
    - your web server firewall allows incoming connections
    on ports 80 (HTTP) and 443 (HTTPS).
    [Both are necessary](https://letsencrypt.org/docs/integration-guide/#firewall-configuration)
    to complete the SSL certificate challenge and offer HTTPS connections.

1. [Set up a fresh clone of the recipe repo](#preparations)

2. open the `.env` file in you favourite text editor
    and uncomment the following line:

    ```bash
    # Uncomment to manually set the name of the proxy docker network
    # PROXY_NETWORK_NAME=NB_proxynet
    ```

    If you change the name of the proxy network, make sure to remember it
    as you will have to use the same name in your other deployments so that
    your deployed services and the proxy server can see each other.

3. Launch the proxy server from the corresponding deployment template:
    `docker-compose.proxy.yml`

    ```bash
    docker compose -f docker-compose.proxy.yml up -d
    ```

You should now see the `nginx` and `nginx-acme` services running:

```bash
docker ps
```

### Node

Begin by [setting up a new clone of the recipe repo](#preparations) for each node.

#### Change security relevant variables

The graph store (GraphDB instance) in a Neurobagel node is secured with password-based access and includes two users: an `admin` superuser and a regular database user, both of which are automatically configured by the Neurobagel deployment recipe.
Passwords for both users are defined via files in the `./secrets` directory of the recipes repository, while the regular database username is set through an environment variable in `.env` file.

??? warning "Changing user names and secrets after the first launch requires a hard reset"

    If you've previously launched a Neurobagel Docker Compose stack following the [Getting started](getting_started.md#the-neurobagel-node-deployment-recipe) instructions,
    you'll need to [reset your graph store](maintaining.md#resetting-your-graphdb-instance) for any changes you have made to user credentials to take effect (steps 1-2 above). 
    Don't worry, any other configuration changes you've already made will be applied when you re-launch your node.

For security and best practice purposes, we recommend changing the following values from their defaults if you are using a deployment profile that includes a graph store:

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
  
3. **Review and change as needed** the following variables in `.env` based on your data sharing requirements:
    - `NB_RETURN_AGG`
    - `NB_MIN_CELL_SIZE`
    !!! info
        These variables are modifiable after node initialization; you can [change their values at any time](maintaining.md#restarting-services-after-an-update).

#### Configuring the node for a production deployment

1. Make sure you have [set up a fresh clone of the recipe repo](#preparations)
    for your node.

2. Set the domain name of your node:

    In the `.env` file under the `CONFIGURATION FOR n-API` section,
    uncomment the value of `NB_NAPI_DOMAIN` and set it to the domain
    (including any subdomain) that you want to use for your node.

    ```bash
    NB_NAPI_DOMAIN=api.mydomain.org
    ```

    !!! warning "Do not include `https://` in the domain name"

3. Set the launch profile to `node`:

    Set the `COMPOSE_PROFILES` variable in the `.env` file to
    [the `node` profile](#profiles). This is the default value.

    ```bash
    COMPOSE_PROFILES=node
    ```

4. **Optional**: Set the URL subdirectory for your node:

    You may want to have your node API respond on a subdirectory of your domain (e.g. `myinstitute.org/node-api`).
    This is especially useful if you want to serve several nodes (or services)
    on the same domain, because you can set a different subdirectory for each
    (e.g. `myinstitute.org/node1`, `myinstitute.org/node2`, ...).

    To do so, uncomment and set the following line in the `.env` file:

    ```bash
    NB_NAPI_BASE_PATH="/node-api"
    ```

5. Save the changes in your `.env` file
6. Launch your node:

    ```bash
    docker compose -f docker-compose.prod.yml up -d
    ```

### Portal

Begin by [setting up a new clone of the recipe repo](#preparations).

#### Configuring local node names and URLs for federation

When using a deployment profile that provides federation (i.e., includes the federation API), 
you can configure the URLs and display names of the **node APIs** of any local nodes you wish to federate over in the file `local_nb_nodes.json`. 
This file is read by the f-API.

    !!! info
        By default, the `portal` profile will also federate
        over all publicly accessible Neurobagel nodes,
        although this behaviour can be disabled in the f-API
        using the environment variable [`NB_FEDERATE_REMOTE_PUBLIC_NODES`](#environment-variables).

        If you only want to federate over a single local node and all public Neurobagel nodes,
        we recommend using the `full_stack` profile to set up your node and federation in one step.
        If you choose to use the `local_federation` profile, 
        you will have to [manually configure your `local_nb_nodes.json` file](#configuring-local-node-names-and-urls-for-federation).

Each node to be federated over is defined using a dictionary with two key-value pairs:
```json
{
  "NodeName": "<DISPLAY NAME OF NODE>",
  "ApiURL": "<URL OF NODE API>"
}
```

!!! warning "`ApiURL` must include the protocol (`http://` or `https://`)"

If you are only running a single node, or only want to federate across your local node and the public Neurobagel nodes, 
you **do not need** to modify the default `ApiURL` in `local_nb_nodes.json`.
However, you may want to customize your node's `NodeName`.

Notes:

- `NodeName` can be any string, and determines how the node appears in the node selection dropdown in the query tool
- To add more local nodes to federate over, simply add more dictionaries to `local_nb_nodes.json`, and ensure the dictionaries are wrapped in a list `[]` (see example below)

!!! Info "Nodes that do not need to be manually configured"
    We maintain a list of publicly accessible Neurobagel nodes 
    [here](https://github.com/neurobagel/menu/blob/main/node_directory/neurobagel_public_nodes.json).
    By default, every new f-API will look up this list
    on startup and include it in its internal list of nodes to
    federate over (this can be disabled using the environment variable [`NB_FEDERATE_REMOTE_PUBLIC_NODES`](#environment-variables)).
    This means that **you do not have to manually add these public nodes** to your `local_nb_nodes.json` file.

**Example:** Assume there are two local nodes already running on different servers of your institutional network:

- a node named `"My Institute"` running on your local computer (`localhost`), on port `8000` 
- a node named `"Node Recruitment"` running on a different computer with the local IP `192.168.0.1`, listening on the default HTTP port `80` 

To set up federation across both nodes, you would configure `local_nb_nodes.json` as follows:
``` {.json title="local_nb_nodes.json"}
[
  {
    "NodeName": "My Institute",
    "ApiURL": "https://neurobagel.myinstitute.edu",
  },
  {
    "NodeName": "Node Recruitment",
    "ApiURL": "http://192.168.0.1"
  }
]
```

??? warning "Do not use `localhost`/`127.0.0.1` in `local_nb_nodes.json`"

    Even if the local node API(s) you are federating over are running 
    on the same host machine as your federation API, 
    you cannot use `localhost` for the `ApiURL` and must instead provide a network-accessible URL, IP address, or container name.
    For an example, see the configuration for the node called `"My Institute"` above.

??? warning "Be careful to not use your federation API's own address for `ApiURL`!"

    This will cause an infinite request loop that will likely overload your service, as an f-API will be repeatedly making requests to itself.

### Production deployment

!!! note "The following section is intended for system administrators"

This section explains how you make your Neurobagel node services
(node API, query tool, etc.) accessible on a specific
[domain name](https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_domain_name)
(e.g. `https://www.myfirstnode.org/query`) rather than your server IP address and port
(e.g. `http://192.168.0.1:3000`) as shown in in the [getting started guide](getting_started.md).

The [Neurobagel `recipes` repository](https://github.com/neurobagel/recipes/)
includes two docker compose files for production:

- `docker-compose.proxy.yaml`: deploys a reverse proxy server and provisions SSL certificates for
your Neurobagel services to be accessible at a custom domain name and via HTTPS.
- `docker-compose.prod.yaml`: deploys Neurobagel services configured to work with the proxy server

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