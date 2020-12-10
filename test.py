import sys
from os import listdir
from os.path import isfile, join
import sys
from main import main
good = sys.argv[1]
bad = sys.argv[2]
files = [join(good, f) for f in listdir(good) if isfile(join(good, f))]
files = [f for f in files if f.endswith(".lat")]

for i, file in enumerate(files):
    args = sys.argv[:2]
    args[1] = file
    result = main(args)
    assert(result == 0)
    print("OK")
bad_files = [join(bad, f) for f in listdir(bad) if isfile(join(bad, f))]
bad_files = [f for f in bad_files if f.endswith(".lat")]
print("bad tests")
for i, file in enumerate(bad_files):
    args = sys.argv[:2]
    args[1] = file
    try:
        a = main(args)
    except:
        continue


