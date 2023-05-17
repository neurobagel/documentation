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


