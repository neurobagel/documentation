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

## Manual post-launch setup

The Neurobagel docker compose recipe will automatically setup and configure 
all services for you after deployment. 
The following steps are only documented as a reference and for advanced users.
You should not need to do this in most cases.

### GraphDB

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