import os
import sys
import json

# Ask about generation options
# C:/Users/George/AppData/Local/Programs/Python/Python310/python.exe "e:/University/_My Scripts/Python Project/FolderToJson.py" "E:\University\_My Scripts\Python\Lab 4" "E:\University\_My Scripts\a.json" ".py .txt"

def file_extensio_stats(files, filter):
    result = {"Total number of files":0, "Sorted by extension":{}}
    for x in files:
        if (os.path.splitext(x)[1] in filter or filter == []) and os.path.splitext(x)[1] != "":
            if os.path.splitext(x)[1] not in result["Sorted by extension"]:
                result["Sorted by extension"][os.path.splitext(x)[1]] = 1
            else:
                result["Sorted by extension"][os.path.splitext(x)[1]] += 1
    for i in result["Sorted by extension"]:
        result["Total number of files"] += result["Sorted by extension"][i]
    return result

def folder_to_dict(folder, filter):
    folder_contents = os.listdir(folder)
    folders = []
    files = []
    for x in folder_contents:
        if os.path.isdir(os.path.join(folder,x)):
            folders.append(os.path.join(folder,x))
        if os.path.isfile(os.path.join(folder,x)):
            files.append(os.path.join(folder,x))
    result = {
        "Full Path" : os.path.abspath(folder), 
        "Number of files": len(files), 
        "Files": files,
        "Extension Stats": file_extensio_stats(files, filter),
        "Total number of files": len(files),
        "Number of folders": len(folders),
        "Folders": {x : folder_to_dict(x, filter) for x in folders}
             }
    if result["Folders"] != {}:
        for x in result["Folders"]:
            result["Total number of files"] += result["Folders"][x]["Total number of files"]
    else:
        result["Total number of files"] = len(files);
    return result
    
def __main__():
    try:
        dir_path = sys.argv[1]
        json_path = sys.argv[2]
    except LookupError:
        print("Not enough elements in the comand line")
        return
    if len(sys.argv) > 3 and sys.argv[3] != "":
        extension_filters = str.split(sys.argv[3], " ")
    else:
        extension_filters = []
    if not os.path.isdir(dir_path):
        print("The search directory doesn't exist")
        return
    if not os.path.isdir(os.path.dirname(json_path)):
        print("The export path is invalid")
        return
    result = folder_to_dict(dir_path, extension_filters)
    json_object = json.dumps(result, indent=4)
    with open(json_path, "w") as outfile:
        outfile.write(json_object)
    
__main__() 