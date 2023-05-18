# SysAdmin

These instructions are for a sysadmin looking to deploy Neurobagel locally in an institute or lab.

## Ecosystem

The Neurobagel ecosystem consists of four tools:

- the **annotation tool** 
    - to create harmonized annotations of phenotypic data
    - intended for use by researchers and domain experts
    - static site, deployed on Github Pages
    - [annotate.neurobagel.org](https://annotate.neurobagel.org)
- the **CommandLineInterface** 
    - to extract metadata from annotated phenotypic and BIDS data
    - intended for data managers to create graph ready data
    - [neurobagel/bagel-cli](https://github.com/neurobagel/bagel-cli)
- the **graph and API**
    - to store and query extracted metadata
    - intended for platform owners and for isolated deployments
    - [api.neurobagel.org](https://api.neurobagel.org)
- The **query tool**
    - to create cohort queries and display results
    - intended for use by researchers and data consumers
    - static site, deployed on Github Pages
    - [query.neurobagel.org](https://query.neurobagel.org)


??? Todo

    Add Neurobagel figure for overview.

## Get a license for Stardog

We use Stardog as our Graph store application. 
Stardog has a free, annually renewable license for academic use.
In order to make a separate deployment of Neurobagel, 
you should therefore first request your own Stardog license.
You can request a Stardog license here:

[https://www.stardog.com/license-request/](https://www.stardog.com/license-request/)

!!! danger "Don't pick the wrong license"

    Stardog is a company that offers their graph store solutions both as a self-hosted,
    downloadable tool (what we want) and as a cloud hosted subscription model (what we do not want). Both tiers offer free access and the website has a tendency to steer
    you towards the cloud offering. Make sure you request a **license key** for Stardog.

![This is what requesting the license would look like](imgs/stardog_request.png)

The Stardog license is typically automatically granted via email in 24 hours. 

The license you receive will be a downloadable file. 
It is valid for one year and for a major version of Stardog.
You will need to download the license in a place that is accessible
to your new Stardog instance when it is launched (see below).


## Launch the API and Graph stack

Please [follow the instructions here](https://github.com/neurobagel/api/blob/main/README.md#docker) 
to pull the API and Stardog Docker images
and then launch both via `docker compose` (Option 1).

Your license file has to be in the `STARDOG_HOME` directory.

## Setup for the first run

When you launch the Stardog graph for the first time,
there are a couple of setup steps that need to be done. 
These will not have to be repeated for subsequent starts.

To intereact with the Stardog graph, 
you have two general options:

1. Send HTTP request against the HTTP API of the Stardog graph instance (e.g. with `curl`). See [https://stardog-union.github.io/http-docs/](https://stardog-union.github.io/http-docs/) for a full reference of API endpoints
2. Use the free Stardog-Studio web app. See the [Stardog documention](https://docs.stardog.com/stardog-applications/dockerized_access#stardog-studio) for instruction to deploy Stardog-Studio as a Docker container.


!!! info 
    Stardog-Studio is the most accessible way 
    of manually interacting with a Stardog instance. 
    Here we will focus instead on using the HTTP API for configuration,
    as this allows programmatic access.
    All of these steps can also be achieved via Stardog-Studio manually.
    Please refer to the 
    [official docs](https://docs.stardog.com/stardog-applications/studio/) to learn how.
