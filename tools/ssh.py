import paramiko

username = "admin"
password = "password"
hostList = ["192.168.60.51", "192.168.60.52"]

ssh = paramiko.SSHClient()

for host in hostList:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username = username, password = password)
    stdin, stdout, stderr = ssh.exec_command('ovs-ofctl dump-groups br0')
    print(stdout.readlines())
    ssh.close
