from fpdf import FPDF

class PDF(FPDF):
    def header(self, title=""):

        #self.image("../docs/fpdf2-logo.png", 10, 8, 33)
        # Setting font: helvetica bold 15
        self.set_font("helvetica", "B", 16)
        # Moving cursor to the right:
        #self.multi_cell(80)
        # Printing title:
        self.set_y(20)
        self.multi_cell(180, 10, title, align="C")
        # Performing a line break:
        self.ln(20)