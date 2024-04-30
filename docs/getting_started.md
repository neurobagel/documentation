If you want to just get an idea of what Neurobagel does:

- take a look at our [Overview page](./overview.md),
- try out the [Annotation tool](https://annotate.neurobagel.org/)
- and [Query tool](https://query.neurobagel.org/)
- or look at our [high level slide deck](https://docs.google.com/presentation/d/1dyRJkJWVwEBSU5CPqj-GuD5Jw_csltOULvGqVswycGc/edit?usp=sharing)

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
### Get neurobagel launch recipe

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
cp local.nb_nodes.template.json local.nb_nodes.json  
```
3. Edit the config files
```bash
ls
```


## Launch Neurobagel

### Profile 1
```bash
docker compose --profile full_stack up -d
```
### Profile 2
