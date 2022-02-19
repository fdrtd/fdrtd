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

Alice (A), Bob (B), and Charlie (C) want to do secure multiparty computation in a peer-to-peer network.
for this exercise, they are going to set up a server each. then, they will connect to their servers
through the fdrtd API and perform a secure sum computation.

## 1. set up servers

first, install the fdrtd base server and the Simon protocol (Simon = SImple Multiparty computatiON):

    pip install fdrtd
    pip install fdrtd-simon
  
now, we are going to run three servers on localhost, one each for Alice, Bob, and Charlie.
on Linux, you can run the servers in the background by adding an ampersand to the command line.
on Windows, you can start the servers in three separate consoles.

    python -m fdrtd.webserver --port=55501 &
    python -m fdrtd.webserver --port=55502 &
    python -m fdrtd.webserver --port=55503 &

## 2. describe a peer-to-peer network

* run your Python interpreter, e.g. `python`
* the following commands are entered in the Python console:

    `nodes = ["http://127.0.0.1:55501", "http://127.0.0.1:55502", "http://127.0.0.1:55503"]`

each of them considers one of the nodes their own:

    network_A = {'nodes': nodes, 'myself': 0}
    network_B = {'nodes': nodes, 'myself': 1}
    network_C = {'nodes': nodes, 'myself': 2}

## 3. connect to public test servers

to connect to the test servers, we need the fdrtd client:

    import fdrtd.client

now, Alice, Bob, and Charlie each acquire the API of their respective servers:

    api_A = fdrtd.client.Api(nodes[0])
    api_B = fdrtd.client.Api(nodes[1])
    api_C = fdrtd.client.Api(nodes[2])

## 4. start a secure computation task

we will be using the 'Simon' microservice for this exercise. Simon stands for (SI)mple (M)ultiparty computati(ON),
a propaedeutic version of a secure multiparty computation protocol:

    protocol_A = api_A.create(protocol="Simon")
    protocol_B = api_B.create(protocol="Simon")
    protocol_C = api_C.create(protocol="Simon")

Alice is going ahead and is creating a task:

    task_A = protocol_A.create_task(microprotocol="SecureSum", network=network_A)

## 5. invite others to join your task

so that Alice, Bob, and Charlie work on the same task, Alice needs to invite Bob and Charlie to join hers:

    invitation = api_A.download(task_A.invite())

Bob and Charlie can use this handle to create matching tasks on their servers:

    task_B = protocol_B.join_task(invitation=invitation, network=network_B)
    task_C = protocol_C.join_task(invitation=invitation, network=network_C)

## 6. provide private input to a tast

Alice, Bob, and Charlie send data to their respective servers and input it into the joint calculation:

    task_A.input(data=10)
    task_B.input(data=7)
    task_C.input(data=14)
    
    task_A.start()
    task_B.start()
    task_C.start()

## 7. query the result of a task

now, Alice, Bob, and Charlie can each query their own server for the result of the joint calculation:

    print(api_A.download(task_A.result()))
    print(api_B.download(task_B.result()))
    print(api_C.download(task_C.result()))

there should be a total of 3 parties ('inputs') providing 3 samples (1 each) and the sum would be 31.

## complete code

    import fdrtd.client

    nodes = ["http://127.0.0.1:55501", "http://127.0.0.1:55502", "http://127.0.0.1:55503"]

    network_A = {'nodes': nodes, 'myself': 0}
    network_B = {'nodes': nodes, 'myself': 1}
    network_C = {'nodes': nodes, 'myself': 2}

    api_A = fdrtd.client.Api(nodes[0])
    api_B = fdrtd.client.Api(nodes[1])
    api_C = fdrtd.client.Api(nodes[2])

    protocol_A = api_A.create(protocol="Simon")
    protocol_B = api_B.create(protocol="Simon")
    protocol_C = api_C.create(protocol="Simon")

    task_A = protocol_A.create_task(microprotocol="SecureSum", network=network_A)

    invitation = api_A.download(task_A.invite())

    task_B = protocol_B.join_task(invitation=invitation, network=network_B)
    task_C = protocol_C.join_task(invitation=invitation, network=network_C)

    task_A.input(data=10)
    task_B.input(data=7)
    task_C.input(data=14)

    task_A.start()
    task_B.start()
    task_C.start()

    print(api_A.download(task_A.result()))
    print(api_B.download(task_B.result()))
    print(api_C.download(task_C.result()))

## conclusion

did you get the correct result 31? excellent work.

you have successfully computed this sum in a secure peer-to-peer calculation among three parties
