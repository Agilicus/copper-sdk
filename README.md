# Copper CRM SDK

Unofficial Copper CRM SDK written in Python

## Official API docs

[https://developer.copper.com/?version=latest#intro](https://developer.copper.com/?version=latest#intro)

## User Guide

### The entrypoint

To make any API via the SDK, you first need to create an instance of the Copper class, configured correctly with your email and Copper API token. This is essentially the entrypoint into using the SDK.

```
from copper_sdk import copper

copper = copper.Copper(
    email = 'joe@bloggs.com`,
    token = 'abc123
)
```

### Making API calls uisng the SDK

All the root entities modelled by the Copper API are modelled as separate classes in this SDK. The currently supported root entities are:

* Users
* Activities
* Companies
* People
* Leads
* Opportunities
* Custom Fields

Each entity has a corresponding python class with the same name and an entrypoint to each of the entities can be retrieved via the main SDK entrypoint, e.g. to make API calls relating to activities:

```
from copper_sdk import copper

copper = copper.Copper(
    email = 'joe@bloggs.com`,
    token = 'abc123
)

all_activities = copper.activities().list()
```

### Request and response bodies

This library does not do any translation of request and response bodies, and merely maps JSON payloads to and from python dictionaries. Therefore, you can construct request bodies as dictionaries that correspond directly with the JSON request bodies defined within the official Copper [API documentation](https://developer.copper.com/?version=latest#intro). And response bodies will be dictionaries directly mapping to the structure of JSON responses as per the official Copper [API documentation](https://developer.copper.com/?version=latest#intro). Please refer to the [documentation](https://developer.copper.com/?version=latest#intro) for details for the structure of request and response bodies.

An example that demonstrates supplying a request body when searching for activities:

```
all_activities = copper.activities().list({
    page_number: 2,
    page_size: 50
})
```

## Developing the library

### Running tests

This library does not currently perform any testing of request bodies and response bodies. At the moment python dictionaries are mapped directly to and from JSON. So, it's really up to users of the library to ensure request bodies are formed as dictionaries as per the official Copper [API documentation](https://developer.copper.com/?version=latest#intro). The scope of the tests is currently to simply make sure the core of the library behaves as expected (e.g. constructs requests using the required HTTP headers).

To force the API to make actual calls, delete the cached responses in the tests/vcr_cassettes directory.

```
# install depds
$ pipenv install
# enter shell
$ pipenv shell
# run tests
$ COPPER_API_TOKEN='<my copper token>' COPPER_API_EMAIL='<my copper email>' pytest
```
