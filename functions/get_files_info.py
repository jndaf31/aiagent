import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_wd_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(
            os.path.join(absolute_wd_path, directory)
        )

        valid_dir = os.path.commonpath([absolute_wd_path, full_path]) == absolute_wd_path

        if not valid_dir:
            return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory\n'

        if not os.path.isdir(full_path):
            return f'   Error: "{directory}" is not a directory\n'

        file_info_list = []
        for item in os.listdir(full_path):
            file_info_list.append([item, os.path.getsize(os.path.normpath(os.path.join(full_path, item))),os.path.isdir(os.path.normpath(os.path.join(full_path, item)))])

        file_info = ""
        for item in file_info_list:
            file_info += "".join(
                f'  - {item[0]}: file_size={item[1]} bytes, is_dir={item[2]}\n'
            )
        return file_info

    except Exception as e:
        return f"   Error: {e}"

