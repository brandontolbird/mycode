#!/usr/bin/env python3
## Moving files with SFTP

import getpass
## import paramiko so we can talk SSH
import paramiko
import os

am_i_done = False

connect_dict = {}
connect_prompts = [('ip', 'Enter IP: '), 
                   ('username', 'Enter user: '),
                   ('password', 'Enter passwd: ')]

def movethemfiles(sftp):
  ## iterate across the files within directory
  remote_dir_exists = False
  while not remote_dir_exists:
    remote_dir = input("Specify the remote target directory: ")
    if remote_dir:
      try:
        sftp.chdir(remote_dir)
      except IOError:
        print("Path '{}' doesn't exist on the remote server!".format(remote_dir))
      else:
        remote_dir_exists = True 
    else:
      print("Please input a directory.")
  for x in os.listdir("/home/student/filestocopy/"): # iterate on directory contents
    if not os.path.isdir("/home/student/filestocopy/"+x): # filter everything that is NOT a directory
      sftp.put("/home/student/filestocopy/"+x, x) # move file to target location


while not am_i_done:
  print("Input server info. Input done on at least one of the three prompts to end script.")
  for key, prompt in connect_prompts:
    if 'pass' in key:
      response = getpass.getpass(prompt)
    else:
      response = input(prompt)
    if response != "done":
      connect_dict[key] = response
    else:
      am_i_done = True

  if len(connect_dict) == len(connect_prompts):
    try:
      ## where to connect to
      ip = connect_dict.get('ip')
      t = paramiko.Transport(ip, 22) ## IP and port

      ## remove ip from the dictionary, so we can pass the whole thing with **
      del connect_dict['ip']
      ## how to connect (see other labs on using id_rsa private / public keypairs)
      t.connect(**connect_dict)

      ## Make an sftp connection object
      sftp = paramiko.SFTPClient.from_transport(t)
      movethemfiles(sftp)
      print("Successfully moved files to target '{}'!".format(ip))
      ## close the connection
      sftp.close() # close the connection
    except:
      print("Some exception happened.")
      if sftp and sftp.is_active():
        sftp.close()
