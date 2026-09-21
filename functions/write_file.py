import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrite files.",
        "parameters": {          
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to the file.",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file.",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(abs_path,file_path))

        valid_path = os.path.commonpath([abs_path, full_path]) == abs_path

        if not valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory\n'

        if os.path.isdir(full_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory\n'

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)\n'

    except Exception as e:
        return f'Error: {e}'

