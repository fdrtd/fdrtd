import uuid as _uuid

from fdrtd.server.microservice import Microservice

from fdrtd.builtins.simon.task import TaskSimon


class MicroserviceSimon(Microservice):

    def __init__(self, bus, endpoint):
        super().__init__(bus, endpoint)
        self.tasks = {}
        self._the_cache = []

    def get_task(self, task_id):
        if task_id in self.tasks:
            return self.tasks.get(task_id)
        else:
            return None

    def create_task(self, microprotocol, network, parameters=None, task_id=None, parent=None):

        if task_id is None:
            task_id = str(_uuid.uuid4())

        if parameters is None:
            parameters = {}

        task = TaskSimon(self.bus, network, microprotocol, self.handle, parameters, task_id, parent)

        for item in self._the_cache:
            if item['task_id'] == task_id:
                task.peer_to_peer(item['body'])

        self.tasks[task_id] = task
        return task

    def join_task(self, invitation, network):

        task_id = invitation['task_id']

        task = TaskSimon(self.bus, network, invitation['microprotocol'], self.handle, invitation['parameters'], task_id, invitation['parent'])

        for item in self._the_cache:
            if item['task_id'] == task_id:
                task.peer_to_peer(item['body'])

        self.tasks[task_id] = task
        return task

    def peer_to_peer(self, callback, body):
        if callback in self.tasks:
            self.tasks[callback].peer_to_peer(body)
        else:
            self._the_cache.append({'task_id': callback, 'body': body})
        return None
