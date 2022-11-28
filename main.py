# import the neccessary modules
import os, PyPDF2
import pypdfium2



# function to extract the individual pages from each pdf found
def split_pdf_pages(root_directory, extract_to_folder):
 # traverse down through the root directory to sub-directories
 for root, dirs, files in os.walk(root_directory):
  for filename in files:
   basename, extension = os.path.splitext(filename)
   # if a file is a pdf
   if extension == ".pdf":
    # create a reference to the full filename path
    fullpath = root + "\\" + basename + extension

    # open the pdf in read mode
    # opened_pdf = PyPDF2.PdfFileReader(open(fullpath, "rb"))
    with open(fullpath, "rb") as f:
      opened_pdf = PyPDF2.PdfFileReader(f)
      for i in range(opened_pdf.numPages):
       output = PyPDF2.PdfFileWriter()
       output.addPage(opened_pdf.getPage(i))

       with open(extract_to_folder + "\\" + basename + "-%s.pdf" % i, "wb") as output_pdf:
        output.write(output_pdf)


    # for each page in the pdf
      for i in range(opened_pdf.numPages):
    # write the page to a new pdf
       output = PyPDF2.PdfFileWriter()
       output.addPage(opened_pdf.getPage(i))

       with open(extract_to_folder + "\\" + basename + "-%s.pdf" % i, "wb") as output_pdf:
        output.write(output_pdf)




# function for renaming the single page pdfs based on text in the pdf
def rename_pdfs(extraced_pdf_folder, rename_folder,converted_folder):
 filenames = []

 # traverse down through the root directory to sub-directories
 for root, dirs, files in os.walk(extraced_pdf_folder):
  for filename in files:
   basename, extension = os.path.splitext(filename)
   # if a file is a pdf
   if extension == ".pdf":
    # create a reference to the full filename path
    fullpath = root + "\\" + basename + extension

    # open the individual pdf
    pdf_file_obj = open(fullpath, "rb")
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)

    # access the individual page
    page_obj = pdf_reader.getPage(0)
    # extract the the text
    pdf_text = page_obj.extractText()
    # print(pdf_text)
    pdf_lines = pdf_text.split('\n')

    for line in pdf_lines:
     if line.startswith('SHIP VIA'):
      line_num = pdf_lines.index(line) + 1

    for line in pdf_lines:
     if pdf_lines.index(line) == line_num:
      order_num = line.split(" ")[3]
      filenames.append(order_num)
      pdf_file_obj.close()
      print(filenames)
      print(order_num)

      filenamecount = 0
      for file in filenames:
       if (file == order_num):
        filenamecount += 1
        print("true")
      print(filenamecount)
      filenamecountstring = str(filenamecount)
      # rename the pdf based on the information in the pdf
      # os.rename(fullpath, rename_folder + "\\" + order_num + "_" + filenamecountstring + ".pdf")
      file_to_convert = rename_folder + "\\" + order_num + "_" + filenamecountstring + ".pdf"
      converted_file = converted_folder + "\\" + order_num + "_" + filenamecountstring + ".png"

      os.rename(fullpath, file_to_convert)
      pdf = pypdfium2.PdfDocument(file_to_convert)
      page = pdf.get_page(0)
      pil_image = page.render_to(
       pypdfium2.BitmapConv.pil_image, scale=600/72
      )
      pil_image.save(converted_file)



# def qvc_logging():
  #success
  #failure
  #monitor logs
  #Site 24/7 Checks for success every hour


def remove_processed_pdfs(root_dir,extract_to):
 root = os.listdir(root_dir)
 extracted = os.listdir(extract_to)


 for item in root:
  if item.endswith(".pdf"):
   os.remove(os.path.join(root_dir, item))

 for item in extracted:
  if item.endswith(".pdf"):
   os.remove(os.path.join(extract_to, item))




# parameter variables
root_dir = r"\\jeg-papi1\api\QVC\Inbox"
extract_to = r"\\jeg-papi1\api\QVC\Extracted"
rename_to = r"\\jeg-papi1\api\QVC\Renamed"
convert_to = r"\\jeg-papi1\api\QVC\Converted"
# use the two functions
split_pdf_pages(root_dir, extract_to)
rename_pdfs(extract_to,rename_to,convert_to)
remove_processed_pdfs(root_dir,extract_to)
