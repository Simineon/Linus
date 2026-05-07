import subprocess
from locale import delocalize


class Runner:
    def __init__(self, file):
        self.file = file
        self.output = ""

    def runPython(self):
        try:
            if self.file:
                self.data = subprocess.run(["python", self.file], capture_output=True, text=True)
                self.output = self.data.stdout
            else:
                self.data = subprocess.run(["python3", self.file])
                self.output = self.data.stdout
        except Exception as e:
            print(e)

    def get_output(self):
        return self.output
