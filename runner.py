import subprocess

class Runner:
    def __init__(self, file):
        self.file = file

    def runPython(self):
        try:
            if self.file:
                subprocess.run(["python", self.file])
            else:
                subprocess.run(["python3", self.file])
        except Exception as e:
            print(e)
