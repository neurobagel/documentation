# The Neurobagel CLI

The Neurobagel CLI is a command-line tool that processes a Neurobagel-annotated dataset and produces harmonized subject-level phenotypic and imaging attributes. 
The resulting harmonized data can be directly integrated into a Neurobagel graph store.

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

=== "Singularity"

    Build a Singularity image for the Neurobagel CLI using the Docker Hub image:  
    ```bash
    singularity pull bagel.sif docker://neurobagel/bagelcli
    ```

## Input files

The Neurobagel CLI creates a single harmonized view of each subject's data in a dataset, and can integrate information from several data sources (phenotypic, raw neuroimaging, processed neuroimaging).

To run the CLI on a dataset, you will need the following files:

<div class="annotate" markdown>
- [ ] [A phenotypic TSV](./data_prep.md)
- [ ] [A Neurobagel JSON data dictionary](../data_models/dictionaries.md) for the TSV
- [ ] (Optional) A valid [BIDS metadata table](preparing_imaging_data.md), if subjects have neuroimaging data available (1)
- [ ] (Optional) A TSV of subject statuses for any image processing pipelines that have been run, following the [Nipoppy processing status file schema](https://nipoppy.readthedocs.io/en/latest/schemas/index.html#bagel-file) (2)

</div>

1. This table can be generated automatically using the CLI's [`bids2tsv`](#generate-a-bids-metadata-table) command, and will be used to generate harmonized raw imaging metadata for subjects.
2. This file is adapted from the [Nipoppy](https://nipoppy.readthedocs.io/en/latest/index.html) workflow and can be automatically generated using [Nipoppy pipeline trackers](https://nipoppy.readthedocs.io/en/latest/how_to_guides/user_guide/tracking.html). It will be used to generate harmonized processing pipeline and derivative metadata for subjects.

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

=== "Singularity"

    ```bash
    # This is a shorthand for: singularity run bagel.sif --help
    singularity run bagel.sif
    ```

### Generate a BIDS metadata table
!!! info
    - If your dataset does not have imaging data, skip this step. 
    - If your dataset's imaging data are **not** in BIDS format, you must manually create a [BIDS metadata table](preparing_imaging_data.md).

To include BIDS imaging data as part of the harmonized subject data, you must first convert the BIDS metadata into a [table](preparing_imaging_data.md). 

You can do this automatically using the CLI's `bids2tsv` command.[^1]

[^1]: `bids2tsv` internally uses [bids2table](https://childmindresearch.github.io/bids2table/bids2table.html).

#### Example

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
        When running the CLI in a container, you must [mount](https://docs.docker.com/engine/storage/bind-mounts/) any input or output directories to directory paths within the container so that the app can access them. In your CLI options, always refer to the **container paths**. 
        In the example above, container paths are set to match the host paths for simplicity.

=== "Singularity"
    ```bash
    singularity run --no-home \
        -B "/data/public,/home/Neurobagel" \
        bagel.sif bids2tsv \
        --bids-dir "/data/public/Dataset1_bids" \
        --output "/home/Neurobagel/Dataset1_bids.tsv"
    ```

    ??? info "Mounting input paths using `-B`/`--bind`"
        When running the CLI in a container, you must [mount](https://docs.sylabs.io/guides/3.0/user-guide/bind_paths_and_mounts.html) any input or output directories to directory paths within the container so that the app can access them. In your CLI options, always refer to the **container paths**. 
        In the example above, the container paths are set to match the host paths for simplicity.

??? tip "This command may be slow on large datasets"
    On datasets with more than a few hundred subjects, `bids2tsv` can take upwards of several minutes 
    due to the time needed for [`PyBIDS`](https://github.com/bids-standard/pybids) to read the dataset structure.

This will produce a BIDS metadata table named `Dataset1_bids.tsv`, which can then be provided as input to the `bids` command below.

### Generate graph-ready data (JSONLD files)

The Neurobagel CLI provides different commands for generating different types of harmonized subject (meta)data:

- `pheno`

    !!! info "Must be run first"
        Each subject in a Neurobagel graph requires at least phenotypic data. 
        The other metadata are optional and can be added afterward via their respective commands in any order.

- `bids`
- `derivatives`

If you are using Docker or Singularity, we strongly recommend placing all the [input files](#input-files) for your dataset into a single directory.
This avoids the need to mount multiple paths into the container when running CLI commands.

#### Viewing help for a command
To view the command-line options for a specific command, such as `pheno`:

=== "Python"
    ```bash
    bagel pheno -h
    ```

=== "Docker"

    ```bash
    docker run --rm neurobagel/bagelcli pheno -h
    ```

=== "Singularity"

    ```bash
    singularity run bagel.sif pheno -h
    ```

#### Example

The following example assumes that the input files for your dataset are located in `/home/Dataset1/Neurobagel`:

``` { .bash .no-copy hl_lines="4-7" }
home/
└── Dataset1/
    ├── Neurobagel/
    │   ├── Dataset1_pheno.tsv # (1)!
    │   ├── Dataset1_pheno.json # (2)!
    │   ├── Dataset1_bids.tsv # (3)!
    │   ├── Dataset1_proc_status.tsv # (4)!
    │   └── ...
    └── ...
```

1. The phenotypic TSV
2. The phenotypic data dictionary
3. The BIDS metadata table
4. The processing status file

Below is an example CLI workflow for generating a graph-ready JSONLD file for Dataset1 (`Dataset1.jsonld`) that incorporates all the available subject data sources:

!!! Tip
    To see all CLI options for a command, including short forms and optional parameters, refer to the [command's help](#viewing-help-for-a-command).

=== "Python"

    Navigate to the directory containing the input files, e.g.:

    ```bash
    cd /home/Dataset1/Neurobagel
    ```

    1. Run the `pheno` command to generate harmonized subject-level phenotypic data as a JSONLD file

        ```bash
        bagel pheno \
            --pheno "Dataset1_pheno.tsv" \
            --dictionary "Dataset1_pheno.json" \
            --name "Dataset 1" \
            --output "Dataset1.jsonld"
        ```

    2. Run the `bids` command to add subjects' BIDS metadata to the dataset JSONLD file

        ```bash
        bagel bids \
            --jsonld-path "Dataset1.jsonld" \
            --bids-table "Dataset1_bids.tsv" \
            --output "Dataset1.jsonld" \
            --overwrite
        ```

    3. Add subjects' processing pipeline metadata to the dataset JSONLD

        ```bash
        bagel derivatives \
            --jsonld-path "Dataset1.jsonld" \
            --tabular "Dataset1_proc_status.tsv" \
            --output "Dataset1.jsonld" \
            --overwrite
        ```

=== "Docker"

    Navigate to the directory containing the input files, e.g.:

    ```bash
    cd /home/Dataset1/Neurobagel
    ```

    1. Run the `pheno` command to generate harmonized subject-level phenotypic data as a JSONLD file

        ```bash
        docker run --rm -v $PWD:$PWD neurobagel/bagelcli pheno \
            --pheno "$PWD/Dataset1_pheno.tsv" \
            --dictionary "$PWD/Dataset1_pheno.json" \
            --name "Dataset 1" \
            --output "$PWD/Dataset1.jsonld"
        ```

    2. Run the `bids` command to add subjects' BIDS metadata to the dataset JSONLD file

        ```bash
        docker run --rm -v $PWD:$PWD neurobagel/bagelcli bids \
            --jsonld-path "$PWD/Dataset1.jsonld" \
            --bids-table "$PWD/Dataset1_bids.tsv" \
            --output "$PWD/Dataset1.jsonld" \
            --overwrite
        ```

    3. Add subjects' processing pipeline metadata to the dataset JSONLD

        ```bash
        docker run --rm --v $PWD:$PWD neurobagel/bagelcli derivatives \
            --jsonld-path "$PWD/Dataset1.jsonld" \
            --tabular "$PWD/Dataset1_proc_status.tsv" \
            --output "$PWD/Dataset1.jsonld" \
            --overwrite
        ```

=== "Singularity"

    Navigate to the directory containing the input files, e.g.:

    ```bash
    cd /home/Dataset1/Neurobagel
    ```

    1. Run the `pheno` command to generate harmonized subject-level phenotypic data as a JSONLD file

        ```bash
        singularity run --no-home -B $PWD bagel.sif pheno \
            --pheno "$PWD/Dataset1_pheno.tsv" \
            --dictionary "$PWD/Dataset1_pheno.json" \
            --name "Dataset 1" \
            --output "$PWD/Dataset1.jsonld"
        ```

    2. Run the `bids` command to add subjects' BIDS metadata to the dataset JSONLD file

        ```bash
        singularity run --no-home -B $PWD bagel.sif bids \
            --jsonld-path "$PWD/Dataset1.jsonld" \
            --bids-table "$PWD/Dataset1_bids.tsv" \
            --output "$PWD/Dataset1.jsonld" \
            --overwrite
        ```

    3. Add subjects' processing pipeline metadata to the dataset JSONLD

        ```bash
        singularity run --no-home -B $PWD bagel.sif derivatives \
            --jsonld-path "$PWD/Dataset1.jsonld" \
            --tabular "$PWD/Dataset1_proc_status.tsv" \
            --output "$PWD/Dataset1.jsonld" \
            --overwrite
        ```

!!! Info
    Replace the Dataset1 files with the input files for your dataset.

??? tip "When to use `-f`/`--overwrite`"
    If you're only interested in the final JSONLD with all metadata added (i.e., after all relevant commands have been run), you can safely overwrite intermediate output files by specifying the same output file path each time.

The resulting JSONLD is ready to upload to a Neurobagel graph database.

### Troubleshooting

#### `File or directory does not exist` error when using Docker/Singularity

This error usually means the container cannot access your input files because the directories were not mounted correctly.

The examples assume you are running the CLI from inside the directory containing your inputs. Thus, they mount the current working directory `$PWD` to the same path inside the container for convenience using the syntax:

=== "Docker"

    ```bash
    docker run --rm -v $PWD:$PWD neurobagel/bagelcli ...
    ```

    However, if your inputs are located in a different directory or spread across multiple directories, you must [mount](https://docs.sylabs.io/guides/3.0/user-guide/bind_paths_and_mounts.html) each directory explicitly using the Docker option `-v /path/on/host:/path/in/container`.

    When passing file paths to the CLI, always use the **absolute path inside the container** to avoid confusion.

=== "Singularity"

    ```bash
    singularity run --no-home -B $PWD bagel.sif ...
    ```

    However, if your inputs are located in a different directory or spread across multiple directories, you must [mount](https://docs.docker.com/engine/storage/bind-mounts/) each directory explicitly using the Singularity option `-B /path/on/host:/path/in/container`.

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

    === "Singularity"

        ```bash
        singularity pull bagel.sif docker://neurobagel/bagelcli
        ```

2. If you have an existing Neurobagel graph database, we recommend regenerating and [reuploading](maintaining.md#updating-the-data-in-your-graph) all existing `.jsonld` files in your database using the latest CLI version.
This keeps the database internally consistent and avoids conflicts with dataset `.jsonld` files generated using older CLI versions.
