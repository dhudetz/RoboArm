import simulate as sim
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(ROOT_DIR, "simulated")
os.mkdir(path)
print(path)
