import pymupdf # imports the pymupdf library
doc = pymupdf.open("“老十针”为主治疗脓毒症合并急性胃肠损伤的临床研究_廖丹.pdf") # open a document
for page in doc: # iterate the document pages
  text = page.get_text() # get plain text encoded as UTF-8
  print(text)