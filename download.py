# -*- coding: utf-8 -*-

################################################################################################################
##  Script tải các ảnh từng trang riêng lẻ của tài liệu trên VNU Repository và nén thành 1 file pdf duy nhất  ##
##  Có thể áp dụng cho bất kỳ trang web xem tài liệu trực tuyến nào có dạng load từng trang là các ảnh riêng  ##
################################################################################################################ 

import urllib.request
import os, sys
import math
from PIL import Image
from fpdf import FPDF
from pathlib import Path
from datetime import datetime

pdf = FPDF()
now = datetime.now()

file_name = "TenTaiLieu" + now.strftime("_%Y%m%d_%H%M%S")
total_page = 95
url_pattern = "https://repository.vnu.edu.vn/flowpaper/services/view.php?doc=63004733082370466556112451057011910599&format=jpg&page={}&subfolder=63/00/47/"

output_image_directory = "output/{}/images".format(file_name)
output_pdf_filename = "output/{}/{}.pdf".format(file_name, file_name)

print("\nStart script download pdf file for document " + file_name + "\n", flush=True)

if not os.path.exists(output_image_directory):
    os.makedirs(output_image_directory)

animation = ["[o_________]","[oo________]", "[ooo_______]", "[oooo______]", "[ooooo_____]", "[oooooo____]", "[ooooooo___]", "[oooooooo__]", "[ooooooooo_]", "[oooooooooo]"] 

for page in range(1, total_page+1):
    sys.stdout.write("\r[+] Downloading image... " + animation[math.ceil(page/total_page*10)-1] + " " + str(int(page/total_page*100))+ "% " + "| {}/{} pages".format(page, total_page))
    sys.stdout.flush()

    imageFile = "{}/{}.png".format(output_image_directory, page)
    url = url_pattern.format(page)
    urllib.request.urlretrieve(url, imageFile)
    cover = Image.open(imageFile)
    width, height = cover.size

    # convert pixel in mm with 1px=0.264583 mm
    width, height = float(width * 0.264583), float(height * 0.264583)

    # given we are working with A4 format size 
    pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

    # get page orientation from image size 
    orientation = 'P' if width < height else 'L'

    #  make sure image size is not greater than the pdf format size
    width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
    height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']

    pdf.add_page(orientation=orientation)

    pdf.image(imageFile, 0, 0, width, height)

print("\n[+] Exporting image to pdf...", flush=True)
pdf.output(output_pdf_filename, "F")

print("\nDone!!!\n", flush=True)
print("File download at:\n" + os.path.join(os.path.dirname(os.path.abspath(__file__)), Path(output_pdf_filename)), flush=True)