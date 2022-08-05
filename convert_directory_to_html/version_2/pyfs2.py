from fs.osfs import OSFS # operating system filesystem
from fs.walk import Step
from typing import List
from fs.info import Info
import fs.path as _p

_dir = 'Project'

with OSFS(_dir) as pfs: # create osfs. the path you pass to the constructor is the root of this filesystem
    w: Step # Step is each level of the walk
    for w in pfs.walk.walk('/'): # walk recursively. definitely look at all of the available keyword arguments
        cur_dir_path = w.path # the relative path of the current directory in the walk process, as string
        dir_files: List[Info] = w.files # a list of the files, as Info, at this path

        f: Info
        for f in dir_files:
            relative_path = f.make_path(w.path) # path relative to the root of the pyfilesystem, e.g. /Practice_1/First_Folder/1.1.1_Test.html
            os_path = pfs.getsyspath(relative_path)

            print(relative_path, '|', os_path)

