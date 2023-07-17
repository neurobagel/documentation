# SysAdmin

These instructions are for a sysadmin looking to deploy Neurobagel locally in an institute or lab.


## Get a license for Stardog

We use Stardog as our graph store application. 
Stardog has a free, annually renewable license for academic use.
In order to make a separate deployment of Neurobagel, 
you should therefore first request your own Stardog license.
You can request a Stardog license here:

[https://www.stardog.com/license-request/](https://www.stardog.com/license-request/)

!!! danger "Don't pick the wrong license"

    Stardog is a company that offers their graph store solutions both as a self-hosted,
    downloadable tool (what we want) and as a cloud hosted subscription model (what we do not want). Both tiers offer free access and the website has a tendency to steer
    you towards the cloud offering. Make sure you request a **license key** for Stardog.

![This is what requesting the license would look like](imgs/stardog_request.png)

The Stardog license is typically automatically granted via email in 24 hours. 

The license you receive will be a downloadable file. 
It is valid for one year and for a major version of Stardog.
You will need to download the license in a place that is accessible
to your new Stardog instance when it is launched (see below).


## Launch the API and graph stack

To launch the API and your Stardog instance using `docker compose`, follow the below steps distilled from [the these instructions](https://github.com/neurobagel/api/blob/main/README.md#local-installation).

### Clone the API repo
```bash
git clone https://github.com/neurobagel/api.git
```

### Set the environment variables
Create a `.env` file in the root of the repository to house the environment variables used by the API-graph network.

Below are all the possible Neurobagel environment variables that can be set in `.env`.

| Environment variable | Required? | Description                                                                                                                              | Default value            |
| -------------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `NB_GRAPH_USERNAME`  | Yes               | Username to access Stardog graph database that API will communicate with                                                                 | -                        |
| `NB_GRAPH_PASSWORD`  | Yes               | Password to access Stardog graph database that API will communicate with                                                                 | -                        |
| `NB_GRAPH_ADDRESS`   | No                | IP address for the graph database (or container name, if graph is hosted locally)                                                        | `206.12.99.17` (`graph`) |
| `NB_GRAPH_DB`        | No                | Name of graph database to query                                                                                                          | `test_data`              |
| `NB_RETURN_AGG`      | No                | Whether to return only dataset-level query results (including data locations) and exclude subject-level attributes. One of [true, false] | `true`                   |
| `NB_API_TAG`         | No                | Tag for API Docker image                                                                                                                 | `latest`                 |
| `STARDOG_TAG`        | No                | Tag for Stardog Docker image                                                                                                             | `8.2.2-java11-preview`   |
| `STARDOG_ROOT`       | No                | Path to directory on host machine containing a Stardog license file                                                                      | `~/stardog-home`         |

For a local deployment, we recommend to **explicitly set** the following variables in `.env`:

- `NB_GRAPH_USERNAME`
- `NB_GRAPH_PASSWORD`
- `NB_GRAPH_DB`
- `STARDOG_ROOT`

```bash title="example .env file"
NB_GRAPH_USERNAME=someuser
NB_GRAPH_PASSWORD=somepassword
NB_GRAPH_DB=test_data       # default
STARDOG_ROOT=~/stardog-home # default
```

Your Stardog license file must be in the `STARDOG_ROOT` directory.

??? warning "Ensure that shell variables do not clash with `.env` file"
    
    If the shell you run `docker compose` from already has any 
    shell variable of the same name set, 
    the shell variable will take precedence over the configuration
    of `.env`!
    Either unset the local variable or always export the `.env` file first.

    For more information, see [Docker's environment variable precedence](https://docs.docker.com/compose/environment-variables/envvars-precedence/).

To export all the variables defined in your `.env` file in one step, run the following:
```bash
export $(cat .env | xargs)
```

### Docker Compose

To spin up the Stardog and API containers using Docker Compose, 
ensure that both [docker](https://docs.docker.com/get-docker/) and [docker compose](https://docs.docker.com/compose/install/) are installed.

Run the following in the repository root (where the `docker-compose.yml` file is) to launch the containers:
```bash
docker compose up -d
```

## Setup for the first run

When you launch the Stardog graph for the first time,
there are a couple of setup steps that need to be done. 
These will not have to be repeated for subsequent starts.

To interact with the Stardog graph, 
you have two general options:

1. Send HTTP request against the HTTP API of the Stardog graph instance (e.g. with `curl`). See [https://stardog-union.github.io/http-docs/](https://stardog-union.github.io/http-docs/) for a full reference of API endpoints
2. Use the free Stardog-Studio web app. See the [Stardog documentation](https://docs.stardog.com/stardog-applications/dockerized_access#stardog-studio) for instruction to deploy Stardog-Studio as a Docker container.


!!! info 
    Stardog-Studio is the most accessible way 
    of manually interacting with a Stardog instance. 
    Here we will focus instead on using the HTTP API for configuration,
    as this allows programmatic access.
    All of these steps can also be achieved via Stardog-Studio manually.
    Please refer to the 
    [official docs](https://docs.stardog.com/stardog-applications/studio/) to learn how.


### Change the superuser password

When you first launch Stardog, 
a default `admin` user with superuser privilege
will automatically be created for you.
You should first change the password of this user:


```console
curl -X PUT -i -u "admin:admin" http://localhost:5820/admin/users/admin/pwd \
--data '{"password": "NewPassword"}'
```

### Create a new user

The `.env` file created as part of the `docker compose` setup instructions
declares the `USERNAME` and `PASSWORD` for the API user.
The API will send requests to the graph using these credentials.
When you launch Stardog for the first time, 
we have to create this user:

```console
curl -X POST -i -u "admin:NewPassword" http://localhost:5820/admin/users \
-H 'Content-Type: application/json' \
--data '{
    "username": "NewUser",
    "password": [
        "NewUserPassword"
    ]
}'
```

Confirm that the new user exists:

```console
curl -u "admin:NewPassword" http://localhost:5820/admin/users
```

!!! note
    Make sure to use the exact `USERNAME` and `PASSWORD` you
    defined in the `.env` file when creating the new user.
    Otherwise the API will not have the correct permission
    to query the graph.

### Create new database

When you first launch Stardog,
there are no graph databases.
You have to create a new one to store
your metadata.

If you have defined a custom `GRAPH_DB` name in the `.env` file,
make sure to create a database with a matching name.
By default the API will query a graph database
with a name of `test_data`.

```console
curl -X POST -i -u "admin:NewPassword" http://localhost:5820/admin/databases \
--form 'root="{\"dbname\":\"test_data\"}"'
```

Now we need to give our new user read and write permission for 
this database:

```console
curl -X PUT -i -u "admin:NewPassword" http://localhost:5820/admin/permissions/user/NewUser \
-H 'Content-Type: application/json' \
--data '{
    "action": "ALL",
    "resource_type": "DB",
    "resource": [
        "test_data"
    ]
}'
```

??? note "Finer permission control is also possible"

    For simplicity's sake, here we give `"ALL"` permission to the user.
    The Stardog API provide more fine grained permission control.
    See [the official API documentation](https://stardog-union.github.io/http-docs/#tag/Permissions/operation/addUserPermission).


### Add some test data

In order to test that the setup has worked correctly,
we need to add some data to the database.

You can take two example files from the [Neurobagel
example](https://github.com/neurobagel/examples) repository to get started:

- [example 1](https://github.com/neurobagel/examples/blob/4ccfffba5330242175e22b0bfa1813625186f9c1/example_1.ttl)
- [example 2](https://github.com/neurobagel/examples/blob/4ccfffba5330242175e22b0bfa1813625186f9c1/example_2.ttl)

Normally you would create these files by first annotating
the phenotypic information of a BIDS dataset with the 
Neurobagel annotator, and then parsing the annotated BIDS
dataset with the Neurobagel CLI.

Upload the example files to the graph using this command:

```console
curl -u "admin:NewPassword" -i -X POST http://localhost:5820/test_data \
-H "Content-Type: text/turtle" \
--data-binary @example_1.ttl
```

### Test the new deployment

You can run a test query against the API via a `curl` request in your terminal:

```console
curl -X 'GET' \
  'http://localhost:8000/query/' \
  -H 'accept: application/json'

# or
curl -L http://localhost:8000/query/
```

Or, you can directly use the interactive documentation of the API (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)) 
by navigating to [http://localhost:8000/docs](http://localhost:8000/docs) in your browser. 
To test the API from the docs interface, expand the `query` endpoint tab with the :fontawesome-solid-chevron-down: icon to view the parameters that can be set, 
and click "Try it out" and then "Execute" to execute a query.

!!! note
    For very large databases, requests to the API using the interactive docs UI may be very slow or time out. 
    If this prevents test queries from succeeding, try setting more parameters to enable an example response from the graph, or use a `curl` request instead.
