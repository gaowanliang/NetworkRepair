import os
import subprocess
import time
import requests
import re
import webbrowser
import OpenSSL

l = [os.path.exists("bin/main.exe"),
     os.path.exists("config/openssl.cnf"),
     os.path.exists("bin/certmgr.exe"),
     os.path.exists("config/domain.conf"),
     os.path.exists("openssl/bin")
     ]
if(not all(l)):
    print("丢失关键文件，无法继续")
    os.system('pause')
    exit()


def cmd(command):
    ex = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    out, _ = ex.communicate()
    ex.wait()
    return out.decode()


def cmdgbk(command):
    ex = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    out, _ = ex.communicate()
    ex.wait()
    return out.decode("gbk")


if(not os.path.exists("./ca")):
    os.mkdir("./ca")

if(not os.path.exists("./host")):
    os.mkdir("./host")
if(not os.path.exists("ca/ca.key")):
    print("正在为你自动化签发CA证书...")
    print(
        "\n===============================\n生成根证书私钥\n===============================\n")
    cmd(r".\openssl\bin\openssl.exe genrsa -out ca/ca.key 2048")
    print(
        "\n===============================\n生成根证书签发申请文件\n===============================\n")
    ex = subprocess.Popen(r".\openssl\bin\openssl.exe req -new -key ca/ca.key -out ca/ca.csr -config config/openssl.cnf",
                          stdout=subprocess.PIPE, shell=True, stdin=subprocess.PIPE)
    time.sleep(0.5)
    ex.communicate("\n\n\n\n\n\n\n\n\n\n".encode())
    ex.wait()
    print(
        "\n===============================\n自签发根证书\n===============================\n")
    cmd(r".\openssl\bin\openssl.exe x509 -req -days 3650 -in ca/ca.csr -signkey ca/ca.key -out ca/ca.crt")
    print(
        "\n===============================\n生成pem格式证书\n===============================\n")
    ex = subprocess.Popen(
        r"copy /b .\ca\ca.crt+.\ca\ca.key .\ca\ca.pem", shell=True)
    ex.wait()
    print("\n⭐⭐⭐自动化签发CA证书结束，请保管好你ca文件夹里的文件，不当传播可能会导致你的访问被劫持⭐⭐⭐")
cert = OpenSSL.crypto.load_certificate(
    OpenSSL.crypto.FILETYPE_PEM, open(r"ca\ca.crt").read())
k = hex(cert.get_serial_number()).upper()[2:]
pattern = re.compile(r'..')
result1 = pattern.findall(k)
cahash = " ".join(result1)
if(cahash not in cmd(r".\bin\certmgr.exe /all /s root")):
    print(
        "⭐⭐⭐下面开始安装CA证书，请在提示时点击“确定”，否则后续会出现错误⭐⭐⭐")
    cmd(r".\bin\certmgr.exe /c /add ca/ca.crt /s root")
path = "C:/WINDOWS/system32/drivers/etc/hosts"
f = open(path, "r")
rawHosts = f.read()
f.close()
if(not os.path.exists("HOSTS.txt") or "pixiv" not in rawHosts):
    print("现在进行HOSTS相关操作")
    updateWeb = "https://cdn.jsdelivr.net/gh/googlehosts/hosts/hosts-files/hosts"
    newHosts = requests.get(updateWeb).text
    f = open("HOSTS.txt", "w+", encoding="utf-8")
    f.write(newHosts)
    f.close()
    newHosts = re.sub(r'\d+?\.\d+?\.\d+?\.\d+?\t', "127.0.0.1\t", newHosts)
    f = open("host/hosts", "w+")
    f.write(newHosts)
    f.close()
    f = open("host/hosts.bak", "w+")
    f.write(rawHosts)
    f.close()
    print("HOSTS已下载，修改和备份完成")
    print("⭐⭐⭐请在弹出的第一个文件夹中复制“hosts”粘贴到第二个弹出的文件夹中，如果需要管理员权限，点击继续即可。⭐⭐⭐")
    print("也就是把软件目录下的data文件夹里的hosts文件替换C:/WINDOWS/system32/drivers/etc/下的hosts文件")
    print("结束后按下任意键继续")
    time.sleep(3)
    os.system(r'C:\Windows\explorer.exe '+os.getcwd()+r"\host")
    time.sleep(1)
    os.system(r'C:\Windows\explorer.exe C:\WINDOWS\system32\drivers\etc')
    os.system('pause')
    f = open(path, "r")
    rawHosts = f.read()
    f.close()
    if("pixiv" not in rawHosts):
        print("hosts修改有误，请重新打开软件并按照提示准确操作")
        os.system('pause')
        exit()
    os.system(r'ipconfig /flushdns')
    tip = "如果发现上网出现异常，请将data文件夹里的host.bak改名为hosts，替换C:/WINDOWS/system32/drivers/etc/里的hosts，并在命令提示符里输入ipconfig /flushdns,回车即可恢复正常。"
    f = open("tip.txt", "w+")
    f.write(tip)
    f.close()
    print("HOSTS已被修改，"+tip+"相关提示已保存到目录下的tip.txt中")
    time.sleep(5)
ps = ""
if(not os.path.exists("config/config.txt")):
    print("正在进行网速测试，请稍等")
    ex = cmdgbk("ping 1.0.0.1")
    if("100%" in ex):
        ex = cmdgbk("ping 8.8.8.8")
        if("100%" in ex):
            print("抱歉，经过测试，你无法使用该工具")
            os.system('pause')
            exit()
        else:
            ps = ' --gfw-dns "8.8.8.8:853"'
    f = open("config/config.txt", "w+")
    f.write(ps)
    f.close()
    print("网速测试结束")
else:
    f = open("config/config.txt", "r")
    ps = f.read()
    f.close()
try:
    print("使用过程中软件必须一直开启，可以按下Ctrl+C停止软件，请保管好你ca文件夹里的文件，不当传播可能会导致你的访问被劫持。本软件仅供学习交流，请勿用于非法用途")
    webbrowser.open("https://www.pixiv.net")
    cmd(
        r".\bin\main.exe -c .\ca\ca.pem -k .\ca\ca.key -l .\config\domain.conf"+ps)
except:
    print("程序已结束")
else:
    print("程序发生异常，已紧急结束，相关报错问题请搜索最后一行fatal msg后面的内容进行处理")
    r'''
    ex = cmdgbk("netstat -ano")
    pattern = re.compile(r'127.0.0.1:443.* (\d+)')
    result1 = pattern.findall(ex)
    # print(result1)
    if(result1 == []):
        pattern = re.compile(r'127.0.0.1:80.* (\d+)')
        result1 = pattern.findall(ex)
    if(result1 == []):
        pattern = re.compile(r'127.0.0.1:80.* (\d+)')
        result1 = pattern.findall(ex)
    if(result1 != []):
        ex = cmdgbk('tasklist|findstr "%s"' % ''.join(result1))
        pattern = re.compile(r"^(.*?)  ")
        result1 = pattern.findall(ex)
        print("请在任务管理器中结束%s软件的运行，然后重新启动软件才能继续使用" % ''.join(result1))
        time.sleep(2)
        cmd(r"C:\WINDOWS\system32\taskmgr.exe")
        '''
os.system('pause')
# print(1)
# 读文件
