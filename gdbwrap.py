import subprocess
import sys
import os

_SCRIPTPATH=os.path.realpath(os.path.dirname(__file__))
_CMDFILE=os.path.join(_SCRIPTPATH, "start.gdb")
_PROMPT="USERINPUT>>>"

def _print_err(*msg):
	sys.stderr.write(
		" ".join(map(str, msg)) + "\n")

class GDBWrapper(object):
	def __init__(self, fname: str):
		self.fname = fname

		self.gdb = subprocess.Popen(
			["gdb", "--command", _CMDFILE, self.fname],
			stdout=subprocess.PIPE,
			stdin=subprocess.PIPE,
			stderr=subprocess.STDOUT)

		line=""
		while not line.endswith(_PROMPT):
			line = self.gdb.stdout.readline().decode("ascii").strip()

	def cmd(self, data: str):
		if self.gdb.poll() is not None:
			_print_err("!Err gdb exited")
			return None

		self.gdb.stdin.write(data.encode("ascii") + b"\n")
		self.gdb.stdin.flush()

		line = ""
		res  = ""
		while True:
			line = self.gdb.stdout.readline().decode("ascii").strip()
			if line.endswith(_PROMPT):
				break
			res += line + "\n"

		return res

	def kill(self):
		self.gdb.stdin.close()
		self.gdb.terminate()
		self.gdb.wait(timeout=0.2)

def open(fname: str):
	return GDBWrapper(fname)
