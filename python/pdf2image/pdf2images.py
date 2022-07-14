from icecream import ic
import os
from pdf2image import convert_from_path
import click

# define the input directory where our PDFs are stored
INPUT_DIR = os.path.join(os.path.curdir, 'pdfs')
# define the directory the images will be written to
OUTPUT_DIR = os.path.join(os.path.curdir, 'output')

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
        for pdfFile in self.allInputPDFs:
            base = os.path.basename(pdfFile)
            if base in converted:
                self.alreadyProcessedPDFs.append(pdfFile)

    def collect_pdf_paths(self) -> None:
        for file in os.listdir(self.sourceDir):
            pdf_path = os.path.join(self.sourceDir, file)
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
                print("Saved {} of {} pages to Image".format(index, num_images))
                img.save(img_file_path, 'JPEG')


def main():
    converter = PDFConverter()
    converter.convert_directory(INPUT_DIR, OUTPUT_DIR)

main()
