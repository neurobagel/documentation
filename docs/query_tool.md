# The Neurobagel Query Tool

Neurobagel's query tool is a web interface for searching across a Neurobagel graph based on various subject clinical-demographic and imaging parameters.

The query tool is a Vue application, developed in [JavaScript](https://www.javascript.com/) using a variety of tools including [Nuxt](https://nuxtjs.org/), [Cypress](https://www.cypress.io/), and [BootstrapVue](https://bootstrap-vue.org/docs).

## Quickstart

The query tool is hosted at https://query.neurobagel.org/ and interfaces with [Neurobagel API](https://api.neurobagel.org/docs).

NOTE: Currently, to access the query tool, you must be connected to the McGill network.

## Local Installation

### Install Dependencies

To run the query tool, you'll need [node package manager (npm)](https://www.npmjs.com/) and [Node.js](https://nodejs.org/en/).
You can find the instructions on installing npm and node in the official [documentation](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

Once you have npm and node installed, you'll need to install the dependencies outlined in the package.json file.
You can do so by running the following command:

```bash
npm install
```

**use node v16.x LTS**!

:warning: 
The query tool is built with the Nuxt framework and currently depends on Nuxt2. 
Nuxt2 does not support node versions beyond the v16 LTS (see e.g. [this Github issue](https://github.com/nuxt/nuxt/issues/10844)).
If you want to run the tool locally, make sure you are using node v16.x.
A good way to manage different node versions is to use the [node version manager](https://github.com/nvm-sh/nvm) tool.

### Set the Environment Variables

You'll need to set the `API_QUERY_URL` environment variable required to run the query tool. `API_QUERY_URL` is the [Neurobagel API](https://github.com/neurobagel/api) URL that the query tool uses to send requests to for results. The query tool utilizes [nuxt dotenv module](https://github.com/nuxt-community/dotenv-module) for managing environment variables. 

To set environment variables, create an `.env` file in the root directory and add the environment variables there. If you're running the API locally on your machine (following the instructions [here](https://github.com/neurobagel/api#local-installation)), your `.env` file would look something like this:

```bash
API_QUERY_URL=http://localhost:8000/
```

if you're using the remote api, your `.env` file would look something like this:

```bash
API_QUERY_URL=https://api.neurobagel.org/
```

### Launch the Query Tool

To launch the tool in developer mode run the following command:

```bash
npm run dev
```

You can also build and then run the tool from the (production) build of the application by running the following command:

```bash
npm run build && npm run start
```

You can verify the tool is running once you receive info messages from Nuxt regarding environment, rendering, and what port the tool is running on in your terminal.

## Usage

To define a cohort, set your inclusion criteria using the following:

- Age: Minimum and/or maximum age (in years) of participant that should be included in the results.
- Sex: Sex of participant that should be included in the results.
- Diagnosis: Diagnosis of participant that should be included in the results
- Healthy control: Whether healthy participants should be included in the results. Once healthy control checkbox is selected, diagnosis field will be disabled since a participant cannot be both a healthy control and have a diagnosis.
- Minimum number of sessions: Minimum number of imaging sessions that participant should have to be included in the results.
- Assessment tool: Non-imaging assessment completed by participant that should be included in the results.
- Modality: Imaging modality of participant scans that should be included in the results.


Once you've defined your criteria, submit them as a query and the query tool will display the results.
The query tool offers two different TSV files for results:

- Dataset-level results TSV contains: dataset id, dataset name, dataset portal uri, number of matching subjects, and available imaging modalities
- Participant-level results TSV contains: dataset id, subject id, age, sex, diagnosis, assessment, session id, session file path, number of sessions, and imaging modality

The output files can be joined using `DatasetID` as key.