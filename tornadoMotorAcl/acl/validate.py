
def check_permissions(user, perm_name, res_name):
    uid = user.uid
    p_id = None
    for p in permissions:
        if p.name == perm_name:
            p_id = p.permission_id
    r_id = None
    for r in resources:
        if r.name == res_name:
            r_id = r.resource_id
    if r_id and p_id:
        for g in groups:
            if uid in g.members:
                for p in g.permissions:
                    if r_id == p.resource_id and p_id in p.permissions:
                        return True
    return False
DB_GROUPS = "acl_groups"
DB_RESOURCES = "acl_resources"
DB_PERMISSIONS = "acl_permissions"

class AclSyntaxError(Exception):
    pass

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
            print "pp:",permission_pairs
            print "inside wrapped_f",  args, kwargs
            print self.db
        print "inside wrap"
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

class request():
    def __init__(self, db):
        self.db = db
    @acl_authorize(("read","write", "update", "egen stamdata"), ("read", "andres stamdata"))
    def post(self):
        print fun

        ''' Handle Tornado HTTP Basic Auth
        def wrap_execute(handler_execute):
            def require_auth(handler, kwargs):
                auth_header = handler.request.headers.get('Authorization')
                handler._username = None
                try:
                    auth_token = extract_auth_token(auth_header)[AUTH_TOKEN]
                    if not auth_token:
                        raise jwt.InvalidTokenError("authorization header is missing")
                    else:
                        jwt_token = validate_token(auth_token)
                        user_id = jwt_token.get('uid', None)
                        if not user_id:
                            raise jwt.InvalidTokenError("token missing uid")
                        handler._user_id = user_id
                        return True
                except jwt.InvalidTokenError, e:
                    print "[auth token error] : ", e
                    handler._transforms = []
                    handler.set_status(401)
                    handler.finish()
                    return False
                return True

            def _execute(self, transforms, *args, **kwargs):
                if require_auth(self, kwargs):
                    return handler_execute(self, transforms, *args, **kwargs)
                else:
                    return False
            return _execute
        handler_class._execute = wrap_execute(handler_class._execute)

        return handler_class
        '''
