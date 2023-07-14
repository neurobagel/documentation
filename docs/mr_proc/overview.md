## What is `mr_proc`? 

[*Process long and prosper*](https://en.wikipedia.org/wiki/Vulcan_salute)

`mr_proc` is a lightweight framework for analyzing (neuro)imaging and clinical data. It is designed to help users do the following:

1. Curate and organize data into a standard directory structure
2. Run data processing pipelines in a semi-automated and reproducible way
3. Track availability (including processing status, if applicable) of raw, tabular and derived data
4. Extract imaging features from MRI derivatives data for downstream analysis

### Example workflow

Given a dataset to process, a typical workflow with `mr_proc` can look like this:
1. Clone the [`mr_proc` template code repository](https://github.com/neurodatascience/mr_proc)
    * This repository contains scripts to run processing pipelines (and track their results) on BIDS data
2. Standardize raw imaging data: convert raw DICOM files into the NIfTI format and organize the dataset according to the [BIDS standard](https://bids-specification.readthedocs.io/en/stable/)
    * This requires some custom scripts, including the [`heuristic.py` file for HeuDiConv](https://heudiconv.readthedocs.io/en/latest/heuristics.html)
3. Run commonly-used image processing pipelines
    * `mr_proc` currently supports [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/), [fMRIPrep](https://fmriprep.org/en/stable/), [TractoFlow](https://tractoflow-documentation.readthedocs.io/en/latest/), and [MRIQC](https://mriqc.readthedocs.io/en/stable/) out-of-the-box, but new pipelines can be added by the user if needed
4. Organize demographic and clinical assessment data
    * This will most likely involve some custom data wrangling, for example to combine clinical assessment scores into a single file
5. Run tracker scripts to determine the availability of imaging (raw and/or processed) and/or tabular data
    * We call these availability/status metadata files "bagels" because they can be ingested by [Neurobagel](https://www.neurobagel.org/) for [dashboarding](https://dash.neurobagel.org/) and [querying](https://query.neurobagel.org/) participants across multiple studies

## Who is `mr_proc` for?

Anyone who wants to process datasets with imaging data and/or use datasets processed with `mr_proc`.

**Data managers**
* People who process datasets, either for specific analyses or to share with others
* Example use cases:
    * Data curation
        * Download/organize raw DICOM files
        * Convert raw data to a BIDS directory structure
        * Organize clinical data
    * Data processing
        * Run pre-existing processing pipelines
        * Add scripts to run custom pipelines
        * Do cross-dataset processing: running the same pipelines/versions on different datasets so that the outputs can be used together
    * Data tracking
        * Check processing failures and relaunch processing
        * Generate bagel files for Neurobagel

**Data users**
* People who use tabular, derivative or other files produced by `mr_proc` (e.g., from a shared `mr_proc`-compliant dataset)
* Example use cases:
    * Data tracking
        * Check availability of raw and/or derived data
        * Check which pipelines and version have been run
    * Data analysis
        * Extract imaging features for downstream analyses from specific pipelines/versions

## How does `mr_proc` work?

### Modules

1. `Code`: Codebase [repo](code_org.md) for running and tracking workflows
    * The codebase should start from the [`mr_proc` template repository](https://github.com/neurodatascience/mr_proc). Additional custom scripts need to be added to process specific datasets.
2. `Data`: [Dataset](data_org.md) organized in a specific directory structure
    * This contains the data only and should not contain any code
3. `Containers`: [Singularity/Apptainer](https://apptainer.org/) containers encapsulating processing pipelines

### Organization
Organization of `Code`, `Data`, and `Container` modules

![mr_proc_org](../imgs/mr_proc_org.jpg)

### Steps
The mr_proc workflow steps and linked identifiers (i.e. `participant_id`, `dicom_id`, `bids_id`) are shown below:

![mr_proc_steps](../imgs/steps.jpg)

## FAQ

1. Can `mr_proc` process my entire dataset out-of-the-box?
    * No: every dataset is different, and it is virtually impossible to have a workflow flexible enough to work with any dataset format or structure. However, once the imaging data is converted to a standard BIDS structure, running the image processing pipelines should be very straightforward.
2. Do I need to follow all the steps listed in the [example workflow](#example-workflow)?
    * No: the purpose of the example worflow is to illustrate what can be done with `mr_proc`, but you can choose to only use it for specific features (e.g., tracking).
3. Can I run `mr_proc` scripts in Windows/macOS?
    * `mr_proc` is designed to run on the Linux operating system, and will likely not work on other operating systems. This is mainly because it relies on Singularity, which [cannot run natively on Windows or macOS](https://apptainer.org/docs/admin/main/installation.html#installation-on-windows-or-mac). It is probably possible to use `mr_proc` with Windows/macOS (e.g., using virtual machines), but we do not recommend it.
4. Do I need to know how to use [Singularity](https://apptainer.org/)?
    * The `mr_proc` code repo contains scripts that call Singularity to run image processing pipelines. Users are not required to use Singularity directly, though we encourage users to learn about containers and/or Singularity if they are not familiar with these terms.
5. I want to use `mr_proc` with my own pipeline. Does it need to be containerized?
    * Although we recommend the use of containers to facilitate reproducibility, it is not a strict requirement. You can run your own pipelines any way you want (on the BIDS data or even raw data), though the outputs should be organized in the same way as the other pipelines (fMRIPrep, TractoFlow, etc.) if you want to use the tracking features.
6. What is [Neurobagel](https://www.neurobagel.org/) and do I need to use it?
    * Neurobagel is a data harmonization project that includes tools to perform cross-datasets searches for imaging data availability. You do not need Neurobagel for `mr_proc`, though some `mr_proc` outputs (specifically the `bagel` tracking files) can be used as input to some Neurobagel tools.
