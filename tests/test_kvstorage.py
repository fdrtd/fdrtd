from tests.api import TestApi
from tests.assertions import TestAssertions
from tests.interface import TestInterface


class TestThreePartiesServices(TestAssertions):

    def test_kvstorage(self):

        interface = TestInterface()
        api = TestApi(interface=interface)

        microservice = api.create(microservice='KeyValueStorage')
        item = microservice.create(value=42, storage='TestStorage')
        value = api.download(item.retrieve())
        self.assertEqual(value, 42)
