The public query tool at [query.neurobagel.org](https://query.neurobagel.org)
queries the public Neurobagel federation API at [federate.neurobagel.org](https://federate.neurobagel.org)
which provides access to all publicly accessible Neurobagel nodes.

To start running your own cohort queries, 
all you have to do is visit [query.neurobagel.org](https://query.neurobagel.org),
enter your cohort criteria into the web interface, and click the "Submit" button.

## Public Neurobagel Nodes

At the moment, the following public Neurobagel nodes are available 
(you can query a specific node by selecting it from the dropdown under "Neurobagel graph" in the query tool):

- **OpenNeuro**. This node contains a (growing) subset of the datasets on [OpenNeuro](https://openneuro.org/).
  The datasets you can find in this node have been annotated by the community and live in the
  [OpenNeuroDatasets-JSONLD](https://github.com/OpenNeuroDatasets-jsonld) GitHub organization.
- **International Neuroimaging Data-sharing Initiative** (INDI): This node contains public datasets from the [INDI](https://fcon_1000.projects.nitrc.org/) project.
  At the moment, the following datasets are queryable in the INDI node:
    - [ABIDE 1](https://fcon_1000.projects.nitrc.org/indi/abide/abide_I.html)
    - [ABIDE 2](https://fcon_1000.projects.nitrc.org/indi/abide/abide_II.html)
    - [ADHD 200](https://fcon_1000.projects.nitrc.org/indi/adhd200/)
    - [Consortium for Reliability and Reproducibility](https://fcon_1000.projects.nitrc.org/indi/CoRR/html/) (CoRR) datasets.
- **Quebec Parkinson Network**: This node contains the [Quebec Parkinson Network](https://rpq-qpn.ca/en/home/) datasets.
  Unlike the other two public nodes, the Quebec Parkinson Network node will not return participant level details.

All nodes except for the Quebec Parkinson Network node allow you to download both participant-level information
and the corresponding imaging data (where available) for the cohorts you search. 
Downloading of imaging data is performed via [datalad](https://rpq-qpn.ca/en/home/).

## Private Neurobagel nodes

Nodes that are not purposefully made public are not accessible 
outside of the institute or network where they are deployed.
If you are interested in deploying a Neurobagel node for your institution,
please refer to our [deployment documentation](guide/getting_started.md) for more information.