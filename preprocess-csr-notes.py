

# # a function to process xml
# def read_xml(document, index=0):

#   # creating a pdf file object
#   tree = et.parse(document)
#   root = tree.getroot()
  
#   xmlstr = et.tostring(root, method='xml', encoding='unicode')
#   if re.findall("<companyName>", xmlstr):
#     # print('File is sound.')

#     # add filename to dataframe
#     m = re.search(r"\\(?!.*\\)(.*)((\.xml))", document)
#     filename_match = m.group(0)
#     filename = re.sub("[\\\/\'\>]", "", filename_match)
#     filename = re.sub("\.\w+", "", filename)
#     df.loc[index, 'file'] = filename
    
#     print("Preprocessing metadata of", filename, "...")

#     # get id
#     df.loc[index, 'id'] = root[0].attrib['Id']
    
#     # get company
#     for company in root.findall('companyName'):
#       df.loc[index, 'company'] = str(company.text)
#     # get ticker
#     for ticker in root.findall('companyTicker'):
#       df.loc[index, 'ticker'] = str(ticker.text)
#     # get date
#     for date in root.findall('startDate'):
#       df.loc[index, 'date'] = str(date.text)

#     # get year
#     df['date'] = pd.to_datetime(df['date'])
#     df['year'] = df['date'].dt.year
#     df['year'] = df['year'].astype(int)
#   else:
#     print("### ERROR ### Missing data in", document)
#     # log errors
#     errors = document + "\n"
#     with open(path + "\\errors.txt", "a") as text_file:
#       text_file.write(errors)
#   return



# # initialize error log
# with open(path + "\\errors.txt", "w") as text_file:
#   text_file.write("")

# # iterate over files in the directory
# i = 0
# for f in files_in_dir:
#     if f.lower().endswith('.xml'):
#         read_xml(f,i)
#     i = i + 1

# # Print log
# print("A list of problematic files (if any) can be found in errors.txt. You must remove or fix these files!")

# Metadata from dataframe as csv
df = df[['id', 'company', 'year']]
df.columns = ['document_id', 'firm_id', 'time']
df.reset_index(drop=True, inplace=True)
df.to_csv(path + '\\input\\id2firms.csv', encoding='utf-8-sig', index=False)

with open(path + "\\input\\document_ids.txt", "w", encoding='utf8') as f_out:
    f_out.write("\n".join(df["document_id"]))

print("Done with metadata.")

#####################################################

"""
Duplicate error list
Change xml to pdf in the copy with regex
Use the error lists to (re)move these files with batch commands
  e.g. for /f %i in (errors.txt) do move %i .\errors
"""

#####################################################

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



# initialize dataframe to hold documents
df = pd.DataFrame(columns=['file'])

# iterate over files in the directory
i = 0
j = 0
for f in files_in_dir:
    if f.lower().endswith('.pdf'):
        read_pdf(f,i)
        j = j + 1
    i = i + 1

df.reset_index(inplace=True)

# Sanity check
# df['content'][0]

# Documents from dataframe as txt
print("Creating documents.txt...")
documents = ""
for index, row in df.iterrows():
    document_string = row['content']
    documents = documents + document_string + '\n'

documents = re.sub(r'[^\x00-\x7F]+', '', documents)  # remove non-ASCII characters
documents = documents.encode('ascii', 'ignore').decode('utf-8')  # remove invalid UTF-8 bytes

with open(path + '\\input\\documents.txt', 'w', encoding='utf8') as f:
  f.write(documents)
