


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

