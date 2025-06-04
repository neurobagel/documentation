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

!!! warning "These steps are for advanced users and production deployments"

In a production deployment, you likely want to serve the services of your Neurobagel node
(e.g. the node API, the query interface, etc) from an easy to remember URL
(e.g. `https://www.myfirstnode.org/query`) rather than the custom port on your server
(e.g. `http://192.168.0.1:3000`) that the [getting started guide](getting_started.md) has helped you set up.

To do so, you need to set up a reverse proxy like [NGINX](https://nginx.org/en/docs/beginners_guide.html) or
[Caddy](https://caddyserver.com/docs/quick-starts/reverse-proxy)
that will handle the correct routing of incoming requests for specific URLs
to the Neurobagel services you have deployed on your server. The [Neurobagel recipes repository on GitHub](https://github.com/neurobagel/recipes/)
includes pre-configured Docker compose files for both NGINX and Caddy, allowing you to chose your preferred option.
These custom files launche a reverse proxy server in addition to the regular Neurobagel services,
automatically request and renew SSL certificates to provide secure HTTPS connections, and handle routing.

If you haven't already, follow the [steps](getting_started.md#the-neurobagel-node-deployment-recipe)
to clone and minimally configure the services in the [Neurobagel deployment recipe](https://github.com/neurobagel/recipes)
as you would for a basic deployment.

=== "NGINX"

    The NGINX Docker Compose file is located in [`recipes/docker-compose-nginx.yml`](https://github.com/neurobagel/recipes/blob/main/docker-compose-nginx.yml).
    Before you deploy your node for the first time,
    you need to manually define a URL for each service by editing the `docker-compose-nginx.yml` file. 
    The values you want to edit are all in the `environments` section of each service.
    
    For example, for the node API service, the section of the `docker-compose-nginx.yml` file 
    that you need to change would look like this:

    ``` yaml title="/docker-compose-nginx.yml"
    api:
    extends:
        file: docker-compose.yml
        service: api
    # For a production deployment, we want to avoid binding ports to the host to avoid conflicts with
    # already running services. So here we override the ports exposed in the recipe we expand from and
    # set the ports to an empty list
    ports: !override []
    environment:
        # Replace the below domain with the domain you want to serve the node API from
        VIRTUAL_HOST: myservice1.myinstitute.org # (1)!
        VIRTUAL_PATH: ${NB_NAPI_BASE_PATH:-/}
        VIRTUAL_PORT: 8000
        # Set the below to the same domain as VIRTUAL_HOST to enable HTTPS
        LETSENCRYPT_HOST: myservice1.myinstitute.org # (2)!
    ```

    1. Replace this with the origin / domain name where the service should be hosted. If you host services on sub-paths (e.g. `https://www.mydomain.org/service1`), then do not include the subdirectory part (e.g. `service1`) here - and instead define it in the appropriate section of the `.env` file.
    2. Put the same value you used for `VIRTUAL_HOST`

    ??? warning "Do not change the `VIRTUAL_PATH` and `VIRTUAL_PORT`" variables
    
        You can look at the [NGINX-Proxy documentation](https://github.com/nginx-proxy/nginx-proxy/tree/main/docs#virtual-hosts-and-ports) 
        to learn more about how these variables work.

    Make these edits for all the Neurobagel services. 
    When you are finished, you must then make the corresponding changes in the `.env` file.
    Make sure to:

    - Update the `NB_API_QUERY_URL` variable in the query tool section to the new URL of the federation API
    - If you want to host services on subpaths of the same domain (e.g. `https://mynode.org/service1` and `https://mynode.org/service2`), 
    make sure to uncomment and edit the respective `XYZ_BASE_PATH` variables in the `.env` file.

    Finally, launch your node by explicitly referencing the `docker-compose-nginx.yml` file:

    ```bash
    docker compose -f docker-compose-nginx.yml up -d
    ```

=== "Caddy"

    The Caddy Docker Compose file is located in [`recipes/docker-compose-caddy.yml`](https://github.com/neurobagel/recipes/blob/main/docker-compose-caddy.yml).
    
    !!! note "You do not need to edit the `docker-compose-caddy.yml` file directly."

    Caddy relies on a separate config file to handle the routes for different services. 
    This config file is located in [`recipes/config/caddy/Caddyfile`](https://github.com/neurobagel/recipes/blob/main/config/caddy/Caddyfile).

    !!! warning "You need to edit the `/config/caddy/Caddyfile` file"

    ```bash title="/config/caddy/Caddyfile"
    # Replace myservice1.myinstitute.org with the custom domain of your node API
    myservice1.myinstitute.org { # (1)!
        reverse_proxy api:8000
    }

    # Replace myservice2.myinstitute.org with the custom domain of your federation API
    myservice2.myinstitute.org { # (2)!
        reverse_proxy federation:8000
    }

    # Replace myservice3.myinstitute.org with the custom domain of your query tool
    myservice3.myinstitute.org { # (3)!
        reverse_proxy query_federation:5173
    }
    ```

    1. Replace myservice1.myinstitute.org with the custom domain of your node API
    2. Replace myservice2.myinstitute.org with the custom domain of your federation API
    3. Replace myservice3.myinstitute.org with the custom domain of your query tool

    Make sure to update the domains in the `Caddyfile` to match the domains you want to use for your services
    as described by the comments in the file.
    
    ??? note "For more complex reverse proxy setups, refer to the Caddy documentation"

        The [Caddy documentation](https://caddyserver.com/docs/caddyfile) has more detailed information
        on subdirectory routing and other configuration options.

Finally, make sure that ports 80 and 443 are open on the host machine where your Docker Compose stack is running
because these are the ports your reverse proxy will listen on for incoming HTTP and HTTPS traffic.

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