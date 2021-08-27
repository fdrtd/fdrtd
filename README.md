![license](https://img.shields.io/github/license/fdrtd/fdrtd)
![swagger-validator](https://img.shields.io/swagger/valid/3.0?specUrl=https%3A%2F%2Fraw.githubusercontent.com%2Ffdrtd%2Ffdrtd%2Fmain%2Fapi%2Fopenapi.yaml)


# description

**fdrtd** is a free and open source implementation of **federated secure computing**,
a modern microservice architecture for privacy-preserving computation:

- [x] multi-protocol technology platform (e.g. secure multipary computation)
- [x] cryptography is offloaded to the server/cloud (separation of concerns)
- [x] client-side business logic is easy to implement (no barriers to entry)
- [x] toolbox of specific microservices (no complex monolithic universality)
- [x] runs in virtually any environment (compatibility and interoperability)
- [x] OpenAPI 3.0 standard for 3rd party developers (plug & play extensions)


# getting started

to run a **fdrtd** server, clone this repo and start the included webserver:

    git clone https://github.com/fdrtd/fdrtd
    python -m fdrtd.webserver --port=55500

you can interact with the server through your browser:

[localhost:55500/ui](http://localhost:55500/ui)


# resources

* developer documentation: [fdrtd.github.io/fdrtd](https://fdrtd.github.io/fdrtd)
* project website: [www.fdrtd.com](https://www.fdrtd.com)
* support by email: [support@fdrtd.com](mailto:support@fdrtd.com)


# how to report bugs

please [open an issue](https://github.com/fdrtd/fdrtd/issues/new)


# license

**fdrtd** is free and open source software under the MIT license.
see the [`LICENSE`](https://github.com/fdrtd/fdrtd/tree/main/LICENSE) file for more information.
