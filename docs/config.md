Neurobagel is designed to be easily deployed with a single command without deep configuration.
In many cases however, you will want to customize your deployment to fit your needs.

If you already have a running Neurobagel node, 
after making any configuration changes 
(including changing the data you want to be available in the graph database), 
follow the instructions to [restart your services](maintaining.md#restarting-services-after-an-update) 
for the changes to take effect.

## Deployment

### Available services
The Neurobagel docker compose recipe includes several services
and coordinates them to work together:

(In parentheses are the names of services within the Docker Compose stack)

- [Neurobagel node API](api.md) (`api`): The API that communicates with the graph store and determines 
    how detailed the response to a query should be.
- Graph store (`graph`): A third-party RDF store that stores Neurobagel-harmonized data to be queried. At the moment our recipe uses the free tier
    of [GraphDB](https://db-engines.com/en/system/GraphDB) for this.
- Neurobagel federation API (`federation`): A special API that can federate over
    multiple Neurobagel nodes to provide a single point of access to multiple nodes.
    By default it will federate over all public nodes and any local nodes you specify. 
- [Neurobagel query tool](query_tool.md): A graphical web tool allows users to query the federation API (or node API)
    and visualize the results. Because the query tool is a static app and is run locally
    in the users browser, this service simply hosts the app.

### Available profiles
Neurobagel offers different deployment profiles that allow you to spin up specific combinations of services (listed below), depending on your use case.

1. `full_stack`: Best profile to get started with Neurobagel. 
    It includes all services you need to run a single standalone Neurobagel node, including a graphical query tool.
    :information_source: By default this profile will also federate over all publicly accessible neurobagel nodes.
       - `api`
       - `graph`
       - `federation`
       - `query_tool`
2. `local_node`: Best profile if you want to run a standalone Neurobagel node
    and rely on a different deployment for providing federation and the query tool.
    :information_source: **This is the default profile** if you don't specify one.
       - `api`
       - `graph` 
3. `local_federation`: Best profile if you already have multiple standalone (local or non-publicly-accessible) Neurobagel node
    deployments running and you now want to provide federation over them. 
    :information_source: If you only want to federate over a local node and all public Neurobagel nodes
    we recommend using the `full_stack` profile to set up your node and federation in one step. If you use the `local_federation` profile, 
    you will have to [manually configure your `local_nb_nodes.json` file](#local_nb_nodesjson).
      - `federation`
      - `query_tool`
4. `local_node_query`: :warning: Deprecated profile. 
    This profile lets you create a local node without 
    federation. The query tool hosted by this deployment will talk only to the
    local node.
       - `api`
       - `graph`
       - `query_tool`

You can then launch these profiles by using the `--profile` flag with `docker compose`, e.g.:

```bash
docker compose --profile full_stack up -d
```

Take a look at the [getting started guide](getting_started.md) for more information setting up for a first launch.

## Environment variables

Below are all the possible Neurobagel environment variables that can be set in `.env`.

{{ read_table('./repos/recipes/docs/neurobagel_environment_variables.tsv') }}

At minimum, we recommend reviewing and changing the values of the following variables in `.env` for security purposes:

> `NB_GRAPH_ADMIN_PASSWORD`  
> `NB_GRAPH_USERNAME`  
> `NB_GRAPH_PASSWORD`  
> `NB_GRAPH_DB` 
> `NB_RETURN_AGG`  
> `NB_API_QUERY_URL`

??? warning "Ensure that shell variables do not clash with `.env` file"
    
    If the shell you run `docker compose` from already has any 
    shell variable of the same name set, 
    the shell variable will take precedence over the configuration
    of `.env`!
    In this case, make sure to `unset` the local variable first.

    For more information, see [Docker's environment variable precedence](https://docs.docker.com/compose/environment-variables/envvars-precedence/).

!!! tip
    Double check that any environment variables you have customized in `.env` are resolved with your expected values using the command `docker compose config`.

## `local_nb_nodes.json`

This file is only used by deployment profiles that include the federation API. 
`local_nb_nodes.json` contains the URLs and (arbitrary) names of the local nodes you wish to federate over.
Each node must be denoted by a dictionary `{}` with two key-value pairs:  
`"NodeName"` for the name of the node,  
`"ApiURL"` for the URL of the API exposed for that node.  
Multiple nodes must be wrapped in a list `[]`.

Let's assume there are two local nodes already running on different servers of your institutional network, and you want to set up federation across both nodes:

- a node named `"Node Archive"` running on your local computer (localhost), on port `8000` and 
- a node named `"Node Recruitment"` running on a different computer with the local IP `192.168.0.1`, listening on the default http port `80`. 

In your `local_nb_nodes.json` file you would configure this as follows:
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
    you cannot use `localhost` for the `ApiURL` and instead have to provide a network-accessible URL or IP address.
    For an example, see the configuration for the node called `"My Institute"` above.


!!! Info "Nodes that do not need to be manually configured"
    We maintain a list of public Neurobagel nodes 
    [here](https://github.com/neurobagel/menu/blob/main/node_directory/neurobagel_public_nodes.json).
    By default every new `f-API` will lookup this list
    on startup and include it in the list of nodes to
    federate over.
    This also means that you do not have to manually
    configure public nodes, i.e. you **do not have to explicitly add them** to your `local_nb_nodes.json` file.

To add one or more local nodes to the list of nodes known to your `f-API`, simply add more dictionaries to this file.

## Manually setting up a Neurobagel graph backend

The Neurobagel docker compose recipe will automatically setup and configure 
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
the `LOCAL_GRAPH_DATA` in the `.env` configuration file. when the Neurobagel stack is launched.
Below is an example of how you would upload data manually using the script 
[`add_data_to_graph.sh`](https://github.com/neurobagel/recipes/blob/main/scripts/add_data_to_graph.sh):

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

The participant variables modeled by Neurobagel are named using Neurobagel's own vocabulary (for more information, see this page on [controlled terms](./term_naming_standards.md)).
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