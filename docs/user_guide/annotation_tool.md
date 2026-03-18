# The Neurobagel Annotation Tool

The Neurobagel annotation tool creates standardized, machine-readable data dictionaries for tabular data using curated FAIR vocabularies. The tool helps to harmonize tabular research data and is compatible with BIDS datasets.

**Workflow summary**:

1. Upload tabular data
2. Column annotation
3. Value annotation
4. Download data dictionary

## 1. Upload tabular data

![Annotation tool upload step screenshot](../imgs/annotate/upload.png)

- **Upload your [data table](data_prep.md)** (.tsv file)
    - Can be `participants.tsv` from a BIDS dataset
- **Optional**: Upload an existing data dictionary (.json file) for extra context
    - Can use `participants.json` from a BIDS dataset
    - Or continue previous Neurobagel annotation work

In the following steps, you will annotate your table by first describing the columns and then the values within the columns.

## 2. Column Annotation

![Annotation tool column annotation step screenshot - non-assessment variables](../imgs/annotate/column_annotation_non-assessment.png)

Each column in your uploaded table is represented as a card on the left side of this page.
Select a column to annotate it.

!!! tip
    To select multiple columns, hold down ++shift++ , ++ctrl++ , or ++cmd++ .

For each column, you can:

- **Add a description**
- **Annotate the [standardized variable](../data_models/variables.md) that best describes the column from the "Standardized Variables" list on the right** (if a suitable match exists)
    - To map one or more columns to a specific standardized variable, select the column(s) and then select the corresponding variable name
    - The number next to a standardized variable (:material-numeric-1-circle:) indicates how many columns are currently mapped to it

    !!! info "Some standardized variables only allow 1 mapped column"
        A standardized variable with a limit of 1 mapped column will appear disabled in the right sidebar once a column has been mapped to it.
        To map a different column to the variable, first clear the mapping for the old column.

- **Annotate the assessment tool used to collect the column's data from the "Assessment Tool" list on the right** (if a suitable match exists)
    - For columns about an assessment tool, select the column(s) and then select the corresponding assessment term

- **Annotate the data type**
    - To indicate the data type of the selected column(s), use the "Map Data Type" buttons
    - Choose "Categorical" if the column contains discrete values, "Continuous" if it contains numerical measurements, or leave it empty if neither applies
    - Columns mapped to certain standardized variables will have their data type inferred automatically

    !!! tip "When to manually annotate data type"
        We recommend manually selecting the data type in two cases:

        1. When your column doesn't match any standardized variable
        2. When your column corresponds to an assessment tool (since a single assessment can be represented by multiple columns with different data types, no default data type is assumed)

### If your dataset has imaging (BIDS) data

The "Participant ID" standardized variable **must** be mapped to a column that contains the BIDS IDs for subjects, following the BIDS naming scheme `sub-<label>`.

For more information, see [this section](data_prep.md#if-your-dataset-has-imaging-bids-data) on preparing the phenotypic data table for a BIDS dataset.

## 3. Value Annotation
![Annotation tool value annotation step screenshot](../imgs/annotate/value_annotation.png)

The left sidebar displays the standardized variables that are represented in your tabular data, along with the column names that have been mapped to those variables.

Click on a standardized variable (or data type, for unannotated columns) subheading in the sidebar to display the columns corresponding to that variable (or data type).
Then, in the column-level view on the right, navigate between the column tabs to annotate the values within each column.

??? note "Understanding sidebar sections"
    The sidebar organizes your columns by their annotation status:

    - **Annotated** contains columns you have mapped to standardized variables
    - **Unannotated** contains columns you have not mapped to a standardized variable
        - Within this section, unannotated columns are organized based on whether you have assigned them a data type

[^1]: Attribute can only be annotated if the column has been mapped to a standardized variable.

### Columns with continuous data

For a column containing continuous data, you can:

- Add a description of the units of measurement
- Select the format of the numerical values[^1]
- Select "Mark as missing" for any values that represent missing, unavailable, or invalid data[^1]
    - Note: the column-level view will only display unique values in the column

??? info "Units vs. Format"
    **Format** refers to how the numeric values in your data are expressed (e.g., `float` for decimal numbers like 25.5, `range` for numeric ranges like 30-35) whereas **Units** describe what the numbers represent (e.g., "years" for age, "points" for test scores, "mg/dL" for measurements).

### Columns with categorical data

For a column containing categorical data, you will be prompted to annotate the unique values detected in the column.
This includes any values that are blank (empty strings) or contain only whitespace.

For each unique column value, you can:

- Add a free-form description of the value
- Select a standardized term that best captures the meaning of the value[^1]
- Select "Mark as missing" if the value:[^1]
    - indicates missing, unavailable, or invalid data
    - OR, does not have a suitable match among the standardized term options

!!! warning
    For the value annotation to be considered complete by Neurobagel, all unique values must either be mapped to a standardized term or marked as missing.

## 4. Download data dictionary
![Annotation tool download step screenshot](../imgs/annotate/download.png)

- **Preview** your annotated data dictionary
- **Download** the data dictionary `.json` file
- **Annotate a new dataset** if desired

!!! tip
    If you see a warning about "Incomplete Annotations", you will need to return to the Value Annotation page to complete any missing annotations before your data dictionary is valid for downstream Neurobagel tools.

Your downloaded data dictionary is BIDS-compatible and, if you see the confirmation that you have successfully created a Neurobagel data dictionary, it is ready to be used to [generate data for a Neurobagel graph database](https://neurobagel.org/user_guide/cli/).
