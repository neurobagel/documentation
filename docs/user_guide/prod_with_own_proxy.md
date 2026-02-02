If you already have a proxy server setup on your machine,
you need to make a few adjustments to the
standard deployment recipes described above.

!!! warning "Do not follow this section if you are using Neurobagel's [containerized proxy server](production_deployment.md#proxy-server)"

    If you are unfamiliar with managing and
    maintaining a bare-metal reverse proxy, you should use the
    [containerized proxy server](#proxy-server) provided with Neurobagel deployment recipes instead.
    
    We document how to run Neurobagel with an existing reverse proxy to help
    facilitate integration into established server setups. This type of deployment
    needs a good deal more manual configuration and maintenance.

!!! warning "**Do not** launch the [`proxy` deployment profile](production_deployment.md#proxy-server)"

    If you want to use your existing reverse proxy setup,
    make sure to not launch the [`proxy` deployment template](#proxy-server)
    provided by Neurobagel, or shut it down if you have already launched it.

## Follow the default setup

Deploying Neurobagel with an existing proxy server
is very similar to using the default deployment recipes.

Begin by following the default setup instructions for your
[desired deployment profile](production_deployment.md#deployment-profiles), but
**skip the final launch step** (i.e., skip "Launch node" or "Launch portal"):

- For a `node` deployment follow the [node setup](production_deployment.md#node)
- For a `portal` deployment follow the [portal setup](production_deployment.md#portal)

!!! note "Do not launch the default deployment template"

    Skip the launch step of the default deployment instructions. Deploying
    behind an existing proxy server requires a different docker compose file.
    Trying to launch a default deployment template without the
    [default proxy service](#proxy-server) running will most likely fail.

## Default ports of services

??? warning "Don't publicly expose service ports on a production server"

    We're providing the default ports as a reference for local deployment, testing, and for scenarios
    where you do not want to use the
    [provided reverse proxy deployment recipes](#proxy-server).
    
    Where possible, we **strongly recommend** that you avoid opening service ports to a public network
    and instead use our
    [reverse proxy deployment recipe](#proxy-server).

Neurobagel node services run inside Docker containers. Each service listens on an *internal port* within its container and
exposes a *host port* that makes it accessible from the host machine. Below, we list the default *host ports* for each service
when running in a fresh deployment,
along with the [environment variables](maintaining.md#environment-variables-reference) that can be used to configure them.

- `api` (the node API)
    - environment variable: `NB_NAPI_PORT_HOST`
    - default host port: `8000`
- `federation` (the federation API)
    - environment variable: `NB_FAPI_PORT_HOST`
    - default host port: `8080`
- `query_tool` (the graphical query web interface)
    - environment variable: `NB_QUERY_PORT_HOST`
    - default host port: `3000`
- `graph` (the internal graph database)
    - environment variable: `NB_GRAPH_PORT_HOST`
    - default host port: `7200`

## Set service host ports

??? info "Differences from the default deployment recipe"

    Unlike the default production Docker Compose file the deployment recipe for an
    existing proxy

    - **does not** expect an existing proxy Docker network to connect with
    - **does** expose the service ports to the host machine,
        so you can configure your existing proxy server
        to reach each service on `localhost` ports

In our modified deployment recipe for an existing proxy server,
Neurobagel services bind to [default ports](#default-ports-of-services)  
on the host. In your `.env` file, you can  
change these ports to avoid conflicts with existing services.
Simply uncomment and set the relevant `NB_<SERVICE>_PORT_HOST` variables.  
See [default ports](#default-ports-of-services)) for the list of port variables.

## Configure your existing reverse proxy

You must manually configure the existing reverse proxy on your machine for Neurobagel services.

For each service you deploy, this includes:

- configuring your reverse proxy routing rules so incoming
  requests are directed to the correct service under the appropriate domain/path
- provisioning and keeping SSL certificates up to date for each domain used to host
  the service

Please refer to the documentation of your existing reverse proxy server on
how to do this.

## Launch services behind your existing proxy

Ensure that you have correctly followed the setup instructions for your desired
[deployment profile](production_deployment.md#deployment-profiles). Then launch your services using the
`docker-compose.noproxy.prod.yml` compose file:

```bash
docker compose -f docker-compose.noproxy.prod.yml up -d
```
