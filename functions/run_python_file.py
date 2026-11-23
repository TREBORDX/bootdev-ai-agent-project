import os
import subprocess
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
    
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[-3::] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]

        if args != None:
            command.extend(args)

        completedProcess = subprocess.run(command, text=True, capture_output=True, timeout=30)

        returnString = []

        if completedProcess.check_returncode() != 0:
            returnString.append(f"Process exited with code {completedProcess.returncode}")

        if completedProcess.stderr is None and completedProcess.stdout is None:
            returnString.append("No output produced")

        if completedProcess.stdout is not None:
            returnString.append(f"STDOUT: {completedProcess.stdout}")

        if completedProcess.stderr is not None:
            returnString.append(f"STDERR: {completedProcess.stderr}")

        return "\n".join(returnString)

    except Exception as e:
        return f"Error: executing Python file: {e}"