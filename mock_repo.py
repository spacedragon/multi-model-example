import argparse
import pathlib
import os
import shutil
import fnmatch
parser = argparse.ArgumentParser(description='Mock repositories.')
parser.add_argument('--copy',  type=int,  default=10, help='number of copy')
parser.add_argument('--version_copy', type=int,  default=1,
                    help='number of versions')
parser.add_argument('--name', type=str, default="*", nargs=1, help='name filters')

parser.add_argument('src', type=pathlib.Path)
parser.add_argument('dest', type=pathlib.Path)


args = parser.parse_args()

print(args.name)

def change_name(dir, name):
    pbFile = os.path.join(dir, "config.pbtxt")
    if os.path.isfile(pbFile):
        f = open(pbFile, "rt")
        lines = f.readlines()
        for i,  line in  enumerate(lines):
            if line.startswith("name:"):
                lines[i] = 'name: "{}"\n'.format(name)
                break
        f.close()
        f = open(pbFile, "wt")
        f.write("".join(lines))
        f.close()

def copy_versions(dir):
    src = os.path.join(dir, "1")
    for i in range(2, args.version_copy + 1):
        dest = os.path.join(dir, str(i))
        if not os.path.exists(dest):
            print("copying version "+ dest)
            shutil.copytree(src , dest)

def mock_repo(): 
    os.makedirs(args.dest, exist_ok=True)

    for dir in os.listdir(args.src):
        match = False
        for filter in args.name:
            if fnmatch.fnmatch(dir,filter):
                match = True
                break
        if not match: 
            continue

        src = os.path.join(args.src, dir)
        if os.path.isdir(src):

            print("processing "+ dir)
            for i in range(0, args.copy):
                target = dir + "_"+ str(i)
                dest = os.path.join(args.dest, target)
                print("copying " + src +" to " + target )
                shutil.copytree(src, dest, dirs_exist_ok=True)
                change_name(dest, target)
                copy_versions(dest)

mock_repo()