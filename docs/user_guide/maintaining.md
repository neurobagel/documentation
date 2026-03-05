Once your Neurobagel node is running and configured correctly,
there are some recurring tasks you may have to do to keep it operating correctly.

## Updating the Neurobagel services

### Updating the Neurobagel Docker images

We are continuously improving Neurobagel tools and services,
so you may want to update your Neurobagel node to the latest version to benefit from new features and bug fixes.
We always publish our tools as [Docker images on Docker Hub](https://hub.docker.com/u/neurobagel).

Each Docker image has a [semantic version](https://semver.org/) tag (vX.Y.Z), and also two rolling tags:

- `latest` (the latest stable release). This is the default tag used in the Neurobagel `docker-compose.yml` file.
- `nightly` (the latest build from the main branch). This tag is only used for compatibility testing and should not be used in production.

You can pull the most recent docker images for Neurobagel tools by running:

```bash
docker compose pull
```

??? tip "Not sure what version you have?"

    Since `latest` is a rolling tag, each `latest` Docker image for a Neurobagel tool includes its corresponding semver number (vX.Y.X) as part of its Docker image labels.

    You can find the labels for an image you have pulled in the image metadata, e.g.:
    ```bash
    docker image inspect neurobagel/api:latest
    ```
    or, to view only the labels:
    ```bash
    docker image inspect --format='{{json .Config.Labels}}' neurobagel/api:latest
    ```
    In either case, you should see something like this in the output:

    ```bash
        "Labels": {
            "org.opencontainers.image.created": "https://github.com/neurobagel/api",
            "org.opencontainers.image.revision": "01530f467e163f3dff595d3327bc60ba453de47d",
            "org.opencontainers.image.version": "v0.3.1"
        }
    ```
    where `"org.opencontainers.image.version"` refers to the version number.

### Restarting services after an update

Whether you have updated the Docker images, the [configuration](production_deployment.md), or the [data](#updating-the-data-in-your-graph)
of your Neurobagel node, you will need to restart the services to apply the changes.

To shut down your Neurobagel services,
navigate to the directory containing your deployment recipe and run:

```bash
docker compose down
```

Then, to start the services again:

```bash
docker compose up -d
```

!!! tip "For production deployments, you must specify the recipe filename"

    To relaunch services for a [`node`](production_deployment.md#node) or [`portal`](production_deployment.md#portal) deployment,
    you must provide the production Docker Compose recipe filename explicitly using the `-f` option:

    ```bash
    docker compose -f docker-compose.prod.yml up -d
    ```

## Updating the data in your graph

The Neurobagel deployment recipe launches a dedicated graph database that stores the datasets for a single node.
The data in this graph database is loaded from the path specified in the
[`LOCAL_GRAPH_DATA` environment variable](#environment-variables-reference),
and can be changed at any time.

By default, the graph database will only contain an [example dataset called `BIDS synthetic`](https://github.com/neurobagel/recipes/blob/main/data/example_synthetic_pheno-bids-derivatives.jsonld).

If you have followed the [initial setup](getting_started.md) for deploying a Neurobagel node from our Docker Compose recipe,
replacing the existing data in your graph database with your own data (or updated data) is a straightforward process.

Once you have generated or updated the JSONLD files you want to upload, to update the data in your graph:

1. Shut down the Neurobagel node, if it is already running

    ```bash
    docker compose down
    ```

2. Update the data files in the directory specified by the `LOCAL_GRAPH_DATA` variable in `.env`, or simply change the path to a directory containing your JSONLD files.
3. (Re)start the Neurobagel node

    ```bash
    docker compose up -d
    ```

!!! tip "For production deployments, you must specify the recipe filename"

    To relaunch services for a production [`node`](production_deployment.md#node) deployment,
    you must provide the production Docker Compose recipe filename explicitly using the `-f` option:

    ```bash
    docker compose -f docker-compose.prod.yml up -d
    ```

Here are some other common scenarios where you might need to update the data in your graph:

### Following a change in my _dataset_

When using Neurobagel tools on a dataset that is still undergoing data collection,
you may need to update the Neurobagel annotations and/or graph-ready data for the dataset
when you want to add new subjects or measurements or to correct mistakes in prior data versions.

For any of the below types of changes, you will need to regenerate a graph-ready `.jsonld` file for the dataset which reflects the change.

#### If the phenotypic (tabular) data have changed

If new variables have been added to the dataset such that there are new columns in the phenotypic TSV you previously annotated using Neurobagel's annotation tool, you will need to:

1. **Generate an updated data dictionary** by annotating the new variables in your TSV following the [annotation workflow](annotation_tool.md)

2. **Generate a new graph-ready data file** for the dataset by [re-running the CLI](cli.md) on your updated TSV and data dictionary

#### If only the imaging data have changed

If the BIDS data for a dataset have changed without changes in the corresponding phenotypic TSV (e.g., if new modalities or scans have been acquired for a subject), you have two options:

- If you still have access to the dataset's phenotypic JSONLD generated from the `pheno` command of the `bagel-cli` (step 1),
  you may choose to [rerun only the `bids` CLI command](cli.md) on the updated BIDS directory.
  This will generate a new graph-ready data file with updated imaging metadata of subjects.

OR

- [Rerun the CLI entirely (`pheno` and `bids` steps)](cli.md) to generate a new graph-ready data file for the dataset.

_When in doubt, rerun both CLI commands._

#### If only the subjects have changed

If subjects have been added to or removed from the dataset but the phenotypic TSV is otherwise unchanged
(i.e., only new or removed rows, without changes to the available variables), you will need to:

- **Generate a new graph-ready data file** for the dataset by [re-running the CLI](cli.md) (`pheno` and `bids` steps) on your updated TSV and existing data dictionary

### Following a change in the _Neurobagel data model_

As Neurobagel continues developing the data model, new tool releases may introduce breaking changes to the data model for subject-level information in a `.jsonld` graph data file.
Breaking changes will be highlighted in the release notes.

_If you have already created `.jsonld` files for a Neurobagel graph database_
but want to update your graph data to the latest Neurobagel data model following such a change,
you can easily do so by [rerunning the CLI](cli.md)
on the existing data dictionaries and phenotypic TSVs for the dataset(s) in the graph.
This will ensure that if you use the latest version of the Neurobagel CLI to process new datasets
(i.e., generate new `.jsonld` files) for your database,
the resulting data will not have conflicts with existing data in the graph.

Note that if upgrading to a newer version of the data model, **you should regenerate the `.jsonld` files for _all_ datasets in your existing graph**.

### Re-uploading a modified dataset

To allow easy (re-)uploading of the updated `.jsonld` for your dataset(s) to a graph database,
we recommend making a copy of it in a central directory on your research data fileserver
or storing local Neurobagel `jsonld` datasets.
Then, simply follow the steps for [uploading/updating a dataset in the graph database](#updating-the-data-in-your-graph).

## Updating your graph backend configuration

### Updating existing database user permissions

If you want to change database access permissions (e.g., adding or removing access to a database) for an _existing_ user in your GraphDB instance, you must do so manually.

Of note, in GraphDB, there is no straightforward REST API call to update a user's database access permissions
without replacing the list of their existing database permissions (`"grantedAuthorities"`) entirely.

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

Each Neurobagel node has its own GraphDB instance, which is used to store the graph data for the node.
If you want to reset your graph database and start again from scratch,
follow these steps:

1. Ensure that your Neurobagel node is not running (i.e., shut down the Docker containers for the node).

    ```bash
    docker compose down
    ```

2. Delete the Docker volume that contains the GraphDB data for your node.

    ```bash
    docker volume rm neurobagel_node_graphdb_home
    ```

    Replace `neurobagel_node_graphdb_home` with the name of the volume created for your node.
    It is usually named `<project_name>_graphdb_home`
    where `<project_name>` is the name of your Docker Compose stack
    as defined in `COMPOSE_PROJECT_NAME` in your `.env` file.

    ??? tip "`docker volume ls` lists all volumes on your system"

        You can use the `docker volume ls` command to list all volumes on your system.
        This will help you identify the name of the volume that was created for your Neurobagel node.

3. Launch your Neurobagel node again.

    ```bash
    docker compose up -d
    ```

    !!! tip "For production deployments, you must specify the recipe filename"

        To relaunch services for a production [`node`](production_deployment.md#node) deployment,
        you must provide the production Docker Compose recipe filename explicitly using the `-f` option:

        ```bash
        docker compose -f docker-compose.prod.yml up -d
        ```

Some examples of when you might want to do this:

- You started but did not complete Neurobagel node setup previously and want to ensure you are using up-to-date instructions and recommended configuration options
- Your local node has stopped working after a configuration change to your graph database
  (e.g., your Neurobagel node API no longer starts or responds with an error,
  but you have confirmed all environment variables you have set should be correct)
- You need to modify credentials for your graph store

!!! warning

    This action will wipe any graph databases and users you previously created!

## Environment variables reference

??? warning "Ensure that shell variables do not clash with `.env` file"

    If the shell you run `docker compose` from already has any
    shell variable of the same name set,
    the shell variable will take precedence over the configuration
    of `.env`!
    In this case, make sure to `unset` the local variable first.

    For more information, see [Docker's environment variable precedence](https://docs.docker.com/compose/environment-variables/envvars-precedence/).

!!! tip
    Double check that any environment variables you have customized in `.env` are resolved with your expected values using the command `docker compose config`.

Below are all the possible Neurobagel environment variables that can be set in `.env`.

{{ read_table('./repos/recipes/docs/neurobagel_environment_variables.tsv') }}
