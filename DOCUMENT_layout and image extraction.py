import torch
from tkinter import *
from tkinter import messagebox
import os
from math import sqrt
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path
from tkinter import filedialog as fd

def getnumpages(filepath,filename):
    with open(os.path.join(filepath, filename), "rb") as pdffile:
        pdf = PdfFileReader(pdffile)
        return pdf.getNumPages()

# path to where you put the Yolov5 folder
yolovlink = "...path/to/yolov5-master"


def runModel():
 paths = [b.get() for b in boxes]
 outlocation = box0.get()
 outpaths = [outlocation + '\\' + p.split('\\')[-1] for p in paths]

 sizeReduction = float(sizeReductionBox.get())
 factor = sqrt((100-sizeReduction)/100)
 for o in outpaths:
  if not os.path.exists(o):
     os.mkdir(o)
 threshold = float(thresholdBox.get())
 weight_path = fd.askopenfilename()  # get weights path
 model = torch.hub.load(yolovlink, 'custom', path=weight_path, source='local')
 ctr=0
 for p in paths:
  outpath = outpaths[ctr]
  ctr+=1
  temporary = os.path.join(outpath,'temporary')
  if not os.path.exists(os.path.join(outpath,'temporary')):
    temporary = os.path.join(outpath,'temporary')
    os.mkdir(temporary)

  with os.scandir(p) as files:
    for file in files:
     filename=file.name
     saved_filename = filename.split('.')[0] + '.png'
     saved_filename_fullpath = os.path.join(temporary, saved_filename)
     if filename.split('.')[-1]=='pdf':
        try:
         number_of_pages=getnumpages(p,filename)

         for i in range(1,number_of_pages,10):

              images = convert_from_path(os.path.join(p,filename),dpi=95,first_page=i,last_page=min(i+9,number_of_pages))
              for j in range(len(images)):
                 pageno = i + j
                 imsize=images[j].size
                 newsize = (int(factor*imsize[0]),int(factor*imsize[1]))
                 im1 = images[j].resize(newsize)
                 im1.save(saved_filename_fullpath,'PNG')
                 result_deteced_from_image = model(saved_filename_fullpath)
                 data_detected = result_deteced_from_image.pandas().xyxy[0]

                 if data_detected.shape[0]>0:
                  for k in range(data_detected.shape[0]):
                     if data_detected['confidence'][k] > threshold:
                         confidence = round(data_detected['confidence'][k],2)
                         imc = images[j].crop((int(data_detected['xmin'][k]/factor), int(data_detected['ymin'][k]/factor),int(data_detected['xmax'][k]/factor), int(data_detected['ymax'][k]/factor)))
                         image_name = str(confidence) + '_page_' + str(pageno) + '_' + filename.split('.')[0] + '_imageNumber_' + str(k+1)
                         imc.save(os.path.join(outpath,image_name+'.png'))
        except:
                 print('ERROR: Cannot extract pages from file {}'.format(filename))
  messagebox.showinfo("Info","All files processed")


window = Tk()
window.geometry('750x650')
window.title('Image classification')
frame1 = LabelFrame(window,text = "Paths",width = 500,height = 600)
frame1.place(x=20,y=40)

frame2 = LabelFrame(window,text = "Set parameters",width = 200,height = 240)
frame2.place(x=535,y=40)

frame3 = LabelFrame(window,text = "Controls",width = 200,height = 350)
frame3.place(x=535,y=290)

label1 = Label(frame1,text="Path to output images")
label1.place(x=5,y=1)

label2 = Label(frame1,text="Paste in paths to images below. \nAdd more boxes if images are in several folders\n Output images will appear in output folder")
label2.place(x=5,y=60)

label3 = Label(frame2,text="Confidence threshold:")
label3.place(x=5,y=10)
thresholdBox = Entry(frame2,width=30)
thresholdBox.place(x=5,y=36)
thresholdBox.insert(0,'0.1')

label4 = Label(frame2,text="Image size reduction %")
label4.place(x=5,y=94)
sizeReductionBox = Entry(frame2, width=30)
sizeReductionBox.place(x=5,y=120)
sizeReductionBox.insert(0,'0')

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

Button(frame3, text="Add folder link box",command = add_folder,width=25).place(x=5,y=20)
Button(frame3, text="Run",command = runModel,width=25).place(x=5,y=80)

mainloop()