import os 
from dotenv import load_dotenv

load_dotenv()
maxChars = int(os.environ.get("MAX_CHARS"))


def get_file_content(working_directory: str, file_path: str) -> str:

    try:

        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        

        with open(target_dir, "r") as f:
            content = f.read(maxChars)
            
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {maxChars} characters]'

            return content



    except Exception as e:
        return f"Error: loading files {e}"

schema_get_files_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the content of a given file within a file path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to a file, relative to the working directory (default is the working directory itself)",
                }
            },
        },
    },
}