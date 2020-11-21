import textract
from pptx import Presentation
import PyPDF2

class FileReader():

    def __init__(self, filename):

        self.filename = filename
        self.path = '/'.join(filename.split("/")[0:-1])
        self.name = filename.split("/")[-1]
        self.extension = filename.split("/")[-1].split(".")[-1]
        self.text = self.extractText()

    def extractText(self):

        if self.extension == "doc" or self.extension == "docx":
            text = self.read_doc()
        elif self.extension == "pdf":
            text = self.read_pdf()
        elif self.extension == "txt":
            text = self.read_text()
        elif self.extension == "ppt" or self.extension == "pptx":
            text = self.read_ppt()

        return text


    def read_pdf(self):

        with open(self.filename, "rb") as f:
            reader = PyPDF2.PdfFileReader(f)
            page = reader.getPage(0)
            text = page.extractText()
        return text

    def read_doc(self):

        text = textract.process(self.filename)
        text = text.rstrip()

        encoding = 'utf-8'
        return text.decode(encoding)
    
    def read_excel(self):
        pass


    def read_text(self):

        f = open(self.filename, "r")
        return(f.read())


    def read_ppt(self):

        def extract_shape_txt(shape):
            if hasattr(shape, "text"):
                shapetext = shape.text
                return shapetext
            else:
                return ''

        prs = Presentation(self.filename)
        text = ' '
        for slide in prs.slides:
            for shape in slide.shapes:
                if "GroupShape" in shape.__str__():
                    for innershape in shape.shapes:
                        text += extract_shape_txt(innershape)
                else:
                    text += extract_shape_txt(shape)

        return text


    def read_image(self):
        pass

