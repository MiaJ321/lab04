import PyPDF2

def pdf_to_text(pdf_path, txt_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
    
    print(f"转换完成：{pdf_path} -> {txt_path}")

if __name__ == "__main__":
    pdf_to_text("lab04_CN.pdf", "lab04_CN.txt") 