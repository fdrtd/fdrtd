![license](https://img.shields.io/github/license/fdrtd/fdrtd)
![swagger-validator](https://img.shields.io/swagger/valid/3.0?specUrl=https%3A%2F%2Fraw.githubusercontent.com%2Ffdrtd%2Ffdrtd%2Fmain%2Ffdrtd%2Fapi%2Fopenapi.yaml)
![CodeQL](https://github.com/fdrtd/fdrtd/workflows/CodeQL/badge.svg)
![unittest](https://raw.githubusercontent.com/fdrtd/fdrtd/main/.github/badges/tests.svg)
![Pylint](https://raw.githubusercontent.com/fdrtd/fdrtd/main/.github/badges/pylint.svg)


# acknowledgements

development of `fdrtd` is being financed by a generous grant by [Stifterverband](https://www.stifterverband.org/english).

the team is also thankful for administrative and technical support by [LMU](https://www.lmu.de/en/index.html) and [LRZ](https://www.lrz.de/english/).


# description

`fdrtd` is a free and open source implementation of **federated secure computing**,
a modern microservice architecture for privacy-preserving computation:

- [x] multi-protocol technology platform (e.g. secure multipary computation)
- [x] cryptography is offloaded to the server/cloud (separation of concerns)
- [x] client-side business logic is easy to implement (no barriers to entry)
- [x] toolbox of specific microservices (no complex monolithic universality)
- [x] runs in virtually any environment (compatibility and interoperability)
- [x] OpenAPI 3.0 standard for 3rd party developers (plug & play extensions)


# server-side installation

## without docker

to install `fdrtd` on the server, use `pip` or a similar tool: `pip install fdrtd`

to run the server, execute the module and provide a port: `python -m fdrtd.webserver --port=55500`

once the server is up, a list of available services can be found at [localhost:55500/representations](http://localhost:55500/representations)

## with docker

use the [Docker](https://github.com/fdrtd/fdrtd/tree/main/packages/docker/Docker)
file in [/packages/docker/](https://github.com/fdrtd/fdrtd/tree/main/packages/docker/)
to run one server in a detached docker container, e.g. on port 55500:

```console
docker build -t webserver .
docker run -d -p 55500:55500 --name webserver webserver
```

stop the container with `docker kill webserver`. there is also a sample configuration [docker-compose.yml](https://github.com/fdrtd/fdrtd/tree/main/packages/docker/docker-compose.yml)
for three servers at ports 55501, 55502, and 55503. run these with `docker-compose up` and stop them with `docker-compose down`


# client-side usage

to install `fdrtd` on the client, use `pip` or a similar tool: `pip install fdrtd`

for example, view the list of available servers:

```python
import fdrtd.clients.python

api = fdrtd.clients.python.Api("http://localhost:55500")
list_of_services = api.list()
print(list_of_services)
```


# resources

* developer documentation: [fdrtd.github.io/fdrtd](https://fdrtd.github.io/fdrtd)
* project website: [www.fdrtd.com](https://www.fdrtd.com)
* support by email: [support@fdrtd.com](mailto:support@fdrtd.com)


# how to report bugs

please [open an issue](https://github.com/fdrtd/fdrtd/issues/new)


# license

`fdrtd` is free and open source software under the MIT license.
see the [LICENSE](https://github.com/fdrtd/fdrtd/tree/main/LICENSE) file for more information.

`fdrtd` is a registered trademark by [bytes for life GmbH](https://www.bytesforlife.com), Munich, Germany.
