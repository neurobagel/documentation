Once your Neurobagel node is running and configured correctly,
there are some recurring tasks you may have to do to keep it operating correctly.

## Updating the Neurobagel services

### Updating the Neurobagel Docker images

We are continuously improving Neurobagel tools and services, 
so you may want to update your Neurobagel node to the latest version to benefit from new features and bug fixes.
We always publish our tools as [Docker images on Dockerhub](https://hub.docker.com/repositories/neurobagel).

Each Docker image has a version tag, and also two rolling tags: 

- `latest` (the latest stable release). This is the default tag used in the Neurobagel `docker-compose.yml` file.
- `nightly` (the latest build from the main branch). This tag is only used for compatibility testing and should not be used in production.

You can pull the most recent docker images for Neurobagel tools by running:

```bash
docker compose --profile full_stack pull
```

!!! warning "`docker compose` will only pull the images that are used by the current deployment profile."

    If you don't specify a deployment profile, the default profile (`local_node`) will be used,
    which only pulls the images for the [API](api.md), and graph store.

    See the [deployment profiles](infrastructure.md#deployment-profiles) 
    section for more information on the available profiles.

### Restarting services after an update

Whether you have updated the Docker images, the [configuration](config.md), or the [data](#updating-the-data-in-your-graph) 
of your Neurobagel node, you will need to restart the services to apply the changes.

To shut down a running Neurobagel node, 
navigate to the path on your file system where 
you have stored the `docker-compose.yml` file from the [initial setup](getting_started.md) and run:

```bash
docker compose --profile full_stack down
```

Then, to start the services again:

```bash
docker compose --profile full_stack up -d
```

!!! note "Specify the deployment profile"
    
    Whenever you use `docker compose` commands, you also have to specify
    the deployment profile you want to use with the `-p` or `--profile` flag.
    If you forget this step, `docker compose` will use the default profile (`local_node`),
    and will only shut down, update, or start the services for that profile.

## Updating the data in your graph

### Following a change in my _dataset_

When using Neurobagel tools on a dataset that is still undergoing data collection, you may need to update the Neurobagel annotations and/or graph-ready data for the dataset when you want to add new subjects or measurements or to correct mistakes in prior data versions.

For any of the below types of changes, you will need to regenerate a graph-ready `.jsonld` file for the dataset which reflects the change.

#### If the phenotypic (tabular) data have changed
If new variables have been added to the dataset such that there are new columns in the phenotypic TSV you previously annotated using Neurobagel's annotation tool, you will need to:  

1. **Generate an updated data dictionary** by annotating the new variables in your TSV following the [annotation workflow](annotation_tool.md)

2. **Generate a new graph-ready data file** for the dataset by [re-running the CLI](cli.md) on your updated TSV and data dictionary

#### If only the imaging data have changed
If the BIDS data for a dataset have changed without changes in the corresponding phenotypic TSV (e.g., if new modalities or scans have been acquired for a subject), you have two options:

- If you still have access to the dataset's phenotypic JSONLD generated from the `pheno` command of the `bagel-cli` (step 1), you may choose to [rerun only the `bids` CLI command](cli.md) on the updated BIDS directory. 
This will generate a new graph-ready data file with updated imaging metadata of subjects.

OR

- [Rerun the CLI entirely (`pheno` and `bids` steps)](cli.md) to generate a new graph-ready data file for the dataset.

_When in doubt, rerun both CLI commands._

#### If only the subjects have changed
If subjects have been added to or removed from the dataset but the phenotypic TSV is otherwise unchanged (i.e., only new or removed rows, without changes to the available variables), you will need to:

- **Generate a new graph-ready data file** for the dataset by [re-running the CLI](cli.md) (`pheno` and `bids` steps) on your updated TSV and existing data dictionary

### Following a change in the _Neurobagel data model_

As Neurobagel continues developing the data model, new tool releases may introduce breaking changes to the data model for subject-level information in a `.jsonld` graph data file. 
Breaking changes will be highlighted in the release notes.

_If you have already created `.jsonld` files for a Neurobagel graph database_ but want to update your graph data to the latest Neurobagel data model following such a change, you can easily do so by [rerunning the CLI](cli.md) on the existing data dictionaries and phenotypic TSVs for the dataset(s) in the graph.
This will ensure that if you use the latest version of the Neurobagel CLI to process new datasets (i.e., generate new `.jsonld` files) for your database, the resulting data will not have conflicts with existing data in the graph.

Note that if upgrading to a newer version of the data model, **you should regenerate the `.jsonld` files for _all_ datasets in your existing graph**.

### Updating the graph database
To allow easy (re-)uploading of the updated `.jsonld` for your dataset(s) to a graph database, make a copy of it in a [central directory on your research data fileserver for storing local Neurobagel `jsonld` datasets](config.md). 
Then, follow the steps for [uploading/updating a dataset in the graph database](config.md#uploading-data-to-the-graph-store) (needs to be completed by user with database write access).

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
