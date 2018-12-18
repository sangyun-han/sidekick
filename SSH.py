import paramiko

username = "root"
password = "root"
hostList = ["192.168.60.51"]

ssh = paramiko.SSHClient()

for host in hostList:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username = username, password = password)
    stdin, stdout, stderr = ssh.exec_command("ls")
    print(stdout.readlines())
    ssh.close
