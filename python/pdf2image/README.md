# pdf2Image

## Overview

Often times information we want to analyze will be stored in PDF format. While it is sometimes possible to parse the content of a PDF file using [PyPDF2](https://pypi.org/project/PyPDF2/), most PDFs are essentially equivalent to images. That is, we can't simply copy and paste content from the pdf like we would from a word document or regular text file.

This means to extract data from the PDF, we'll need to do optical character recognition with a library like [pytesseract](https://pypi.org/project/pytesseract/).

Before we do that, we'll first need to convert our PDF file into a batch of images, creating one image for each page in the PDF. We'll use [pdf2image](https://pypi.org/project/pdf2image/) to do this.

The code below demonstrates creating a `PDFConverter` class for efficiently managing this process. Using python classes can help us organize our processing, make our code more legible and less redundant, as well as more modular and reusable.

## Setup

Note that you'll first need to install the pdf2image dependency poppler first. You can install it with homebrew:

```
brew install poppler
```

In our project directory, we'll create two folders `pdfs`, and `output`, and our `main.py` script

```md
- main.py
- pdf
- output
```

Our `main.py` script will work like this:

1. For each pdf in the `pdfs` folder, create a directory in the `output` folder
2. For each page in a pdf, generate an image and save it to the folder

So after we're done running the script, our project directory will look like this:

```md
- main.py
- output
  - pdf1.pdf
    - pdf1.pdf_page_1
    - pdf1.pdf_page_2
  - pdf1.pdf
    - pdf2.pdf_page_1
    - pdf2.pdf_page_2
- pdfs
  - pdf1.pdf
  - pdf2.pdf
```

## main.p

Let's first import our dependencies:

```python
# for easy debugging
from icecream import ic
# for working with file paths
import os
# for converting our images
from pdf2image import convert_from_path
# for handling user input
import click
```

Then we set up `INPUT_DIR` and `OUTPUT_DIR` variables, specifying the
`pdfs` and `output` folders we made earlier:

```python
# define the input directory where our PDFs are stored
INPUT_DIR = os.path.join(os.path.curdir, 'pdfs')
# define the directory the images will be written to
OUTPUT_DIR = os.path.join(os.path.curdir, 'output')
```

Next let's setup our `PDFConverter` class. We'll create descriptive variables properties for this class like `allInputPDFs` and `PDFsToConvert` that help us organize and reference the files we're processing:

```python
# create a PDFConverter for managing the conversion process
class PDFConverter():
    def __init__(self):
        #all of the pdf files in our pdfs folder
        self.allInputPDFs = []
        #we may not want to convert all of the pdfs each time we run our script. For example, if we add new pdfs at a later point, we may want to only process the new pdfs in order to save time. If self.overwriteExisting is true, our script will reprocess each pdf, but if it is False, then it will check to see which pdfs have been already been converted and skip them
        self.overwriteExisting = False
        #The list of pdfs we will convert. If self.overwriteExisting is True, then PDFsToConvert will be the same as self.allInputPDFs, otherwise it will be equal to self.allInputPDFs - alreadyProcessedPDFs.
        self.PDFsToConvert = []
        #The list of pdfs already converted and present in our output folder.
        #weather or not already converted pdfs should be overwritten and skipped
        self.alreadyProcessedPDFs = []
        #The directory with our pdf files
        self.sourceDir = ""
        #The directory where we will save our images
        self.outDir = ""

    def convert_directory(self, sourceDir: str, outDir: str) -> None:
        #set our sourceDir and outDir variables
        self.sourceDir = sourceDir
        self.outDir = outDir
        #get a list of pdfs in our sourDir
        self.get_pdfs()
        #get the list of pdfs we have previously processed
        self.check_processed_PDFs()
        #prompt the user to input if they would like to convert and overwrite all pdfs
        if click.confirm('Found {} previously converted Files, do you want to overwrite these PDFs?'.format(len(self.alreadyProcessedPDFs)), default=False):
            self.overwriteExisting = True
        #based on the user input, set which pdfs are to be converted
        self.set_pdfs_to_convert()
        #convert and save the pdfs to images
        self.write_images()

        print("Successfully converted {} PDFs to Images".format(len(self.PDFsToConvert)))
    #sets which pdfs will be converted based on the value of self.overwriteExisting
    def set_pdfs_to_convert(self):
        if self.overwriteExisting:
            self.PDFsToConvert = self.allInputPDFs
        else:
            self.PDFsToConvert = list(set(self.allInputPDFs) - set(selfalreadyProcessedPDFs))
    #checks for pdfs in our pdfs folder which have alreayd been outputted to our self.outDir. If there is a directory with a name that matches the pdf file, then we add that pdf to self.alreadyProcessedPDFs.
    def check_processed_PDFs(self):
        converted = os.listdir(self.outDir)
        for pdfFile in self.allInputPDFs:
            base = os.path.basename(pdfFile)
            if base in converted:
                self.alreadyProcessedPDFs.append(pdfFile)
    #gets a list of all the files in our self.sourceDir
    def get_pdfs(self) -> None:
        for file in os.listdir(self.sourceDir):
            pdf_path = os.path.join(self.sourceDir, file)
            self.allInputPDFs.append(pdf_path)
    #Creates a directory for each of the pdfs in self.PDFsToConvert, then uses pdf2image to convert each page from the pdf into an image. The images are then saved in the the directory.
    def write_images(self)->None:
        for index, pdf in enumerate(self.PDFsToConvert):
            print("processing PDF {} of {}".format(index, len(self.PDFsToConvert)))
            pdf_image_pages =  convert_from_path(pdf)
            out_put_dir = os.path.join(self.outDir, os.path.basename(pdf))
            num_images = len(pdf_image_pages)
            if not os.path.exists(out_put_dir):
                os.makedirs(out_put_dir)
            for index, img in enumerate(pdf_image_pages):
                filename = os.path.basename(out_put_dir) + "_page_{}".format(index) + ".jpg"
                img_file_path = os.path.join(out_put_dir, filename)
                print("Saved {} of {} pages to Image".format(index, num_images))
                img.save(img_file_path, 'JPEG')

```

Here's how we'd invoke our class:

```python
def main():
    converter = PDFConverter()
    converter.convert_directory(INPUT_DIR, OUTPUT_DIR)
main()
```
