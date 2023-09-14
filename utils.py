import math
import os
import shutil
import subprocess


# ----------------------------------------------------------------------------------------------------------------------------------
def roundUp(value, ndigits= 0) :
    multiplier= 10.0**ndigits
    value*= multiplier

    #return math.ceil(value)/multiplier

    if (value%1.0) > 0.00001 :
        value+= 1.0

    return float(int(value))/multiplier

# ----------------------------------------------------------------------------------------------------------------------------------
def expandEnv(i_str, toSlashes= False) :
    result= os.path.expandvars(i_str)
    if toSlashes :
        result= result.replace("\\", "/")
    return result

# ----------------------------------------------------------------------------------------------------------------------------------
def userFolder() :
    userFolder= os.path.expanduser("~")
    documentsFolder= userFolder+"/Documents"

    if fileExists(documentsFolder) :
        return documentsFolder

    return userFolder

# ----------------------------------------------------------------------------------------------------------------------------------
def fileExists(path) :
    if not path :
        return False

    path= expandEnv(path)

    return os.path.exists(path)

# ----------------------------------------------------------------------------------------------------------------------------------
def createFolder(path) :
    path= expandEnv(path)

    if not os.path.exists(path) :
        os.makedirs(path)

# ----------------------------------------------------------------------------------------------------------------------------------
def fileTime(path) :
    path= expandEnv(path)

    if fileExists(path) :
        return os.path.getmtime(path)
    else :
        return None

# ----------------------------------------------------------------------------------------------------------------------------------
def copyFile(i_dst, i_src) :
    i_dst= expandEnv(i_dst)
    i_src= expandEnv(i_src)

    t= fileTime(i_src)
    if not t :
        return

    folder= os.path.dirname(i_dst)
    if folder != "" :
        createFolder(folder)

    try :
        shutil.copyfile(i_src, i_dst)
    except :
        return False

    os.utime(i_dst, (t, t))

    return True

# ----------------------------------------------------------------------------------------------------------------------------------
def readFile(path, binary= False) :
    result= None

    path= expandEnv(path)

    try :
        if fileExists(path) :
            mode= "rb" if binary else "r"
            with open(path, mode) as f :
                result= f.read()

    except :
        pass

    return result

# ----------------------------------------------------------------------------------------------------------------------------------
def writeFile(path, data) :
    path= expandEnv(path)

    try :
        createFolder(os.path.dirname(path))
        with open(path, "w") as f :
            f.write(data)

    except :
        return False

    return True

# ----------------------------------------------------------------------------------------------------------------------------------
def browse(path, select= False) :
    path= expandEnv(path).replace("/", "\\")

    if not select :
        path= os.path.dirname(path)
        subprocess.call("explorer \"{0}\"".format(path))
    else :
        subprocess.call("explorer /select,\"{0}\"".format(path))
