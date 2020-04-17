#3. create shortcut on desktop
#5. all those things driven by nice tkinter window :)

import os
import threading
import sys
from datetime import datetime
import subprocess

try:
	import tkinter as tkinter
	import tkinter.ttk as ttk
	import tkinter.messagebox as messagebox
	import tkinter.scrolledtext as scrolledtext
except (ImportError, ModuleNotFoundError):
	import Tkinter as tkinter
	import Tkinter.ttk as ttk
	import Tkinter.messagebox as messagebox
	import Tkinter.scrolledtext as scrolledtext

def ShowErrorMessage():
	root = tkinter.Tk()
	root.withdraw()
	messagebox.showinfo("Installation error!", "Cannot use git command. Make sure if you have git installed\non your machine.\nFor further information visit https://github.com/m4reQ/Oss-2.0")
	sys.exit()

try:
	subprocess.Popen("git")
except OSError:
	ShowErrorMessage()

REPO_URL = "https://github.com/m4reQ/Oss-2.0"
TARGET_DIR = os.path.expandvars(r"%APPDATA%\Oss")

MODULES = ["pygame", "requests", "Pillow", "pywin32", "wmi", "GitPython", "winshell"]

TASK_COUNT = len(MODULES) + 4

def GetDate():
	return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

class Window:
	def __init__(self, title, geometry, icon=None):
		self.title = title
		self.width = int(geometry.split('x')[0])
		self.height = int(geometry.split('x')[1])

		self.master = tkinter.Tk()
		self.canvas = tkinter.Canvas(self.master, width=self.width, height=self.height - self.height / 3, highlightthickness=0)

		self.master.title(self.title)
		self.master.geometry(geometry)
		if icon:
			self.master.iconbitmap(icon)
		self.master.resizable(False, False)
		self.master.configure(bg="white")

		self.canvas.config(bg="white")
		self.canvas.pack()

	def Update(self):
		self.master.update()
	
	def ReinitCanvas(self, size):
		self.canvas = tkinter.Canvas(self.master, width=size[0], height=size[1], highlightthickness=0)
		self.canvas.config(bg="white")
		self.canvas.pack()

class InstallationScene:
	current = 1
	installer = None

	@staticmethod
	def Present(window):
		if InstallationScene.current == 1:
			InstallationScene.FirstScene(window)
		elif InstallationScene.current == 2:
			InstallationScene.SecondScene(window)
		elif InstallationScene.current == 3:
			InstallationScene.ThirdScene(window)
	
	@staticmethod
	def NextScene(master):
		for widget in master.winfo_children():
			widget.destroy()
		InstallationScene.current += 1
	
	@staticmethod
	def FirstScene(window):
		mainIcon = tkinter.PhotoImage(file="icon@256.pgm")
		window.master.img = mainIcon #prevent garbage collection
		window.canvas.create_image(window.width / 2 - mainIcon.width() / 2, 20, anchor=tkinter.NW, image=mainIcon)
		window.canvas.create_text(window.width / 2, 20 + mainIcon.height() + 32, text="Welcome to \nOss! installer", font=("Purisa", 24), justify=tkinter.CENTER)
		button = tkinter.Button(window.master, text="Install", command=InstallationScene.installer.Proceed, font=("Purisa", 17))
		button.pack()
		window.Update()
		button.place(x=window.width - button.winfo_width() - 10, y=window.height - button.winfo_height() - 10)
	
	@staticmethod
	def SecondScene(window):
		mainIcon = tkinter.PhotoImage(file="icon@128.pgm")
		window.master.img = mainIcon #prevent garbage collection
		window.canvas.create_image(20, 20, anchor=tkinter.NW, image=mainIcon)
		window.canvas.create_text(20 + mainIcon.width() + 5, 20 + mainIcon.height() / 2, text="Installing Oss...", font=("Purisa", 24),  anchor=tkinter.NW)
		bar = ttk.Progressbar(window.master, maximum=100, variable=InstallationScene.installer.progress, orient='horizontal', mode='determinate')
		bar.pack(fill=tkinter.BOTH)
		textFrame = tkinter.Frame(window.master, bg="white")
		textFrame.pack(expand=True, fill=tkinter.BOTH)
		installText = scrolledtext.ScrolledText(textFrame, width=30, height=10, wrap=tkinter.WORD)
		installText.pack(expand=True, fill=tkinter.BOTH)
		button = tkinter.Button(window.master, text="End Installation", command=InstallationScene.installer.End, font=("Purisa", 17), state=tkinter.DISABLED)
		button.pack(side=tkinter.RIGHT)
		
		while True:
			prog = InstallationScene.installer.progress.get()
			if not prog == 100:
				InstallationScene.installer.progress.set(InstallationScene.installer.progressInt)
				installText.delete('1.0', tkinter.END)
				installText.insert(tkinter.END, InstallationScene.installer.installationInfo)
				installText.yview_pickplace(tkinter.END)
				window.Update()
			else:
				InstallationScene.installer.installationThread.join()
				button.config(state=tkinter.NORMAL)
				installText.yview_pickplace(tkinter.END)
				window.Update()

	@staticmethod
	def ThirdScene(window):
		mainIcon = tkinter.PhotoImage(file="icon@128.pgm")
		window.master.img = mainIcon #prevent garbage collection
		window.canvas.create_image(20, 20, anchor=tkinter.NW, image=mainIcon)
		window.canvas.create_text(window.width / 2, window.height / 2, text="Thanks for installing Oss.\nIf you encounter any problems please visit\nmain project page.\nGood luck, have fun and\nplz enjoy game ;)", font=("Purisa", 17), justify=tkinter.CENTER)
		button = tkinter.Button(window.master, text="Close", command=InstallationScene.installer.Done, font=("Purisa", 17))
		button.pack()
		window.Update()
		button.place(x=window.width - button.winfo_width(), y=window.height - button.winfo_height())

