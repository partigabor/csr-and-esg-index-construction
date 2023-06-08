import pandas as pd
import regex as re
import os, sys
import PyPDF2
import global_options
path = global_options.DATA_FOLDER

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

# function to read a pdf file and add them to a dataframe
def read_pdf(document, index=0):
  """Read and parse a pdf file.
  This function uses the PyPDF2 package to read and extract 
  the contents of a pdf file, page by page.

  Keyword arguments:
  document -- the document to be read in.
  index -- the index of the document, an integer (default 0)
  """
  # add filename to dataframe
  m = re.search(r"\\(?!.*\\)(.*)_(.*)_(\d+)(_?.*)?(\.pdf)", document.lower())
  filename_match = m.group(0)
  filename = re.sub("[\\\/\'\>]", "", filename_match)
  filename = re.sub("\.\w+", "", filename)
  exchange = m.group(1)
  company = m.group(2)
  year = m.group(3)
  # type = m.group(4)
  # type = re.sub("^_", "", type)
  # ext = m.group(4)
  # ext = re.sub("\.", "", ext)

  df.loc[index, 'file'] = filename
  df.loc[index, 'exchange'] = exchange
  df.loc[index, 'company'] = company
  df.loc[index, 'year'] = year
  # df.loc[index, 'type'] = type
  # if type == "":
    # df.loc[index, 'type'] = 'not_csr'
  
  print("Parsing", filename, "...")

  # #####
  # y = re.search("([0-9]{4})", filename)
  # if y is None:
  #   df.loc[index, 'year'] = np.nan
  # else:
  #   df.loc[index, 'year'] = y[0]
  # #####

  # creating a pdf file object
  pdf = open(document, 'rb') 

  # n = re.search(r"\\(?:.(?!\\))+$", filename_with_path)
  # filename_match = n.group(0)

  # creating a pdf reader object 
  reader = PyPDF2.PdfReader(pdf, strict=False) 
      
  # printing number of pages in pdf file 
  # print("Number of pages:", pdfReader.numPages)
  pages = len(reader.pages)

  # add page number to dataframe
  # df.loc[index, 'pages'] = pages

  # creating a page object 
  pageObj = reader.pages[0]

  pages_with_contents = []
  for p in range(pages):
    pageObj = reader.pages[p]
    page_contents = pageObj.extract_text()
    pages_with_contents.append(page_contents)

  # join pages into one document
  contents = " ".join(pages_with_contents)

  #closing the pdf file object 
  pdf.close() 

  # cleaning
  contents = re.sub("\n", " ", contents)
  contents = re.sub("\.", ". ", contents)
  contents = re.sub("\)", ") ", contents)

  # remove symbols
  # contents = re.sub(r"[^a-zA-Z0-9]", " ", contents)

  # lowercase
  # contents = contents.lower()

  #remove extra spaces
  contents = re.sub("\s+", " ", contents)

  # add contents to dataframe
  df.loc[index, 'contents'] = contents

  return

# assign relative directory
directory = os.path.join(sys.path[0], path+"\\raw") ### INPUT FOLDER HERE ### "testdata\\csr"
print("Your input directory is:", directory)

# list files in directory
files_in_dir = list_files(directory)
# files_in_dir = os.listdir(directory)

# count files in directory
print("Number of files:",len(files_in_dir))

# initialize dataframe to hold documents
df = pd.DataFrame(columns=['file'])

# iterate over files in the directory
misc_files = []
i = 0
for f in files_in_dir:
    if f.lower().endswith('.pdf'):
        read_pdf(f,i)
    else:
        print("Found something else.")
        misc_files.append(f)
    i = i + 1

# df.reset_index(inplace=True, drop=True)

if len(misc_files) > 0:
    print("Warning, some files with dubious extensions were found but not parsed:", print(misc_files))
else:
    print("All files read in.")

# sanity check
df.head()
# df['contents'][2]

# Metadata to input
df_meta = df[['file', 'company', 'year']]
df_meta.columns = ['document_id', 'firm_id', 'time']
df_meta.reset_index(drop=True, inplace=True)
df_meta.to_csv(path + '\\input\\id2firms.csv', encoding='utf-8-sig', index=False)

with open(path + "\\input\\document_ids.txt", "w", encoding='utf8') as f_out:
    f_out.write("\n".join(df_meta["document_id"]))

print("Done with metadata.")

# Documents from dataframe as txt
print("Creating documents.txt...")
documents = ""
for index, row in df.iterrows():
    document_string = row['contents']
    documents = documents + document_string + '\n'
documents = re.sub(r'[^\x00-\x7F]+', '', documents)  # remove non-ASCII characters
documents = documents.encode('ascii', 'ignore').decode('utf-8')  # remove invalid UTF-8 bytes

with open(path + '\\input\\documents.txt', 'w', encoding='utf8') as f:
  f.write(documents)

print("Done.")

