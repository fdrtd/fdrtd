import uuid as _uuid

from fdrtd.builtins.simon.peer_to_peer import PeerToPeer
import representation


class Microprotocol:

    def __init__(self, bus, properties, myself):

        self.bus = bus
        self.uuid = properties['task_id']
        self.network = PeerToPeer({'namespace': "fdrtd", 'protocol': "Simon"},
                                  properties['task_id'], properties, myself)
        self.stage = 0
        self.stages = {}
        self.caches = {}
        self.result = None
        self.parameters = properties['parameters']
        if properties['parent'] is None:
            self.parent_id = None
            self.parent_token = None
        else:
            self.parent_id = properties['parent']['parent_id']
            self.parent_token = properties['parent']['parent_token']
        self.handle = properties['handle']
        self.myself = myself

    def register_cache(self, argument, cache):
        self.caches[argument] = cache

    def register_stage(self, stage, required_arguments, handler):
        self.stages[stage] = (required_arguments, handler)

    def process(self, message):
        self.caches[message['token']].process(message['body'])
        self.continue_processing()

    def continue_processing(self):

        if self.stage not in self.stages:
            return

        (required_arguments, handler) = self.stages[self.stage]

        arguments = {'stage': self.stage}
        for argument in required_arguments:
            if argument not in self.caches:
                break
            arg = self.caches[argument].get_data()
            if arg is None:
                break
            arguments[argument] = arg
        else:
            self.stage = -1
            stage_after, ret = handler(arguments)
            if stage_after == -1:
                self.result = ret
                if self.parent_id is not None:
                    message = {'token': self.parent_token, 'sender': self.network.myself, 'receiver': self.network.myself, 'body': ret['result']}
                    microservice = self.bus.lut_uuid_to_repr[self.handle]
                    task = microservice['public']['get_task'](task_id=self.parent_id)
                    task.microprotocol.process(message)
            else:
                self.stage = stage_after
                self.continue_processing()

    def get_result(self):
        return self.result

    def start_pipeline(self, microprotocol, token, body):
        network = {'nodes': self.network.nodes, 'myself': self.network.myself}
        task = self.derive_task(network, microprotocol, self.uuid, token)
        task.input(data=body)
        task.start()

    def derive_task(self, network, microprotocol, parent_id, token):
        node = network['nodes'][network['myself']]
        if isinstance(node, str):
            api = representation.Api(url=node)
        else:
            api = representation.Api(interface=node)  # for local testing
        microservice = api.create(namespace="fdrtd", protocol="Simon")
        return microservice.create_task(microprotocol=microprotocol, network=network,
                                        parent={'parent_id': parent_id, 'parent_token': token},
                                        task_id=str(_uuid.uuid5(_uuid.UUID(parent_id), token)))
