The following sections will show you 
at a high level how to deploy and use the 
Neurobagel tools on your own hardware.
If you want to go more in depth on the technical
architecture and options to configure Neurobagel
for your use case, refer to [NOT YET MADE LINK]()

Whether you just want to try them out 
or deploy them for other users, 
the setup is the same.

## Prerequisites

Neurobagel tools are provided as Docker containers 
and are launched with docker compose. 

!!! danger "Don't install Neurobagel tools directly on your machine"
    
    Please only use the docker images provided by Neurobagel 
    (or the third party providers Neurobagel relies on) and only launch
    them with our provided `docker-compose.yml` recipe.

    Do not install graphDB locally on your computer, 
    as that can interfere with the deployment of the Neurobagel tools.

### `docker` and `docker compose` 
If you haven't yet, please install both `docker` and `docker compose`
for your operating system:

=== "Linux"

    Directly install `docker engine` 
    
    - [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
    - and then follow the post-setup instructions: [https://docs.docker.com/engine/install/linux-postinstall/](https://docs.docker.com/engine/install/linux-postinstall/)

    Next, install `docker compose`: 

    - [https://docs.docker.com/compose/install/linux/#install-using-the-repository](https://docs.docker.com/compose/install/linux/#install-using-the-repository)

=== "Windows"

    To install `docker` on Windows you can either:

    - install "Docker Desktop on Windows": [https://docs.docker.com/desktop/install/windows-install/](https://docs.docker.com/desktop/install/windows-install/) or
    - consider using [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install)
    to get a Windows supported Linux installation. You can then install `docker` using the Linux instructions

    If you install "Docker Desktop on Windows" you will also install `docker compose` automatically.

=== "MacOS"

    Install Docker Desktop on Mac: [https://docs.docker.com/desktop/install/mac-install/](https://docs.docker.com/desktop/install/mac-install/).
    If you install "Docker Desktop on Mac" you will also install `docker compose` automatically.

??? warning "Linux is the only supported OS"

    We test and deploy on Linux and ensure that our
    deployment instructions work on Linux systems.

    We also try to provide docs and help for different architectures,
    but as a small team with limited resources we won't be able to 
    help you debug Operating System specific problems. 

Because we rely on some modern features of these
tools, please make sure you have at least the following
versions on your machine:

- `docker` engine: [v20.10.24](https://docs.docker.com/engine/release-notes/20.10/) or greater
```bash
docker --version
```
- `docker compose`: [v2.0.0](https://github.com/docker/compose/releases/tag/v2.0.0) or above
```bash
docker compose version
```
### Get the neurobagel launch recipe

The [`neurobagel/recipes` repository](https://github.com/neurobagel/recipes) 
on GitHub contains our official
docker compose setup recipe. 

1. Clone the github repository to your machine and navigate to it
```bash
git clone https://github.com/neurobagel/recipes.git
cd recipes
```
2. Make copies of the template config files
```bash
cp template.env .env
cp local_nb_nodes.template.json local_nb_nodes.json
```
3. Change `NB_API_QUERY_URL` in the `.env` file 

    You **must** replace the placeholder value for `NB_API_QUERY_URL`in the `.env` file
    
    ```bash
    NB_API_QUERY_URL=http://XX.XX.XX.XX
    ```
    with the address of the machine you are going to deploy Neurobagel on.

    - If you are deploying Neurobagel **for yourself** or just to try things out locally, 
   you can use: `NB_API_QUERY_URL=http://localhost:8080` 
    where `:8080` is the default port for the federation API.
    - If you are deploying Neurobagel on a server for other users, 
   you **must** use the IP (and Port) or URL that your users will access the server with. 
   
!!! info

    This is the minimal configuration you need to make before you can launch Neurobagel.
    In most cases, and especially when you are deploying Neurobagel for other users,
    you will have to make additional configurations. 

    Please refer to [our detailed documentation]() for a complete overview of 
    configuration options.

## Launch Neurobagel

Once you have configured your Neurobagel deployment by editing the `.env`
and optionally the `local_nb_nodes.json` file, you can launch the Neurobagel
tools using `docker compose` like this: 

```bash
docker compose --profile full_stack up -d
```

this will:

- pull the correct docker images (if you haven't pulled them before)
- launch the Neurobagel services
- automatically setup and configure the services for you
- automatically upload data to the Neurobagel graph (we provide example data for testing purposes)

You can check that your docker containers have launched correctly by running:

```bash
docker ps
```
and you will want to see something like this to show all 4 services running:
```bash
❯ docker ps
CONTAINER ID   IMAGE                              COMMAND                  CREATED         STATUS         PORTS                                                 NAMES
d5e43f9ff0c2   neurobagel/federation_api:latest   "/bin/sh -c 'uvicorn…"   8 seconds ago   Up 8 seconds   0.0.0.0:8080->8000/tcp, :::8080->8000/tcp             recipes-federation-1
f0a26d0ea574   neurobagel/api:latest              "/usr/src/api_entryp…"   8 seconds ago   Up 8 seconds   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp             recipes-api-1
d44d0b7359c8   ontotext/graphdb:10.3.1            "/usr/src/neurobagel…"   8 seconds ago   Up 8 seconds   0.0.0.0:7200->7200/tcp, :::7200->7200/tcp, 7300/tcp   recipes-graph-1
29a61a2d83de   neurobagel/query_tool:latest       "/bin/sh -c 'npm run…"   8 seconds ago   Up 8 seconds   0.0.0.0:3000->5173/tcp, :::3000->5173/tcp             recipes-query_federation-1
```

The `docker-compose.yml` recipe provides additional profiles
for specific deployment use cases. Please refer to
our [detailed profile documentation]() for details.

## Next steps

:tada: You are now the proud owner of a running Neurobagel stack. Here are some things you can do now:

- Try your own query tool (e.g. [http://localhost:3000](http://localhost:3000)) and read about the [query tool](./query_tool.md) guide
- [Prepare your own dataset](./data_prep.md) for Neurobagel
- [Annotate your own data](./annotation_tool.md) with the Neurobagel Annotator
- Add your own data to your Neurobagel graph to search: [TODO Link]()
- Learn about the different configuration options in Neurobagel: [TODO link]()
- Hopefully all went well, but if you are experiencing issues: 
  - Look at our [TODO FrequentlyAskedQuestions]()
  - and if that doesn't help: [TODO open an issue]()
- Say hello on our discord: [TODO Discord]()