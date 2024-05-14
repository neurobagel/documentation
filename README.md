# documentation
The neurobagel documentation.

Our docs are built with the [Material Theme](https://squidfunk.github.io/mkdocs-material/) for [MKdocs](https://www.mkdocs.org/).


## Setup
Create a new virtual environment with `python -m venv venv` and activate it.
Then install the dependencies with `pip install -r requirements.txt`

## Build

To spin up the side locally while you edit it, run:

`mkdocs serve`

More details are in the [mkdocs documentation](https://squidfunk.github.io/mkdocs-material/creating-your-site/#previewing-as-you-write).

## Deploy

At the moment we are using mkdocs to deploy directly to gh-pages.

When your local build runs well, commit the changes to the `main` branch with a PR and then call

```bash
mkdocs gh-deploy
```

See the [docs for more details](https://www.mkdocs.org/user-guide/deploying-your-docs/).

## Installing tailwind

To install tailwind, run:

```bash
npm i
```

## Rebuilding tailwind

If you need to rebuild the tailwind css, run:

```bash
npx tailwindcss build docs/stylesheets/tailwind.css -o docs/stylesheets/output.css
```