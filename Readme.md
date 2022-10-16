# Folder Structure Generation from JSON file

## What this tool is about?
* This tool can help you generate folder structure from a JSON file. This JSON file needs to follow certain rules,
    1. JSON file should contain keys which specify where to create file/folder.
    2. This top level keys can represent folder's relative or absolute path.
    3. Corresponding value of that key will specify the desired folder structure.
    4. This value should be a list or `null`.
    5. Empty list or `null` implies that folder should be empty.
    6. File should be specifield as string in the list.
    7. Sub folders should be specified as json object themself with key having their name and value satisfying criterias `3-6`.
    8. Inside any folder, file and folder names should be unique.
* This can also help you save the JSON structure of given folders.

## Examples
```shell
$ python3 json_folder_struct.py -g folder_structure.json
```
Above command will generate two folders with structure like this,
```
.
├───test_folder
│   │   file1.txt
│   │   file2.txt
│   │
│   ├───fol1
│   │   │   file3.txt
│   │   │   file4.txt    
│   │   │
│   │   ├───fol3
│   │   │       file5.txt
│   │   │
│   │   ├───fol4
│   │   └───fol5
│   │           file6.txt
│   │
│   └───fol2
│       └───fol6
└───test_folder_2        
    │   file1.txt        
    │
    ├───fol1
    │       file2.txt    
    │       file3.txt    
    │
    └───fol2
        └───fol3
                file4.txt
```
And if you run below command, it will create same folder structure specified in `folder_structure.json` and save it in that file.
```shell
$ python json_folder_struct.py -s test_folder test_folder_2
```
To get help run
```shell
$ python json_folder_struct.py
```

## Features
* Boilerplate folder structure generation for projects.
* Colored output.