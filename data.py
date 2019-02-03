
class UserNotExists(Exception):
    pass
class NotACommand(Exception):
    pass
class PermissionDenied(Exception):
    pass
class CmdSyntaxError(Exception):
    pass
class DatabaseError(Exception):
    pass
