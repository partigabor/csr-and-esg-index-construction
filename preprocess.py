import pandas as pd
import regex as re
import os, sys
import xml.etree.ElementTree as et
import PyPDF2

path = "data-transcripts"

# a function to walk through all files in a folder and its subfolders
def list_files(dir):                                                                                                  
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).__next__()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file in files:                                                                                        
                r.append(os.path.join(subdir, file))                                                                         
    return r

# processing pdf to text
def read_pdf(document, index=0):

  # add filename to dataframe
  m = re.search(r"\\(?!.*\\)(.*)((\.pdf))", document)
  filename_match = m.group(0)
  filename = re.sub("[\\\/\'\>]", "", filename_match)
  filename = re.sub("\.\w+", "", filename)
  df.loc[index, 'file'] = filename
  
  print("Preprocessing", filename, "...")

  # creating a pdf file object
  pdf = open(document, 'rb') 

  # creating a pdf reader object 
  reader = PyPDF2.PdfReader(pdf, strict=False) 
      
  # printing number of pages in pdf file 
  # print("Number of pages:", pdfReader.numPages)
  pages = len(reader.pages)

  # creating a page object 
  page = reader.pages[0]

  # extracting text from page 
  # print(pageObj.extractText())

  pages_with_contents = []

  for p in range(pages):
    page = reader.pages[p]
    page_contents = page.extract_text()
    pages_with_contents.append(page_contents)

  # join pages into one document
  contents = " ".join(pages_with_contents)

  #closing the pdf file object 
  pdf.close() 

  # cleaning
  contents = re.sub("\n", " ", contents)
  contents = re.sub("\r", " ", contents)
  contents = re.sub("\t", " ", contents)

  # remove symbols
  # contents = re.sub(r"[^a-zA-Z0-9]", " ", contents)

  # # lowercase
  # contents = contents.lower()

  #remove extra spaces
  contents = re.sub("\s+", " ", contents)

  # add contents to dataframe
  df.loc[index, 'content'] = contents

  return

# assign relative directory
directory = os.path.join(sys.path[0], path + "\\raw") ### INPUT FOLDER HERE ###

# list files in directory
files_in_dir = list_files(directory)

# count files in directory
print("Your input directory is:", directory, "number of files:",len(files_in_dir))

# initialize dataframe to hold documents
df = pd.DataFrame(columns=['file'])

# iterate over files in the directory
i = 0
for f in files_in_dir:
    if f.lower().endswith('.pdf'):
        read_pdf(f,i)
    i = i + 1

df

# Sanity check
df['content'][0]

# Documents from dataframe as txt
print("Creating documents.txt...")
documents = ""
for index, row in df.iterrows():
    document_string = row['content']
    documents += document_string + '\n'

print(documents)

with open(path + '\\input\\documents.txt', 'w') as f:
    f.write(documents)

# Document ids from dataframe as txt
print("Creating document_ids.txt...")
document_ids = ""
for index, row in df.iterrows():
    document_id = row['file']
    document_ids += document_id + '\n'

print(document_ids)

with open(path + '\\input\\document_ids.txt', 'w') as f:
    f.write(document_ids)

print("Done!")