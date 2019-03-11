#!/usr/bint/python

import Tkinter as tk
from tkFont import Font
import control

class anomalyGUI(object):

    def __init__(self):
        # create root window
        self.main_window = tk.Tk()
        self.main_window.pack_propagate(0)
        self.main_window.geometry("500x700")
        self.main_window.title("ECSU Protein Anomaly Labeling")
        self.main_window.configure(bg = "SlateGray3")
        self.main_window.resizable(0, 0)

        # create frames
        self.font = Font(family='Times', size=24, weight = "bold")
        self.frame1 = tk.LabelFrame(self.main_window, text = "Inputs", bg = "SlateGray3", fg = "RoyalBlue3", bd = 5, relief = "groove", font = self.font) # create frame 1
        self.frame1.place(x = 10, y = 10, anchor="nw", height = 80, width = 480)

        self.frame2 = tk.LabelFrame(self.main_window, text = "Sequence", bg = "SlateGray3", fg = "RoyalBlue3", bd = 5, relief = "groove", font = self.font) # create frame 2
        self.frame2.place(x = 10, y = 90, anchor = "nw", height = 200, width = 480)

        self.frame3 = tk.LabelFrame(self.main_window, text = "Labels", bg = "SlateGray3", fg = "RoyalBlue3", bd = 5, relief = "groove", font = self.font) # create frame 3
        self.frame3.place(x = 10, y = 290, anchor = "nw", height = 400, width = 480)

        # add components into frame1
        self.label1 = tk.Label(self.frame1, text = "Chain", relief = "groove", bg = "SlateGray3", fg = "blue4", font = Font(family = "helvetica", size = 16, weight = "bold"))
        self.label1.place(x = 10, y = 5, anchor = "nw", height = 30, width = 80)
        self.options = control.getChains()
        #self.options = ["A", "B"]
        self.variable = tk.StringVar(self.frame1)
        self.variable.set(self.options[0])
        self.menu = tk.OptionMenu(self.frame1, self.variable, *self.options)
        self.menu.config(bg = "SlateGray3")
        self.menu.place(x = 100, y = 5, anchor = "nw", height = 30, width = 150)
        self.menu.bind('<Activate>', self.choose_chain)
        self.label2 = tk.Label(self.frame1, text = "Threshold", relief = "groove", bg = "SlateGray3", fg = "blue4", font = Font(family = "helvetica", size = 16, weight = "bold"))
        self.label2.place(x = 280, y = 5, anchor = "nw", height = 30, width = 120)
        self.threhold = tk.StringVar(self.frame1, value='10')
        self.entry = tk.Entry(self.frame1, textvariable = self.threhold, bd = 1, relief = "flat", justify = "center", bg = "SlateGray3", fg = "blue4")
        self.entry.config(highlightbackground="SlateGray3")
        self.entry.place(x = 410, y = 5, height = 30, width = 50, anchor = "nw")

        # data
        self.current_chain = self.variable.get()
        self.current_threhold = self.entry.get()

        # add components into frame2
        self.add_residues()

        tk.mainloop()

    def choose_chain(self, event):
        print('Choose chain ...', self.variable.get())
        for widget in self.frame2.winfo_children():
            widget.destroy()
        self.current_chain = self.variable.get()
        self.add_residues()

    def add_residues(self):
        self.residues = control.getResidueInChain(self.current_chain)
        label_width = 12 # width of each residue label
        label_height = 25 # height of each residue label
        line_space = 5 # space between lines
        number_line = int(460/label_width) # number of labels each line
        for index, r in enumerate(self.residues):
            info = control.residueSingleLetter(r[1])
            print(index, info)
            rowIndex = int(index/number_line)
            columnIndex = index - rowIndex*number_line
            l = tk.Label(self.frame2, text = info, bg = "SlateGray2", fg = "blue4",  font = Font(family = "Times", size = 8), justify = "left")
            l.place(x =5+columnIndex*label_width, y = (label_height+line_space)*rowIndex, height = label_height, width = label_width, anchor = "nw")

def main():
    gui = anomalyGUI()

if __name__ == '__main__':
    main()
