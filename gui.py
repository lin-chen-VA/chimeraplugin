#!/usr/bint/python

import os
import Tkinter as tk
from tkFont import Font
from chimera import runCommand as rc
import control
import model

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
        self.label1.place(x = 5, y = 5, anchor = "nw", height = 30, width = 80)
        self.options = control.getChains()
        #self.options = ["A", "B"]
        self.variable = tk.StringVar(self.frame1)
        self.variable.set(self.options[0])
        self.menu = tk.OptionMenu(self.frame1, self.variable, *self.options)
        self.menu.config(bg = "SlateGray3")
        self.menu.place(x = 90, y = 5, anchor = "nw", height = 30, width = 100)
        #self.menu.bind('<Activate>', self.choose_chain)
        self.label2 = tk.Label(self.frame1, text = "Threshold", relief = "groove", bg = "SlateGray3", fg = "blue4", font = Font(family = "helvetica", size = 16, weight = "bold"))
        self.label2.place(x = 210, y = 5, anchor = "nw", height = 30, width = 120)
        self.threhold = tk.StringVar(self.frame1, value='10')
        self.entry = tk.Entry(self.frame1, textvariable = self.threhold, bd = 1, relief = "flat", justify = "center", bg = "SlateGray3", fg = "blue4")
        self.entry.config(highlightbackground="SlateGray3")
        self.entry.place(x = 340, y = 5, height = 30, width = 50, anchor = "nw")
        self.button = tk.Button(self.frame1, text = "Check", relief = "groove", bd = 1, bg = "SlateGray3", fg = "blue4", font = Font(family = "helvetica", size = 16, weight = "bold"), command = self.update)
        self.button.place(x = 390, y = 10, anchor = "nw")

        # data
        self.current_chain = self.variable.get()
        self.current_threshold = float(self.entry.get())
        self.mol_name = control.getMolName()
        #print 'Molecule name:', self.mol_name
        #print 'Threhold:', self.current_threshold

        os.chdir(os.path.dirname(os.path.realpath(__file__))) # change the working directory, the default directory is root which is not writable
        #print 'Working directory: ', os.path.dirname(os.path.realpath(__file__))
        self.labels = model.detect(self.mol_name, self.current_threshold) # information of labeled residues
        #print(self.labels)

        # Chimera display
        rc('color blue') # display whole molecule as blue

        # add components into frame2

        tk.mainloop()

    def display_labels(self):
        # display the labeled residues as yellow in Chimera window
        if len(self.labels) == 0:
            return
        rc('select '+control.getLabels(self.labels, self.current_chain))
        rc('color yellow sel')
        rc('show sel')
        # display the labeled residues on chain
        self.color_labels = control.getLabeledResidueInChain(self.labels, self.current_chain, self.residues)
        #print 'Labels: ', self.color_labels
        for index in self.color_labels:
            self.residue_labels[index].config(bg = "yellow", relief = "sunken")

        # display labeled residues in Chimera window
        command = 'select '
        for r in self.color_labels:
            r = self.residues[r]
            command += ':'+str(r[0])+'.'+self.current_chain
        rc(command)
        rc('color yellow sel')
        rc('show sel')

    def update(self):
        self.current_chain = self.variable.get() # udpate selected chain
        self.residue_labels = None
        self.selected_residues = None
        rc('preset apply interactive 1')
        rc('color blue')
        rc('~show')
        rc('~sel')
        self.clear_chain() # remove all residue buttons in frame2
        self.add_residues() # add residue buttons for selected chain
        self.display_labels()
        self.add_table()

    def clear_chain(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()

    def add_table(self):
        chain_labels = control.getLabelsInTable(self.labels, self.current_chain)

        record_width = 60
        record_height = 25
        record_space = 5
        # add colume names
        l = tk.Label(self.frame3, text = "Residue", bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "ridge")
        l.place(x = 5, y = 5, height = record_height, width = record_width, anchor = "nw")
        l2 = tk.Label(self.frame3, text = "Index", bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "ridge")
        l2.place(x = 10+record_width, y = 5, height = record_height, width = record_width, anchor = "nw")
        l3 = tk.Label(self.frame3, text = "B-Dist", bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "ridge")
        l3.place(x = 15+2*record_width, y = 5, height = record_height, width = record_width, anchor = "nw")
        l4 = tk.Label(self.frame3, text = "S-Dist", bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "ridge")
        l4.place(x = 20+3*record_width, y = 5, height = record_height, width = record_width, anchor = "nw")
        l5 = tk.Label(self.frame3, text = "Phi", bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "ridge")
        l5.place(x = 25+4*record_width, y = 5, height = record_height, width = record_width, anchor = "nw")
        l6 = tk.Label(self.frame3, text = "Psi", bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "ridge")
        l6.place(x = 30+5*record_width, y = 5, height = record_height, width = record_width, anchor = "nw")
        l7 = tk.Label(self.frame3, text = "Chi_1", bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "ridge")
        l7.place(x = 35+6*record_width, y = 5, height = record_height, width = record_width, anchor = "nw")

        # add information for each labeled residue
        for index, r in enumerate(chain_labels):
            m = tk.Label(self.frame3, text = str(r[3]), bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "groove")
            m.place(x = 5, y = 5+(record_height+record_space)*(index+1), height = record_height, width = record_width, anchor = "nw")
            m2 = tk.Label(self.frame3, text = str(r[2]), bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "groove")
            m2.place(x = 10+record_width, y = 5+(record_height+record_space)*(index+1), height = record_height, width = record_width, anchor = "nw")
            if r[4] < 2:
                m3 = tk.Label(self.frame3, text = str(round(r[4], 2)), bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "groove")
                m3.place(x = 15+2*record_width, y = 5+(record_height+record_space)*(index+1), height = record_height, width = record_width, anchor = "nw")
            else:
                m3 = tk.Label(self.frame3, text = str(round(r[4], 2)), bg = "SlateGray3", fg = "red", font = Font(family = "Times", size = 6), justify = "left", relief = "groove")
                m3.place(x = 15+2*record_width, y = 5+(record_height+record_space)*(index+1), height = record_height, width = record_width, anchor = "nw")

            if r[5] < 2:
                m4 = tk.Label(self.frame3, text = str(round(r[5], 2)), bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "groove")
                m4.place(x = 20+3*record_width, y = 5+(record_height+record_space)*(index+1), height = record_height, width = record_width, anchor = "nw")
            else:
                m4 = tk.Label(self.frame3, text = str(round(r[5], 2)), bg = "SlateGray3", fg = "red", font = Font(family = "Times", size = 6), justify = "left", relief = "groove")
                m4.place(x = 20+3*record_width, y = 5+(record_height+record_space)*(index+1), height = record_height, width = record_width, anchor = "nw")

            if r[6] < 2:
                m5 = tk.Label(self.frame3, text = str(round(r[6], 2)), bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "groove")
                m5.place(x = 25+4*record_width, y = 5+(record_height+record_space)*(index+1), height = record_height, width = record_width, anchor = "nw")
            else:
                m5 = tk.Label(self.frame3, text = str(round(r[6], 2)), bg = "SlateGray3", fg = "red", font = Font(family = "Times", size = 6), justify = "left", relief = "groove")
                m5.place(x = 25+4*record_width, y = 5+(record_height+record_space)*(index+1), height = record_height, width = record_width, anchor = "nw")

            if r[7] < 2:
                m6 = tk.Label(self.frame3, text = str(round(r[7], 2)), bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "groove")
                m6.place(x = 30+5*record_width, y = 5+(record_height+record_space)*(index+1), height = record_height, width = record_width, anchor = "nw")
            else:
                m6 = tk.Label(self.frame3, text = str(round(r[7], 2)), bg = "SlateGray3", fg = "red", font = Font(family = "Times", size = 6), justify = "left", relief = "groove")
                m6.place(x = 30+5*record_width, y = 5+(record_height+record_space)*(index+1), height = record_height, width = record_width, anchor = "nw")

            if r[8] < 2:
                m7 = tk.Label(self.frame3, text = str(round(r[8], 2)), bg = "SlateGray3", fg = "blue4", font = Font(family = "Times", size = 6), justify = "left", relief = "groove")
                m7.place(x = 35+6*record_width, y = 5+(record_height+record_space)*(index+1), height = record_height, width = record_width, anchor = "nw")
            else:
                m7 = tk.Label(self.frame3, text = str(round(r[8], 2)), bg = "SlateGray3", fg = "red", font = Font(family = "Times", size = 6), justify = "left", relief = "groove")
                m7.place(x = 35+6*record_width, y = 5+(record_height+record_space)*(index+1), height = record_height, width = record_width, anchor = "nw")

    def add_residues(self):
        self.residue_labels = []
        self.selected_residues = []
        self.residues = control.getResidueInChain(self.current_chain)
        label_width = 12 # width of each residue label
        label_height = 25 # height of each residue label
        line_space = 5 # space between lines
        number_line = int(460/label_width) # number of labels each line
        for index, r in enumerate(self.residues):
            info = control.residueSingleLetter(r[1])
            #print(index, info)
            rowIndex = int(index/number_line)
            columnIndex = index - rowIndex*number_line
            l = tk.Label(self.frame2, text = info, bg = "SlateGray2", fg = "blue4",  font = Font(family = "Times", size = 6), justify = "left")
            l.place(x =5+columnIndex*label_width, y = (label_height+line_space)*rowIndex, height = label_height, width = label_width, anchor = "nw")
            l.bind('<Button-1>', lambda event, n = r[0], i = index : self.show_residue(event, n, i))
            self.residue_labels.append(l)

    def show_residue(self, event, n, index):
        """Color selected residue

        Args:
            n, residue index in cif file
            index, residue index started from 0
        """
        # display the selected residues
        self.selected_residues.append(n) # append select residue to selected container
        command = 'select '
        for s in self.selected_residues:
            command += ':'+str(s)+'.'+self.current_chain
        self.residue_labels[index].config(bg = "SlateGray3", relief = "sunken")
        rc(command)
        rc('color red sel')

        # display selectee residues and labeled residues in Chimera window
        command = 'select '
        for r in self.color_labels:
            r = self.residues[r]
            command += ':'+str(r[0])+'.'+self.current_chain
        for s in self.selected_residues:
            command += ':'+str(s)+'.'+self.current_chain
        rc(command)
        rc('show sel')

def main():
    gui = anomalyGUI()

if __name__ == '__main__':
    main()
