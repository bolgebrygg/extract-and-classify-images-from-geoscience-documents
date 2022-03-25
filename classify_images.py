from lobe import ImageModel
from tkinter import *
from tkinter import messagebox
def runModel():

 modelLink=box0.get()
 model = ImageModel.load(modelLink)

 from pathlib import Path
 import shutil
 import os
 done=[]

 # get a list of all image directories from the gui:
 paths = [(box.get()).strip() for box in boxes]
 ctr = 0
 while ctr < len(paths):
     if paths[ctr] == "" or paths[ctr] == " ":
         paths.pop(ctr)
     else:
         ctr += 1

 paths = [n + '\\' for n in paths]

 # output image paths are placed in a directory at the same level as where the input folder resides
 pathOuts = [n.replace(n.split('\\')[-2],"Classified_"+n.split('\\')[-2]) for n in paths]

 # open folder, read recursively all files
 out_counter=0
 for path in paths:
  counter = 0
  pathOut=pathOuts[out_counter]
  folder = path.split('\\')[-2]
  print(folder)
  Path(pathOut).mkdir(parents=True, exist_ok=True)
  out_counter+=1
  for dname, dirs, files in os.walk(path):
     for fname in files: # loop over all of them
         try:
             fpath = os.path.join(dname, fname) #input file
             if fname not in done: # this bit just makes sure you dont process the same file twice
              result = model.predict_from_file(fpath) # run prediction

              prefix = str(result.labels[0][1])[0:6]+'_'
              done.append(prefix+fname)
              fpathOutFull = os.path.join(pathOut+result.prediction, prefix+fname) # ) # output folder
              Path(pathOut+result.prediction).mkdir(parents=True, exist_ok=True) # create folder if it does not exist yet
              shutil.copy(fpath,fpathOutFull)

              counter+=1
              print(str(counter) ," images from {} processed".format(folder))

         except:
             pass
 messagebox.showinfo("Message", "Processing complete")

# for the GUI:
window = Tk()
window.geometry('750x650')
window.title('Image classification')
frame1 = LabelFrame(window,text = "Paths",width = 500,height = 600)
frame1.place(x=20,y=40)

frame2 = LabelFrame(window,text = "Controls",width = 200,height = 600)
frame2.place(x=535,y=40)

label1 = Label(frame1,text="Paste in path to model")
label1.place(x=5,y=1)

label2 = Label(frame1,text="Paste in paths to images below. \nAdd more boxes if images are in several folders\n Output images will appear in parent folder")
label2.place(x=5,y=60)

box0 = Entry(frame1,width=80)
box0.place(x=5,y=23)
nums=[75]
boxes=[]

#method for adding space for additional directories
def add_folder():
    n=nums[0]
    box1 = Entry(frame1, width=80)
    box1.place(x=5, y=n+40)
    nums[0]+=40
    boxes.append(box1)

Button(frame2, text="Add folder link box",command = add_folder,width=25).place(x=5,y=20)
Button(frame2, text="Run",command = runModel,width=25).place(x=5,y=70)

mainloop()
