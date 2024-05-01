Neurobagel is designed to be easily deployed with a single command without deep configuration.
In many cases however, you will want to customize your deployment to fit your needs.

## Deployment profiles

1. full_stack
2. api_only
3. query_tool_only
4. local_node

## Environment variables

Below are all the possible Neurobagel environment variables that can be set in `.env`.

{{ read_table('./repos/recipes/docs/neurobagel_environment_variables.tsv') }}

For a local deployment, we recommend to **explicitly set** at least the following variables in `.env`
(note that `NB_GRAPH_USERNAME` and `NB_GRAPH_PASSWORD` must always be set):

> `NB_GRAPH_USERNAME`  
> `NB_GRAPH_PASSWORD`  
> `NB_GRAPH_DB`  
> `NB_GRAPH_IMG`  
> `NB_RETURN_AGG`  
> `NB_API_ALLOWED_ORIGINS`

??? warning "Ensure that shell variables do not clash with `.env` file"
    
    If the shell you run `docker compose` from already has any 
    shell variable of the same name set, 
    the shell variable will take precedence over the configuration
    of `.env`!
    In this case, make sure to `unset` the local variable first.

    For more information, see [Docker's environment variable precedence](https://docs.docker.com/compose/environment-variables/envvars-precedence/).

!!! tip
    Double check that any environment variables you have customized in `.env` are resolved with your expected values using the command `docker compose config`.

### federation service specific `.env` variables

#### `local_nb_nodes.json`
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
    "NodeName": "Node Archive",
    "ApiURL": "http://host.docker.internal:8000",
  },
  {
    "NodeName": "Node Recruitment",
    "ApiURL": "http://192.168.0.1"
  }
]
```

!!! warning "Do not use `localhost`/`127.0.0.1` in `local_nb_nodes.json`"

    If the local node API(s) you are federating over is running on the same host machine as your federation API (e.g., the URL to access the node API is http://localhost:XXXX), make sure that you replace `localhost` with `host.docker.internal` in the `"ApiURL"` for the node inside `local_nb_nodes.json`.
    For an example, see the configuration for the node called `"Node Archive"` above.


!!! Info "Nodes that do not need to be manually configured"
    We maintain a list of public Neurobagel nodes 
    [here](https://github.com/neurobagel/menu/blob/main/node_directory/neurobagel_public_nodes.json).
    By default every new `f-API` will lookup this list
    on startup and include it in the list of nodes to
    federate over.
    This also means that you do not have to manually
    configure public nodes, i.e. you **do not have to explicitly add them** to your `local_nb_nodes.json` file.

To add one or more local nodes to the list of nodes known to your `f-API`, simply add more dictionaries to this file.


#### `.env`

`.env` holds environment variables needed for the `f-API` deployment.

``` {.bash .annotate title=".env"}
# Configuration for f-API
# Define the port that the f-API will run on INSIDE the docker container (default 8000)
NB_API_PORT=8000
# Define the port that the f-API will be exposed on to the host computer (and likely the outside network)
NB_API_PORT_HOST=8080
# Chose the docker image tag of the f-API (default latest)
NB_API_TAG=latest

# Configuration for query tool
# Define the URL of the f-API as it will appear to a user
NB_API_QUERY_URL=http://206.12.85.19:8080 # (1)!
# Chose the docker image tag of the query tool (default latest)
NB_QUERY_TAG=latest
# Chose the port that the query tool will be exposed on the host and likely the network (default 3000)
NB_QUERY_PORT_HOST=3000
```

1.  When a user uses the graphical query tool to query your
    f-API, these requests will be sent from the user's machine,
    not from the machine hosting the query tool.

    Make sure you set the `NB_API_QUERY_URL` in your `.env`
    as it will appear to a user on their own machine 
    - otherwise the request will fail.

The template file above can be adjusted according to your own deployment. 
If you have used the default Neurobagel configuration for your local `n-API` up to this point, you likely do not need to change anything in this file.


## Manual post-launch setup

The Neurobagel docker compose recipe will automatically setup and configure 
all services for you after deployment. 
The following steps are only documented as a reference and for advanced users.
You should not need to do this in most cases.

### Configuring graph store

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
However, if you need to upload data manually, you can use the script 
[`add_data_to_graph.sh`](https://github.com/neurobagel/recipes/blob/main/scripts/add_data_to_graph.sh):

``` bash
./add_data_to_graph.sh PATH/TO/YOUR/GRAPH-DATA \
  localhost:7200 repositories/my_db DBUSER DBPASSWORD \
  --clear-data
