


from schematics.transforms import blacklist
from schematics.types import StringType, EmailType, DateTimeType, BooleanType, IntType
from schematics.types.serializable import serializable
from schematics.types.compound import ListType, ModelType
from schematics.contrib.mongo import ObjectIdType

from schematics.models import Model

from bson.objectid import ObjectId

class Permission(Model): # for db
    name = StringType()
    permission_id = ObjectIdType()

class Resource(Model): #for db
    name = StringType()
    resource_id = ObjectIdType()

class ResourcePermissionPair(Model):#for embed in doc
    resource_id = ObjectIdType()
    permissions = ListType(ObjectIdType())

class Group(Model):# for db
    name = StringType()
    permissions = ListType(ModelType(ResourcePermissionPair))
    members = ListType(ObjectIdType())
    group_id = ObjectIdType()

permissions = [
        Permission({"name":"read", "permission_id":1}),
        Permission({"name":"write", "permission_id": 2})
        ]
resources = [
        Resource({"name":"egen stamdata", "resource_id":1}),
        Resource({"name":"andres stamdata", "resource_id":2})
        ]
groups = [
        Group({"name":"brugere",
            "permissions":[
                ResourcePermissionPair({"resource_id":1,
                    "permissions":[
                        1,2
                        ]
                    })
                ],
            "members":[1,2],
            "group_id":1
            }),
         Group({"name":"super brugere",
            "permissions":[
                ResourcePermissionPair({"resource_id":1,
                    "permissions":[
                        1,2
                        ]
                    }),
                 ResourcePermissionPair({"resource_id":2,
                    "permissions":[
                        1
                        ]
                    })
                ],
            "members":[2],
            "group_id":2
            })
        ]

class User(Model):
    name = StringType()
    uid = IntType()

users = [
        User({"name": "oscar", "uid":1}),
        User({"name": "johannes", "uid":2})
        ]

oscar = users[0]


