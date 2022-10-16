import os
import json
import argparse
import traceback

from pathlib import Path
from enum import Enum, unique
from typing import Dict, List, Union

# text colors enum
@unique
class TextColors(str, Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    RESET = "\033[39m"

    def __str__(self) -> str:
        return self.value


# define folder structure json data type
FolderJsonTypeStruct = Union[List[Union['FolderJsonType', str]], None]
FolderJsonType = Dict[str, FolderJsonTypeStruct]


# function to create files and folder
def create_file_folder_recursive(
    root_path: Path,
    folder_path: Path,
    folder_struct: FolderJsonTypeStruct
) -> None:
    if (
        folder_struct and
        isinstance(folder_struct, (Dict, List, str))
    ):
        file_names: List[str] = [x.name for x in folder_path.glob("*") if x.is_file()]
        existing_dirs: List[str] = [f.name for f in folder_path.iterdir() if f.is_dir()]
        
        folder_names: List[str] = []
        folder_structs: List[FolderJsonType] = []

        for file_or_folder in folder_struct:
            if isinstance(file_or_folder, str) and len(file_or_folder) > 0:
                file_names.append(file_or_folder)
            elif isinstance(file_or_folder, Dict):
                folder_names.extend(file_or_folder.keys())
                folder_structs.append(file_or_folder)

        assert len(folder_names) == len(set(folder_names)), "Folder names should be unique."
        assert len(
            (set(folder_names) | set(existing_dirs)).intersection(set(file_names))
        ) == 0, "File and folder names cannot be same."

        dict_folder_struct = {name: struct for structs in folder_structs for name, struct in structs.items()}

        for name in set(file_names):
            file_creation_path = folder_path / name
            if file_creation_path.is_file():
                print(TextColors.YELLOW + f"{file_creation_path.relative_to(root_path)} file already exists.")
            else:
                file_creation_path.touch()
                print(TextColors.GREEN + f"{file_creation_path.relative_to(root_path)} file created successfully.")


        for name, struct in dict_folder_struct.items():
            folder_creation_path = folder_path / name
            if folder_creation_path.is_dir():
                print(TextColors.YELLOW + f"{folder_creation_path.relative_to(root_path)} folder already exists.")
            else:
                folder_creation_path.mkdir()
                print(TextColors.GREEN + f"{folder_creation_path.relative_to(root_path)} folder created successfully.")
            
            create_file_folder_recursive(root_path, folder_creation_path, struct)



def create_struct_from_folder(folder_path: Path) -> FolderJsonType:
    folder_struct: FolderJsonTypeStruct = []
    sub_folder_structs: FolderJsonType = {}

    for x in folder_path.glob("*"):
        if x.is_file():
            folder_struct.append(x.name)
        if x.is_dir() and not x.name.startswith("."):
            sub_folder_structs.update(create_struct_from_folder(x))

    if sub_folder_structs:
        folder_struct.append(sub_folder_structs)

    return {folder_path.name: folder_struct}


def generate_file_folder(arg_file_path: str) -> None:
    # root folder structure
    root_file_path = Path(arg_file_path).absolute()

    if not root_file_path.exists() or not os.path.isfile(root_file_path):
        print(TextColors.BLUE + f"Given is not a valid file path.")
        return

    with open(root_file_path) as f:
        ROOT_FOLDER: FolderJsonType = json.load(f)

    for root_folder_name, root_folder_struc in ROOT_FOLDER.items():
        if root_folder_name:
            # get the absolute root path
            root_path = Path(root_folder_name).absolute()

            if root_path.exists() and os.path.isfile(root_path):
                print(TextColors.BLUE + f"File with same name already exists.")
                continue
            
            if not root_path.is_dir():
                print(TextColors.BLUE + f"Creating {root_path}")
                # create root folder
                root_path.mkdir(parents=True, exist_ok=True)
            
            print(TextColors.BLUE + f"Starting for {root_path}")

            # create files and folder
            create_file_folder_recursive(root_path, root_path, root_folder_struc)


def generate_struct_from_folder(arg_folder_paths: str) -> None:
    folder_structs: FolderJsonType = {}

    for path in arg_folder_paths:
        folder_path = Path(path).absolute()
        
        if not folder_path.is_dir():
            print(TextColors.BLUE + f"{folder_path} not a valid folder path.")
            continue

        print(TextColors.BLUE + f"Generating for {folder_path}")
        folder_structs.update(create_struct_from_folder(folder_path))

    with open("folder_structure.json", "w") as f:
        json.dump(folder_structs, f, indent=2)

    print(TextColors.BLUE + "Save structs in folder_structure.json")
    

def main():
    parser = argparse.ArgumentParser()

    meg = parser.add_mutually_exclusive_group()
    meg.add_argument(
        "-g",
        "--generate",
        help="Generate files/folders from given folder structure."
        " Give absolute or relative path of the JSON file."
        " Note: It will override any content of that file if present."
    )
    meg.add_argument(
        "-s",
        "--struct",
        nargs="+",
        help="Saves folder structure of given folders in folder_structure.json file."
        " Give absolute or relative paths of the folders in space seperated manner."
    )

    args = parser.parse_args()

    try:

        if args.generate:
            generate_file_folder(args.generate)
        elif args.struct:
            generate_struct_from_folder(args.struct)
        else:
            parser.print_help()
    except:
        print(TextColors.RED + traceback.format_exc())
    finally:
        # reset coloring of terminal
        print(TextColors.RESET + "Finished!!")

if __name__ == "__main__":
    main()
