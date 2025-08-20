# The Neurobagel CLI

The Neurobagel CLI is a command-line tool that processes a Neurobagel-annotated dataset and produces harmonized subject-level phenotypic and imaging attributes. 
The resulting harmonized data can be directly integrated into a Neurobagel graph store.

## Installation

=== "Python"

    The Neurobagel CLI can be installed from [PyPI](https://pypi.org/project/bagel/) using `pip`.

    1. Before installing the Python package, we recommend first creating and activating a Python virtual environment (such as [venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments)).

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

The Neurobagel CLI can compile information from several different data sources to create a single harmonized representation of subject data. To run the CLI on a dataset, you will need:

<div class="annotate" markdown>
- [A phenotypic TSV](./data_prep.md)
- [A Neurobagel JSON data dictionary](../data_models/dictionaries.md) for the TSV
- (Optional) The imaging dataset in [BIDS](https://bids-specification.readthedocs.io/en/stable/) format, if subjects have imaging data available (1)
- (Optional) A TSV containing subject statuses for any image processing pipelines that have been run, following the [Nipoppy processing status file schema](https://nipoppy.readthedocs.io/en/latest/schemas/index.html#bagel-file) (2)

## Running the CLI
CLI commands can be accessed using the Docker/Singularity image.

</div>

1. The CLI will use a valid BIDS dataset to generate harmonized raw imaging metadata for subjects.
2. This file will be used by the CLI to generate harmonized processing pipeline and derivative metadata for subjects.
It has compatibility with the [Nipoppy](https://nipoppy.readthedocs.io/en/latest/index.html) workflow, and can be automatically generated using the [Nipoppy pipeline trackers](https://nipoppy.readthedocs.io/en/latest/how_to_guides/user_guide/tracking.html).

### Viewing CLI commands and options

The Neurobagel CLI provides different commands for generating different types of subject (meta)data:

- `pheno`
- `bids`
- `derivatives`

!!! info "Important"
    The `pheno` command must be run first on a dataset, since each subject in a Neurobagel graph requires at least phenotypic data. 
    The other metadata are optional and can be added afterward in any order.

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

### Running the CLI on your data
1. `cd` into your local directory containing your [CLI input files](#input-files) 
(at minimum, a phenotypic TSV and corresponding Neurobagel annotated JSON data dictionary).
2. Run a `bagel-cli` container and include your CLI command and arguments at the end in the following format:

=== "Python"
    ```bash
    bagel <CLI command here>
    ```

=== "Docker"
    ```bash
    docker run --rm --volume=$PWD:$PWD -w $PWD neurobagel/bagelcli <CLI command here>
    ```

    ??? info "What is this command doing?"

        The combination of options `--volume=$PWD:$PWD -w $PWD` mounts your current working directory (containing all inputs for the CLI) at the same path inside the container, and also sets the _container's_ working directory to the mounted path (so it matches your location on your host machine). 
        This allows you to pass paths to the containerized CLI which are composed the same way as on your local machine. (And both absolute paths and relative top-down paths from your working directory will work!)

=== "Singularity"
    ```bash
    singularity run --no-home --bind $PWD --pwd $PWD /path/to/bagel.sif <CLI command here>
    ```

    ??? info "What is this command doing?"

        The combination of options `--bind $PWD --pwd $PWD` mounts your current working directory (containing all inputs for the CLI) at the same path inside the container, and also sets the _container's_ working directory to the mounted path (so it matches your location on your host machine). 
        This allows you to pass paths to the containerized CLI which are composed the same way as on your local machine. (And both absolute paths and relative top-down paths from your working directory will work!)


### Example  
If your dataset lives in `/home/data/Dataset1`:

``` { .bash .no-copy hl_lines="5 6 8 13" }
home/
└── data/
    └── Dataset1/
        ├── tabular/
        │   ├── Dataset1_pheno.tsv
        │   ├── Dataset1_pheno.json
        │   └── ...
        ├── bids/
        │   ├── sub-01/
        │   ├── sub-02/
        │   └── ...
        ├── derivatives/
        │   ├── Dataset1_proc_status.tsv
        │   └── ...
        └── ...
```
!!! note
    This is an example directory structure following the [Nipoppy specification](https://nipoppy.readthedocs.io/en/latest/index.html) for dataset organization. Your input data may be organized differently.


To generate a single, graph-ready JSONLD file incorporating all subject data sources recognized by Neurobagel (`Dataset1.jsonld`), 
you could run the CLI as follows:

=== "Docker"

    ``` bash
    cd /home/data/Dataset1

    # 1. Generate harmonized phenotypic data at the subject level
    docker run --rm --volume=$PWD:$PWD -w $PWD neurobagel/bagelcli pheno \
        --pheno "tabular/Dataset1_pheno.tsv" \
        --dictionary "tabular/Dataset1_pheno.json" \
        --name "My dataset 1" \
        --output "Dataset1.jsonld"

    # 2. Add subjects' BIDS data to the existing .jsonld
    docker run --rm --volume=$PWD:$PWD -w $PWD neurobagel/bagelcli bids \
        --jsonld-path "Dataset1.jsonld" \
        --bids-dir "bids" \
        --output "Dataset1.jsonld" \
        --overwrite  # (1)!

    # 3. Add subjects' processing pipeline metadata to the existing .jsonld
    docker run --rm --volume=$PWD:$PWD -w $PWD neurobagel/bagelcli derivatives \
        --tabular "derivatives/Dataset1_proc_status.tsv" \
        --jsonld-path "Dataset1.jsonld" \
        --output "Dataset1.jsonld" \
        --overwrite
    ```

    1. To keep outputs of different CLI commands as separate files, omit the `--overwrite` flag.

    !!! tip
        Short forms for a CLI command's options can be found by running:  
        `docker run --rm neurobagel/bagelcli pheno --help`


=== "Singularity"

    ``` .bash 
    cd /home/data/Dataset1

    # 1. Generate harmonized phenotypic data at the subject level
    singularity run --no-home --bind $PWD --pwd $PWD bagel.sif pheno \
        --pheno "tabular/Dataset1_pheno.tsv" \
        --dictionary "tabular/Dataset1_pheno.json" \
        --name "My dataset 1" \
        --output "Dataset1.jsonld"

    # 2. Add subjects' BIDS data to the existing .jsonld
    singularity run --no-home --bind $PWD --pwd $PWD bagel.sif bids \
        --jsonld-path "Dataset1.jsonld" \
        --bids-dir "bids" \
        --output "Dataset1.jsonld" \
        --overwrite  # (1)!

    # 3. Add subjects' processing pipeline metadata to the existing .jsonld
    singularity run --no-home --bind $PWD --pwd $PWD bagel.sif derivatives \
        --tabular "derivatives/Dataset1_proc_status.tsv" \
        --jsonld-path "Dataset1.jsonld" \
        --output "Dataset1.jsonld" \
        --overwrite
    ```

    1. To keep outputs of different CLI commands as separate files, omit the `--overwrite` flag.

    !!! tip
        Short forms for a CLI command's options can be found by running:  
        `singularity run bagel.sif pheno --help`

!!! note "Speed of the `bids` command"
    The `bids` command of the CLI currently can take upwards of several minutes for datasets with more than a few hundred subjects, due to the time needed for pyBIDS to read the dataset structure.
    Once the slow initial dataset reading step is complete, you should see the message:
    ```bash
    BIDS parsing completed.
    ...
    ```

## Upgrading data to a newer version of the CLI
Neurobagel is under active development and future releases of the CLI may introduce breaking changes to the data model for subject-level information in the output `.jsonld` graph file. 
Breaking changes are highlighted in the [release notes](https://github.com/neurobagel/bagel-cli/releases).

To keep an existing Neurobagel graph database up to date (and prevent conflicts with dataset `.jsonld` files generated using the latest CLI version), you can [regenerate and reupload existing `.jsonld` files for your database](maintaining.md#following-a-change-in-the-neurobagel-data-model) at any time under the latest data model.
