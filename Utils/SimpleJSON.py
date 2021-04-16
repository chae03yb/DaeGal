import json
import shutil
import os

def Read(Path=None):
    if Path is None:
        raise RequirePath
    else:
        with open(Path, 'r') as File:
            jsonData = json.load(fp=File)
            return jsonData

def Write(Path=None, Object=None):
    if Path is None:
        raise RequirePath
    if Object == {}:
        pass
    elif Object is None:
        raise RequireObject
    with open(Path, 'w') as File:
        json.dump(fp=File, obj=Object, indent=4)

def BackupWrite(Path=None, Object=None) -> str:
    if Path is None:
        raise RequirePath
    if Object == {}:
        pass
    elif Object is None:
        raise RequireObject
    originalFileName = str(Path).split('.')
    backupFileName = originalFileName[0] + "_backup" + originalFileName[1]
    shutil.copyfile(src=Path, dst=backupFileName)
    result = 0
    try:
        with open(Path, 'w') as File:
            json.dump(fp=File, obj=Object, indent=4)
        result = "success"
    except json.JSONDecodeError:
        with open(backupFileName, 'r') as File:
            Data = File.read()
            with open(Path, 'r') as File:
                json.dump(fp=File, obj=Data, indent=4)
            result = f"JSONDecodeError\n\n{json.JSONDecodeError.msg}"
    except Exception as Error:
        result = Error
    finally:
        os.remove(path=backupFileName)
        return result

class SimpleJSONExceptions(Exception): pass
class RequirePath(SimpleJSONExceptions): pass
class RequireObject(SimpleJSONExceptions): pass