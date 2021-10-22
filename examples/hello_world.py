import representation

api = representation.Api("http://localhost:55500")
list_of_services = api.list()
print(list_of_services)
