import sqlite3

class SimpleSQL:
    def __init__(self, Path=None):
        self.Path = Path
        self.Con = None
        if self.Path is None:
            raise RequirePath

    def Select(self, table=None, where="*"):
        if table is None:
            raise RequireTableName
        self.Con.cursor().execute(f"select {where} from {table};")

    def CreateTable(self, tableName=None, *values):
        if tableName is None:
            raise RequireTableName

    def Insert(self, tableName=None, *values):
        if tableName is None:
            raise RequireTableName
        self.Con.cursor().execute(f"")

    def Delete(self, tableName=None, where=None):
        if tableName is None:
            raise RequireTableName
        if where is None:
            raise SimpleSQLExceptions # new exceptions

    def Update(self, tableName=None, where=None):
        if tableName is None:
            raise RequireTableName
        if where is None:
            raise SimpleSQLExceptions # new exceptions

    def Drop(self, tableName=None):
        if tableName is None:
            raise RequireTableName

        
"""
Exceptions
"""
class SimpleSQLExceptions(Exception): pass

class RequirePath(SimpleSQLExceptions): pass
class RequireTableName(SimpleSQLExceptions): pass