#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import with_statement
import os
from io import BytesIO
from struct import unpack
from threading import Thread
import Tkinter as tk
from ttk import Progressbar
import tkFileDialog
from snesrestore import restore_brr_samples

def snes_convert(bin, sfc):
  statusbar.configure(text=u'Status: Running…')
  progressbar.start(10)
      
  try:
    with open(bin, 'rb') as f:
      f.seek(0x10)
      tmp = f.read(0x4)
      rom_start = unpack('<l', tmp)[0]
      
      f.seek(0x14)
      tmp = f.read(0x4)
      pcm_start = unpack('<l', tmp)[0]
      
      rom_size = pcm_start - rom_start
      
      f.seek(0x35)
      tmp = f.read(0x4)
      pcm_size = unpack('<l', tmp)[0]
    
      f.seek(rom_start)
      tmp = f.read(rom_size)
      rom_data = BytesIO(tmp)
        
      f.seek(pcm_start)
      tmp = f.read(pcm_size)
      pcm_data = BytesIO(tmp)
    
    sfc_data = restore_brr_samples(rom_data, pcm_data)
    
    with open(sfc, 'wb') as f:
      f.write(sfc_data)
    
    statusbar.configure(text='Status: Done!')
  except:
    statusbar.configure(text='Status: Failed!')

  progressbar.stop()
  bin_button.configure(state=tk.NORMAL)
  sfc_button.configure(state=tk.NORMAL)
  start_button.configure(state=tk.NORMAL)
  
def start_thread():
  if (bin_str.get() != '') & (sfc_str.get() != ''):
    bin_button.configure(state=tk.DISABLED)
    sfc_button.configure(state=tk.DISABLED)
    start_button.configure(state=tk.DISABLED)
    
    th = Thread(target=lambda:snes_convert(bin_str.get(), sfc_str.get()))
    th.daemon = True
    th.start()
  
def bin_select():
  dir = os.path.expanduser('~')
  file = tkFileDialog.askopenfilename(initialdir=dir)
  bin_str.set(file)
  
def sfc_select():
  dir = os.path.expanduser('~')
  file = tkFileDialog.asksaveasfilename(initialdir=dir)
  sfc_str.set(file)

root = tk.Tk()
root.title('VC SNES Converter')
root.geometry('500x140')
root.resizable(0, 0)

frame1 = tk.Frame(root)
frame1.grid_columnconfigure(1, weight=1)
frame1.pack(padx=4, pady=4, fill=tk.X)

bin_label = tk.Label(frame1, text='"data.bin" file')
bin_label.grid(row=0, column=0, sticky=tk.E)

bin_str = tk.StringVar()
bin_entry = tk.Entry(frame1, textvariable=bin_str, state=tk.DISABLED)
bin_entry.grid(row=0, column=1, sticky=tk.W+tk.E)

bin_button = tk.Button(frame1, text=u'Browse…', command=bin_select)
bin_button.grid(row=0, column=2)

sfc_label = tk.Label(frame1, text='Output ".sfc" file')
sfc_label.grid(row=1, column=0, sticky=tk.E)

sfc_str = tk.StringVar()
sfc_entry = tk.Entry(frame1, textvariable=sfc_str, state=tk.DISABLED)
sfc_entry.grid(row=1, column=1, sticky=tk.W+tk.E)

sfc_button = tk.Button(frame1, text=u'Browse…', command=sfc_select)
sfc_button.grid(row=1, column=2)

statusbar = tk.Label(root, text='Status: Idle')
statusbar.pack(side=tk.BOTTOM, fill=tk.X)

frame2 = tk.Frame(root)
frame2.grid_columnconfigure(0, weight=1)
frame2.pack(padx=4, pady=4, side=tk.BOTTOM, fill=tk.X)

progressbar = Progressbar(frame2, mode='indeterminate')
progressbar.grid(row=0, column=0, sticky=tk.W+tk.E)

start_button = tk.Button(frame2, text='Start', command=start_thread)
start_button.grid(row=0, column=1)

root.mainloop()