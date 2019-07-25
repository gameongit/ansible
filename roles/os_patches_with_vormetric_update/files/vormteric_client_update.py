#!/usr/bin/python
# Script is created by Lalit Sharma
'''
DOCSTRING = This Script is to download and install vormetric client package as per the package available in the repo.
'''
import os
import sys
import shutil
import rpm
import urllib2
import commands

LOCATION = "/tmp/Vormetric"
BKP_LOCATION = "/tmp/Vormetric_bkp"

DIR = rpm.TransactionSet()
PKGLST = DIR.dbMatch()

'''
DOCSTRING = To Check the RPM packages
'''
def rpmpackages(pack):
    for line in PKGLST:
        if pack in line['name']:
            return "%s.%s" % (line['version'], line['release'])

'''
DOCSTRING = To install the RPM packages
'''
def packageinstall(i):
    for line in PKGLST:
        if i == line['name']:
            print "%s.%s" % (line['version'], line['release'])
            break
    else:
        print i+" is not installed"
        os.system(Install+" "+i)

if not os.path.isdir(LOCATION):
    os.mkdir(LOCATION)
if not os.path.isdir(BKP_LOCATION):
    os.mkdir(BKP_LOCATION)

lists = os.listdir(LOCATION)
for content in lists:
    shutil.move(os.path.join(LOCATION, content), os.path.join(BKP_LOCATION, content))

if os.path.isfile("/etc/redhat-release"):
    OSV = (open('/etc/redhat-release', 'r').read().split(' ')[6].split('.')[0])
    PA = "RHEL"+OSV
    OS = "rh"+OSV
    OLDVER = "older%20version"
    RPMV = (rpmpackages("vee-fs"))
    print RPMV
    Install = "yum -y install"
    int_ver = RPMV
    print int_ver
    import yum
    packageinstall('poppler-utils')
    KERNEL_1 = (commands.getstatusoutput("rpm -qa --last | grep -i 'kernel-2.' | head -1 | awk '{print $1}' | cut -c 8-"))
    KERNEL = str(KERNEL_1[1])
else:
    for f in open("/etc/SuSE-release", "r"):
        if "VERSION" in f:
            OSV = (f.split(' ')[2])
    PA = "SLES"
    OS = "sles"+OSV
    OLDVER = "older"
    RPMV = rpmpackages("vee-fs")
    print RPMV
    int_ver = RPMV
    Install = "zypper -n install"
    packageinstall('poppler-tools')
    KERNEL_1 = (commands.getstatusoutput("rpm -qa --last | grep -i kernel-default-3 | head -1 |awk '{print $1}' | cut -c 16- |rev| cut -c 3-| rev"))
    KERNEL = str(KERNEL_1[1]+"-default")

def file_write():
    f = open('/tmp/comp.txt', 'w')
    f.write(response.read())
    f.close()

#KERNEL=os.uname()[2]
#KERNEL=str(os.system("rpm -qa --last | grep -i 'kernel-2.' | head -1 | awk '{print $1}' | cut -c 8-"))
URL = "http://****/repository/master-ops-vormetric"
print KERNEL
response = urllib2.urlopen(URL+'/Compatibility/')
file_write()
File = (open('/tmp/comp.txt', 'r'))
for line in File:
    if "Compatibility_Matrix" in line:
        last = line
PDF = last.split('"')[1]
print PDF
VerName1 = (PDF).split('_')[0]
print VerName1
os.system("wget "+URL+"/Compatibility/"+PDF+" -P "+LOCATION)
TXTFileName = (os.path.splitext(PDF)[0]+'.txt')
os.system("pdftotext "+LOCATION+"/"+PDF+" 2> /dev/null")
TextFile = (LOCATION+"/"+TXTFileName)
second = "VTE"

def latest_version(string_to_search, before, after, file_to_search, second_string):
    with open(file_to_search) as f:
        all_lines = f.readlines()
        last_line_number = len(all_lines)
        for current_line_no, current_line in enumerate(all_lines):
            if string_to_search in current_line:
                LEN = (len(current_line))
                start_line_no = max(current_line_no - before, 0)
                end_line_no = min(last_line_number, current_line_no+after+0)
                for i in range(current_line_no, end_line_no):
                    if LEN > 150:
                        YY = (all_lines[i].split(KERNEL)[1])
                    else:
                        YY = (all_lines[i])
                    if second_string in YY:
                        T = (YY.split('VTE')[1])
                        if len(T) > 1:
                            lat_ver = T.split(')')[0].split('/')[-1].strip().split(' ')[0]
                            return lat_ver
                            break
                        else:
                            T = all_lines[i+1]
                            lat_ver = (T.split(')')[0].split('/')[-1].strip().split(' ')[0])
                            return lat_ver
                            break
        else:
            print KERNEL+" is not present in the doc"
            exit()

lat_ver = latest_version(KERNEL, 0, 2, TextFile, second)
lat_v = ((lat_ver[::-1]).replace(".", "-", 1)[::-1])
binary = (("vee-fs-"+lat_v+"-"+OS).strip())
URL_NEW = (URL+'/'+PA+'/')
URL_OLDER = (URL+'/'+PA+'/older/')

def binary_package_search(urL):
    response = urllib2.urlopen(urL)
    filewrite_temp = open('/tmp/comp.txt', 'w')
    filewrite_temp.write(response.read())
    filewrite_temp.close()
    fileread_temp = (open('/tmp/comp.txt', 'r'))
    for line in fileread_temp:
        if binary in line:
            bin_pack = (line.split('"')[1])
            return bin_pack

def install_pack():
    os.chmod(LOCATION, 0o744)
    os.system("cd "+LOCATION+" ; sh "+ LOCATION +'/'+binary_pack+' -e')
    os.listdir(LOCATION)
    os.system("rpm -Uvh " + LOCATION + '/' + '*.rpm')
    New_ver_after = (rpmpackages("vee-fs"))
    if lat_ver == New_ver_after:
        print "New package installed successfully"
    else:
        os.system("for i in $(df -PHT | grep secfs | grep -v '/opt' | awk '{print $7}'); do echo $i; fuser -km $i ; done")
        os.system("rpm -Uvh " + LOCATION + '/' + '*.rpm')
        if lat_ver == New_ver_after:
            print "New package installed successfully"
        else:
            print "New package is not installed, Need to check manually"

if int_ver == lat_ver:
    print "Latest package is already installed"
else:
    binary_pack = binary_package_search(URL_NEW)
    if binary_pack:
        os.system("wget "+URL_NEW+"/"+binary_pack+" -P "+LOCATION)
        print binary_pack
        install_pack()
    else:
        binary_pack = binary_package_search(URL_OLDER)
        os.system("wget "+URL_OLDER+"/"+binary_pack+" -P "+LOCATION)
        print binary_pack
        install_pack()


