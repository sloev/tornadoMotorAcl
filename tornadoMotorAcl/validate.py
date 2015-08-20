from bson.objectid import ObjectId
DB_GROUPS = "acl_groups"
DB_RESOURCES = "acl_resources"
DB_PERMISSIONS = "acl_permissions"

class AclSyntaxError(Exception):
    pass
class ValidException(Exception):
    pass

def check_permissions(permission_marks,func_permissions, db_permissions):
    new_fp = []

    for index, p in enumerate(func_permissions):
        if p in db_permissions:
            permission_marks[index] = 1
    #print "func not in db", new_fp, "func", func_permissions, "db", db_permissions
    return permission_marks
#    return False not in [x in db_permissions for x in func_permissions]
    

def acl_authorize(*permission_pairs):
    '''authorizes funcs in tornado requests using motor and mongodb
    takes it for granted that a motor mungo db is accessible through self.db
    and 
    that current_user is accessible through self.current_user
    
    args:
        permission_pairs can be:
        [("read", "news"),("delete","money")]
        or
        [("read", "write", "news"), ("delete", "update", "money")]
    '''

    def wrap(func):
        def wrapped_f(self, *args, **kwargs):
            #print "[permissions, (acl):",permission_pairs
            permission_marks = [0 for x in permission_pairs]

            #print "inside wrapped_f",  args, kwargs
            query = {}
            _id = self.current_user._id
            #print type(_id)
            #print "[validate]:user_id", _id
            cursor = self.db[DB_GROUPS].find({"members":str(_id)})
            try:
                while (yield cursor.fetch_next):
                    group_permissions = cursor.next_object()['permissions']
                    #print "[validate]:group found:", group_permissions
                    for p in group_permissions:
                        db_permissions = p['permissions']
                        db_resource = p['resource']
                        db_permission_pairs = [(perm, db_resource) for perm in db_permissions]
                        #print permission_pairs, db_permissions

                        permission_marks = check_permissions(permission_marks, permission_pairs, db_permission_pairs)
                        if 0 in permission_marks:
                            pass
                        else:
                            #print "perm pairs  IN db", permission_pairs, db_permission_pairs
                            raise ValidException
                self.set_status(403)
                self.finish()
            except ValidException:
                self.set_status(200)
                func(self, *args, **kwargs)
        #print "inside wrap"
        return wrapped_f
    """check if input format is ok"""
    new_permission_pairs = []
    for pp in permission_pairs:
        if not len(pp) > 1:
            raise AclSyntaxError("malformed args for acl_authorize")
        permissions = pp[:-1]
        resource = pp[-1]
        new_permission_pairs += [(permission, resource) for permission in permissions]
    permission_pairs = new_permission_pairs
    return wrap

