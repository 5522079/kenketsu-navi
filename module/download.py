import os

import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader, PdfWriter


site = 'https://www.jrc.or.jp/donation/blood/data/'
response = requests.get(site)
soup = BeautifulSoup(response.content, "html.parser")

row = soup.find("tr")
pdf = row.find("a", href=True)
pdf_url = pdf['href']
if not pdf_url.startswith("https"):
    pdf_url = '/'.join(site.split('/')[:3]) + pdf_url  # 有効なURLに変換
    # print(f"Downloading PDF: {pdf_url}")

pdf_response = requests.get(pdf_url)
if pdf_response.status_code == 200:
    tmp_pdf = "../data/tmp.pdf"
    with open(tmp_pdf, 'wb')as pdf_file:
        pdf_file.write(pdf_response.content)
    
    # PDFの1ページ目を抽出
    reader = PdfReader(tmp_pdf)
    writer = PdfWriter()
    writer.add_page(reader.pages[0])
    first_page_pdf = "../data/row_data.pdf"
    with open(first_page_pdf, 'wb') as first_page_pdf_file:
        writer.write(first_page_pdf_file)
    
    os.remove(tmp_pdf)