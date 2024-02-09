## Glossary

This page lists some definitions for important/recurring terms used in the Nipoppy framework.

### `participant_id`

**Appears in**: `manifest.csv`, `doughnut.csv`

:   Unique identifier for the participant (i.e., subject ID), as provided by the study.

### `datatype`

**Appears in**: `manifest.csv`

:   A BIDS-compliant "data type" value (see the [BIDS specification website](https://bids-specification.readthedocs.io/en/stable/common-principles.html#definitions) for a comprehensive list). The most common data types for magnetic resonance imaging (MRI) data are `"anat"`, `"func"`, and `"dwi"`.

### `visit`

**Appears in**: `manifest.csv`

:   An identifier for a data collection event, not restricted to imaging data.

See also: [`session` vs `visit`](#session-vs-visit)

### `session`

**Appears in**: `manifest.csv`, `doughnut.csv`

:   A BIDS-compliant session identifier. Consists of the `"ses-"` prefix followed by the [`session_id`](#session_id).

#### [`session`](#session) vs [`visit`](#visit)

Nipoppy uses `session` for imaging data, following the convention established by BIDS. The term `visit`, on the other hand, is used to refer to any data collection event (not necessarily imaging-related). In most cases, `session` and `visit` will be identical (or `session`s will be a subset of `visit`s). However, having two descriptors becomes particularly useful when imaging and non-imaging assessments do not use the same naming conventions.

### `participant_dicom_dir`

**Appears in**: `doughnut.csv`

:   The name of the directory in which the raw DICOM data (before the DICOM organization step) are found. Usually, this is the same as [`participant_id`](#participant_id), but depending on the study it could be different.

### `dicom_id`

**Appears in**: `doughnut.csv`

:   The [`participant_id`](#participant_id), stripped of any non-alphanumerical character. For studies that do not use non-alphanumerical characters in their participant IDs, this is exactly the same as [`participant_id`](#participant_id).

### `bids_id`

**Appears in**: `doughnut.csv`

:   A BIDS-compliant participant identifier. Obtained by adding the `"sub-"` prefix to the [`dicom_id`](#dicom_id), which itself is derived from the [`participant_id`](#participant_id). A participant's raw BIDS data and derived imaging data are stored in directories named after their `bids_id`.

