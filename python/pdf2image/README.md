# pdf2Image

Often times information we want to analyze will be stored in PDF format. While it is sometimes possible to parse the content of a PDF file using [PyPDF2](https://pypi.org/project/PyPDF2/), most PDFs are essentially equivalent to images. That is, we can't simply copy and paste content from the pdf like we would from a word document or regular text file.

This means to extract data from the PDF, we'll need to do optical character recognition with a library like [pytesseract](https://pypi.org/project/pytesseract/).

Before we do that, we'll first need to convert our PDF file into a batch of images, creating one image for each page in the PDF. We'll use [pdf2image](https://pypi.org/project/pdf2image/) to do this.

The code below demonstrates creating a `PDFConverter` class for efficiently managing this process. Using python classes can help us organize our processing, make our code more legible and less redundant, as well as more modular and reusable.

Let's import our dependencies:

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

Our directory structure for the project will look like this:

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

We'll have a directory full of our pdf files `pdf`, and an `output` directory for our images. For each pdf that we process, we'll create a directory, and then place the images from that pdf in the directory. This will make processing the images later easier.

So we setup `INPUT_DIR` and `OUTPUT_DIR ` variables:

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
        self.allInputPDFs = []
        self.PDFsToConvert = []
        self.existingConversions = []
        self.overwriteExisting = False
        self.alreadyProcessedPDFs = []
        self.sourceDir = ""
        self.outDir = ""

    def convert_directory(self, sourceDir: str, outDir: str) -> None:
        self.sourceDir = sourceDir
        self.outDir = outDir
        self.collect_pdf_paths()
        self.check_processed_PDFs()
        self.set_pdfs_to_convert()
        if click.confirm('Found {} previously converted Files, do you want to overwrite these PDFs?'.format(len(self.alreadyProcessedPDFs)), default=False):
            self.overwriteExisting = True
        self.write_images()

        print("Successfully converted {} PDFs to Images".format(len(self.PDFsToConvert)))

    def set_pdfs_to_convert(self):
        if self.overwriteExisting:
            self.PDFsToConvert = self.allInputPDFs
        else:
            self.PDFsToConvert = list(set(self.allInputPDFs) - set(self.alreadyProcessedPDFs))

    def check_processed_PDFs(self):
        converted = os.listdir(self.outDir)
        ic(converted)
        for pdfFile in self.allInputPDFs:
            base = os.path.basename(pdfFile)
            ic(base)
            if base in converted:
                self.alreadyProcessedPDFs.append(pdfFile)

    def collect_pdf_paths(self) -> None:
        for file in os.listdir(self.sourceDir):
            ic(file)
            ic(self.sourceDir)
            pdf_path = os.path.join(self.sourceDir, file)
            ic(pdf_path)
            self.allInputPDFs.append(pdf_path)

    def write_images(self)->None:
        for index, pdf in enumerate(self.PDFsToConvert):
            print("processing PDF {} of {}".format(index, len(self.PDFsToConvert)))
            pdf_image_pages =  convert_from_path(pdf)
            out_put_dir = os.path.join(self.outDir, os.path.basename(pdf))
            ic(os.path.basename(pdf))
            ic(out_put_dir)
            num_images = len(pdf_image_pages)
            if not os.path.exists(out_put_dir):
                os.makedirs(out_put_dir)
            for index, img in enumerate(pdf_image_pages):
                filename = os.path.basename(out_put_dir) + "_page_{}".format(index) + ".jpg"
                img_file_path = os.path.join(out_put_dir, filename)
                ic(img_file_path)
                print("Saved {} of {} pages to Image".format(index, num_images))
                img.save(img_file_path, 'JPEG')

```

Finally let's invoke our class:

```python
def main():
    converter = PDFConverter()
    converter.convert_directory(INPUT_DIR, OUTPUT_DIR)

main()
```
