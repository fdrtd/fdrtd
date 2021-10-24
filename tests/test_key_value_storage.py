from tests.api import TestApi
from tests.assertions import TestAssertions
from tests.interface import TestInterface


class TestKeyValueStorage(TestAssertions):

    def test_key_value_storage(self):

        interface = TestInterface()
        api = TestApi(interface=interface)

        microservice = api.create(microservice='KeyValueStorage')
        item = microservice.create(value=42, storage='TestStorage')
        value = api.download(item.retrieve())
        self.assertEqual(value, 42)
