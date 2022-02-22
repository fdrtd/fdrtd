from tests.api import TestApi
from tests.assertions import TestAssertions
from tests.interface import TestInterface


class TestKeyValueStorage(TestAssertions):

    def test_key_value_storage(self):

        interface = TestInterface()
        api = TestApi(interface=interface)

        microservice = api.create(microservice='KeyValueStorage')
        kvstorage = microservice.create(storage='TestStorage')
        kvstorage.store(key='meaning', value=42)
        value = api.download(kvstorage.retrieve('meaning'))
        self.assertEqual(value, 42)
