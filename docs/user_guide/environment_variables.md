??? warning "Ensure that shell variables do not clash with variables in `.env`"
    The Neurobagel deployment recipe reads environment variables from a `.env` file
    generated automatically by the [Neurobagel configuration wizard](production_deployment.md#install-the-neurobagel-configuration-wizard) from your `nb_config.ini` configuration file.

    If the shell you run `docker compose` commands from already has any
    shell variable of the same name set,
    the shell variable will take precedence over the `.env`!
    In this case, make sure to `unset` the local variable(s) first.

    For more information, see [Docker's environment variable precedence](https://docs.docker.com/compose/environment-variables/envvars-precedence/).

!!! tip
    After running `configure-nb` to configure your deployment, double check that any variables you have customized are resolved with your expected values by running the command `docker compose config` in the directory with the generated `.env`.

Below are all possible configuration variables for a Neurobagel deployment.
Note that `quickstart` indicates whether the variable has an effect in a default test deployment.

{{ define_all_env_vars() }}
