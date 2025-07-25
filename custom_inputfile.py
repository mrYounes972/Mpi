import mimetypes

class InputFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.mime_type = mimetypes.guess_type(file_path)[0]

    def read(self):
        with open(self.file_path, "rb") as f:
            return f.read()

    def get_mime_type(self):
        return self.mime_type or "application/octet-stream"