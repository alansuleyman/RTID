from os import path
from pathlib import Path

class RtidOutInfo:
  CURRENT_DIR = path.dirname(path.abspath(__file__))
  OUT_DIR_NAME = "out"
  OUT_DIR = path.join(Path(CURRENT_DIR).parent.absolute(), OUT_DIR_NAME)
