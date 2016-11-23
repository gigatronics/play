import os
data = [3, 4, 2]

cwd = os.getcwd()

f = open(cwd+"/calib/cam-para.txt", "w")
f.write("camera parameters: \n %s" % data)
f.close()

with open(cwd+"/calib/cam-para2.txt", "w") as f2:
    print ("camera parameters: \n %s" % data)
