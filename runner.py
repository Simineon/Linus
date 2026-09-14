import subprocess
import sys


class Runner:
    def __init__(self, file_path):
        self.file_path = file_path
        self.output = ""
        self.error = ""

    def runPython(self):
        try:
            process = subprocess.Popen(
                [sys.executable, self.file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            stdout, stderr = process.communicate()

            output_parts = []
            if stdout:
                output_parts.append(stdout)
            if stderr:
                output_parts.append("\n" + "=" * 50 + "\n")
                output_parts.append("ERRORS:\n")
                output_parts.append(stderr)

            self.output = ''.join(output_parts)

            if not self.output and process.returncode == 0:
                self.output = "Process completed successfully (no output)"
            elif not self.output and process.returncode != 0:
                self.output = f"Process failed with return code: {process.returncode}"

            return self.output

        except FileNotFoundError:
            error_msg = f"Error: File '{self.file_path}' not found"
            self.output = error_msg
            return error_msg
        except Exception as e:
            error_msg = f"Error running file: {str(e)}"
            self.output = error_msg
            return error_msg

    def get_output(self):
        return self.output if self.output else "No output available"