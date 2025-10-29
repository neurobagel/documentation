Neurobagel is designed to be easily deployed with a single command without deep configuration.
In many cases however, you will want to customize your deployment to fit your needs.

If you already have a running Neurobagel node, 
after making any configuration changes 
(including changing the data you want to be available in the graph database), 
follow the instructions to [restart your services](maintaining.md#restarting-services-after-an-update) 
for the changes to take effect.

## Deployment

### Available services
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

### Available profiles
Neurobagel offers different deployment profiles that allow you to spin up specific combinations of services (listed below), depending on your use case.

1. `full_stack`: Best profile to get started with Neurobagel. 
    It includes all services you need to run a local Neurobagel node and have the ability to query public nodes, along with a graphical query tool.
       - `api`
       - `graph`
       - `federation`
       - `query_tool`

    !!! info
        This is the **default profile** if you don't specify one.
    
        By default, this profile will also federate over all publicly accessible Neurobagel nodes, although this behaviour can be disabled in the f-API using the environment variable [`NB_FEDERATE_REMOTE_PUBLIC_NODES`](#environment-variables).

2. `local_node`: Best profile if you want to run a standalone Neurobagel node
    but rely on a separate deployment for providing federation and a graphical query tool (such as Neurobagel's own hosted public instances).
       - `api`
       - `graph`

3. `local_federation`: Best profile if you already have multiple standalone (local or non-publicly-accessible) Neurobagel node
    deployments running and you now want to provide federation over them.  
       - `federation`
       - `query_tool`
    !!! info
        If you only want to federate over a single local node and all public Neurobagel nodes,
        we recommend using the `full_stack` profile to set up your node and federation in one step.
        If you choose to use the `local_federation` profile, 
        you will have to [manually configure your `local_nb_nodes.json` file](#configuring-local-node-names-and-urls-for-federation).

#### Launching a profile
You can then launch a specific profile using the `--profile` or  `-p` flag with `docker compose`, e.g.:
```bash
docker compose --profile full_stack up -d
```
If no profile is specified, `docker compose up -d` will start the services for the default profile, `full_stack`.

Take a look at the [getting started guide](getting_started.md) for more information setting up for a first launch.

### Default host ports for services

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

## Environment variables

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

### Change security relevant variables

The graph store (GraphDB instance) in a Neurobagel node is secured with password-based access and includes two users: an `admin` superuser and a regular database user, both of which are automatically configured by the Neurobagel deployment recipe.
Passwords for both users are defined via files in the `./secrets` directory of the recipes repository, while the regular database username is set through an environment variable in `.env` file.

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

4. If you've previously launched a Neurobagel Docker Compose stack following the [Getting started](getting_started.md#the-neurobagel-node-deployment-recipe) instructions,
    you'll need to [reset your graph store](maintaining.md#resetting-your-graphdb-instance) for any changes you have made to user credentials to take effect (steps 1-2 above). 
    Don't worry, any other configuration changes you've already made will be applied when you re-launch your node.

## Configuring local node names and URLs for federation

When using a deployment profile that provides federation (i.e., includes the federation API), 
you can configure the URLs and display names of the **node APIs** of any local nodes you wish to federate over in the file `local_nb_nodes.json`. 
This file is read by the f-API.

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

## Behind a reverse proxy

!!! warning "These steps are for advanced users and production deployments"

To make your Neurobagel node services (node API, query tool, etc.) accessible via custom URLs
(e.g. `https://www.myfirstnode.org/query`) rather than a server IP address and port
(e.g. `http://192.168.0.1:3000`) as shown in in the [getting started guide](getting_started.md), 
you will need to set up a reverse proxy such as [NGINX](https://nginx.org/en/docs/beginners_guide.html) or
[Caddy](https://caddyserver.com/docs/quick-starts/reverse-proxy). 
This will route incoming requests for custom URLs to the Neurobagel services deployed on your server. 

The [Neurobagel `recipes` repository](https://github.com/neurobagel/recipes/)
includes pre-configured Docker Compose files for both NGINX and Caddy,
each of which can be used to launch a reverse proxy server alongside the services in your Neurobagel node.
The reverse proxy setup will then automatically handle routing 
and also manage and renew SSL certificates (providing secure HTTPS connections) for node services.

1. If you haven't already, follow the [steps](getting_started.md#the-neurobagel-node-deployment-recipe)
to clone and minimally configure the services in the [Neurobagel deployment recipe](https://github.com/neurobagel/recipes).

2. Ensure you have already registered your desired domain(s) with a DNS provider and configured the DNS settings to resolve correctly to your host machine.

3. Ensure ports 80 and 443 are open on the host machine where your Docker Compose stack is running.
These are the ports your reverse proxy will listen on for incoming HTTP and HTTPS traffic.

=== "NGINX"

    4. In your local `docker-compose-nginx.yml` file, for **each** service
    (i.e. `api`, `federation`, and `query_federation`),

        1. Locate the `environment` section for that service 
        2. Update the value of the following variables to the custom domain that specific service will use:

            - `VIRTUAL_HOST`
            - `LETSENCRYPT_HOST`

            Both variables must have the same value for a given service, and must not include a protocol (`http://` or `https://`).
        3. (Optional) To host services on different subpaths instead of different subdomains (e.g., `myinstitute.org/service1` instead of `service1.myinstitute.org`), 
        **do not include the subpath in the `VIRTUAL_HOST` or `LETSENCRYPT_HOST` values**. 
        Instead, update the corresponding `XXX_BASE_PATH` variables for the services in the `.env` file.
        The full list of service-specific base path variables can be found [here](config.md#environment-variables).

            For example, to host your node API at `myinstitute.org/node`:

            ``` { .yaml title="docker-compose-nginx.yml" }
            ...
            api:
              environment: 
                VIRTUAL_HOST: myinstitute.org
                LETSENCRYPT_HOST: myinstitute.org
            ...
            ```
            
            ``` { .bash title=".env" }
            ...
            NB_NAPI_BASE_PATH="/node"
            ...
            ```

        ??? warning "Do not change the `VIRTUAL_PATH` and `VIRTUAL_PORT` variables"
            You can look at the [NGINX-Proxy documentation](https://github.com/nginx-proxy/nginx-proxy/tree/main/docs#virtual-hosts-and-ports) to learn more about how these variables work.

    5. In your `.env` file, set `NB_API_QUERY_URL` to your custom URL for the **federation API**, including any subpath if used. 
    This URL must always begin with `https://`.

        Example:
        ``` { .bash title=".env" }
        ...
        NB_API_QUERY_URL="https://myinstitute.org/federate"
        ...
        ```

    6. Finally, launch your node by explicitly referencing the custom Docker Compose file:

        ```bash
        docker compose -f docker-compose-nginx.yml up -d
        ```

=== "Caddy"

    !!! note "You do not need to edit the `docker-compose-caddy.yml` file directly."

    4. In your local `recipes/config/caddy/Caddyfile`,
    change the default URL for each service to the URL you want to use for that service.
    Follow the comments in the file for guidance.
    
    ??? note "For more complex reverse proxy setups, refer to the Caddy documentation"

        The [Caddy documentation](https://caddyserver.com/docs/caddyfile) has more detailed information
        on subdirectory routing and other configuration options.

    5. Finally, launch your node by explicitly referencing the custom Docker Compose file:

        ```bash
        docker compose -f docker-compose-caddy.yml up -d
        ```
