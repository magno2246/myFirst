# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:41:35 2022

@author: magno
"""

"""
@ Description: Closing Stock Price using Quote Endpoint from Alpha Vantage
@ API Documentation: https://www.alphavantage.co/documentation/
"""
import requests
from tkinter import *
from tkinter import Tk, ttk
from tkinter.messagebox import showinfo, showwarning
class StockGUI:
    def __init__(self, guiWin, api_key):
        self.guiWin_ = guiWin
        self.guiWin_.title("Stock Price")
        self.api_key = api_key
        
        # Declares root canvas is a grid of only one row and one column
        self.guiWin_.columnconfigure(0, weight=1)
        self.guiWin_.rowconfigure(0, weight=1)
        
        # Create Frame inside GUI canvas
        self.mainframe = ttk.Frame(self.guiWin_, padding="5 12 5 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        
        # Set styles for TK Label, Entry and Button Widgets
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 20),foreground='black')
        
        # Add Label Widgets to mainframe
        ttk.Label(self.mainframe, text="Symbol"). \
                                               grid(column=1,row=1, sticky=W)
        ttk.Label(self.mainframe, text="Close Price (USD)"). \
                                              grid(column=1, row=2, sticky=W)
        ttk.Label(self.mainframe, text="Previous Close"). \
                                              grid(column=1, row=3, sticky=W)
        ttk.Label(self.mainframe, text="Percent Change"). \
                                              grid(column=1, row=4, sticky=W)
        ttk.Label(self.mainframe, text="Volume"). \
                                              grid(column=1, row=5, sticky=W)
        
        self.style.configure("TEntry", font=("Arial", 25),foreground='maroon')
        # Add Entry Widget for Entering the Stock Symbol
        self.symbol = StringVar()
        self.symbol_entry = ttk.Entry(self.mainframe, width=10,justify=CENTER,
                        textvariable=self.symbol, font=("Arial", 20, "bold"))
        self.symbol_entry.grid(column=2, row=1, sticky=(W, E))
                           
        # Add Entry Widget for Display of the Last Stock Close Price           
        self.close_price = StringVar()
        self.close_price_entry = ttk.Entry(self.mainframe, width=10, 
                                textvariable=self.close_price, justify=CENTER)
        self.close_price_entry.grid(column=2, row=2, sticky=(W, E))
        
        # Add Entry Widget for Display of the Previous Stock Close Price
        self.p_close_price = StringVar()
        self.p_close_price_entry = ttk.Entry(self.mainframe, width=10, 
                              textvariable=self.p_close_price, justify=CENTER)
        self.p_close_price_entry.grid(column=2, row=3, sticky=(W, E))
        
        # Add Entry Widget for Display of the Percent Change in Price
        self.change = StringVar()
        self.change_entry = ttk.Entry(self.mainframe, width=10, 
                                     textvariable=self.change, justify=CENTER)
        self.change_entry.grid(column=2, row=4, sticky=(W, E))
        
        # Add Entry Widget for Display of Trading Volume for Last Day
        self.vol = StringVar()
        self.vol_entry = ttk.Entry(self.mainframe, width=10, 
                                        textvariable=self.vol, justify=CENTER)
        self.vol_entry.grid(column=2, row=5, sticky=(W, E))
        self.style.configure("TButton",font=("Arial", 20),foreground='maroon')
        # Add Button Widget for Calling stock_close() to Display Quote 
        ttk.Button(self.mainframe, text="Price", cursor="hand2", 
                   command=self.stock_close).grid(column=2, row=6, sticky=W)
        
    # Function to get stock close information 
    def stock_close(self) : 
        # Check for missing stock symbol
        if self.symbol.get() == "":
            showinfo(title="Warning", message="Symbol Missing")
            self.clear_entries()
            return
        c_symbol = self.symbol.get().upper()
        self.symbol.set(c_symbol)
        # base_url variable store base url  
        base_url = \
        r"https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
        # main_url variable store complete url 
        main_url = base_url + "&symbol=" + c_symbol + \
                   "&apikey=" + self.api_key      
        # get method of requests module returns response object  
        res_obj = requests.get(main_url) 
        # json method returns json format data into python dictionary data type. 
        # rates are returned in a list of nested dictionaries 
        self.result = res_obj.json()
        try:
            # Get and Display Last Closing Price
            self.c_price = self.result["Global Quote"]['05. price']
            f_price = round(float(self.c_price), 2)
            self.c_price = str(f_price)
            self.close_price.set("$"+self.c_price)
            
            # Get and Display Previous Day's Closing Price
            self.pc_price = self.result["Global Quote"]['08. previous close']
            f_price = round(float(self.pc_price), 2)
            self.pc_price = str(f_price)
            self.p_close_price.set("$"+self.pc_price)
            # Get and Display Percent Change in Stock Value
            self.p_change = self.result["Global Quote"]['10. change percent']
            self.change.set(self.p_change)
            
            # Get and Display Last Day's Volume for this Stock
            self.volume = self.result["Global Quote"]['06. volume']
            v = int(self.volume) # converts the string self.volume to integer
            v = "{:,}".format(v) # converts int to string with commas
            self.vol.set(v)
            
        except:
            # If Stock Symbol is Invalid Display a Warning
            warn_msg = "Symbol " + c_symbol + " Not Found"
            showwarning(title="Warning", message=warn_msg)
            self.clear_entries()
    def clear_entries(self):
        self.symbol.set("")
        self.close_price.set("")
        self.p_close_price.set("")
        self.change.set("")
        self.vol.set("")
        
# ***** End of Class SimpleGUI_A *****
# Instantiate GUI Canvas Using Tk   
api_key  = "demo"
api_key  = "CK8FNM4QB629PDZL"
root     = Tk()
root.title("Stock Price")
# Paint Canvas Using Class StockGUI __init__()
my_gui = StockGUI(root, api_key)
# Display GUI
root.mainloop()