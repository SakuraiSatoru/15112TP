import os
import re
import json


def walker(path):
    fileList = [None] * 15
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            num, hwname = check(name)
            if num is not None:
                dict = {}
                dict["no"] = num
                dict["path"] = os.path.join(root, name)
                dict["name"] = hwname
                if num == "6" and fileList[
                    6] is not None and "driver" not in hwname:
                    fileList[6].append(dict)
                elif "driver" not in hwname:
                    fileList[int(num)] = [dict]
    # fileLIst: [[{}], [{}], ... [{},{},{}], ....]
    return fileList


def extractScripts(fileList):
    returnDict = {}
    for f in fileList:
        if f is not None and isinstance(f, list):
            dict = {}
            dict["scripts"] = [""] * 5
            for d in f:
                dict["no"] = d["no"]
                dict["name"] = d['name']
                with open(d["path"], "r") as file:
                    # scriptsList = [""] * 5
                    scripts = file.read()
                    poslist = [m.start() for m in
                               re.finditer("def .*:\n", scripts)]
                    for i in range(len(poslist) - 1):
                        s = scripts[poslist[i]:poslist[i + 1]]
                        if "def test" in s:
                            continue
                        s = ' '.join(s.split())
                        s = s.replace("\n", " ").strip()
                        j = 0
                        while j < 5:
                            if (len(s) > len(dict["scripts"][j])):
                                # scriptsList.insert(j, s)
                                # scriptsList.pop()
                                dict["scripts"].insert(j, s)
                                dict["scripts"].pop()
                                break
                            else:
                                j += 1
            dict["scripts"] = dict["scripts"][::-1]
            returnDict[int(dict["no"])] = dict
    return returnDict


def check(file):
    # fileinfo = os.path.getsize(file)
    filename = file.split('\\')[-1].lower().strip()
    pattern = '^hw\d{1,2}.*\.py'
    if re.match(pattern, filename):
        return re.search("\d{1,2}", filename).group(0), re.search(
            "^hw\d{1,2}[^\.]*", filename).group(0)
    else:
        return None, None


def write(data, file):
    fout = open(file, 'w')
    sent_data = data
    dumped_json_string = json.dumps(sent_data)
    binary_data = ' '.join(
        format(ord(letter), 'b') for letter in dumped_json_string)
    fout.write(binary_data)
    fout.close()


def read(file):
    if os.path.isfile(file):
        with open(file, "r") as f:
            binary_data = f.read()
            jsn = ''.join(chr(int(x, 2)) for x in binary_data.split())
            received_data = json.loads(jsn)
            return received_data


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


if __name__ == '__main__':
    # data = extractScripts(walker("."))
    # pretty(data)
    # write(data, r".\data\default.dat")
    # pretty(read(r".\data\default.dat"))
    pass
