def scanpage(imagename, lang):
    xml = pytesseract.image_to_alto_xml(Image.open(imagename),lang=lang)
    txt = pytesseract.image_to_string(Image.open(imagename),lang=lang)
    return xml, txt

def convert2Jpeg(infilename):
    # open input file with error handling
    try:
        convert_from_path(f"pdf/{infilename}", output_folder="temp/img", dpi=200, fmt="jpeg", use_cropbox=True)
    except IOError or PDFInfoNotInstalledError or PDFPageCountError or PDFSyntaxError as error:
        print("Can’t open file, reason:", str(error))
        sys.exit(1)

    print("File successfully converted to images")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # ------------ Initialise -------------

    import pytesseract
    import os
    import glob
    from PIL import Image
    from pdf2image import convert_from_path
    from pdf2image.exceptions import (
        PDFInfoNotInstalledError,
        PDFPageCountError,
        PDFSyntaxError
    )
    import sys

    pytesseract.pytesseract.tesseract_cmd = r'/Users/bixson/IdeaProjects/DKVS/tesseract/tesseract'

    # Clear contents of temp/img
    files = glob.glob('./temp/img/*.jpg', recursive=False)
    for f in files:
        os.remove(f)

    # Clear contents of temp/img
    files = glob.glob('./temp/alto/*.xml', recursive=False)
    for f in files:
        os.remove(f)

    # ------------ Load pdf and convert to images -------------

    # Input the filename
    infilename = input("Type filename of pdf in pdf folder.")

    # check for .pdf suffix
    if not ".pdf" in infilename:
        infilename += ".pdf"

    # Reserve name-part without suffix for later:
    Name = "".join(infilename.split(".")[:-1])

    convert2Jpeg(infilename)

    # ------------ Convert pages -------------

    # Page file names to list

    imagePaths = glob.glob("./temp/img/*.jpg", recursive=False)

    # number of pages
    pages = len(imagePaths)

    # Create list of xml alto
    altoList = []

    # Create list of xml alto
    txtList = []

    # Use function to convert pages
    pagecount = 1

    print()

    lang=input("Input the text language. (dan/eng)")

    for path in imagePaths:
        altoList.append(scanpage(path,lang)[0])
        txtList.append(scanpage(path,lang)[1])
        print(f"Finished scanning page {pagecount} of {pages}")

        pagecount += 1

    print(f"\nImages succesfully converted to Alto XML")

    # List for saving paths of saved xml pages
    altoPaths = []

    # List for saving paths of saved txt files
    txtPaths = []

    for idx in range(len(altoList)):
        # Make one file for each page
        outfilename = f"temp/alto/alto{idx + 1}.xml"
        # Save path
        altoPaths.append(outfilename)

        # open output file with error handling
        try:
            outfile = open(outfilename, 'wb')
        except IOError as error:
            print("Can’t open file, reason:", str(error))
            sys.exit(1)

        # write from altoList to pages one per page
        outfile.write(altoList[idx])
        outfile.close()

    del altoList

    # ------------ load and collect pages -------------

    # Outfile load

    outfilename = f"alto/{Name}.xml"

    # Save to final xml-file
    # open output file with error handling
    try:
        outfile = open(outfilename, 'w', encoding="utf8")
    except IOError as error:
        print("Can’t open file, reason:", str(error))
        sys.exit(1)

    # load first page

    # open input file with error handling
    try:
        infile = open(altoPaths[0], 'r', encoding="utf8")
    except IOError as error:
        print("Can’t open file, reason:", str(error))
        sys.exit(1)

    # opens file and loops through the lines
    line = infile.readline()

    # Flag for defining which file or string to save to
    collectFlag = True
    endString = ""

    # While the lines have content the loop keeps going.
    while line != "":

        # Page numbers at changed to match actual page number
        if line.startswith("\t\t<Page"):
            line = line.replace("page_0", "page_1")
            line = line.replace("PHYSICAL_IMG_NR=\"0\"", "PHYSICAL_IMG_NR=\"1\"")

        # Lines are saved to CollectString
        if collectFlag is True:
            outfile.write(line)

        # Save last lines to endStr to finish document
        if collectFlag is False:
            endString += line

        # First file every is taken until "\t\t</Page>" (this line is included)
        if line.startswith("\t\t</Page>"):
            collectFlag = False

        # Load next  line
        line = infile.readline()

    infile.close()

    # load rest of pages:

    for idx in range(1, len(altoPaths)):

        # open input file with error handling
        try:
            infile = open(altoPaths[idx], 'r', encoding="utf8")
        except IOError as error:
            print("Can’t open file, reason:", str(error))
            sys.exit(1)

        # opens file and loops through the lines
        line = infile.readline()

        # reset collectFlag
        collectFlag = False

        # While the lines have content the loop keeps going.
        while line != "":

            # Collect flag is raised at "\t\t<Page>" (this line is included)
            if line.startswith("\t\t<Page"):
                collectFlag = True
                line = line.replace("page_0", f"page_{idx+1}")
                line = line.replace("PHYSICAL_IMG_NR=\"0\"", f"PHYSICAL_IMG_NR=\"{idx+1}\"")

            # save line to collectString
            if collectFlag is True:
                outfile.write(line)

            #  "\t\t</Page>" lowers the collectflag (this line is included)
            if line.startswith("\t\t</Page>"):
                collectFlag = False

            # Load next  line
            line = infile.readline()

        infile.close()

    # Endstring inserted
    outfile.write(endString)
    outfile.close()

    print(f"Alto XML file is collected and saved to {outfilename}")

    # ------------ Collect text to one file -------------

    # Make one file for each page
    outfilename = f"txt/{Name}.txt"
    # Save path

    # open output file with error handling
    try:
        outfile = open(outfilename, 'w', encoding="utf8")
    except IOError as error:
        print("Can’t open file, reason:", str(error))
        sys.exit(1)

    # write from altoList to pages one per page
    outfile.write("\f".join(txtList))
    outfile.close()

    print(f"Text file is saved to {outfilename}")

    # ------------ Create pdf from images -------------

    # open all images
    images = [
        Image.open(f)
        for f in imagePaths
    ]

    # pdf save path
    pdf_path = f"imgpdf/{Name}.pdf"

    # Save PDF
    images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )
    print(f"Image PDF saved to {pdf_path}")