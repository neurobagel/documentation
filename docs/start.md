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


## Getting started

### Get a license for the graph store

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
