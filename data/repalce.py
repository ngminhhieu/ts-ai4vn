import os
from pprint import pprint
pathiter = (os.path.join(root, filename)
            for root, _, filenames in os.walk('./res')
            for filename in filenames
            )
for path in pathiter:
    pprint(path)
    newname = path.replace('gt', 'res')
    if newname != path:
        os.rename(path, newname)
