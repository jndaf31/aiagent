import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run python .py file with optional args.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to the file.",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of optional args.",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(abs_path,file_path))

        valid_dir = os.path.commonpath([abs_path, full_path]) == abs_path

        if not valid_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        command = ["python", full_path]

        if args != None:
            command.extend(args)

        process = subprocess.run(command, 
                                capture_output=True,
                                cwd = working_directory, 
                                text=True, 
                                timeout=30)

        output_string = ""

        if process.returncode != 0:
            output_string += f"Process exited with code {process.returncode}\n"
        
        if process.stderr == "" and process.stdout == "":
            output_string += f"No output produced"
        elif process.stderr == "":
            output_string += f"STDOUT:\n{process.stdout}"
        elif process.stdout == "":
            output_string += f"STDERR:\n{process.stderr}"
        else:
            output_string += f"STDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}"

        return output_string
    
    except Exception as e:
        return f"Error: executing Python file: {e}"