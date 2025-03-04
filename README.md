# Neurobagel Documentation

![GitHub branch check runs](https://img.shields.io/github/check-runs/neurobagel/documentation/main?style=flat-square)
![Static Badge](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue?style=flat-square&logo=python)
![GitHub License](https://img.shields.io/github/license/neurobagel/documentation?style=flat-square&color=purple&link=LICENSE)

The neurobagel documentation.

Our docs are built with the [Material Theme](https://squidfunk.github.io/mkdocs-material/) for [MKdocs](https://www.mkdocs.org/).


## Setup
Create a new virtual environment with `python -m venv venv` and activate it.
Then install the dependencies with `pip install -r requirements.txt`

## Adding new pages to the navigation
We use [`mkdocs-awesome-nav`](https://lukasgeiter.github.io/mkdocs-awesome-nav/) to define the navigation structure of the docs.

To add a new page to the navigation, add it to the `.nav.yml` (structured the same way as the `nav` section of `mkdocs.yml`) of the directory the markdown file lives in.

To add an entire subdirectory (section) of pages, you can simply specify the subdirectory name. 
Each subdirectory can then itself contain a `.nav.yml` to organize the pages within.

Note: Both relative and absolute paths can be used to specify files or directories in `.nav.yml`.

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