class Installer:
	def __init__(self):
		InstallationScene.installer = self
		self.window = Window("Oss! - Installer", "470x560", "icon@256.ico")
		
		InstallationScene.Present(self.window)

		self.progress = tkinter.IntVar()
		self.progress.set(0)

		self.progressInt = 0

		self.isRunning = True
		self.installationThread = None

		self.installationInfo = ""

	def Run(self):
		while self.isRunning:
			try:
				self.window.Update()
			except tkinter.TclError:
				self.isRunning = False
	
	def Proceed(self):
		InstallationScene.NextScene(self.master)
		self.window.ReinitCanvas((self.window.width, 153))
		self.installationThread = threading.Thread(target=self.Install)
		self.installationThread.start()
		InstallationScene.Present(self.window)
	
	def Install(self):
		#modules installation using pip
		processes = []
		for module in MODULES:
			self.installationInfo += "[{}] Starting installation: {}\n".format(GetDate(), module)
			p = subprocess.Popen("py -m pip install {} --user".format(module), shell=False, creationflags=0x08000000)
			processes.append((p, module))
		
		for pair in processes:
			pair[0].wait()
			self.progressInt += 100 / TASK_COUNT
			self.installationInfo += "[{}] Module installation completed: {}\n".format(GetDate(), pair[1])

		self.installationInfo += "[{}] Modules installation complete.\n".format(GetDate())
		
		#testing modules
		self.installationInfo += "[{}] Testing installed modules.\n".format(GetDate())
		try:
			import PIL
			import pygame
			import requests
			import wmi
			import pywin32_system32
			from git.repo.base import Repo
			import winshell
		except (ImportError, ModuleNotFoundError):
			self.installationInfo += "[{}] Import test failed.\n".format(GetDate())
		else:
			self.installationInfo += "[{}] Test succeded.\n".format(GetDate())
		self.progressInt += 100 / TASK_COUNT

		#download repository
		self.installationInfo += "[{}] Downloading Oss.\n".format(GetDate())
		try:
			Repo.clone_from(REPO_URL, TARGET_DIR, branch='master')
		except Exception as e:
			self.installationInfo += "[{}] Repository download fail: {}\n".format(GetDate(), e)
		else:
			self.installationInfo += "[{}] Repository downloaded.\n".format(GetDate())
		self.progressInt += 100 / TASK_COUNT

		#remove unnecessary files
		self.installationInfo += "[{}] Removing standard repository files.\n".format(GetDate())
		print(os.path.join(TARGET_DIR, ".git"))
		subprocess.Popen('rmdir /S /Q "{}"'.format(os.path.join(TARGET_DIR, ".git")), shell=True, creationflags=0x08000000)
		subprocess.Popen('rmdir /S /Q "{}"'.format(os.path.join(TARGET_DIR, ".github")), shell=True, creationflags=0x08000000)
		subprocess.Popen('del /S /Q "{}"'.format(os.path.join(TARGET_DIR, ".gitignore")), shell=True, creationflags=0x08000000)
		subprocess.Popen('del /S /Q "{}"'.format(os.path.join(TARGET_DIR, "README.md")), shell=True, creationflags=0x08000000)
		subprocess.Popen('del /S /Q "{}"'.format(os.path.join(TARGET_DIR, "requirements.txt")), shell=True, creationflags=0x08000000)
		self.progressInt += 100 / TASK_COUNT

		#create shortcut
		from win32com.client import Dispatch
		self.installationInfo += "[{}] Creating desktop shortcut.".format(GetDate())
		desktop = winshell.desktop()
		path = os.path.join(desktop, "Oss!.lnk")
		target = os.path.expandvars(r'C:\Windows\System32\cmd.exe')
		args = r'/k py -3 "%appdata%\Oss\oss\oss.py"'
		wDir = os.path.expandvars(r"%appdata%\Oss\oss")
		iconPath = os.path.expandvars(r"%appdata%\Oss\oss\Resources\icons\icon@256.ico")
		
		shell = Dispatch("WScript.Shell")
		shortcut = shell.CreateShortCut(path)
		shortcut.TargetPath = target
		shortcut.WorkingDirectory = wDir
		shortcut.Arguments = args
		shortcut.IconLocation = iconPath
		shortcut.save()

		self.progressInt += 100 / TASK_COUNT
	
	def End(self):
		InstallationScene.NextScene(self.master)
		self.window.ReinitCanvas((self.window.width, 400))
		InstallationScene.Present(self.window)
	
	def Done(self):
		self.isRunning = False

	@property
	def canvas(self):
		return self.window.canvas
	
	@property
	def master(self):
		return self.window.master

if __name__ == "__main__":
	Installer().Run()