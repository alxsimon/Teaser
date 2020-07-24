#!/usr/bin/env python
import os
import sys
major=sys.version_info[0]

errors=[]

def error(msg):
	errors.append(msg)

def sub(cmd,ignore_errors=False):
	if os.system(cmd) != 0:
		if not ignore_errors:
			errors.append("Command failed: %s"%cmd)
		return False
	else:
		return True

print("Checking Python version...")
if major != 2:
	error("Teaser currently requires Python 2! Version: %s"%str(sys.version_info))

print("Downloading software packages (Mappers and Simulators)...")
sub("wget http://www.cibiv.at/software/teaser/teaser_software.tar.gz")
sub("tar -zxvf teaser_software.tar.gz software/mason")
sub("rm teaser_software.tar.gz")

print("Downloading example reference genome (E. coli)...")
os.chdir("references")
sub("wget http://www.cibiv.at/software/teaser/E_coli.fasta")
os.chdir("..")

print("Building tools...")
os.chdir("tools")
tool_build_success=sub("g++ fastindex.cpp -O3 -o fastindex_build")
if tool_build_success:
	sub("mv fastindex_build fastindex")
os.chdir("..")

if len(errors)==0:
	print("Installation completed successfully!")
else:
	print("Errors occured during installation:")
	for msg in errors:
		print("\t%s"%msg)
