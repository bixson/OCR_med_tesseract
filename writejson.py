# Denne fil drillede lidt med at virke, da der var "filepath" fejl da man prøver at åbne alto filerne.
# Dette blev løst ved at ændre i File2Str funktionen, så den åbner filerne med encoding="utf8".
# Derudover blev der tilføjet fejlmeddelelser og en bekræftelsesbesked i submitInfo funktionen.
# -Alexander
# --------- Description ------------
# Dette script opretter en GUI til at generere JSON-filer baseret på brugerinput.
# Det indlæser tekst- og XML-filer, og gemmer dataene i en JSON-fil.
# Fejlmeddelelser og bekræftelsesbeskeder vises ved handlinger.
# -Alexander

# Import packages
import sys
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --------- Functions ------------
def File2Str(path):
    # open input file with error handling
    try:
        infile = open(path, 'r', encoding="utf8")
    except IOError as error:
        print("Can’t open file, reason:", str(error))
        sys.exit(1)

    string = ""
    for line in infile:
        line = line.replace(r"\n\n", r"\r\n")
        string += line

    return string

def submitInfo():
    try:
        # Get filename from dropdown
        filename = combo.get()

        # Load Text and Alto
        Text = File2Str(f"txt/{filename}.txt")
        Alto = File2Str(f"alto/{filename}.xml")

        # Data to be written
        dictionary = {
            "Id": Id_var.get(),
            "Forfatter": Forfatter_var.get(),
            "Red": Red_var.get(),
            "Titel": Titel_var.get(),
            "Undertitel": Undertitel_var.get(),
            "By": By_var.get(),
            "Aar": Aar_var.get(),
            "Serietitel": Serietitel_var.get(),
            "Serienr": Serienr_var.get(),
            "Sprogkode": Sprogkode_var.get(),
            "SerienrFork": SerienrFork_var.get(),
            "Bind1": Bind1_var.get(),
            "Bind2": Bind2_var.get(),
            "Bind3": Bind3_var.get(),
            "Artikler": None,
            "Filnavn": filename + ".pdf",
            "Tekst": Text,
            "Alto": Alto
        }

        with open("json/" + filename + "_json.json", "w", encoding="utf8") as outfile:
            outfile.write("[")
            json.dump(dictionary, outfile, ensure_ascii=False, indent=4)
            outfile.write("]")

        messagebox.showinfo("Success", "JSON file created successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Window
window = tk.Tk()
window.title("Lav .json-fil")
window.geometry()

# Define variables
Id_var = tk.StringVar()
Forfatter_var = tk.StringVar()
Red_var = tk.StringVar()
Titel_var = tk.StringVar()
Undertitel_var = tk.StringVar()
By_var = tk.StringVar()
Aar_var = tk.StringVar()
Serietitel_var = tk.StringVar()
Serienr_var = tk.StringVar()
Sprogkode_var = tk.StringVar()
SerienrFork_var = tk.StringVar()
Bind1_var = tk.StringVar()
Bind2_var = tk.StringVar()
Bind3_var = tk.StringVar()

# ------ Padding ------
frm = ttk.Frame(master=window, padding=10)
frm.grid(row=0)

# ------ Choose name ------
import glob

# Find alto files
altoPath = glob.glob('./alto/*.xml', recursive=False)

# Strip paths from path and save to new list
strippedName = []
for string in altoPath:
    strippedName.append(string.split("/")[-1].split(".")[0])

combo = ttk.Combobox(
    master=frm,
    state="readonly",
    values=strippedName,
    width=77
)

nameLabel = ttk.Label(master=frm, text="Vælg fil", padding=5)
nameLabel.grid(column=0, row=0)
combo.grid(column=1, row=0)

# ------ Create input ------
nameList = ["Id", "Forfatter", "Red", "Titel", "Undertitel", "By", "Aar", "Serietitel", "Serienr", "Sprogkode", "SerienrFork", "Bind1", "Bind2", "Bind3"]

# ------ Dictionary for UX ------
transList = [r"ID nummer", r"Forfattere adskilt af 'og' eller 'and'", r"Redigeret af", r"Titel", r"Undertitel", r"By", r"Årstal for udgivelse", r"Serietitel", r"Serienummer", r"Sprogkode (Dan/Eng)", r"Forkortet serietitel", r"Overordnet Bind", r"Artikelnummer", r"Underindeling oftest 0"]

transDict = dict(zip(nameList, transList))

# Variables
for name in nameList:
    CommandString = (name + "_var = tk.StringVar()")
    exec(CommandString)

# Row counter defined
row = 1

for name in nameList:
    CommandString = (f"{name}Label=ttk.Label(master=frm,text=\"{transDict[name]}\",padding=5)\n" +
                     f"{name}Label.grid(column=0, row={str(row)})\n" +
                     f"{name}=ttk.Entry(master=frm, textvariable = " + name + "_var , width= 80)\n" +
                     f"{name}.grid(column=1, row={str(row)})"
                     )

    row += 1

    # Commands are executed
    exec(CommandString)

# ------ Submit button ------
buttonFrm = ttk.Frame(master=window, padding=10)
buttonFrm.grid(row=1)

submitButton = ttk.Button(master=buttonFrm, text="Write .json", command=submitInfo, padding=8)
submitButton.grid(column=1, row=row + 1, padx=5)

closeButton = ttk.Button(master=buttonFrm, text="Cancel", command=window.quit, padding=8)
closeButton.grid(column=0, row=row + 1, padx=5)

# Run main loop
window.mainloop()