import json
import os.path

class LocalState(object):
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def save(self, obj, file_name, overwrite=False):
        f_name = os.path.join(self.data_dir, file_name)
        if overwrite or not os.path.exists(f_name):
            with open(f_name, "w") as f:
                f.write(json.dumps(obj, indent=4))
        else:
            raise Exception("File exists")

    def load(self, file_name):
        with open(os.path.join(self.data_dir, file_name), "r") as f:
            return json.loads(f.read())