from tkinter import *

root = Tk()

root.geometry(f"+{(root.winfo_screenwidth()+root.winfo_screenwidth())//2}" 
            f"+{(root.winfo_screenheight()+root.winfo_screenheight())//2}")
print(root.winfo_screenwidth())
print(root.winfo_screenheight())
root.mainloop()