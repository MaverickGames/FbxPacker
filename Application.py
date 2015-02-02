from Tkinter import *
from ttk import *
import tkFileDialog
import os


# Main Application class
class Application():
	def __init__(self, frame):
		# data
		self.openedFbxFiles = []

		# initialize sdk
		self.dirname = "results"
		if not os.path.exists(self.dirname):
			os.makedirs(self.dirname)

		# Tkinter settings
		self.master = frame
		self.master.config(width=500, height=600)

		reserved_packs = []

		self.b_open = Button(frame, text="Open", command=self.open_file)
		reserved_packs.append(self.b_open)

		self.item_view = Treeview(frame, columns=("files", "path"))
		self.item_view.column("#0", width=30)
		self.item_view.column("files", width=80)

		self.item_view.heading("files", text="File")
		self.item_view.heading("path", text="Path")
 
		self.item_view.bbox = (15, 15, 3000, 500)
		reserved_packs.append(self.item_view)

		for to_pack in reserved_packs:
			to_pack.pack()


	def open_file(self):
		# set file options
		self.opt = {}
		self.opt["defaultextension"] = ".fbx"
		self.opt["filetypes"] = [("Fbx Files", "*.fbx")]
		
		fbxFiles = tkFileDialog.askopenfiles(mode="rw", **self.opt)
		
		for fbxFile in fbxFiles:
			self.openedFbxFiles.append(fbxFile.name)
			self.item_view.insert("", "end", text=0, values=(os.path.basename(fbxFile.name), fbxFile.name))



# run if main
if __name__=="__main__":
	master=Tk()
	master.resizable(width=FALSE, height=FALSE)
	master.minsize(width=666, height=666)
	master.maxsize(width=666, height=666)
	Application(master)
	master.mainloop()