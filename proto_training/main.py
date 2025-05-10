import test_pb2

person = test_pb2.Person()
person.name = "John Doe"
person.id = 1234
person.email = "jdoe@example.com"

serialized = person.SerializeToString()

new_person = test_pb2.Person()
new_person.ParseFromString(serialized)