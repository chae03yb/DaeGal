import json
import shutil
import os

def Read(Path=None):
    if Path is None:
        raise RequirePath
    else:
        with open(Path, 'r') as File:
            jsonData = json.load(fp=File)
            return dict(jsonData)

def Write(Path=None, Object=None):
    if Path is None:
        raise RequirePath
    if Object is None:
        raise RequireObject
    else:
        with open(Path, 'w') as File:
            json.dump(fp=File, obj=Object, indent=4)
            return

def BackupWrite(Path=None, Object=None):
    if Path is None:
        raise RequirePath
    if Object is None:
        raise RequireObject
    else:
        originalFileName = str(Path).split('.')
        backupFileName = originalFileName[0] + "_backup" + originalFileName[1]
        shutil.copyfile(src=Path, dst=backupFileName)
        try:
            with open(Path, 'w') as File:
                json.dump(fp=File, obj=Object, indent=4)
        except json.JSONDecodeError:
            with open(backupFileName, 'r') as File:
                Data = File.read()
                with open(Path, 'r') as File:
                    json.dump(fp=File, obj=Data, indent=4)
        finally:
            os.remove(path=backupFileName)

class SimpleJSONExceptions(Exception): pass
class RequirePath(SimpleJSONExceptions): pass
class RequireObject(SimpleJSONExceptions): pass