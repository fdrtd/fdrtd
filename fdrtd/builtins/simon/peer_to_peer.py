import representation


class PeerToPeer:

    def __init__(self, endpoint, task_id, properties, myself):
        self.endpoint = endpoint
        self.task_id = task_id
        self.properties = properties
        self.nodes = properties['nodes']
        self.myself = myself
        self.count = len(self.nodes)

    def broadcast(self, body, token):
        for index in range(self.count):
            self.send_to_node(body, index, token)

    def send_to_next_node(self, body, token):
        index = (self.myself + 1) % len(self.nodes)
        self.send_to_node(body, index, token)

    def send_to_previous_node(self, body, token):
        index = (self.myself - 1) % len(self.nodes)
        self.send_to_node(body, index, token)

    def send_to_node(self, body, receiver, token):
        if isinstance(self.nodes[receiver], str):
            api = representation.Api(url=self.nodes[receiver])
        else:
            api = representation.Api(interface=self.nodes[receiver]) # for testing purposes
        microservice = api.create(**self.endpoint)
        microservice.peer_to_peer(callback=self.task_id,
                                  body={
                                      'task': self.properties,
                                      'message': {
                                          'token': token,
                                          'sender': self.myself,
                                          'receiver': receiver,
                                          'body': body
                                      }
                                  })
