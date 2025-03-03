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

For security and best practice purposes, follow the below additional steps to configure your node if you are using a deployment profile that includes a graph store:

1. **Change the values** of the following variables in `.env` from their defaults:
    - `NB_GRAPH_USERNAME`
    - `NB_GRAPH_DB`

2. **Replace the default passwords** for the `admin` superuser and the newly created graph database user (`NB_GRAPH_USERNAME`) for your graph store with your own secure passwords. 

    ??? warning "Already launched a Neurobagel node?"
        If you have already completed the [Getting started](getting_started.md#the-neurobagel-node-deployment-recipe) instructions and launched a Neurobagel Docker Compose stack for the first time,
        you will have to [reset your graph store](maintaining.md#resetting-your-graphdb-instance) before proceeding with this step. Don't worry, any other configuration changes you've made will be applied when you re-launch your node.

    - These passwords are stored in the directory defined under `NB_GRAPH_SECRETS_PATH` in `.env` ([`./secrets`](https://github.com/neurobagel/recipes/tree/main/secrets) by default), as the file contents of `NB_GRAPH_ADMIN_PASSWORD.txt` and `NB_GRAPH_PASSWORD.txt`, respectively.
    - To generate a random password in the terminal, you can use:
      ```bash
      openssl rand -hex 16
      ```

    - (Optional) Change the directory where your password files are stored by editing the variable `NB_GRAPH_SECRETS_PATH` in `.env`.

    ??? info "Graph store passwords are not meant for use by node query users"
        The passwords specified in the deployment recipe are only used internally by the scripts that (automatically) set up and update the graph store, 
        or to interact directly with the graph store (e.g., to modify database configuration or data).
        The passwords are also used to secure internal communication between your graph and its node API,
        such that an external user cannot query your graph directly.

    ??? info "Passwords are handled as Docker secrets"

        The contents of `NB_GRAPH_ADMIN_PASSWORD.txt` and `NB_GRAPH_PASSWORD.txt` are passed to Neurobagel containers as [Docker secrets](https://docs.docker.com/reference/compose-file/secrets/).
        This ensures that your passwords are not exposed in the container logs or in the `docker-compose.yml` file.
        
        Make sure to not share your password files with others.
  
2. **Review and change as necessary** values of the following variables in `.env` from their defaults, based on your data sharing requirements:
    - `NB_RETURN_AGG`
    - `NB_MIN_CELL_SIZE`
    !!! info
        These variables are modifiable after node initialization; you can [change their values at any time](maintaining.md#restarting-services-after-an-update).


## Configuring local node names and URLs for federation

When using a deployment profile that provides federation (i.e., includes the federation API), you can define
the URLs and display names of the **node APIs** of any local nodes you wish to federate over in a file called `local_nb_nodes.json`. 
This file is used by the f-API.

Each node to be federated over is defined using a dictionary with two key-value pairs:
```json
{
  "NodeName": "<display name for the node>",
  "ApiURL": "<URL of the node API exposed for that node>"
}
```

Values of `NodeName` are arbitrary. Multiple nodes must be wrapped in a list `[]`.  

!!! Info "Nodes that do not need to be manually configured"
    We maintain a list of publicly accessible Neurobagel nodes 
    [here](https://github.com/neurobagel/menu/blob/main/node_directory/neurobagel_public_nodes.json).
    By default, every new f-API will look up this list
    on startup and include it in its internal list of nodes to
    federate over (this can be disabled using the environment variable [`NB_FEDERATE_REMOTE_PUBLIC_NODES`](#environment-variables)).
    This also means that **you do not have to explicitly add these public nodes** to your `local_nb_nodes.json` file.

Example: Assume there are two local nodes already running on different servers of your institutional network, and you want to set up federation across both nodes:

- a node named `"My Institute"` running on your local computer (localhost), on port `8000` and 
- a node named `"Node Recruitment"` running on a different computer with the local IP `192.168.0.1`, listening on the default http port `80`. 

You would configure your `local_nb_nodes.json` as follows:
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

!!! warning "Do not use `localhost`/`127.0.0.1` in `local_nb_nodes.json`"

    Even if the local node API(s) you are federating over are running 
    on the same host machine as your federation API, 
    you cannot use `localhost` for the `"ApiURL"` and must instead provide a network-accessible URL, IP address, or container name.
    For an example, see the configuration for the node called `"My Institute"` above.

**Ensure that you not accidentally provide the address of your actual federation API for `"ApiURL"`!** This will cause an infinite request loop that will likely overload your service (as an f-API will be repeatedly making requests to itself).

To add one or more local nodes to the list of nodes known to your f-API, simply add more dictionaries to `local_nb_nodes.json`.

## Behind a reverse proxy

!!! warning "For advanced users"

To allow access to your Neurobagel node using a custom domain name, you will likely want to set up a reverse proxy (e.g., [NGINX](https://nginx.org/en/docs/beginners_guide.html), [Caddy](https://caddyserver.com/docs/quick-starts/reverse-proxy)) for your services. 
This will route incoming requests from your custom domain(s) to your local Neurobagel node API, your local Neurobagel query tool, etc.

Below is an example implementation of a reverse proxy, using a custom Docker Compose file that builds on [`docker-compose.yml`](https://github.com/neurobagel/recipes/blob/main/docker-compose.yml) in the default Neurobagel deployment recipe: 

1. If you haven't already, follow the [steps](getting_started.md#the-neurobagel-node-deployment-recipe) to clone and minimally configure the services in the [Neurobagel deployment recipe](https://github.com/neurobagel/recipes).
2. Replace the default `docker-compose.yml` in the `recipes` directory with the appropriate file(s) below which contain an example reverse proxy configuration, based on the reverse proxy server you are using:
    - Ensure you have already registered your desired domain(s) with a DNS provider and configured the DNS settings to resolve correctly to your host machine.

    === "NGINX"
        !!! info
            This file adds:

            - [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy) to run NGINX in a container, and automatically generate/refresh NGINX reverse proxy configurations when Neurobagel service containers are started
            - [acme-companion](https://github.com/nginx-proxy/acme-companion) to automatically create and renew SSL certificates for NGINX proxied service containers

        **Instructions:**

        - In the file below, replace the values of the variables `VIRTUAL_HOST` and `LETSENCRYPT_HOST` in the `environment` section for the `api`, `federation`, and `query_federation` services to the custom domains your proxied services will use

        ??? abstract "`docker-compose.yml` with NGINX configuration"
            ```{ .yaml .annotate title="docker-compose.yml" }
            services:
              api:
                image: "neurobagel/api:${NB_NAPI_TAG:-latest}"
                profiles:
                  - "local_node"
                  - "full_stack"
                ports:
                  - "${NB_NAPI_PORT_HOST:-8000}:8000"
                environment:
                  NB_GRAPH_USERNAME: ${NB_GRAPH_USERNAME}
                  NB_GRAPH_ADDRESS: graph
                  NB_GRAPH_PORT: 7200
                  NB_GRAPH_DB: ${NB_GRAPH_DB:-repositories/my_db}
                  NB_RETURN_AGG: ${NB_RETURN_AGG:-true}
                  NB_MIN_CELL_SIZE: ${NB_MIN_CELL_SIZE:-0}
                  NB_API_PORT: 8000
                  NB_NAPI_BASE_PATH: ${NB_NAPI_BASE_PATH}
                  NB_API_ALLOWED_ORIGINS: ${NB_NAPI_ALLOWED_ORIGINS:-"*"}
                  NB_ENABLE_AUTH: ${NB_ENABLE_AUTH:-false}
                  NB_QUERY_CLIENT_ID: ${NB_QUERY_CLIENT_ID}
                  VIRTUAL_HOST: myservice1.myinstitute.org 
                  LETSENCRYPT_HOST: myservice1.myinstitute.org 
                  VIRTUAL_PORT: 8000
                volumes:
                  - "./scripts/api_entrypoint.sh:/usr/src/api_entrypoint.sh"
                entrypoint:
                  - "/usr/src/api_entrypoint.sh"
                secrets:
                  - db_user_password

              graph:
                image: "ontotext/graphdb:10.3.1"
                profiles:
                  - "local_node"
                  - "full_stack"
                volumes:
                  - "graphdb_home:/opt/graphdb/home"
                  - "./scripts:/usr/src/neurobagel/scripts"
                  - "./vocab:/usr/src/neurobagel/vocab"
                  - "${LOCAL_GRAPH_DATA:-./data}:/data"
                ports:
                  - "${NB_GRAPH_PORT_HOST:-7200}:7200"
                environment:
                  NB_GRAPH_USERNAME: ${NB_GRAPH_USERNAME}
                  NB_GRAPH_PORT: 7200
                  NB_GRAPH_DB: ${NB_GRAPH_DB:-repositories/my_db}
                entrypoint:
                  - "/usr/src/neurobagel/scripts/setup.sh"
                working_dir: "/usr/src/neurobagel/scripts"
                secrets:
                  - db_admin_password
                  - db_user_password

              federation:
                image: "neurobagel/federation_api:${NB_FAPI_TAG:-latest}"
                profiles:
                  - "local_federation"
                  - "full_stack"
                ports:
                  - "${NB_FAPI_PORT_HOST:-8080}:8000"
                volumes:
                  - "./local_nb_nodes.json:/usr/src/local_nb_nodes.json:ro"
                environment:
                  NB_API_PORT: 8000
                  NB_FAPI_BASE_PATH: ${NB_FAPI_BASE_PATH}
                  NB_FEDERATE_REMOTE_PUBLIC_NODES: ${NB_FEDERATE_REMOTE_PUBLIC_NODES:-True}
                  NB_ENABLE_AUTH: ${NB_ENABLE_AUTH:-false}
                  NB_QUERY_CLIENT_ID: ${NB_QUERY_CLIENT_ID}
                  VIRTUAL_HOST: myservice2.myinstitute.org
                  LETSENCRYPT_HOST: myservice2.myinstitute.org
                  VIRTUAL_PORT: 8000

              query_federation:
                image: "neurobagel/query_tool:${NB_QUERY_TAG:-latest}"
                profiles:
                  - "local_federation"
                  - "full_stack"
                ports:
                  - "${NB_QUERY_PORT_HOST:-3000}:5173"
                environment:
                  NB_API_QUERY_URL: ${NB_API_QUERY_URL}
                  NB_QUERY_APP_BASE_PATH: ${NB_QUERY_APP_BASE_PATH:-/}
                  NB_ENABLE_AUTH: ${NB_ENABLE_AUTH:-false}
                  NB_QUERY_CLIENT_ID: ${NB_QUERY_CLIENT_ID}
                  NB_QUERY_HEADER_SCRIPT: ${NB_QUERY_HEADER_SCRIPT}
                  VIRTUAL_HOST: myservice3.myinstitute.org
                  LETSENCRYPT_HOST: myservice3.myinstitute.org
                  VIRTUAL_PORT: 5173

              nginx-proxy:
                image: nginxproxy/nginx-proxy
                container_name: nginx-proxy
                ports:
                  - "80:80"
                  - "443:443"
                volumes:
                  - ./config/nginx/reverse_proxy.conf:/etc/nginx/conf.d/reverse_proxy.conf
                  - vhost:/etc/nginx/vhost.d
                  - html:/usr/share/nginx/html
                  - certs:/etc/nginx/certs:ro
                  - /var/run/docker.sock:/tmp/docker.sock:ro

              acme-companion:
                image: nginxproxy/acme-companion
                container_name: nginx-proxy-acme
                volumes_from:
                  - nginx-proxy
                volumes:
                  - certs:/etc/nginx/certs:rw
                  - acme:/etc/acme.sh
                  - /var/run/docker.sock:/var/run/docker.sock:ro

            secrets:
              db_admin_password:
                file: ${NB_GRAPH_SECRETS_PATH:-./secrets}/NB_GRAPH_ADMIN_PASSWORD.txt
              db_user_password:
                file: ${NB_GRAPH_SECRETS_PATH:-./secrets}/NB_GRAPH_PASSWORD.txt

            volumes:
              graphdb_home:
              vhost:
              html:
              certs:
              acme:
            ```

    === "Caddy"
        !!! warning "Community Contribution"
            **Disclaimer:** This example `docker-compose.yml` is a community-contributed resource and is not officially maintained or supported by the Neurobagel team.
            
            **Compatibility Note:** This example has been tested with version `v0.5.0` of the [Neurobagel deployment recipes](https://github.com/neurobagel/recipes). Ensure you are using the same or a compatible version for optimal results.
        
        **Instructions:**

          - Copy both files below into your `recipes` directory
          - In the `Caddyfile`, replace the placeholder domains with the custom domains your proxied services will use (see comments) 
        
        ??? abstract "`docker-compose.yml` with Caddy and corresponding `Caddyfile`"
            ```{ .yaml .annotate title="docker-compose.yml" }
            services:
              api:
                image: "neurobagel/api:${NB_NAPI_TAG:-latest}"
                profiles:
                  - "local_node"
                  - "full_stack"
                ports:
                  - "${NB_NAPI_PORT_HOST:-8000}:8000"
                environment:
                  NB_GRAPH_USERNAME: ${NB_GRAPH_USERNAME}
                  NB_GRAPH_ADDRESS: graph
                  NB_GRAPH_PORT: 7200
                  NB_GRAPH_DB: ${NB_GRAPH_DB:-repositories/my_db}
                  NB_RETURN_AGG: ${NB_RETURN_AGG:-true}
                  NB_MIN_CELL_SIZE: ${NB_MIN_CELL_SIZE:-0}
                  NB_API_PORT: 8000
                  NB_NAPI_BASE_PATH: ${NB_NAPI_BASE_PATH}
                  NB_API_ALLOWED_ORIGINS: ${NB_NAPI_ALLOWED_ORIGINS:-"*"}
                  NB_ENABLE_AUTH: ${NB_ENABLE_AUTH:-false}
                  NB_QUERY_CLIENT_ID: ${NB_QUERY_CLIENT_ID}
                volumes:
                  - "./scripts/api_entrypoint.sh:/usr/src/api_entrypoint.sh"
                entrypoint:
                  - "/usr/src/api_entrypoint.sh"
                secrets:
                  - db_user_password

              graph:
                image: "ontotext/graphdb:10.3.1"
                profiles:
                  - "local_node"
                  - "full_stack"
                volumes:
                  - "graphdb_home:/opt/graphdb/home"
                  - "./scripts:/usr/src/neurobagel/scripts"
                  - "./vocab:/usr/src/neurobagel/vocab"
                  - "${LOCAL_GRAPH_DATA:-./data}:/data"
                ports:
                  - "${NB_GRAPH_PORT_HOST:-7200}:7200"
                environment:
                  NB_GRAPH_USERNAME: ${NB_GRAPH_USERNAME}
                  NB_GRAPH_PORT: 7200
                  NB_GRAPH_DB: ${NB_GRAPH_DB:-repositories/my_db}
                entrypoint:
                  - "/usr/src/neurobagel/scripts/setup.sh"
                working_dir: "/usr/src/neurobagel/scripts"
                secrets:
                  - db_admin_password
                  - db_user_password

              federation:
                image: "neurobagel/federation_api:${NB_FAPI_TAG:-latest}"
                profiles:
                  - "local_federation"
                  - "full_stack"
                ports:
                  - "${NB_FAPI_PORT_HOST:-8080}:8000"
                volumes:
                  - "./local_nb_nodes.json:/usr/src/local_nb_nodes.json:ro"
                environment:
                  NB_API_PORT: 8000
                  NB_FAPI_BASE_PATH: ${NB_FAPI_BASE_PATH}
                  NB_FEDERATE_REMOTE_PUBLIC_NODES: ${NB_FEDERATE_REMOTE_PUBLIC_NODES:-True}
                  NB_ENABLE_AUTH: ${NB_ENABLE_AUTH:-false}
                  NB_QUERY_CLIENT_ID: ${NB_QUERY_CLIENT_ID}

              query_federation:
                image: "neurobagel/query_tool:${NB_QUERY_TAG:-latest}"
                profiles:
                  - "local_federation"
                  - "full_stack"
                ports:
                  - "${NB_QUERY_PORT_HOST:-3000}:5173"
                environment:
                  NB_API_QUERY_URL: ${NB_API_QUERY_URL}
                  NB_QUERY_APP_BASE_PATH: ${NB_QUERY_APP_BASE_PATH:-/}
                  NB_ENABLE_AUTH: ${NB_ENABLE_AUTH:-false}
                  NB_QUERY_CLIENT_ID: ${NB_QUERY_CLIENT_ID}
                  NB_QUERY_HEADER_SCRIPT: ${NB_QUERY_HEADER_SCRIPT}

              caddy:
                image: caddy:latest
                container_name: caddy
                ports:
                  - "80:80"
                  - "443:443"
                volumes:
                  - ./Caddyfile:/etc/caddy/Caddyfile
                  - caddy_data:/data
                  - caddy_config:/config

            secrets:
              db_admin_password:
                file: ${NB_GRAPH_SECRETS_PATH:-./secrets}/NB_GRAPH_ADMIN_PASSWORD.txt
              db_user_password:
                file: ${NB_GRAPH_SECRETS_PATH:-./secrets}/NB_GRAPH_PASSWORD.txt

            volumes:
              graphdb_home:
              caddy_data:
              caddy_config:
            ```
        
            ```{ .annotate title="Caddyfile" }
            # Replace myservice1.myinstitute.org with the custom domain of your node API
            myservice1.myinstitute.org {
                reverse_proxy api:8000
            }
            
            # Replace myservice2.myinstitute.org with the custom domain of your federation API
            myservice2.myinstitute.org {
                reverse_proxy federation:8000
            }
            
            # Replace myservice3.myinstitute.org with the custom domain of your query tool
            myservice3.myinstitute.org {
                reverse_proxy query_federation:5173
            }
            ```

3. Running the Stack

- After selecting your reverse proxy configuration and updating the required values, start the services by running:

    ```bash
    docker compose up -d
    ```

4. Make sure that ports 80 and 443 are open on the host machine where your Docker Compose stack is running.

## Manually setting up a Neurobagel graph backend

The Neurobagel Docker Compose recipe will automatically set up and configure 
all services for you after deployment.
The automated setup steps are explained in more detail below.

!!! warning "For advanced users / debugging purposes only"

    The following steps are only documented as a reference and for advanced users.
    You should not need to do this in most cases.

### Configuring the graph store

These are manual steps for configuring the GraphDB backend after launching the Neurobagel stack.

1: Set the password of the default `admin` superuser and enable password-based access to databases

??? info "Details"

    When you first launch the graph server, a default `admin` user with superuser privilege will automatically be created for you. 
    This `admin` user is meant to create other database users and modify their permissions.
    (For more information, see the [official GraphDB documentation](https://graphdb.ontotext.com/documentation/10.0/devhub/rest-api/curl-commands.html#security-management).)

??? example "Doing this manually with `curl`"

    First, change the password for the admin user that has been automatically
    created by GraphDB:

    ```bash
    curl -X PATCH --header 'Content-Type: application/json' http://localhost:7200/rest/security/users/admin -d '
    {"password": "NewAdminPassword"}'
    ```
    (make sure to replace `"NewAdminPassword"` with your own, secure password).

    Next, enable GraphDB security to only allow authenticated users access:
    ```bash
    curl -X POST --header 'Content-Type: application/json' -d true http://localhost:7200/rest/security
    ```

    and confirm that this was successful:
    ```bash
    ➜ curl -X GET http://localhost:7200/rest/security                                                  
    true
    ```

2: Create a new graph database user based on credentials defined in your `.env` file

??? info "Details"
    
    We do not recommend using `admin` for normal read and write operations, instead we can create a regular database user.

    The `.env` file created as part of the `docker compose` setup instructions
    declares the `NB_GRAPH_USERNAME` and `NB_GRAPH_PASSWORD` for the database user.
    The Neurobagel API will send requests to the graph using these credentials.

??? example "Doing this manually with `curl`"

    When you launch the RDF store for the first time, 
    we have to create a new database user:

    ```bash
    curl -X POST --header 'Content-Type: application/json' -u "admin:NewAdminPassword" -d '
    {
    "username": "DBUSER",
    "password": "DBPASSWORD"
    }' http://localhost:7200/rest/security/users/DBUSER
    ```

    Make sure to use the exact `NB_GRAPH_USERNAME` and `NB_GRAPH_PASSWORD` you defined in the `.env` file when creating the new database user.
    Otherwise the Neurobagel API will not have the correct permission to query the graph.

3: Create a new graph database with the name defined in your `.env`

??? info "Details"

    When you first launch the graph store, there are no graph databases.
    You have to create a new one to store your metadata.

    By default the Neurobagel API will query a graph database named `my_db`. 
    If you have defined a custom `NB_GRAPH_DB` name in the `.env` file, you will first need to create a database with a matching name.

??? example "Doing this manually with `curl`"

    In GraphDB, graph databases are called resources.
    To create a new one, you will also have to prepare a `data-config.ttl` file
    that contains the settings for the resource you will create 
    (for more information, see the [GraphDB docs](https://graphdb.ontotext.com/documentation/10.0/devhub/rest-api/location-and-repository-tutorial.html#create-a-repository)).

    You can edit [this example file](https://github.com/neurobagel/recipes/blob/main/scripts/data-config_template.ttl) and save
    it as `data-config.ttl` locally.
    **Ensure the value for `rep:repositoryID`
    in `data-config.ttl` matches the value in
    `NB_GRAPH_DB` in your `.env` file**. 
    For example, if `NB_GRAPH_DB=repositories/my_db`, then
    `rep:repositoryID "my_db" ;`.

    Then, create a new graph database with the following command (replace "my_db" as needed). 
    If your `data-config.ttl` is not in the current directory, replace `"@data-config.ttl"` in the command with `"@PATH/TO/data-config.ttl"`.

    ```bash
    curl -X PUT -u "admin:NewAdminPassword" http://localhost:7200/repositories/my_db --data-binary "@data-config.ttl" -H "Content-Type: application/x-turtle"
    ```

4: Grant the newly created user from step 2 permissions to access the database

??? example "Doing this manually with `curl`"

    ```bash
    curl -X PUT --header 'Content-Type: application/json' -d '
    {"grantedAuthorities": ["WRITE_REPO_my_db","READ_REPO_my_db"]}' http://localhost:7200/rest/security/users/DBUSER -u "admin:NewAdminPassword"
    ```

    - `"WRITE_REPO_my_db"`: Grants write permission.
    - `"READ_REPO_my_db"`: Grants read permission.

    Make sure you replace `my_db` with the name of the graph db you have just created.


??? info "Non-automated options for interacting with the GraphDB backend"

    1. Directly send HTTP requests to the HTTP REST endpoints of the GraphDB backend 
    e.g. using `curl`. GraphDB uses the [RDF4J API](https://rdf4j.org/documentation/reference/rest-api/) specification.
    2. Use the GraphDB web interface (called [the Workbench](https://graphdb.ontotext.com/documentation/10.0/architecture-components.html)), which offers a more accessible way to manage the GraphDB instance. 
    Once your local GraphDB backend is running
    you can connect to the Workbench at [http://localhost:7200](http://localhost:7200).
    The Workbench is well documented on the [GraphDB website](https://graphdb.ontotext.com/documentation/10.0/workbench-user-interface.html).

### Uploading data to the graph store

Data are automatically uploaded to the graph from the path specified with
the `LOCAL_GRAPH_DATA` in the `.env` configuration file when the Neurobagel stack is (re-)started.

If you instead prefer to upload data manually,
you can use the
[`add_data_to_graph.sh`](https://github.com/neurobagel/recipes/blob/main/scripts/add_data_to_graph.sh) script:

``` bash
./add_data_to_graph.sh PATH/TO/YOUR/GRAPH-DATA \
  localhost:7200 repositories/my_db DBUSER DBPASSWORD \
```
!!! warning
    To update any _existing_ datasets in your graph database, you can clear the database and reupload all datasets using `add_data_to_graph.sh` following the command above and including the `--clear-data` flag. 

    Ensure that you also re-upload the Neurobagel vocabulary file `nb_vocab.ttl` following the section below.

### Adding vocabulary files to the graph database

??? "Why we need vocabulary files in the graph"
    In the context of an RDF store, in addition to information about specific observations of given standardized concepts such as "subject", "age", and "diagnosis" (represented in the subject-level JSONLDs generated by Neurobagel tools),
    hierarchical relationships between concepts themselves can also be represented.
    Including these relationships in a graph is important to be able to answer questions such as how many different diagnoses are represented in a graph database, to query for higher-order concepts for a given variable, and more.

The participant variables modeled by Neurobagel are named using Neurobagel's own vocabulary (for more information, see this page on [controlled terms](../data_models/term_naming_standards.md)).
This vocabulary, which defines internal relationships between vocabulary terms, 
is serialized in the file [`nb_vocab.ttl`](https://github.com/neurobagel/recipes/blob/main/vocab/nb_vocab.ttl) available from the `neurobagel/recipes` repository.
If you have cloned this repository, you will already have downloaded the vocabulary file.

**The `nb_vocab.ttl` file should be added to every created Neurobagel graph database.**
Below is an example of how you would do this using the same script we used to upload the dataset JSONLD files, [`add_data_to_graph.sh`](https://github.com/neurobagel/recipes/blob/main/scripts/add_data_to_graph.sh).

(assumes you are in the `scripts` subdirectory inside the `recipes` repository):

``` bash
./add_data_to_graph.sh ../vocab \
  localhost:7200 repositories/my_db DBUSER DBPASSWORD
```