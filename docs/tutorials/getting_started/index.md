---
layout: default
parent: tutorials
title: getting started
nav_order: 1
has_children: true
---

# getting started
{: .no_toc }

<details open markdown="block">
  <summary>
    table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>


## welcome

welcome to the 'getting started' tutorial.

this tutorial is designed for anyone who has not yet used fdrtd.    

in case you have any questions, need help, or want to give feedback, please contact [support@fdrtd.com](mailto:support@fdrtd.com).

## overview

### learning goals

in this 5-minute tutorial, you are going to learn to
1. install and run a fdrtd server locally
2. install the fdrtd client on your machine
3. connect to the server's API
4. find a microservice on the server
5. remotely execute a microservice

### metadata

* **level:** beginner
* **natural language:** English
* **programming language:** Python
* **operating system:** OS independent
* **industry/function:** all
* **intended audience:** all

### prequisites

to complete this tutorial, you need
* basic understanding of the Python programming language.
* basic understanding of your system's command line shell.

to execute the steps on your system, it needs
* Python 3.x, from [www.python.org/downloads/](https://www.python.org/downloads/).
* a web browser

---

## 1. install and run a fdrtd server locally

fdrtd is a client-server architecture. we will send commands from a client to a server, and the server will execute microservices for us.
so the first step is to get a server up and running.

### installation

* open a console
* clone the fdrtd server: `git clone https://github.com/fdrtd/server`
* change directory to the new `server` directory.
* add some basic microservices: `git clone https://github.com/fdrtd/plugin_basics`

### deployment

* in the `server` directory, run: `python -m openapi_server -port:55500`
* we will let this server run in the background for the time being
* in your web browser, visit `localhost:55500`
* do you see some output? if yes, your fdrtd server is running and ready to serve your requests

## 2. install the fdrtd client on your machine

you could use your web browser to interact with your fdrtd server, but we want to write Python programs using its microservices.
to do so, we need to install the fdrtd client which is basically a library of functions making it easy to interact with the server.

* open a new console (the first console still has the server running)
* use Python's package manager to install the libary: `pip install fdrtd` (you might need admin/sudo privileges for this)

## 3. connect to the server's API

* run your Python interpreter, e.g. `python`
* the following commands are entered in the Python console:
* import the fdrtd client library: `import fdrtd`
* use the built-in HTTP interface with the URL and port of your local server: `interface = fdrtd.HttpInterface("http://localhost:55500")`
* create an API object using the HTTP interface: `api = fdrtd.Api(interface)`
* check if the connection is working: `api.list_microservices()`
* are you seeing a similar output as in the web browser before or like below?

```
[{'identifiers': {'microservice': 'KeyValueStorage', 'namespace': 'fdrtd', 'plugin': 'Basics', 'version': '0.2.0'}}]
```

## 4. find a microservice on the server

the list of microservices contains one by the name of 'KeyValueStorage'. it is provided by the 'plugin_basics' we have installed on our server.

* to select it, we need to use named arguments: `kvstorage = api.select_microservice(microservice='KeyValueStorage')`

## 5. remotely execute a microservice

the local object `kvstorage` is a handle to the microservice on the server. we can treat it like it had all the member functions of that microservice itself:

* let's put a value ('Peter') into a new storage ('Names'): `name = kvstorage.create(value='Peter', storage='Names')`
* let's try to read that value back: `name.retrieve()`


## cleanup

* always clean up your sensitive data: `name.delete()`
* check if the data has been wiped: `name.exists()`
* you can exit the Python console by: `exit()`
* in the other console, remember to terminate the running server (depending on your system, e.g. Ctrl+C)


## conclusion

did you get the answer 'Peter' from the server? excellent work.

you have successfully installed the fdrtd server and client and remotely executed microservices on the server.