```

### Updating a dataset in the graph database
If the raw data for a previously harmonized dataset (i.e., already has a corresponding JSONLD _which is in the graph_) has been updated, [a new JSONLD file must first be generated for that dataset](updating_dataset.md).
To push the update to the corresponding graph database, our current recommended approach is to simply clear the database and re-upload all existing datasets, including the **new** JSONLD file for the updated dataset.

To do this, rerun `add_data_to_graph.sh` on the directory containing the JSONLD files currently in the graph database, including the replaced JSONLD file for the dataset that has been updated.
**Make sure to include the `--clear-data` flag when running the script so that the database is cleared first.**

**After the dataset(s) have been uploaded, ensure that you also re-upload the Neurobagel vocabulary file `nb_vocab.ttl` to the graph database following [this section](#adding-vocabulary-files-to-the-graph-database).**


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
This can be done using the same script we used to upload the dataset JSONLD files, [`add_data_to_graph.sh`](https://github.com/neurobagel/recipes/blob/main/scripts/add_data_to_graph.sh), which adds all `.ttl` and/or `.jsonld` files in a given directory to the specified graph.

Run the following code (assumes you are in the `scripts` subdirectory inside the `recipes` repository):

``` bash
./add_data_to_graph.sh ../vocab \
  localhost:7200 repositories/my_db DBUSER DBPASSWORD
```

## Updating your graph backend configuration

### Updating existing database user permissions

If you want to change database access permissions (e.g., adding or removing access to a database) for an _existing_ user in your GraphDB instance, you must do so manually.

Of note, in GraphDB, there is no straightforward REST API call to update a user's database access permissions without replacing the list of their existing database permissions (`"grantedAuthorities"`) entirely. 

!!! tip
    You can verify a user's settings at any time with the following:
    ```bash
    curl -u "admin:NewAdminPassword" http://localhost:7200/rest/security/users/DBUSER
    ```

Example: if user `DBUSER` was granted read/write access to database `my_db1` with the following command
(this command is run by default as part of [`graphdb_setup.sh`](https://github.com/neurobagel/recipes/blob/main/scripts/graphdb_setup.sh)):

```bash
curl -X PUT --header 'Content-Type: application/json' -d '
{"grantedAuthorities": ["WRITE_REPO_my_db","READ_REPO_my_db"]}' http://localhost:7200/rest/security/users/DBUSER -u "admin:NewAdminPassword"
```

To grant `DBUSER` read/write access to a second database `my_db2` (while keeping the existing access to `my_db1`), 
you would rerun the above `curl` command with _all_ permissions (existing and new) specified since the existing permissions list will be overwritten:

```bash
curl -X PUT --header 'Content-Type: application/json' -d '
{"grantedAuthorities": ["WRITE_REPO_my_db1","READ_REPO_my_db1", "WRITE_REPO_my_db2","READ_REPO_my_db2"]}' http://localhost:7200/rest/security/users/DBUSER -u "admin:NewAdminPassword"
```

Similarly, to revoke `my_db1` access so `DBUSER` only has access to `my_db2`:

```bash
curl -X PUT --header 'Content-Type: application/json' -d '
{"grantedAuthorities": ["WRITE_REPO_my_db2","READ_REPO_my_db2"]}' http://localhost:7200/rest/security/users/DBUSER -u "admin:NewAdminPassword"
```

??? tip "Managing user permissions using the GraphDB Workbench"

    If you are managing multiple GraphDB databases, the web-based administration interface for a GraphDB instance, the Workbench, 
    might be an easier way to manage user permissions than the REST API.
    More information on using the GraphDB Workbench can be found [here](https://graphdb.ontotext.com/documentation/10.0/workbench-user-interface.html).

### Resetting your GraphDB instance

If you previously set up a Neurobagel node on your machine but want to reset your graph database to start again _from scratch_, 
the most foolproof way would be to start with a clean GraphDB configuration to avoid conflicts with any previously created credentials or databases.

Some examples of when you might want to do this:

- You started but did not complete Neurobagel node setup previously and want to ensure you are using up-to-date instructions and recommended configuration options
- Your local node has stopped working after a configuration change to your graph database (e.g., your Neurobagel node API no longer starts or responds with an error, but you have confirmed all environment variables you have set should be correct)

The configuration for a given GraphDB instance is not tied to a specific GraphDB Docker container, but to the persistent home directory for GraphDB on the host machine.

So, to 'reset' your GraphDB instance for Neurobagel, you need to clear the contents of your persistent GraphDB home directory on your filesystem (this is the path specified for `NB_GRAPH_ROOT_HOST` in your `.env`, which is `~/graphdb-home` by default).

!!! warning

    This action will wipe any graph databases and users you previously created!
    
    We recommend shutting down any Neurobagel services you are currently running (including the graph, API, and query tool containers) before doing this to prevent your services from breaking in unexpected ways.

You can now follow the instructions on this page to (re-)set up your graph database from scratch.
