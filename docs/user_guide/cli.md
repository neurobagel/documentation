# The Neurobagel CLI

The Neurobagel CLI is a command-line tool that processes a Neurobagel-annotated dataset
and produces harmonized subject-level phenotypic and imaging attributes.
The resulting harmonized data can be directly integrated into a Neurobagel graph store.

## System dependencies

The Neurobagel CLI can be run using Python, Docker, or Apptainer.

=== "Python"

    The CLI requires **Python 3.11 or later**.

    1. [Install Python](https://www.python.org/downloads/).

    2. Verify the installation:
    ```bash
    python --version
    ```

=== "Docker"

    1. [Install Docker](https://docs.docker.com/get-docker/).

    2. Verify the installation:
    ```bash
    docker --version
    ```

=== "Apptainer"

    1. [Install Apptainer](https://apptainer.org/docs/admin/main/installation.html).

    2. Verify the installation:
    ```bash
    apptainer --version
    ```

## Installation

=== "Python"

    The Neurobagel CLI can be installed from [PyPI](https://pypi.org/project/bagel/) using `pip`.

    1. Before installing the Python package, we recommend first creating and activating a Python virtual environment (using a tool such as [venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments)).

    2. Install the `bagel` package into your virtual environment:
    ```bash
    pip install bagel
    ```

=== "Docker"

    Pull the Docker image for the Neurobagel CLI from Docker Hub:
    ```bash
    docker pull neurobagel/bagelcli
    ```

=== "Apptainer"

    Build a Apptainer image for the Neurobagel CLI using the Docker Hub image:
    ```bash
    apptainer pull bagel.sif docker://neurobagel/bagelcli
    ```

## Input files

The Neurobagel CLI creates a single harmonized view of each subject's data in a dataset,
and can integrate information from several data sources
(phenotypic, raw neuroimaging, processed neuroimaging).

To run the CLI on a dataset, you will need the following files:

<div class="annotate" markdown>
- [ ] [A phenotypic TSV](./data_prep.md)
- [ ] [A Neurobagel JSON data dictionary](../data_models/dictionaries.md) for the TSV
- [ ] [A dataset description JSON](./dataset_description.md) for the dataset
- [ ] (Optional) A valid [BIDS metadata table](preparing_imaging_data.md), if subjects have neuroimaging data available (1)
- [ ] (Optional) A TSV of subject statuses for any image processing pipelines that have been run,
      following the [Nipoppy processing status file schema](https://nipoppy.readthedocs.io/en/latest/how_to_guides/tracking/index.html) (2)

</div>

1. This table can be generated automatically using the CLI's [`bids2tsv`](#generate-a-bids-metadata-table) command,
   and will be used to generate harmonized subject imaging data availability.
1. This file is adapted from the [Nipoppy](https://nipoppy.readthedocs.io/en/latest/index.html) workflow
   and can be automatically generated using [Nipoppy pipeline trackers](https://nipoppy.readthedocs.io/en/latest/how_to_guides/tracking/index.html).
   It will be used to generate harmonized subject processed imaging data availability.

## Running the CLI

To view the general CLI help and information about the available commands:

=== "Python"
    ```bash
    bagel -h
    ```

=== "Docker"

    ```bash
    # This is a shorthand for: docker run --rm neurobagel/bagelcli --help
    docker run --rm neurobagel/bagelcli
    ```

=== "Apptainer"

    ```bash
    # This is a shorthand for: apptainer run bagel.sif --help
    apptainer run bagel.sif
    ```

### Generate a BIDS metadata table

!!! info
    - If your dataset does not have imaging data, skip this step.
    - If your dataset's imaging data are **not** in BIDS format, you must manually create a [BIDS metadata table](preparing_imaging_data.md).

To include BIDS imaging data as part of the harmonized subject data, you must first convert the BIDS metadata into a [table](preparing_imaging_data.md).

The `bids2tsv` command provides a way for you to do this automatically.[^1]

[^1]: `bids2tsv` internally uses [bids2table](https://childmindresearch.github.io/bids2table/bids2table.html).

**Example:**

If your BIDS directory is located at `/data/public/Dataset1_bids` and you want the table output to be saved to `/home/Neurobagel`:

=== "Python"
    ```bash
    bagel bids2tsv \
        --bids-dir "/data/public/Dataset1_bids"
        --output "/home/Neurobagel/Dataset1_bids.tsv"
    ```

=== "Docker"
    ```bash
    docker run --rm \
        -v "/data/public:/data/public" \
        -v "/home/Neurobagel:/home/Neurobagel" \
        neurobagel/bagelcli bids2tsv \
        --bids-dir "/data/public/Dataset1_bids" \
        --output "/home/Neurobagel/Dataset1_bids.tsv"
    ```

    ??? info "Mounting input paths using `-v`/`--volume`"
        When running the CLI in a container, you must [mount](https://docs.docker.com/engine/storage/bind-mounts/) any input or output directories to directory paths within the container so that the app can access them.
        In your CLI options,
        always refer to the **container paths**.
        In the example above, container paths are set to match the host paths for simplicity.

=== "Apptainer"
    ```bash
    apptainer run --no-home \
        -B "/data/public,/home/Neurobagel" \
        bagel.sif bids2tsv \
        --bids-dir "/data/public/Dataset1_bids" \
        --output "/home/Neurobagel/Dataset1_bids.tsv"
    ```

    ??? info "Mounting input paths using `-B`/`--bind`"
        When running the CLI in a container,
        you must [mount](https://docs.sylabs.io/guides/3.0/user-guide/bind_paths_and_mounts.html) any input or output directories to directory paths within the container so that the app can access them.
        In your CLI options, always refer to the **container paths**.
        In the example above, the container paths are set to match the host paths for simplicity.

??? tip "This command may be slow on large datasets"
    On datasets with more than a few hundred subjects, `bids2tsv` can take upwards of several minutes
    due to the time needed for [`PyBIDS`](https://github.com/bids-standard/pybids) to read the dataset structure.

This will produce a BIDS metadata table named `Dataset1_bids.tsv`,
which can then be provided as input to the `bids` command below.

### Generate graph-ready data (JSONLD files)

<!-- TODO: Confirm version number -->
!!! info "Changed in v0.12.0"
    Prior to v0.12.0, the Neurobagel CLI used separate commands for generating JSONLD files from phenotypic, imaging, and derivative data.
    We recommend upgrading to the latest version before generating new JSONLD files.

The `create` command creates a JSONLD file representing harmonized subject-level data for a dataset that can be uploaded to a Neurobagel graph store.

Using command-line options, you can include different types of (meta)data about subjects from [standardized input files](#input-files).
Phenotypic data, raw neuroimaging metadata, and processing pipeline information are currently supported.

Each subject in a Neurobagel graph must have phenotypic data; other data types are optional.

!!! tip

    If you are using Docker or Apptainer,
    we strongly recommend placing all the [input files](#input-files) for your dataset into a single directory.
    This avoids the need to mount multiple paths into the container when running CLI commands.

#### Viewing the command help

To view the command-line options for `create`:

=== "Python"
    ```bash
    bagel create -h
    ```

=== "Docker"

    ```bash
    docker run --rm neurobagel/bagelcli create -h
    ```

=== "Apptainer"

    ```bash
    apptainer run bagel.sif create -h
    ```

#### Example usage

The following example assumes that the input files for your dataset are located in `/home/Dataset1/Neurobagel`:

``` { .bash .no-copy hl_lines="4-8" }
home/
└── Dataset1/
    ├── Neurobagel/
    │   ├── Dataset1_pheno.tsv # (1)!
    │   ├── Dataset1_pheno.json # (2)!
    │   ├── Dataset1_bids.tsv # (3)!
    │   ├── Dataset1_proc_status.tsv # (4)!
    │   ├── Dataset1_description.json # (5)!
    │   └── ...
    └── ...
```

1. The phenotypic TSV
2. The phenotypic data dictionary
3. The BIDS metadata table
4. The processing status file
5. The dataset description file

Navigate to the directory containing your input files, e.g.:

```bash
cd /home/Dataset1/Neurobagel
```

Run the `create` command to generate harmonized subject-level data for your dataset as a JSONLD file:

=== "Python"

    ```bash
    bagel create \
        --pheno "Dataset1_pheno.tsv" \
        --dictionary "Dataset1_pheno.json" \
        --dataset-description "Dataset1_description.json" \
        --bids-table "Dataset1_bids.tsv" \
        --processing-status "Dataset1_proc_status.tsv" \
        --output "Dataset1.jsonld"
    ```

=== "Docker"

    ```bash
    docker run --rm -v $PWD:$PWD neurobagel/bagelcli pheno \
        --pheno "$PWD/Dataset1_pheno.tsv" \
        --dictionary "$PWD/Dataset1_pheno.json" \
        --dataset-description "$PWD/Dataset1_description.json" \
        --bids-table "$PWD/Dataset1_bids.tsv" \
        --processing-status "$PWD/Dataset1_proc_status.tsv" \
        --output "$PWD/Dataset1.jsonld"
    ```

=== "Apptainer"

    ```bash
    apptainer run --no-home -B $PWD bagel.sif pheno \
        --pheno "$PWD/Dataset1_pheno.tsv" \
        --dictionary "$PWD/Dataset1_pheno.json" \
        --dataset-description "$PWD/Dataset1_description.json" \
        --bids-table "$PWD/Dataset1_bids.tsv" \
        --processing-status "$PWD/Dataset1_proc_status.tsv" \
        --output "$PWD/Dataset1.jsonld"
    ```

!!! Note
    Replace the Dataset1 files with the actual input files for your dataset.

!!! Tip
    Refer to the [command help](#viewing-the-command-help) for more information on the available options,
    including short forms.

The above example will produce a JSONLD file (`Dataset1.jsonld`) that describes phenotypic data, imaging modality availability, and processing pipeline availability for each subject.

If you do not have a [BIDS metadata table](#generate-a-bids-metadata-table) or a [Nipoppy processing status file](https://nipoppy.readthedocs.io/en/latest/how_to_guides/tracking/index.html) for your dataset,
simply omit the corresponding option(s) when running the `create` command.

The resulting JSONLD is ready for upload to a Neurobagel graph database.

#### When some inputs have errors

The `create` command runs in error-tolerant mode by default.
As long as the required phenotypic TSV, data dictionary, and dataset description are valid,
it will try to generate a valid, partial JSONLD file by processing as many valid input files as possible,
even if other inputs contain errors.

To abort the command and skip JSONLD generation when an input file cannot be processed due to an error
(i.e., if not all input data sources can be successfully included in the subject graph data),
use the `--strict` flag.

!!! tip
    Always check the command logs for input validation errors or warnings about skipped data.

### Troubleshooting

#### `File or directory does not exist` error when using Docker/Apptainer

This error usually means the container cannot access your input files because the directories were not mounted correctly.

The examples assume you are running the CLI from inside the directory containing your inputs.
Thus, they mount the current working directory `$PWD`
to the same path inside the container for convenience using the syntax:

=== "Docker"

    ```bash
    docker run --rm -v $PWD:$PWD neurobagel/bagelcli ...
    ```

    However, if your inputs are located in a different directory or spread across multiple directories,
    you must [mount](https://docs.sylabs.io/guides/3.0/user-guide/bind_paths_and_mounts.html) each directory explicitly
    using the Docker option `-v /path/on/host:/path/in/container`.

    When passing file paths to the CLI, always use the **absolute path inside the container** to avoid confusion.

=== "Apptainer"

    ```bash
    apptainer run --no-home -B $PWD bagel.sif ...
    ```

    However, if your inputs are located in a different directory or spread across multiple directories,
    you must [mount](https://docs.docker.com/engine/storage/bind-mounts/) each directory explicitly
    using the Apptainer option `-B /path/on/host:/path/in/container`.

    When passing file paths to the CLI, always use the **absolute path inside the container** to avoid confusion.

## Upgrading data to a newer version of the CLI

Neurobagel is under active development and future CLI releases may introduce breaking changes to the data model used in subject-level `.jsonld` graph files.
Breaking changes are highlighted in the [release notes](https://github.com/neurobagel/bagel-cli/releases).

To upgrade to the latest version of the data model:

1. Upgrade to the latest CLI version:

    === "Python"

        ```bash
        pip install --upgrade bagel
        ```

    === "Docker"

        ```bash
        docker pull neurobagel/bagelcli
        ```

    === "Apptainer"

        ```bash
        apptainer pull bagel.sif docker://neurobagel/bagelcli
        ```

2. If you have an existing Neurobagel graph database,
   we recommend regenerating and [reuploading](maintaining.md#updating-the-data-in-your-graph)
   all existing `.jsonld` files in your database using the latest CLI version.
   This keeps the database internally consistent and avoids conflicts with dataset `.jsonld` files generated using older CLI versions.
