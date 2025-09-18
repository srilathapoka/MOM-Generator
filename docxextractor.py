from docx import Document

def text_extractor_docx(docx_file):
    docx=Document(docx_file)
    docx_text=''.join([p.text for p in docx.paragraphs])
    
    return docx_text