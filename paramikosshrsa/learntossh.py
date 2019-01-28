#!/usr/bin/env python3

## import paramiko so we can talk SSH
import paramiko
import os

## shortcut issuing commands to remote
def commandissue(command_to_issue):
  ssh_stdin, ssh_stdout, ssh_stderr = sshsession.exec_command(command_to_issue)
  return ssh_stdout.read()

sshsession = paramiko.SSHClient()

############# IF YOU WANT TO CONNECT USING UN / PW #############
#sshsession.connect(server, username=username, password=password)
############## IF USING KEYS #################

## mykey is our private key
mykey = paramiko.RSAKey.from_private_key_file("/home/student/.ssh/id_rsa")

## if we never went to this SSH host, add the fingerprint to the known host file
sshsession.set_missing_host_key_policy(paramiko.AutoAddPolicy())

host_input = ""
host_user_list = list()
print("Please input server IP/hostname and username pairs as comma-separated\n"
      "tuples (ex: 10.10.2.3,bender). Enter 'done' when finished.")
while host_input != "done":
  host_input = input(": ")
  if ',' in host_input and len(host_input.split(',')) == 2:
    host_user_list.append(host_input.split(','))

our_input = input("Input commands to run across the machines (comma-separated): ")
our_commands = our_input.split(',')

total_response = ""

for host_user_pair in host_user_list:
  ## creds to connect
  sshsession.connect(hostname=host_user_pair[0], username=host_user_pair[1], pkey=mykey)

  ## a simple list of commands to issue across our connection
  #our_commands = ["touch sshworked.txt", "touch create.txt", "touch file3.txt", "ls"]


  ## cycle through our commands, and issue them on the far end
  for x in our_commands:
    response = commandissue(x).decode('utf-8')
    total_response += "Ran '{}' command on host '{}' with user '{}'." \
    " It returned:\n{}".format(x, *host_user_pair, response)
    print(response)


with open("results.log","w") as out_file:
  out_file.write(total_response)

