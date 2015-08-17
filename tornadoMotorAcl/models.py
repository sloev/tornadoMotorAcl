


from schematics.transforms import blacklist
from schematics.types import StringType, EmailType, DateTimeType, BooleanType, IntType
from schematics.types.serializable import serializable
from schematics.types.compound import ListType, ModelType
from schematics.contrib.mongo import ObjectIdType

from schematics.models import Model

from bson.objectid import ObjectId

class Permission(Model): # for db
    #_id = ObjectIdType(required=False)
    name = StringType()

class Resource(Model): #for db
    #_id = ObjectIdType(required=False)
    name = StringType()

class ResourcePermissionPair(Model):#for embed in doc
    resource = StringType()
    permissions = ListType(StringType())

class Group(Model):# for db
    #_id = ObjectIdType(required=False)
    name = StringType()
    permissions = ListType(ModelType(ResourcePermissionPair))
    members = ListType(ObjectIdType())

