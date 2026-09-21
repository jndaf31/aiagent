import os
from config import *

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns a file's content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to the file.",
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(abs_path, file_path))
        valid_dir = os.path.commonpath([abs_path, full_path]) == abs_path

        if not valid_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n'

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"\n'

        file = open(full_path)

        file_content = ""
        file_content += file.read(10000)

        if file.read(1) != 0:
            file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content + "\n"


    except Exception as e:
        return f'Error: {e}'