import pandas as pd
import regex as re
import os, sys
import xml.etree.ElementTree as et

path = "data-test"

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

# processing xml
def read_xml(document, index=0):

  # add filename to dataframe
  m = re.search(r"\\(?!.*\\)(.*)((\.xml))", document)
  filename_match = m.group(0)
  filename = re.sub("[\\\/\'\>]", "", filename_match)
  filename = re.sub("\.\w+", "", filename)
  df.loc[index, 'file'] = filename
  
  print("Preprocessing", filename, "...")

  # creating a pdf file object
  tree = et.parse(document)
  root = tree.getroot()
  
  # Get Id
  df.loc[index, 'id'] = root[0].attrib['Id']

  for company in root.findall('companyName'):
    df.loc[index, 'company'] = company.text

  for ticker in root.findall('companyTicker'):
    df.loc[index, 'ticker'] = ticker.text

  for date in root.findall('startDate'):
    df.loc[index, 'date'] = date.text

  df['date'] = pd.to_datetime(df['date'])
  df['year'] = df['date'].dt.year

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
    if f.lower().endswith('.xml'):
        read_xml(f,i)
    i = i + 1

# Metadata from dataframe as csv
df = df[['id', 'company', 'year']]
df.columns = ['document_id', 'firm_id', 'time']
df.reset_index(drop=True, inplace=True)
df.to_csv(path + '\\input\\id2firms.csv')

print("Done!")