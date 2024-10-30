# The Neurobagel CLI

The `bagel-cli` is a simple Python command-line tool to automatically parse and describe subject phenotypic and imaging attributes in an annotated dataset for integration into the Neurobagel graph.

## Installation

=== "Docker"

    Option 1 (RECOMMENDED): Pull the Docker image for the CLI from DockerHub:
    ```bash
    docker pull neurobagel/bagelcli
    ```

    Option 2: Clone the repository and build the Docker image locally:
    ```bash
    git clone https://github.com/neurobagel/bagel-cli.git
    cd bagel-cli
    docker build -t bagel .
    ```

=== "Singularity"

    Build a Singularity image for `bagel-cli` using the DockerHub image:  
    ```bash
    singularity pull bagel.sif docker://neurobagel/bagelcli
    ```

## Running the CLI
CLI commands can be accessed using the Docker/Singularity image.

!!! note 
    The Docker examples below assume that you are using the official Neurobagel Docker Hub image for the CLI. 
    If you have instead locally built an image, replace `neurobagel/bagelcli` in commands with your built image tag.

### Input files
The Neurobagel CLI can compile information from several different data sources to create a single harmonized representation of subject data. To run the CLI on a dataset, you will need:

<div class="annotate" markdown>
- [A phenotypic TSV](./data_prep.md)
- [A Neurobagel JSON data dictionary](./dictionaries.md) for the TSV
- (Optional) The imaging dataset in [BIDS](https://bids-specification.readthedocs.io/en/stable/) format, if subjects have imaging data available (1)
- (Optional) A TSV containing subject statuses for any image processing pipelines that have been run, following the [Nipoppy processing status file schema](https://nipoppy.readthedocs.io/en/latest/schemas/index.html#bagel-file) (2)
    
Note: The CLI does not require a BIDS dataset to accept a processing status file, and vice versa.
</div>

1. A valid BIDS dataset is needed for the CLI to automatically generate harmonized raw imaging metadata for subjects.
2. This file is used by the CLI to generate harmonized processing pipeline and derivative metadata for subjects.
It has compatibility with the [Nipoppy](https://nipoppy.readthedocs.io/en/latest/index.html) workflow, and can be automatically generated using the [Nipoppy pipeline trackers](https://nipoppy.readthedocs.io/en/latest/user_guide/tracking.html).

### Viewing CLI commands and options

The `bagel-cli` has different commands:

- `pheno`
- `bids`
- `derivatives`


To view the general CLI help and information about the commands:

=== "Docker"

    ```bash
    # This is a shorthand for `docker run --rm neurobagel/bagelcli --help`
    docker run --rm neurobagel/bagelcli
    ```

=== "Singularity"

    ```bash
    # This is a shorthand for `singularity run bagel.sif --help`
    singularity run bagel.sif
    ```

To view the command-line arguments for a specific command (e.g., `pheno`):

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

    ``` { .bash .annotate}
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

    ``` { .bash .annotate }
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

The `pheno` command must always be run first on a dataset; other metadata can be added in an arbitrary order.

!!! note "Speed of the `bids` command"
    The `bids` command of the `bagel-cli` (step 2) currently can take upwards of several minutes for datasets greater than a few hundred subjects, due to the time needed for pyBIDS to read the dataset structure.
    Once the slow initial dataset reading step is complete, you should see the message:
    ```bash
    BIDS parsing completed.
    ...
    ```

## Upgrading to a newer version of the CLI
Neurobagel is under active, early development and future releases of the CLI may introduce breaking changes to the data model for subject-level information in a `.jsonld` graph file. Breaking changes will be highlighted in the release notes!

_If you have already created `.jsonld` files for your Neurobagel graph database using the CLI_, 
they can be quickly re-generated under the new data model by following the instructions [here](maintaining.md#following-a-change-in-the-neurobagel-data-model) so that they will not conflict with dataset `.jsonld` files generated using the latest CLI version.

## Development environment
{%
   include-markdown "https://raw.githubusercontent.com/neurobagel/bagel-cli/main/README.md"
   start="## Development environment"
   end="## Regenerating the Neurobagel vocabulary file"
%}
