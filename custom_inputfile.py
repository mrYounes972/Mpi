import mimetypes

class CustomInputFile:
    def __init__(self, path):
        self.path = path
        self.filename = path.split("/")[-1]

    def get_mime_type(self):
        mime_type, _ = mimetypes.guess_type(self.path)
        return mime_type or "application/octet-stream"

    def read(self):
        with open(self.path, "rb") as file:
            return file.read()
