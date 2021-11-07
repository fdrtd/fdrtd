---
layout: default
parent: tutorials
title: secure sum
nav_order: 2
---

# secure sum
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

welcome to the 'secure sum' tutorial.

this tutorial is designed for anyone who has not yet run secure computations with fdrtd. 

in case you have any questions, need help, or want to give feedback, please contact [support@fdrtd.com](mailto:support@fdrtd.com).

## overview

### learning goals

in this 15-minute tutorial, you are going to learn to
1. describe a peer-to-peer network
2. connect to public test servers
3. start a secure computation task
4. invite others to join your task
5. provide private input to a tast
6. query the result of a task

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
* the fdrtd client library (`pip install fdrtd`)

---

## 1. describe a peer-to-peer network

* run your Python interpreter, e.g. `python`
* the following commands are entered in the Python console:

Alice (A), Bob (B), and Charlie (C) want to do secure multiparty computation in a peer-to-peer network.
for this exercise, they are going to use three public test servers:

* `nodes = ["https://lrz.fdrtd.com/public1", "https://lrz.fdrtd.com/public2", "https://lrz.fdrtd.com/public3"]`

each of them considers one of the nodes their own:

* `network_A = {'nodes': nodes, 'myself': 0}`
* `network_B = {'nodes': nodes, 'myself': 1}`
* `network_C = {'nodes': nodes, 'myself': 2}`

## 2. connect to public test servers

to connect to the test servers, we need the fdrtd client:

* import the fdrtd client library: `import fdrtd`

now, Alice, Bob, and Charlie each acquire the API of their respective servers:

* `api_A = fdrtd.Api(fdrtd.HttpInterface(nodes[0]))`
* `api_B = fdrtd.Api(fdrtd.HttpInterface(nodes[1]))`
* `api_C = fdrtd.Api(fdrtd.HttpInterface(nodes[2]))`

## 3. start a secure computation task

we will be using the 'Simon' microservice for this exercise. Simon stands for (SI)mple (M)ultiparty computati(ON),
a propaedeutic version of a secure multiparty computation protocol:

* `protocol_A = api_A.select_microservice(protocol="Simon")`
* `protocol_B = api_B.select_microservice(protocol="Simon")`
* `protocol_C = api_C.select_microservice(protocol="Simon")`

Alice is going ahead and is creating a task:

* `task_A = protocol_A.create(microprotocol="SecureSum", network=network_A)`

## 4. invite others to join your task

so that Alice, Bob, and Charlie work on the same task, Alice needs to invite Bob and Charlie to join hers:

* `invitation = task_A.invite()`

Bob and Charlie can use this handle to create matching tasks on their servers:

* `task_B = protocol_B.join(invitation=invitation, network=network_B)`
* `task_C = protocol_C.join(invitation=invitation, network=network_C)`

## 5. provide private input to a tast

Alice, Bob, and Charlie send data to their respective servers and input it into the joint calculation:

* `kvstorage_A = api_A.select_microservice(microservice="KeyValueStorage")`
* `kvstorage_B = api_B.select_microservice(microservice="KeyValueStorage")`
* `kvstorage_C = api_C.select_microservice(microservice="KeyValueStorage")`

* `data_A = kvstorage_A.create(value=10)`
* `data_B = kvstorage_B.create(value=7)`
* `data_C = kvstorage_C.create(value=14)`

* `task_A.input(source=data_A)`
* `task_B.input(source=data_B)`
* `task_C.input(source=data_C)`

## 6. query the result of a task

now, Alice, Bob, and Charlie can each query their own server for the result of the joint calculation:

* `task_A.result()`
* `task_B.result()`
* `task_C.result()`

there should be a total of 3 parties ('inputs') providing 3 samples (1 each) and the sum would be 31.

## cleanup

always clean up your sensitive data:

* `data_A.delete()`
* `data_B.delete()`
* `data_C.delete()`

you can exit the Python console

* `exit()`

## conclusion

did you get the correct result 31? excellent work.

you have successfully computed this sum in a secure peer-to-peer calculation among three parties
