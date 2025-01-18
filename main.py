from tkinter import *
from tkinter import messagebox as mb,ttk
import easygui
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import os


def image():
    # By specifying 'filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.webp")]' in
    # below parenthesis, the file explorer only show specified formats.
    value = easygui.fileopenbox()
    return value


def watermark():
    if len(mark.get()) > 0 : # Checking if text field is empty
        img = image()
        try:
            # Converting image to 'RGBA' mode for transparency
            with Image.open(img).convert("RGBA") as base:
                marker = mark.get()
                loc = corner.get()
                loc_dict = {'Top Left corner': (30, 10),
                            'Top Right Corner': (base.width - 250, 10),
                            'Bottom Left Corner': (30, base.height - 50),
                            'Bottom Right Corner': (base.width - 250, base.height - 50),
                            'Center': (base.width // 2 - 125, base.height // 2 - 25),
                            }
                # make a blank image for the text, initialized to transparent text color
                txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
                # Font
                fnt = ImageFont.truetype("font/CaviarDreams.ttf", 40)
                # Drawing Text
                d = ImageDraw.Draw(txt)

                # draw text, half opacity
                for key, value in loc_dict.items():
                    if key == loc:
                        d.text(xy = value, text=marker, font=fnt, fill=(255, 255, 255, 128))
                preview = mb.askyesno(title="Success", message="Press 'OK' for Preview")

                out = Image.alpha_composite(base, txt)
                # Convert to RGB if the output format doesn't support transparency
                output_format = os.path.splitext(img)[1].lower()
                if output_format in [".jpg", ".jpeg", ".bmp"]:
                    out = out.convert("RGB")
                if preview:
                    mark.delete(0, END)
                    out.show()
                else:
                    mark.delete(0, END)
                download = mb.askyesno(title="Download", message="Save In Your Current Dir")
                if download:
                    out.save('output.png')
        except UnidentifiedImageError:
            mb.showerror(title="Error",message="Please Select an Image Format")
        except Exception as e:
            mb.showerror(title="Error", message=f"An error occurred: {e}")
    else:
        mb.showerror(title="Error", message="Please Enter Watermark Text")


window = Tk()
window.title("Water Marker")
window.config(padx=20,pady=20)

# Labels-----------------------------------------------
title = Label(text="Water Marker",padx=20, pady=20)
title.grid(row = 0,column = 0, columnspan = 2)

file = Label(text="Upload image :",padx=20, pady=10)
file.grid(row = 3, column = 0)

text = Label(text="Enter Watermark Text :",padx=20, pady=10)
text.grid(row = 1, column = 0)

location = Label(text="Location :", padx=20, pady=10)
location.grid(row=2, column = 0)
# -----------------------------------------------------

# Entries ---------------------------------------------
mark = Entry(width=32)
mark.grid(row = 1, column = 1)
# -----------------------------------------------------

# Button-----------------------------------------------
choose = Button(text="Choose", command=watermark)
choose.grid(row = 3, column = 1, sticky=W)
# -----------------------------------------------------

# ComboBox---------------------------------------------
combo = StringVar()
corner = ttk.Combobox(window, textvariable=combo,
   values=('Top Left corner', 'Top Right Corner', 'Bottom Left Corner', 'Bottom Right Corner', 'Center'))
corner.grid(row = 2, column =1, sticky=W)
corner.current(0)
# -----------------------------------------------------

window.mainloop()