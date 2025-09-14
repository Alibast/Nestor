import glob, pathlib

def search_files(pattern: str = "data/**/*.txt"):
    return [str(p) for p in pathlib.Path(".").glob(pattern)]
