import os
import json
import re 
import argparse

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
    dir_path = ""
    json_path = ""
    try:
        parser = argparse.ArgumentParser(description="List of formmating options.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('dir_path', type=str)
        parser.add_argument('json_path', type=str)
        parser.add_argument("-rl","--recursion-limit",type=int,help="Limit the exploration depth",required=False)
        parser.add_argument("-exex","--exclude-extension",nargs='+', type=str,help="Filters the statistics only to the given extensions",required=False)
        parser.add_argument("-exfi","--exclude-files",nargs='+', type=str,help="Excludes the files out of the entire json file",required=False)
        parser.add_argument("-exfo","--exclude-folders",nargs='+', type=str,help="Excludes the folder out of the entire json file",required=False)
        for mode, value in parser.parse_args()._get_kwargs():
            if mode == "dir_path":
                dir_path = value
            elif mode == "json_path":
                json_path = value
            elif mode == "recursion_limit" and value is not None:
                recursion_level = value
            elif mode == "exclude_extension" and value is not None:
                exclude_extension = value
            elif mode == "exclude_files" and value is not None:
                exclude_file = value
            elif mode == "exclude_folders"  and value is not None:
                exclude_folder = value
    except:
        print("Invalid Arguments")
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