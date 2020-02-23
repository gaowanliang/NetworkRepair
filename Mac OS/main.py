import os
import subprocess
import time
import re
import webbrowser

import sys


def appPath():
    if hasattr(sys, "frozen"):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)


# print(appPath())

# exit()

def cmd(command):
    ex = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    out, _ = ex.communicate()
    ex.wait()
    return out.decode()


pypi = "pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple "
try:
    import requests
except ImportError:
    cmd(pypi+"requests")
    import requests

try:
    import OpenSSL
except ImportError:
    cmd(pypi+"pyopenssl")
    import OpenSSL


l = [os.path.exists(appPath()+"/bin/main"),
     os.path.exists(appPath()+"/config/openssl.cnf"),
     os.path.exists(appPath()+"/config/domain.conf")]
if(not all(l)):
    print("丢失关键文件，无法继续")
    input("请按回车(Enter)键继续......")
    exit()


def cmdgbk(command):
    ex = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    out, _ = ex.communicate()
    ex.wait()
    return out.decode("gbk")


if(not os.path.exists(appPath()+"/ca")):
    os.mkdir(appPath()+"/ca")
if(not os.path.exists(appPath()+"/host")):
    os.mkdir(appPath()+"/host")
if(not os.path.exists(appPath()+"/ca/ca.key")):
    print("正在为你自动化签发CA证书...")
    print(
        '\n===============================\n生成根证书私钥\n===============================\n')
    cmd(r'openssl genrsa -out "ca/ca.key" 2048'.replace('ca/', appPath()+'/ca/'))
    print(
        '\n===============================\n生成根证书签发申请文件\n===============================\n')
    ex = subprocess.Popen(r'openssl req -new -key "ca/ca.key" -out "ca/ca.csr" -config "'.replace('ca/', appPath()+'/ca/')+appPath()+'/config/openssl.cnf"',
                          stdout=subprocess.PIPE, shell=True, stdin=subprocess.PIPE)
    time.sleep(0.5)
    ex.communicate('\n\n\n\n\n\n\n\n\n\n'.encode())
    ex.wait()
    print(
        '\n===============================\n自签发根证书\n===============================\n')
    cmd(r'openssl x509 -req -days 3650 -in "ca/ca.csr" -signkey "ca/ca.key" -out "ca/ca.crt"'.replace('ca/', appPath()+'/ca/'))
    print(
        '\n===============================\n生成pem格式证书\n===============================\n')
    ex = subprocess.Popen(
        r'cat "./ca/ca.crt" "./ca/ca.key" > "./ca/ca.pem"'.replace('./ca/', appPath()+'/ca/'), shell=True)
    ex.wait()
    print('\n⭐⭐⭐自动化签发CA证书结束，请保管好你ca文件夹里的文件，不当传播可能会导致你的访问被劫持⭐⭐⭐')
if('Gaowan Liang Future Technology Co., Ltd' not in cmd("security dump-keychain")):
    print(
        "⭐⭐⭐下面开始安装CA证书，请在提示Password时输入密码，否则后续会出现错误（密码是隐形的，直接打即可）⭐⭐⭐")
    cmd(r'sudo security add-trusted-cert -d -r trustRoot -k "/Library/Keychains/System.keychain" "ca/ca.crt"'.replace("ca/", appPath()+"/ca/"))
path = "/etc/hosts"
f = open(path, "r")
rawHosts = f.read()
f.close()
if(not os.path.exists(appPath()+"/HOSTS.txt") or "pixiv" not in rawHosts):
    print("现在进行HOSTS相关操作")
    updateWeb = "https://cdn.jsdelivr.net/gh/googlehosts/hosts/hosts-files/hosts"
    newHosts = requests.get(updateWeb).text
    f = open(appPath()+"/HOSTS.txt", "w+", encoding="utf-8")
    f.write(newHosts)
    f.close()
    newHosts = re.sub(r'\d+?\.\d+?\.\d+?\.\d+?\t', "127.0.0.1\t", newHosts)
    f = open(appPath()+"/host/hosts", "w+")
    f.write(newHosts)
    f.close()
    f = open(appPath()+"/host/hosts.bak", "w+")
    f.write(rawHosts)
    f.close()
    print("HOSTS已下载，修改和备份完成，请在打开的第一个文件夹中复制“hosts”粘贴到第二个打开的文件夹中，替换较旧的项目，如果需要管理员权限，输入密码继续即可。结束后按下任意键继续")
    time.sleep(3)
    os.system(r'open "'+appPath()+r'/host"')
    time.sleep(1)
    os.system(r'open /etc')
    input("请按回车(Enter)键继续......")
    f = open(path, "r")
    rawHosts = f.read()
    f.close()
    if("pixiv" not in rawHosts):
        print("hosts修改有误，请重新打开软件并按照提示准确操作")
        input("请按回车(Enter)键继续......")
        exit()
    # os.system(r'ipconfig /flushdns')
    tip = "如果发现上网出现异常，请将data文件夹里的host.bak改名为hosts，替换/etc/里的hosts即可恢复正常。"
    f = open(appPath()+"/tip.txt", "w+")
    f.write(tip)
    f.close()
    print("HOSTS已被修改，"+tip+"相关提示已保存到目录下的tip.txt中")
    time.sleep(5)
ps = ""
if(not os.path.exists(appPath()+"/config/config.txt")):
    print("正在进行网速测试，请稍等")
    ex = cmdgbk("ping -c 4 1.0.0.1")
    if("100.0%" in ex):
        ex = cmdgbk("ping -c 4 8.8.8.8")
        if("100.0%" in ex):
            print("抱歉，经过测试，你无法使用该工具")
            input("请按回车(Enter)键继续......")
            exit()
        else:
            ps = ' --gfw-dns "8.8.8.8:853"'
    f = open(appPath()+"/config/config.txt", "w+")
    f.write(ps)
    f.close()
    print("网速测试结束")
    print("Mac OS因为系统限制，需要每次输入密码，请下次打开时提示Password：时输入你的密码")
else:
    f = open(appPath()+"/config/config.txt", "r")
    ps = f.read()
    f.close()
try:
    print("使用过程中软件必须一直开启，可以按下Ctrl+C停止软件，请保管好你ca文件夹里的文件，不当传播可能会导致你的访问被劫持。本软件仅供学习交流，请勿用于非法用途")
    command= r'sudo '+appPath().replace(" ","\\ ")+r'/bin/main -c "./ca/ca.pem" -k "./ca/ca.key" -l "'.replace("./ca/", appPath()+"/ca/")+appPath()+'/config/domain.conf"'+ps
    # print(command,1)
    cmd(command)
    
except:
    print("程序已结束")
else:
    print("程序发生异常，已紧急结束，相关报错问题请搜索最后一行FATA[0000]后面的内容进行处理")

input("请按回车(Enter)键继续......")
# print(1)
# 读文件
