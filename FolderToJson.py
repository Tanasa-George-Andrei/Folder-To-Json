import os
import sys
import json
import re 

# C:/Users/George/AppData/Local/Programs/Python/Python310/python.exe "e:/University/_My Scripts/Python Project/FolderToJson.py" "E:\University\_My Scripts\Python\Lab 4" "E:\University\_My Scripts\a.json" ".py .txt"

def file_extensio_stats(files, exclude_extension):
    result = {"Total number of files":0, "Sorted by extension":{}}
    for x in files:
        if (os.path.splitext(x)[1] in exclude_extension or exclude_extension == []) and os.path.splitext(x)[1] != "":
            if os.path.splitext(x)[1] not in result["Sorted by extension"]:
                result["Sorted by extension"][os.path.splitext(x)[1]] = 1
            else:
                result["Sorted by extension"][os.path.splitext(x)[1]] += 1
    for i in result["Sorted by extension"]:
        result["Total number of files"] += result["Sorted by extension"][i]
    return result

def folder_to_dict(folder, exclude_extension, remaining_recursion_level, exclude_file, exclude_folder):
    folder_contents = os.listdir(folder)
    folders = []
    files = []
    for x in folder_contents:
        if os.path.isdir(os.path.join(folder,x)) and not any([bool(re.search(y, x)) for y in exclude_folder]):
            folders.append(os.path.join(folder,x))
        if os.path.isfile(os.path.join(folder,x)) and not any([bool(re.search(y, x)) for y in exclude_file]):
            files.append(os.path.join(folder,x))
    result = {}
    result["Full Path"] = os.path.abspath(folder),
    result["Number of files"] = len(files),
    result["Files"] = files
    result["Extension Stats"] = file_extensio_stats(files, exclude_extension)
    result["Total number of files"] = len(files)
    result["Number of folders"] = len(folders)
    if remaining_recursion_level == -1:
        result["Folders"] = {x : folder_to_dict(x, exclude_extension, -1, exclude_file, exclude_folder) for x in folders}
    elif remaining_recursion_level > 0:
        result["Folders"] = {x : folder_to_dict(x, exclude_extension, remaining_recursion_level - 1, exclude_file, exclude_folder) for x in folders}
    elif remaining_recursion_level == 0:
        result["Folders"] = folders
    else:
        print("Invalid Recursion Limit")
        return
    if result["Folders"] != {} and type(result["Folders"]) != list:
        for x in result["Folders"]:
            result["Total number of files"] += result["Folders"][x]["Total number of files"]
    else:
        result["Total number of files"] = len(files);
    return result
    
def __main__():
    recursion_level = -1
    exclude_extension = []
    exclude_file = []
    exclude_folder = []
    try:
        dir_path = sys.argv[1]
        json_path = sys.argv[2]
    except LookupError:
        print("Not enough elements in the comand line")
        return
    if (len(sys.argv)) % 2 == 0:
        print("Wrong number of arguments")
        return 
    for i in range(int((len(sys.argv)-3)/2)):
        mode = sys.argv[3+i*2]
        value = sys.argv[4+i*2]
        if mode == "-rl":
            recursion_level = int(value)
        elif mode == "-exex":
            for x in str.split(value, " "):
                exclude_extension.append(x)
        elif mode == "-exfi":
            exclude_file.append(value)
        elif mode == "-exfo":
            exclude_folder.append(value)
        else:
            print("Invalid mode")
            return
    if not os.path.isdir(dir_path):
        print("The search directory doesn't exist")
        return
    if not os.path.isdir(os.path.dirname(json_path)):
        print("The export path is invalid")
        return
    result = folder_to_dict(dir_path, exclude_extension ,recursion_level, exclude_file, exclude_folder)
    json_object = json.dumps(result, indent=4)
    with open(json_path, "w") as outfile:
        outfile.write(json_object)
    
__main__() 