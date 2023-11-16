So you want to federate?


!!! TODO

    Put a figure here to show how the f-API comes into play.
    e.g. from Miro

## When would you want to do this
These notes are only for a case where you are deploying neurobagel nodes locally,
e.g. in your own institute network.

There are two main reasons to set up federation locally:

- you have a local node, but you want your users to also be able to see external public data
- you have several local nodes, and you want your local users to search over them at the same time.
e.g. if you have several PIs in an institute.

## How to
You need to first have at least one local neurobagel node API with a graph backend deployed. 
Here are the docs for these steps: 

1. Spin up a n-API, graph, and query tool using docker-compose
2. docker pull the f-API image
3. before you run the f-API container, make a `.federation_env` file based on this example:


```bash
API_URL=http://localhost:8000
API_TYPE=federate
```

This is so we now know what API is running


```
docker pull neurobagel/federation_api

# Make sure to run the next command in the same directory where your .env file is
docker run -d --name=federation -p 8080:8000 --env-file=.env neurobagel/federation_api
```

Now your f-API is running, we need to tell your query tool about it:

1. Shut down your query tool that is already deployed: `docker stop query-tool`
2. Change the following value in the `.env` file of the query tool: `API_TYPE=federate`
3. Relaunch the query tool `docker start query_tool`

Now your query tool should be running against the f-API. 
You can confirm that by doing XYZ

!!! TODO

    what's the best way to confirm we're running against a f-API here?