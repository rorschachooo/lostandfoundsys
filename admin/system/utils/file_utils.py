import hashlib

# File Tools
class FileUtils():
    def calculate_md5(file):
        md5_hash = hashlib.md5()
        for chunk in file.chunks():
            md5_hash.update(chunk)
        return md5_hash.hexdigest()