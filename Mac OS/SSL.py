import os

print(os.getcwd())

def cmd(command):
    ex = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    out, _ = ex.communicate()
    ex.wait()
    return out.decode()

os.system(r'open "'+os.getcwd()+r'/host"')