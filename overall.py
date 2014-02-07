from __future__ import division
import Tkinter
import re, sys, os
import threading
import Queue
import time
import ttk
from Tkinter import *
from ttk import *
import tkMessageBox
from tokenize import mergeparts, assigntoall, leftovers,finalrun

           
    
# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT)
        canvas = Canvas(self, bd=0, highlightthickness=0, height=600,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH)
        vscrollbar.config(command=canvas.yview)
        

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
            # if interior.winfo_reqheight() != canvas.winfo_height():
                # update the canvas's width to fit the inner frame
            #    canvas.config(height=interior.winfo_reqheight())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
            # if interior.winfo_reqheight() != canvas.winfo_height():
                # update the inner frame's width to fill the canvas
            #    canvas.itemconfigure(interior_id, height=canvas.winfo_height())
        canvas.bind('<Configure>', _configure_canvas)


if __name__ == "__main__":

    class SampleApp(Tk):
        def __init__(self, *args, **kwargs):
            root = Tk.__init__(self, *args, **kwargs)
            
            self.root = root
            
            self.queue = Queue.Queue()
            # self.cancelcommand = False
            self.removeall()
            self.all_len = None
            self.sample_len = None
            
            self.var25 = None
            self.var30 = None
            self.var35 = None
            self.var45 = None
            self.var55 = None
            
            self.frame = VerticalScrolledFrame(root)
            self.frame.pack()
            
            stepFour = Tkinter.LabelFrame(self.frame.interior, text=" Source Files (txt) ")
            stepFour.grid(row=4, columnspan=15, sticky='N', padx=5, pady=5, ipadx=5, ipady=5)
            
            self.var0 = Tkinter.StringVar()
            self.var0.set("")
            
            self.Val0Lbl = Tkinter.Label(stepFour, text="Abstracts (separated by new line)*")
            self.Val0Lbl.grid(row=4, column=0, sticky='W', padx=5, pady=2)
            self.Val0Txt = Tkinter.Entry(stepFour)
            self.Val0Txt.grid(row=4, column=1, columnspan=6, pady=2, sticky='WE')
            
            BrowseBtn = Tkinter.Button(stepFour, text="Browse", command=lambda:self.askopenfile(self.var0, self.Val0Txt))
            BrowseBtn.grid(row=4, column=8, sticky='E', padx=5, pady=2)
            
            self.var1 = Tkinter.StringVar()
            self.var1.set("")
            
            self.Val1Lbl = Tkinter.Label(stepFour, text="Titles (separated by new line)*")
            self.Val1Lbl.grid(row=6, column=0, sticky='W', padx=5, pady=2)
            self.Val1Txt = Tkinter.Entry(stepFour)
            self.Val1Txt.grid(row=6, column=1, columnspan=6, pady=2, sticky='WE')
            
            BrowseBtn2 = Tkinter.Button(stepFour, text="Browse", command=lambda:self.askopenfile(self.var1, self.Val1Txt))
            BrowseBtn2.grid(row=6, column=8, sticky='E', padx=5, pady=2)
            
            self.var2 = Tkinter.StringVar()
            self.var2.set("")
            
            self.Val2Lbl = Tkinter.Label(stepFour, text="Sample documents to be labelled (optional)")
            self.Val2Lbl.grid(row=8, column=0, sticky='W', padx=5, pady=2)
            self.Val2Txt = Tkinter.Entry(stepFour)
            self.Val2Txt.grid(row=8, column=1, columnspan=6, pady=2, sticky='WE')
            
            BrowseBtn3 = Tkinter.Button(stepFour, text="Browse", command=lambda:self.askopenfile(self.var2, self.Val2Txt))
            BrowseBtn3.grid(row=8, column=8, sticky='E', padx=5, pady=2)
            
            self.var3 = Tkinter.StringVar()
            self.var3.set("")
            
            self.Val3Lbl = Tkinter.Label(stepFour, text="Titles of sample documents (optional)")
            self.Val3Lbl.grid(row=10, column=0, sticky='W', padx=5, pady=2)
            self.Val3Txt = Tkinter.Entry(stepFour)
            self.Val3Txt.grid(row=10, column=1, columnspan=6, pady=2, sticky='WE')
            
            BrowseBtn4 = Tkinter.Button(stepFour, text="Browse", command=lambda:self.askopenfile(self.var3, self.Val3Txt))
            BrowseBtn4.grid(row=10, column=8, sticky='E', padx=5, pady=2)
            
            stepFive = Tkinter.LabelFrame(self.frame.interior, text="Potential labels (txt) - to be induced on corpus")
            stepFive.grid(row=12, columnspan=15, sticky='N', padx=5, pady=5, ipadx=5, ipady=5)
            
            self.var4 = Tkinter.StringVar()
            self.var4.set("")
            
            self.Val4Lbl = Tkinter.Label(stepFive, text="Full list of potential labels (optional)")
            self.Val4Lbl.grid(row=12, column=0, sticky='E', padx=5, pady=2)
            self.Val4Txt = Tkinter.Entry(stepFive)
            self.Val4Txt.grid(row=12, column=1, columnspan=6, pady=2, sticky='WE')
            
            BrowseBtn5 = Tkinter.Button(stepFive, text="Browse", command=lambda:self.askopenfile(self.var4, self.Val4Txt))
            BrowseBtn5.grid(row=12, column=8, sticky='W', padx=5, pady=2)
            
            self.var5 = Tkinter.StringVar()
            self.var5.set("")
            
            self.Val5Lbl = Tkinter.Label(stepFive, text="To be added to the list of potential labels (optional)")
            self.Val5Lbl.grid(row=14, column=0, sticky='E', padx=5, pady=2)
            self.Val5Txt = Tkinter.Entry(stepFive)
            self.Val5Txt.grid(row=14, column=1, columnspan=6, pady=2, sticky='WE')
            
            BrowseBtn6 = Tkinter.Button(stepFive, text="Browse", command=lambda:self.askopenfile(self.var5, self.Val5Txt))
            BrowseBtn6.grid(row=14, column=8, sticky='W', padx=5, pady=2)
            
            stepSix = Tkinter.LabelFrame(self.frame.interior, text="Do you want to change the model parameters?")
            stepSix.grid(row=16, columnspan=15, sticky='N', padx=5, pady=5, ipadx=5, ipady=5)
            
            self.var6 = Tkinter.StringVar()
            self.var6.set(1)
            
            self.Val6Lbl = Tkinter.Label(stepSix, text="Check the titles?")
            self.Val6Lbl.grid(row=18, column=0, sticky='E', padx=5, pady=2)
            self.Val6Txt = Tkinter.Checkbutton(stepSix, variable=self.var6)
            self.Val6Txt.grid(row=18, column=1)
            
            
            self.var7 = Tkinter.StringVar()
            self.var7.set(1)
            
            self.Val7Lbl = Tkinter.Label(stepSix, text="Remove the duplicates?")
            self.Val7Lbl.grid(row=20, column=0, sticky='E', padx=5, pady=2)
            self.Val7Txt = Tkinter.Checkbutton(stepSix, variable=self.var7)
            self.Val7Txt.grid(row=20, column=1)
            
            self.var8 = Tkinter.StringVar()
            self.var8.set(15)
            
            self.Val8Lbl = Tkinter.Label(stepSix, text="The max number of instances for the best scoring word should be not less than")
            self.Val8Lbl.grid(row=22, column=0, sticky='E', padx=5, pady=2)
            self.Val8Txt = Tkinter.Entry(stepSix, textvariable=self.var8)
            self.Val8Txt.grid(row=22, column=1)
            
            self.var9 = Tkinter.StringVar()
            self.var9.set(1.6)
            
            self.Val9Lbl = Tkinter.Label(stepSix, text="The threshold for match score more than (minimum 1) ")
            self.Val9Lbl.grid(row=24, column=0, sticky='E', padx=5, pady=2)
            self.Val9Txt = Tkinter.Entry(stepSix, textvariable=self.var9)
            self.Val9Txt.grid(row=24, column=1)
            
            self.SubmitBtn = Tkinter.Button(self.frame.interior, text="Submit", command=self.spawnthread)
            self.SubmitBtn.grid(row=18, column=5, sticky='W', padx=5, pady=2)
            
            self.CancelBtn = Tkinter.Button(self.frame.interior, text="Cancel", command=self.cancel)
            self.CancelBtn.grid(row=18, column=7, sticky='E', padx=5, pady=2)
            
            
            self.listbox = Tkinter.Listbox(self.frame.interior, width=80, height=15)
            self.progressbar = ttk.Progressbar(self.frame.interior, orient='horizontal',
                                               length=300, mode='determinate')
            self.progressbar.step(0.16)
            self.listbox.grid(row=20, sticky='S', padx=5, pady=2)
            # self.listbox.pack(padx=10, pady=10)
            # self.progressbar.pack(padx=10, pady=10)
            self.progressbar.grid(row=24, sticky='S', padx=5, pady=2)
            

        def spawnthread(self):
            if float(self.var9.get()) < 1:
                tkMessageBox.showwarning("", "The minimum value for the match score is 1, please review and start again")
            elif (self.Val0Txt.get() == "" or self.Val1Txt.get() == ""):
                tkMessageBox.showwarning("", "Please enter the mandatory information (*)")
            elif ((self.Val0Txt.get() != "" and self.Val1Txt.get() != "") and self.Val4Txt.get() != "" and self.Val5Txt.get() == "" and self.var25 is None and self.var30 is None):
                if (tkMessageBox.askyesno("", "Have you already tokenized the labels Wiki pages?") == 1):
                    self.addfields()
                else:
                    self.starting_all()
            elif (self.Val4Txt.get() != "" and self.Val5Txt.get() != ""):
                tkMessageBox.showwarning("", "You should define either full list of labels or the one to be merged with - not both!")
            elif ((self.Val2Txt.get() != "" and self.Val3Txt.get() == "") or (self.Val2Txt.get() == "" and self.Val3Txt.get() != "")):
                tkMessageBox.showwarning ("", "Please provide both abstracts and titles for the sample or leave both fields empty")
            elif (((self.Val0Txt.get() != "" and self.Val1Txt.get() != "") or (self.Val2Txt.get() != "" and self.Val3Txt.get() != "")) and self.Val4Txt.get() == "" and self.Val5Txt.get() != "" and self.var45 is None and self.var30 is None):
                if (tkMessageBox.askyesno("", "Have you already tokenized the labels Wiki pages that are to be added?") == 1):
                    self.addfields()
                else:
                    self.starting_all()
            elif (self.Val4Txt.get() != "" and self.var25 is not None):
                self.starting_all()
            else:
                self.starting_all()
            
        def starting_all(self):
            if (self.Val0Txt.get() != "" and self.Val1Txt.get() != ""):
                path = self.Val0Txt.get()
                path2 = self.Val1Txt.get()
                abst = open(path, 'rb').read().split('\n')
                titl = open(path2, 'rb').read().split('\n')
                if (len(abst) == len(titl)):
                    self.all_len = len(abst)
                    if (self.Val2Txt.get() != "" and self.Val3Txt.get() != ""):
                        path3 = self.Val2Txt.get()
                        path4 = self.Val3Txt.get()
                        abstsam = open(path3, 'rb').read().split('\n')
                        titlsam = open(path4, 'rb').read().split('\n')
                        self.sample_len = len(abstsam)
                        if (len(abstsam) == len(titlsam) and self.var25):
                            self.starting2()
                        elif (len(abstsam) == len(titlsam) and self.var30 is None):
                            self.starting()
                        elif (len(abstsam) == len(titlsam) and self.var30):
                            self.starting2()
                        else:
                            tkMessageBox.showwarning("", "Sample abstracts and titles do not match - please check the source files")
                    elif (self.Val2Txt.get() == "" and self.Val3Txt.get() == "" and self.var25):
                        self.starting2()
                    elif (self.Val2Txt.get() == "" and self.Val3Txt.get() == "" and self.var30):
                        self.starting2()
                    elif (self.Val2Txt.get() == "" and self.Val3Txt.get() == "" and self.var30 is None):
                        self.starting()
                    else:
                        tkMessageBox.showwarning("", "Please enter both abstracts and titles source for the sample")
                else:
                    tkMessageBox.showwarning("", "Abstracts and titles do not match - please check the source files")
            
        
        def addfields(self):
            top = self.top = Toplevel(self.root)
            top.wm_attributes("-topmost", 1)
            
            self.var10 = Tkinter.StringVar()
            self.var10.set("")
            
            self.Val10Lbl = Tkinter.Label(top, text="Labels Wiki tokens (txt)")
            self.Val10Lbl.grid(row=4, column=0, sticky='W', padx=5, pady=2)
            self.Val10Txt = Tkinter.Entry(top)
            self.Val10Txt.grid(row=4, column=1, columnspan=6, pady=2, sticky='WE')
            
            BrowseBtn10 = Tkinter.Button(top, text="Browse", command=lambda:self.askopenfile(self.var10, self.Val10Txt))
            BrowseBtn10.grid(row=4, column=8, sticky='E', padx=5, pady=2)
            
            self.var15 = Tkinter.StringVar()
            self.var15.set("")
            
            self.Val15Lbl = Tkinter.Label(top, text="Labels Wiki clean titles (txt) (optional)")
            self.Val15Lbl.grid(row=6, column=0, sticky='W', padx=5, pady=2)
            self.Val15Txt = Tkinter.Entry(top)
            self.Val15Txt.grid(row=6, column=1, columnspan=6, pady=2, sticky='WE')
            
            BrowseBtn15 = Tkinter.Button(top, text="Browse", command=lambda:self.askopenfile(self.var15, self.Val15Txt))
            BrowseBtn15.grid(row=6, column=8, sticky='E', padx=5, pady=2)
            
            
            if self.Val4Txt.get() != "":
                b = Button(top, text="OK", command=self.ok)
                b.grid(row=8, column=2, sticky='W', padx=5, pady=2)
            else:
                b = Button(top, text="OK", command=self.ok2)
                b.grid(row=8, column=2, sticky='W', padx=5, pady=2)
        
            b2 = Button(top, text="Cancel", command=self.cancDialog)
            b2.grid(row=8, column=4, sticky='E', padx=5, pady=2)
            
        def ok(self):
            if self.Val10Txt.get() != "" and self.Val15Txt.get() != "":
                self.var25 = self.Val10Txt.get()
                self.var35 = self.Val15Txt.get()
                self.top.destroy()
            elif self.Val10Txt.get() != "" and self.Val15Txt.get() == "":
                self.var25 = self.Val10Txt.get()
                self.top.destroy()
            else:
                tkMessageBox.showwarning("", "You haven't entered any path to the tokenized Wiki file!")

        
        def ok2(self):
            if self.Val10Txt.get() != "" and self.Val15Txt.get() != "":
                self.var45 = self.Val10Txt.get()
                self.var55 = self.Val15Txt.get()
                self.top.destroy()
            elif self.Val10Txt.get() != "" and self.Val15Txt.get() == "":
                self.var45 = self.Val10Txt.get()
                self.top.destroy()
            else:
                tkMessageBox.showwarning("", "You haven't entered any path to the tokenized Wiki file!")

        
                    
        def adddir(self):
            top = self.top = Toplevel(self.root)
            top.wm_attributes("-topmost", 1)
            
            self.var40 = Tkinter.StringVar()
            self.var40.set("")
            
            self.Val20Lbl = Tkinter.Label(top, text="Please specify folder")
            self.Val20Lbl.grid(row=4, column=0, sticky='W', padx=5, pady=2)
            self.Val20Txt = Tkinter.Entry(top)
            self.Val20Txt.grid(row=4, column=1, columnspan=6, pady=2, sticky='WE')
            
            BrowseBtn20 = Tkinter.Button(top, text="Browse", command=lambda:self.askdirectory(self.var40, self.Val20Txt))
            BrowseBtn20.grid(row=4, column=8, sticky='E', padx=5, pady=2)
            
            b = Button(top, text="OK", command=self.okdir)
            b.grid(row=8, column=2, sticky='W', padx=5, pady=2)
    
            b2 = Button(top, text="Cancel", command=self.cancDialog)
            b2.grid(row=8, column=4, sticky='E', padx=5, pady=2)
    
        
        def okdir(self):
    
            if self.Val20Txt.get() != "":
                self.var30 = self.Val20Txt.get()
                self.top.destroy()
            else:
                tkMessageBox.showwarning("", "You haven't entered any information!")
    
        def cancDialog(self):
            self.top.destroy()
            self.starting2()
            
        def starting(self):
            if (tkMessageBox.askyesno("", "Do you want to keep the label list?") == 1):
                self.adddir()
            else:
                self.SubmitBtn.config(state="disabled")
                self.thread = ThreadedClient(self.queue)
                self.thread.start()
                self.periodiccall()
                
        def starting2(self):
            self.SubmitBtn.config(state="disabled")
            self.thread = ThreadedClient(self.queue)
            self.thread.start()
            self.periodiccall()
            
        
        def cancel(self):
            if (tkMessageBox.askyesno("", "Are you sure you want to exit?") == 1):
                self.destroy()
            else:
                pass
            
        def periodiccall(self):
            self.checkqueue()
            if self.thread.is_alive():
                self.after(100, self.periodiccall)
            else:
                self.SubmitBtn.config(state="active")
        
        def checkqueue(self):
            while self.queue.qsize():
                try:
                    msg = self.queue.get(0)
                    self.listbox.insert('end', msg)
                    self.progressbar.step(20)
                except Queue.Empty:
                    pass
        
        def tokensAll(self):
            from tokenize import tokens
            if self.Val4Txt.get() == "":
                tokens.tokenize(self.Val0Txt.get(), "1", self.listbox, lemmat=True, message=True)
                tokens.tokenize(self.Val0Txt.get(), "2", self.listbox, lemmat=False, message=False)
            else:
                pass
            
        def tokensSam(self):
            from tokenize import tokensSample
            if self.Val2Txt.get() == "":
                tokensSample.tokenize(self.Val0Txt.get(), self.Val1Txt.get(), self.listbox)
            else:
                tokensSample.tokenize(self.Val2Txt.get(), self.Val3Txt.get(), self.listbox)
            
        def toxls(self):
            from tokenize import shapexls
            if self.Val2Txt.get() == "":
                shapexls.record(self.Val0Txt.get(), self.Val1Txt.get())
            else:
                shapexls.record(self.Val2Txt.get(), self.Val3Txt.get())
        
        def assignment(self):
            if self.var25 is None and self.var30 is None:
                assigntoall.assign('docs/provisional/sample/', 'docs/provisional/real-titles-wiki.txt', 'docs/provisional/tokens-wikilabels.txt', self.var6.get(), self.var7.get(), int(self.var8.get()), float(self.var9.get()), 0, None, first=True)
            elif (self.var25 is None and self.var30):
                assigntoall.assign('docs/provisional/sample/', str(self.var30) + '/real-titles-wiki.txt', str(self.var30) + '/tokens-wikilabels.txt', self.var6.get(), self.var7.get(), int(self.var8.get()), float(self.var9.get()), 0, None, first=True)
            elif (self.var25 and not self.var35):
                assigntoall.assign('docs/provisional/sample/', self.Val4Txt.get(), self.var25, self.var6.get(), self.var7.get(), int(self.var8.get()), float(self.var9.get()), 0, None, first=True)
            elif (self.var25 and self.var35):
                assigntoall.assign('docs/provisional/sample/', self.var35, self.var25, self.var6.get(), self.var7.get(), int(self.var8.get()), float(self.var9.get()), 0, None, first=True)
            else:
                pass
            mergeparts.merger()
            self.listboxins("30%")
            
            
        def listboxins(self,percent):
            line = self.listbox.get(4)
            line+=percent
            self.listbox.delete(4)
            self.listbox.insert(4,line)
            
        def assigntoall_next(self):
            self.left = leftovers.count()
            if (int(self.var6.get()) == 1 and int(self.var7.get()) == 1 and int(self.var8.get()) > 10 and float(self.var9.get()) > 1.4):
                self.lefty(0, 1, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...40%")
                mergeparts.merger()
                
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 0)
                self.listboxins("...60%")
                
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()) - 0.3, 0)
                self.listboxins("...70%")
                
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()) - 0.3, 1)
                self.listboxins("...80%")
                
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...90%")
                mergeparts.merger()
   
            elif (int(self.var6.get()) == 0 and int(self.var7.get()) == 1 and int(self.var8.get()) > 10 and float(self.var9.get()) > 1.4):
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()) - 0.3, 0)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()) - 0.3, 1)
                self.listboxins("...80%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...90%")
                mergeparts.merger()
            elif (int(self.var6.get()) == 0 and int(self.var7.get()) == 0 and int(self.var8.get()) > 10 and float(self.var9.get()) > 1.4):
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()) - 0.3, 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()) - 0.3, 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
            elif (int(self.var6.get()) == 1 and int(self.var7.get()) == 0 and int(self.var8.get()) > 10 and float(self.var9.get()) > 1.4):
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...40%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()) - 0.3, 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()) - 0.3, 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
            
            elif (int(self.var6.get()) == 1 and int(self.var7.get()) == 1 and int(self.var8.get()) <= 10 and float(self.var9.get()) > 1.4):
                self.lefty(0, 1, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...40%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()) - 0.3, 0)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()) - 0.3, 1)
                self.listboxins("...80%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...90%")
                mergeparts.merger()
            
            elif (int(self.var6.get()) == 0 and int(self.var7.get()) == 1 and int(self.var8.get()) <= 10 and float(self.var9.get()) > 1.4):
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()) - 0.3, 0)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()) - 0.3, 1)
                self.listboxins("...80%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...90%")
                mergeparts.merger()
            elif (int(self.var6.get()) == 0 and int(self.var7.get()) == 0 and int(self.var8.get()) <= 10 and float(self.var9.get()) > 1.4):
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()) - 0.3, 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()) - 0.3, 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
            elif (int(self.var6.get()) == 1 and int(self.var7.get()) == 0 and int(self.var8.get()) <= 10 and float(self.var9.get()) > 1.4):
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()) - 0.3, 0)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()) - 0.3, 1)
                self.listboxins("...80%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...90%")
                mergeparts.merger()
            
            elif (int(self.var6.get()) == 1 and int(self.var7.get()) == 1 and int(self.var8.get()) <= 10 and float(self.var9.get()) <= 1.4 and float(self.var9.get()) > 1.1):
                self.lefty(0, 1, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...40%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, 1.1, 0)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, 1.1, 1)
                self.listboxins("...80%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...90%")
                mergeparts.merger()
            
            elif (int(self.var6.get()) == 0 and int(self.var7.get()) == 1 and int(self.var8.get()) <= 10 and float(self.var9.get()) <= 1.4 and float(self.var9.get()) > 1.1):
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...40%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, 1.1, 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, 1.1, 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
            elif (int(self.var6.get()) == 0 and int(self.var7.get()) == 0 and int(self.var8.get()) <= 10 and float(self.var9.get()) <= 1.4 and float(self.var9.get()) > 1.1):
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, 1.1, 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, 1.1, 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
            elif (int(self.var6.get()) == 1 and int(self.var7.get()) == 0 and int(self.var8.get()) <= 10 and float(self.var9.get()) <= 1.4 and float(self.var9.get()) > 1.1):
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, 1.1, 0)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, 1.1, 1)
                self.listboxins("...80%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...90%")
                mergeparts.merger()
            
            elif (int(self.var6.get()) == 1 and int(self.var7.get()) == 1 and int(self.var8.get()) <= 10 and float(self.var9.get()) <= 1.1):
                self.lefty(0, 1, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...40%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
                
            elif (int(self.var6.get()) == 0 and int(self.var7.get()) == 1 and int(self.var8.get()) <= 10 and float(self.var9.get()) <= 1.1):
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
                
            elif (int(self.var6.get()) == 0 and int(self.var7.get()) == 0 and int(self.var8.get()) <= 10 and float(self.var9.get()) <= 1.1):
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 1)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
                
            elif (int(self.var6.get()) == 1 and int(self.var7.get()) == 0 and int(self.var8.get()) <= 10 and float(self.var9.get()) <= 1.1):
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 2, float(self.var9.get()), 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
                
            elif (int(self.var6.get()) == 1 and int(self.var7.get()) == 1 and int(self.var8.get()) > 10 and float(self.var9.get()) <= 1.1):
                self.lefty(0, 1, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...40%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
                
            elif (int(self.var6.get()) == 0 and int(self.var7.get()) == 1 and int(self.var8.get()) > 10 and float(self.var9.get()) <= 1.1):
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
                
            elif (int(self.var6.get()) == 0 and int(self.var7.get()) == 0 and int(self.var8.get()) > 10 and float(self.var9.get()) <= 1.1):
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
                
            elif (int(self.var6.get()) == 1 and int(self.var7.get()) == 0 and int(self.var8.get()) > 10 and float(self.var9.get()) <= 1.1):
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
                
            
            elif (int(self.var6.get()) == 1 and int(self.var7.get()) == 1 and int(self.var8.get()) > 10 and float(self.var9.get()) <= 1.4 and float(self.var9.get()) > 1.1):
                self.lefty(0, 1, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...40%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, 1.1, 0)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, 1.1, 1)
                self.listboxins("...80%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...90%")
                mergeparts.merger()
            elif (int(self.var6.get()) == 0 and int(self.var7.get()) == 1 and int(self.var8.get()) > 10 and float(self.var9.get()) <= 1.4 and float(self.var9.get()) > 1.1):
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...40%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, 1.1, 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, 1.1, 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
            elif (int(self.var6.get()) == 0 and int(self.var7.get()) == 0 and int(self.var8.get()) > 10 and float(self.var9.get()) <= 1.4 and float(self.var9.get()) > 1.1):
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 0)
                self.listboxins("...40%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, 1.1, 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, 1.1, 1)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
            elif (int(self.var6.get()) == 1 and int(self.var7.get()) == 0 and int(self.var8.get()) > 10 and float(self.var9.get()) <= 1.4 and float(self.var9.get()) > 1.1):
                self.lefty(0, 0, int(self.var8.get()), float(self.var9.get()), 0)
                self.listboxins("...40%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, float(self.var9.get()), 0)
                self.listboxins("...50%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, 1.1, 0)
                self.listboxins("...60%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.lefty(0, 0, int(self.var8.get()) - 5, 1.1, 1)
                self.listboxins("...70%")
                mergeparts.merger()
                self.left = leftovers.count()
                self.finale()
                self.listboxins("...80%")
                mergeparts.merger()
            
            
            else:
                pass
            
            self.toxls()
                
            
        def lefty(self, vary1, vary2, vary3, vary4, vary5):
            if self.sample_len is not None:
                if len(self.left) > 0.1 * self.sample_len:
                    if self.var25 is None and self.var30 is None:
                        assigntoall.assign('docs/provisional/sample/', 'docs/provisional/real-titles-wiki.txt', 'docs/provisional/tokens-wikilabels.txt', vary1, vary2, vary3, vary4, vary5, self.left)
                    elif (self.var25 is None and self.var30):
                        assigntoall.assign('docs/provisional/sample/', str(self.var30) + '/real-titles-wiki.txt', str(self.var30) + '/tokens-wikilabels.txt', vary1, vary2, vary3, vary4, vary5, self.left)
                    elif (self.var25 and not self.var35):
                        assigntoall.assign('docs/provisional/sample/', self.Val4Txt.get(), self.var25, vary1, vary2, vary3, vary4, vary5, self.left)
                    elif (self.var25 and self.var35):
                        assigntoall.assign('docs/provisional/sample/', self.var35, self.var25, vary1, vary2, vary3, vary4, vary5, self.left)
                    else:
                        pass
                
                else:
                    self.toxls()
                    # self.destroy()
                    exit()
            else:
                if len(self.left) > (self.all_len * 0.1):
                    if (self.var25 is None and self.var30 is None):
                        assigntoall.assign('docs/provisional/sample/', 'docs/provisional/real-titles-wiki.txt', 'docs/provisional/tokens-wikilabels.txt', vary1, vary2, vary3, vary4, vary5, self.left)
                    elif (self.var25 is None and self.var30):
                        assigntoall.assign('docs/provisional/sample/', str(self.var30) + '/real-titles-wiki.txt', str(self.var30) + '/tokens-wikilabels.txt', vary1, vary2, vary3, vary4, vary5, self.left)
                    elif (self.var25 and not self.var35):
                        assigntoall.assign('docs/provisional/sample/', self.Val4Txt.get(), self.var25, vary1, vary2, vary3, vary4, vary5, self.left)
                    elif (self.var25 and self.var35):
                        assigntoall.assign('docs/provisional/sample/', self.var35, self.var25, vary1, vary2, vary3, vary4, vary5, self.left)
                    else:
                        pass
                else:
                    self.toxls()
                    # self.destroy()
                    exit()
        
        def finale(self):
            if self.sample_len is not None:
                if len(self.left) > 0.1 * self.sample_len:
                    if self.var25 is None and self.var30 is None:
                        finalrun.finalize('docs/provisional/sample/', 'docs/provisional/real-titles-wiki.txt', 'docs/provisional/tokens-wikilabels.txt', self.left)
                    elif (self.var25 is None and self.var30):
                        finalrun.finalize('docs/provisional/sample/', str(self.var30) + '/real-titles-wiki.txt', str(self.var30) + '/tokens-wikilabels.txt', self.left)
                    elif (self.var25 and not self.var35):
                        finalrun.finalize('docs/provisional/sample/', self.Val4Txt.get(), self.var25, self.left)
                    elif (self.var25 and self.var35):
                        finalrun.finalize('docs/provisional/sample/', self.var35, self.var25, self.left)
                    else:
                        pass
                
                else:
                    self.toxls()
                    # self.destroy()
                    exit()
            else:
                if len(self.left) > (self.all_len * 0.1):
                    if (self.var25 is None and self.var30 is None):
                        finalrun.finalize('docs/provisional/sample/', 'docs/provisional/real-titles-wiki.txt', 'docs/provisional/tokens-wikilabels.txt', self.left)
                    elif (self.var25 is None and self.var30):
                        finalrun.finalize('docs/provisional/sample/', str(self.var30) + '/real-titles-wiki.txt', str(self.var30) + '/tokens-wikilabels.txt', self.left)
                    elif (self.var25 and not self.var35):
                        finalrun.finalize('docs/provisional/sample/', self.Val4Txt.get(), self.var25, self.left)
                    elif (self.var25 and self.var35):
                        finalrun.finalize('docs/provisional/sample/', self.var35, self.var25, self.left)
                    else:
                        pass
                else:
                    self.toxls()
                    # self.destroy()
                    exit()
        
        def potlabels(self):
            from tokenize import potlabels
            if (self.Val4Txt.get() == "" and self.var30 is None):
                potlabels.potential(None, self.listbox)
            elif (self.Val4Txt.get() == "" and self.var30):
                potlabels.potential(self.var30, self.listbox)
            else:
                pass    

        def labelstokenize(self):
            from tokenize import labelstok
            if self.var25 is None:
                if (self.Val4Txt.get() == "" and self.Val5Txt.get() == "" and self.var30 is None):
                    labelstok.labelstokenize(self.Val0Txt.get(), 'docs/provisional/potential-labels.txt', None, None, None, self.var30, self.listbox)
                elif (self.Val4Txt.get() == "" and self.Val5Txt.get() == "" and self.var30):
                    labelstok.labelstokenize(self.Val0Txt.get(), str(self.var30) + '/potential-labels.txt', None, None, None, self.var30, self.listbox)
                elif (self.Val4Txt.get() != "" and self.Val5Txt.get() == ""):
                    labelstok.labelstokenize(self.Val0Txt.get(), self.Val4Txt.get(), None, None, None, self.var30, self.listbox)
                elif (self.Val4Txt.get() == "" and self.Val5Txt.get() != "" and self.var30 is None and self.var45 is None):
                    labelstok.labelstokenize(self.Val0Txt.get(), 'docs/provisional/potential-labels.txt', self.Val5Txt.get(), None, None, self.var30, self.listbox)
                elif (self.Val4Txt.get() == "" and self.Val5Txt.get() != "" and self.var30 and self.var45 is None):
                    labelstok.labelstokenize(self.Val0Txt.get(), str(self.var30) + '/potential-labels.txt', self.Val5Txt.get(), None, None, self.var30, self.listbox)
                elif (self.Val4Txt.get() == "" and self.Val5Txt.get() != "" and self.var30 is None and self.var45):
                    if self.var55:
                        labelstok.labelstokenize(self.Val0Txt.get(), 'docs/provisional/potential-labels.txt', self.Val5Txt.get(), self.var45, self.var55, self.var30, self.listbox)
                    else:
                        labelstok.labelstokenize(self.Val0Txt.get(), 'docs/provisional/potential-labels.txt', self.Val5Txt.get(), self.var45, None, self.var30, self.listbox)
                elif (self.Val4Txt.get() == "" and self.Val5Txt.get() != "" and self.var30 and self.var45):
                    if self.var55:
                        labelstok.labelstokenize(self.Val0Txt.get(), str(self.var30) + '/potential-labels.txt', self.Val5Txt.get(), self.var45, self.var55, self.var30, self.listbox)
                    else:
                        labelstok.labelstokenize(self.Val0Txt.get(), str(self.var30) + '/potential-labels.txt', self.Val5Txt.get(), self.var45, None, self.var30, self.listbox)
                
                else:
                    tkMessageBox.showwarning("", "An error has occurred: please restart the application")
            else:
                pass
            
        def askopenfile(self, var, val):
            from tkFileDialog import askopenfilename
            var = askopenfilename()
            self.var = var
            self.val = val
            val.delete(0, Tkinter.END)
            val.insert(0, self.var)
        
        def askdirectory(self, var, val):
            from tkFileDialog import askdirectory
            var = askdirectory()
            self.var = var
            self.val = val
            val.delete(0, Tkinter.END)
            val.insert(0, self.var)
            
            
        def removeall(self):
            self.filelist = ["docs/provisional/" + f for f in os.listdir("docs/provisional") if re.search('\.txt', f)]
            self.filelist2 = ["docs/labels/" + f for f in os.listdir('docs/labels') if re.search('\.txt', f)]
            self.filelist3 = ["docs/provisional/sample/" + f for f in os.listdir('docs/provisional/sample') if re.search('\.txt', f)]
            self.filelist.extend(self.filelist2)
            self.filelist.extend(self.filelist3)
            for f in self.filelist:
                os.remove(f)
            
        def error(self):
            self.var_status.set("Error: Please check settings you have entered")
            self.Val22Lbl.config(bg="red")
        
        def empty(self):
            self.var_status.set("Error: Please fill in all required fields (*)")
            self.Val22Lbl.config(bg="purple")
        
        def errormes(self):
            if (tkMessageBox.showerror("", "An error has occurred: please restart the application")):
                self.destroy()
            


    class ThreadedClient(threading.Thread):
        def __init__(self, queue):
            threading.Thread.__init__(self)
            self.queue = queue
            
        def run(self):
            msg1 = "Step 1: Tokenization started..."
            self.queue.put(msg1)
            app.tokensAll()
            msg3 = "Step 2: Forming/Fetching list of potential wikilabels..."
            self.queue.put(msg3)
            try:
                app.potlabels()
            except:
                msg4 = "ERROR!"
                self.queue.put(msg4)
                app.errormes()
                #app.destroy()
                exit()
            msg6 = "Step 3: Tokenizing Wiki pages/Fetching tokens file..."
            self.queue.put(msg6)
            try:
                app.labelstokenize()
            except:
                msg7 = "ERROR!"
                self.queue.put(msg7)
                app.errormes()
                #app.destroy()
                exit()
            msg8 = "Step 4: Tokenizing sample..."
            self.queue.put(msg8)
            try:
                app.tokensSam()
            except:
                msg81 = "ERROR!"
                self.queue.put(msg81)
                app.errormes()
                #app.destroy()
                exit()
            msg9 = "Step 5: Assigning wikilabels to documents..."
            self.queue.put(msg9)
            try:
                app.assignment()
                app.assigntoall_next()
                app.listboxins("...Done!")
            except:
                msg10 = "ERROR!"
                self.queue.put(msg10)
                app.errormes()
                # app.destroy()
                exit()
            msg11 = "Task finished... Congratulations!"
            self.queue.put(msg11)
            msg12 = "You can check the result in the 'Final' folder"
            self.queue.put(msg12)
            
            
            
            

    app = SampleApp()
    app.title("Wikilabels")
    app.mainloop()
