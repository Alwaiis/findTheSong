from PyPDF2 import PdfReader


# ->[str] means that the def must return an array of strings
def extract_text_from_pdf(pdf_file: str)-> [str]:
    with open(pdf_file, 'rb') as pdf:
        reader = PdfReader(pdf, strict=False)
        pdf_text = []
        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)

        return pdf_text


if __name__ == '__main__':
    extracted_text = extract_text_from_pdf('TLQNF.pdf')
    for text in extracted_text:
        print(text)
