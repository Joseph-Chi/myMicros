import os,sys
import numpy as np
import pytesseract
import cv2
import time
from fastapi import FastAPI, Response, File, UploadFile

app = FastAPI()
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/OCR")
async def tOCR(file: UploadFile):
    
    t0=time.time()
    sublist=[]
    # define the image areas for OCR; each row represnt the two coordinates for single rectangle 
    areas=[[(300,1470),(440,1520)],
        [(300,1670),(400,1730)],
        [(300,1740),(400,1800)],
        [(300,1800),(470,1910)]]

    def prepImage(imgInput):
        imgOutputs=[] 
        imgInput.seek(0)
        b2n = np.frombuffer(imgInput.read(), np.uint8)
        img = cv2.imdecode(b2n, 1)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        
         
        for area in areas:
            index=areas.index(area)
            imgchop = img [area[0][1]:area[1][1],area[0][0]:area[1][0]]
            #  crop_img = img[y:y+h, x:x+w]
            if (index<1):
                ret,imgbw = cv2.threshold(imgchop,127,255,cv2.THRESH_BINARY)
            else:
                ret,imgbw = cv2.threshold(imgchop,127,255,cv2.THRESH_BINARY_INV)
                if (index==3):
                    imgbw= cv2.resize(imgbw, (80, 50), interpolation=cv2.INTER_CUBIC)
            imgOutputs.append(imgbw)
        return(imgOutputs)
     
    def recImage(imgInput):
            custom_config = r'-c tessedit_char_blacklist=/kKbB --psm 7'
            text = pytesseract.image_to_string(img,config=custom_config,lang='eng')
            return(text)
    
    imageOutputs = prepImage(file.file)
    for img in imageOutputs:
        text = recImage(img)
        text = text.replace("\n", "")
        sublist.append(text)
        
        
    # attrs = vars(file.file)
    # debugout=', '.join("%s: %s" % item for item in attrs.items())
   

    return {"filename": file.filename,
            "contentype": file.content_type,
            # "debug output": debugout,
            "Uszie": sublist[0],
            "AITime": sublist[1],
            "ULTime": sublist[2],
            "TTime": sublist[3]
            }
