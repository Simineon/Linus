import subprocess

class Runner:
    def __init__(self, file):
        self.file = file

    def runPython(self):
        try:
            if self.file:
                self.data = subprocess.run(["python", self.file])
            else:
                self.data = subprocess.run(["python3", self.file])
        except Exception as e:
            print(e)

    def get_output_data(self):
        data = self.data.stdout
