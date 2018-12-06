import json
import os
import re


class ValidationError(Exception):
    pass


def walker(path=r".\data"):
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
    fileList = [x for x in fileList if x is not None]
    if len(fileList) < 10:
        raise ValidationError(
            r"Please copy hw folders containing hw 1,2,3,4,5,6,8,9,10,11! into .\data")
    return fileList


def extractScripts(fileList):
    returnDict = {}
    for f in fileList:
        if f is not None and isinstance(f, list):
            dict = {}
            dict["scripts"] = [""] * 4
            for d in f:
                dict["no"] = d["no"]
                dict["name"] = d['name'].split("-")[0]
                with open(d["path"], "r") as file:
                    scripts = file.read()
                    poslist = [m.start() for m in
                               re.finditer("def .*:\n", scripts)]
                    for i in range(len(poslist) - 1):
                        s = scripts[poslist[i]:poslist[i + 1]]
                        if "def test" in s:
                            continue
                        s = ' '.join(s.split())
                        s = s.replace("\n", " ").strip()
                        # remove all white space!
                        s = s.replace(" ", "")
                        j = 0
                        while j < 4:
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


def write(data, file=r".\data\user.dat"):
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
    else:
        return None


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


def delete(file=r".\data\user.dat"):
    if os.path.exists(file):
        os.remove(file)


def writeScore(score):
    path = r".\data\score.dat"
    outDict = {}
    if os.path.exists(path):
        try:
            s = read(path)
            scores = list(s.values())
            scores.append(score)
            scores = list(sorted(scores, reverse=True))
            if len(scores) > 5:
                scores.pop()
            for i in range(len(scores)):
                outDict[str(i + 1)] = scores[i]
        except:
            delete(path)
            outDict = {1: score}
            print("score file damaged")
    else:
        print("file don;t exist")
        outDict = {1: score}
    write(outDict, path)
    pretty(read(path))


if __name__ == '__main__':
    data = extractScripts(walker(r".\data"))
    write(data, r".\data\user.dat")
    pretty(read(r".\data\user.dat"))
