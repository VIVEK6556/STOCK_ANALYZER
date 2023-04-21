import os
import threading
import functools as ft
import time
import schedule
import pandas as pd
import tkinter as tk
from datetime import date, datetime
from tkinter import ttk, RIGHT, Y, BOTH, VERTICAL, LEFT, HORIZONTAL, BOTTOM, X, TOP, FLAT
import urllib
import requests
import warnings
import calendar
warnings.filterwarnings('ignore')
from urllib.request import urlretrieve as ret
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
from tkinter.filedialog import askdirectory
from PIL import ImageTk,Image
from thefirstock import thefirstock
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, relative_path)
class Smart_Analogy():
    def Firststock_login(self):
        self.stop_Thread = threading.Event()
        self.bot = tk.Tk()
        self.bot.title("FIRSTOCK_LOGIN")
        def clock():
            ttk.Label(self.bot, background='yellow', font=my_font, text=time.strftime("%H:%M:%S")).grid(row=0, column=1)
            ttk.Label(self.bot, background='yellow', font=my_font, text=time.strftime("%d/%m/%Y")).grid(row=1, column=1)
            self.bot.after(1000, clock)

        my_font = ('times', 30, 'bold')
        self.clock_update = ttk.Label(self.bot, background='yellow', font=my_font, text=time.strftime("%H:%M:%S")).grid(
            row=0,
            column=1)
        self.clock_update = ttk.Label(self.bot, background='yellow', font=my_font, text=time.strftime("%d/%m/%Y")).grid(
            row=1,
            column=1)
        clock()
        self.bot.frame = ttk.Frame(self.bot, padding=(20, 10), borderwidth=70)
        self.bot.frame.grid()
        self.bot.frame.columnconfigure(0, weight=1)
        self.bot.frame.rowconfigure(1, weight=1)

        def Folder_slection():
            self.path = askdirectory()
        def submit():
            if self.stop_Thread.is_set():
                return
            ttk.Label(self.bot, text="Please Wait....", background='Yellow').grid(column=0, row=3, pady=2, padx=2)
            totp = self.TOTP.get()
            self.TOTP.set("")
            userid = self.userid.get()
            self.userid.set("")
            api_key = self.api_key.get()
            self.api_key.set("")
            password = self.password.get()
            self.password.set("")
            vendorcode = self.vendor_code.get()
            self.vendor_code.set("")
            login = thefirstock.firstock_login(
                userId=str(userid),  # VI2097
                password=str(password),  # 655665@Vg
                TOTP=str(totp),
                    vendorCode=str(vendorcode),  # VI2097_API
                apiKey=str(api_key),  # 44622c2eb3d0e8535d2fa6f78e525b0f
            )
            if login == None:
                ttk.Label(self.bot, text="Login Unsuccesful", background='Yellow').grid(column=0, row=3, pady=2, padx=2)
            else:
                urls = ["https://swagger.thefirstock.com/NFOSymbolDownloadCSV",
                        "https://swagger.thefirstock.com/indexSymbols",
                        "https://swagger.thefirstock.com/NSESymbolDownload",
                        "https://swagger.thefirstock.com/BSESymbolDownload"]
                file_names = [self.path + "\\NFOSymbol.csv", self.path + "\\indexSymbols.csv",
                              self.path + "\\NSESymbol.csv",
                              self.path + "\\BSESymbol.csv", ]
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-Agent', 'MyApp/1.0')]
                urllib.request.install_opener(opener)
                for i, j in zip(urls, file_names):
                    status = requests.get(i)
                    if status.ok:
                        ret(i, j)
                    else:
                        pass
                time.sleep(5)
                ttk.Label(self.bot, text="Login Succesful", background='Yellow').grid(column=0, row=3, pady=2, padx=2)

        self.TOTP = tk.StringVar()
        self.userid = tk.StringVar()
        self.api_key = tk.StringVar()
        self.password = tk.StringVar()
        self.vendor_code = tk.StringVar()
        ttk.Label(self.bot.frame, text="USERID:", background='yellow').grid(column=0, row=2, padx=2, pady=2)
        ttk.Label(self.bot.frame, text="PASSWORD:", background='yellow').grid(column=0, row=3, padx=2, pady=2)
        ttk.Label(self.bot.frame, text="TOTP:", background='yellow').grid(column=0, row=1, padx=2, pady=2)
        ttk.Label(self.bot.frame, text="VENDORCODE:", background='yellow').grid(column=0, row=4, padx=2, pady=2)
        ttk.Label(self.bot.frame, text="API_KEY:", background='yellow').grid(column=0, row=5, padx=2, pady=2)
        ttk.Entry(self.bot.frame, width=6, textvariable=self.TOTP).grid(column=1, row=1, padx=2, pady=2)
        ttk.Entry(self.bot.frame, width=6, textvariable=self.userid).grid(column=1, row=2, padx=2, pady=2)
        ttk.Entry(self.bot.frame, width=32, textvariable=self.api_key).grid(column=1, row=5, padx=2, pady=2)
        # def show():
        #     hide_button = ttk.Button(self.bot.frame,  image=hide_image,command=hide).grid(column=2, row=3, padx=2, pady=2)
        #     ttk.Entry(self.bot.frame, width=10, textvariable=self.password, show='').grid(column=1, row=3, padx=2, pady=2)
        # def hide():
        #     show_button = ttk.Button(self.bot.frame, image=show_image,command=show).grid(column=2,row=3, padx=2, pady=2)
        #     ttk.Entry(self.bot.frame, width=10, textvariable=self.password, show='*').grid(column=1, row=3, padx=2, pady=2)
        # show_image=ImageTk.PhotoImage(file="./UNHIDE.png",height=-200,width=-200)
        # # hide_image=ImageTk.PhotoImage(file="./HIDE.png",height=-200,width=200)
        # show_button=ttk.Button(self.bot.frame,image=show_image,command=show).grid(column=2,row=3, padx=2, pady=2)
        ttk.Entry(self.bot.frame, width=10, textvariable=self.password, show='*').grid(column=1, row=3, padx=2, pady=2)
        ttk.Entry(self.bot.frame, width=10, textvariable=self.vendor_code).grid(column=1, row=4, padx=2, pady=2)
        ttk.Button(self.bot, text="Submit", command=threading.Thread(target=submit).start).grid(column=0, row=6, pady=2,
                                                                                                padx=2)
        ttk.Button(self.bot, text="Next", command=threading.Thread(target=self.Application).start).grid(column=2, row=6,
                                                                                                        pady=2,
                                                                                                        padx=2)
        ttk.Button(self.bot, text="SELECT_FOLDER", command=Folder_slection).grid(column=1, row=6, pady=2, padx=2)
        ttk.Button(self.bot, text="Quit", command=self.bot.destroy).grid(column=3, row=6, pady=2, padx=2)
        self.bot.mainloop()
    def Application(self):
        if self.stop_Thread.is_set():
            return
        self.Future_Cur = self.spot = self.ATM_1CP_1 = self.ATM_CC_1 = self.ATM_3CP_1 = self.ATM_4CP_1 = self.ATM_1CC_1 = self.ATM_1NP_1 = self.ATM_1FP_1 \
            = self.ATM_2CP_1 = self.ATM_4CC_1 = self.ATM_3CC_1 = self.ATM_CP_1 = self.ATM_1NC_1 = self.ATM_3NP_1 = self.Future_Near = self.ATM_NC_1 = self.ATM_2NC_1 = \
            self.ATM_3NC_1 = self.Future_Far = self.ATM_NP_1 = self.ATM_4NP_1 = self.ATM_2CC_1 = self.ATM_2FC_1 = self.ATM_4FC_1 = self.ATM_3FP_1 = \
            self.ATM_3FC_1 = self.ATM_1FC_1 = self.ATM_4NC_1 = self.ATM_2FP_1 = self.ATM_FP_1 = self.ATM_2NP_1 = self.ATM_FC_1 = self.ATM_4FP_1 = 000000
        self.BATM_1CP_1 = self.BATM_CC_1 = self.BATM_3CP_1 = self.BATM_4CP_1 = self.BATM_1CC_1 = self.BATM_1NP_1 = self.BATM_1FP_1 \
            = self.BATM_2CP_1 = self.BATM_4CC_1 = self.BATM_3CC_1 = self.BATM_CP_1 = self.BATM_1NC_1 = self.BATM_3NP_1 = self.Future_BNear = self.BATM_NC_1 = self.BATM_2NC_1 = \
            self.BATM_3NC_1 = self.Future_BFar = self.BATM_NP_1 = self.BATM_4NP_1 = self.BATM_2CC_1 = self.BATM_2FC_1 = self.BATM_4FC_1 = self.BATM_3FP_1 = \
            self.BATM_3FC_1 = self.BATM_1FC_1 = self.BATM_4NC_1 = self.BATM_2FP_1 = self.BATM_FP_1 = self.BATM_2NP_1 = self.BATM_FC_1 = self.BATM_4FP_1 = 00000
        self.BATM_NCP_1 = self.ATM_4CP_1 = 0000
        self.Cdf1 = pd.DataFrame(
            {'DATE_TIME': [''], 'Equities Derivatives': [''],
             'SCAFPA-2': [''],
             'SCAFPA-1': [''],
             'SCAFPA': [''],
             'SCAFPA+1': [''],
             'SCAFPA+2': ['']})
        self.Ndf1 = pd.DataFrame(
            {'DATE_TIME': [''],'Equities Derivatives': [''],
             'SCAFPA-2': [''],
             'SCAFPA-1': [''],
             'SCAFPA': [''],
             'SCAFPA+1': [''],
             'SCAFPA+2': ['']})
        self.Fdf1 = pd.DataFrame(
            {'DATE_TIME': [''],'Equities Derivatives': [''],
             'SCAFPA-2': [''],
             'SCAFPA-1': [''],
             'SCAFPA': [''],
             'SCAFPA+1': [''],
             'SCAFPA+2': ['']})
        self.BCdf1 = pd.DataFrame(
            {'DATE_TIME': [''], 'Equities Derivatives': [''],
             'SCAFPA-2': [''],
             'SCAFPA-1': [''],
             'SCAFPA': [''],
             'SCAFPA+1': [''],
             'SCAFPA+2': ['']})
        self.BNdf1 = pd.DataFrame(
            {'DATE_TIME': [''],'Equities Derivatives': [''],
             'SCAFPA-2': [''],
             'SCAFPA-1': [''],
             'SCAFPA': [''],
             'SCAFPA+1': [''],
             'SCAFPA+2': ['']})
        self.BFdf1 = pd.DataFrame(
            {'DATE_TIME': [''],'Equities Derivatives': [''],
             'SCAFPA-2': [''],
             'SCAFPA-1': [''],
             'SCAFPA': [''],
             'SCAFPA+1': [''],
             'SCAFPA+2': ['']})
        self.root = tk.Tk()
        self.root.title("Stock Analyzer")
        self.root.configure(background="LightBlue",borderwidth=10)
        main_frame= ttk.Frame(self.root)
        main_frame.pack(fill=BOTH,expand=1)
        my_canvas= tk.Canvas(main_frame)
        my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
        my_scroolbar=ttk.Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview)
        my_scroolbar.pack(side=RIGHT,fill=Y)
        my_canvas.configure(yscrollcommand=my_scroolbar.set)
        my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        my_scroolbar = ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=my_canvas.xview)
        my_scroolbar.pack(side=BOTTOM, fill=X)

        self.second_frame= ttk.Frame(my_canvas)
        self.second_frame.grid_rowconfigure(0, weight=0)
        my_canvas.create_window((0,0),window=self.second_frame,anchor='nw')
        ttk.Label(self.second_frame, text="NIFTY", background='red').grid(column=0, row=0, padx=2, pady=1)
        def clock():
            ttk.Label(self.second_frame, background='yellow',text=time.strftime("%H:%M:%S")).grid(row=1, column=8)
            ttk.Label(self.second_frame, background='yellow', text=time.strftime("%d/%m/%Y")).grid(row=1, column=12)
            self.root.after(1000,clock)
        ttk.Label(self.second_frame,background='yellow',text=time.strftime("%H:%M:%S")).grid(row=1,column=8)
        ttk.Label(self.second_frame, background='yellow', text=time.strftime("%d/%m/%Y")).grid(row=1, column=12)
        ttk.Label(self.second_frame, background='yellow', text='TIME').grid(row=0, column=8)
        ttk.Label(self.second_frame, background='yellow', text='DATE').grid(row=0, column=12)
        clock()
        def Thread_Closing():
            self.second_frame.quit()
            time.sleep(5)
            self.stop_Thread.set()
            time.sleep(180)
            try:
                threading.Thread(target=self.Application).join()
            except:
                pass
            try:
                threading.Thread(target=self.Data_Upadting()).join()
            except:
                pass
            try:
                threading.Thread(target=self.Scheduled_DataSaving()).join()
            except:
                pass


        ttk.Button(self.second_frame,  text='QUIT',command=Thread_Closing).grid(row=0, column=16)
        self.minute=''
        self.hour=''
        initial_value = tk.StringVar(value='20')
        ttk.Label(self.second_frame, text="HOUR", background='yellow').grid(column=20, row=0, padx=2, pady=2)
        spin_1= ttk.Spinbox(self.second_frame,from_=1,to=24,textvariable=initial_value,wrap=False)
        def grab():
            self.hour=spin_1.get()
            self.minute = spin_2.get()
        spin_1.grid(row=1, column=20)
        initial_value_1= tk.StringVar(value='20')
        ttk.Label(self.second_frame, text="MINUTE", background='yellow').grid(column=24, row=0, padx=2, pady=2)
        spin_2 = ttk.Spinbox(self.second_frame, from_=0, to=55,increment=5, textvariable=initial_value_1, wrap=False)
        spin_2.grid(column=24, row=1)
        ttk.Button(self.second_frame, text='SUBMIT', command=grab()).grid(column=26, row=1, padx=2, pady=2)
        ttk.Label(self.second_frame, text="Current_Month", background='yellow').grid(column=2, row=1, padx=2, pady=1)
        ttk.Label(self.second_frame, text="Spot_Value", background='orange').grid(column=4, row=2, padx=2, pady=1)
        ttk.Label(self.second_frame, width=15).grid(column=4, row=3, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="Future_Value", background='orange').grid(column=6, row=2, sticky="EW",padx=2, pady=1)
        ttk.Label(self.second_frame, width=15).grid(column=8, row=3, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA+2", background='orange').grid(column=8, row=2, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, width=15).grid(column=10, row=3, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA+1", background='orange').grid(column=10, row=2, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, width=15).grid(column=12, row=3, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA", background='orange').grid(column=12, row=2, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, width=15).grid(column=14, row=3, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA-1", background='orange').grid(column=14, row=2, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, width=15).grid(column=16, row=3, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA-2", background='orange').grid(column=16, row=2, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, width=15).grid(column=18, row=3, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA+2", background='orange').grid(column=18, row=2, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, width=15).grid(column=20, row=3, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA+1", background='orange').grid(column=20, row=2, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, width=15).grid(column=22, row=3, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA", background='orange').grid(column=22, row=2, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, width=15).grid(column=24, row=3, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA-1", background='orange').grid(column=24, row=2, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, width=15).grid(column=26, row=3, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA-2", background='orange').grid(column=26, row=2, sticky="EW", padx=2,
                                                                            pady=1)
        # # Result_output
        ttk.Label(self.second_frame, text="SED", background='lightgreen').grid(column=4, row=4)
        ttk.Label(self.second_frame, text="   ").grid(column=4, row=5)
        ttk.Label(self.second_frame, text="SCA+2", background='lightgreen').grid(column=8, row=4, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA+1", background='lightgreen').grid(column=10, row=4, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="SCA", background='lightgreen').grid(column=12, row=4, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA-1", background='lightgreen').grid(column=14, row=4, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="SCA-2", background='lightgreen').grid(column=16, row=4, sticky="EW", padx=2,
                                                                           pady=1)
        # Put_Value
        ttk.Label(self.second_frame, text="FPA+2", background='lightgreen').grid(column=18, row=4, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="FPA+1", background='lightgreen').grid(column=20, row=4, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="FPA", background='lightgreen').grid(column=22, row=4, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="FPA-1", background='lightgreen').grid(column=24, row=4, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="FPA-2", background='lightgreen').grid(column=26, row=4, sticky="EW", padx=2,
                                                                           pady=1)
        # Final_output
        ttk.Label(self.second_frame, text="SCAFPA", background='violet').grid(column=4, row=6, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="     ").grid(column=4, row=7, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="SCAFPA+2", background='violet').grid(column=8, row=6, sticky="EW", padx=2,
                                                                                pady=1)
        ttk.Label(self.second_frame, text="SCAFPA+1", background='violet').grid(column=10, row=6, sticky="EW", padx=2,
                                                                                pady=1)
        ttk.Label(self.second_frame, text="SCAFPA", background='violet').grid(column=12, row=6, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="SCAFPA-1", background='violet').grid(column=14, row=6, sticky="EW", padx=2,
                                                                                pady=1)
        ttk.Label(self.second_frame, text="SCAFPA-2", background='violet').grid(column=16, row=6, sticky="EW", padx=2,
                                                                                pady=1)
        # # NEAR MONTH
        ttk.Label(self.second_frame, text="Near_Month", background='yellow').grid(column=2, row=8)
        ttk.Label(self.second_frame, text="Spot_Value", background='orange').grid(column=4, row=9)
        ttk.Label(self.second_frame, text="Future_Value", background='orange').grid(column=6, row=9, sticky="EW",
                                                                                    padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA+2", background='orange').grid(column=8, row=9, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="CA+1", background='orange').grid(column=10, row=9, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="CA", background='orange').grid(column=12, row=9, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA-1", background='orange').grid(column=14, row=9, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="CA-2", background='orange').grid(column=16, row=9, sticky="EW", padx=2,
                                                                            pady=1)
        # # Put_Value
        ttk.Label(self.second_frame, text="PA+2", background='orange').grid(column=18, row=9, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="PA+1", background='orange').grid(column=20, row=9, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="PA", background='orange').grid(column=22, row=9, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA-1", background='orange').grid(column=24, row=9, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="PA-2", background='orange').grid(column=26, row=9, sticky="EW", padx=2,
                                                                            pady=1)
        # # Result_output
        ttk.Label(self.second_frame, text="SED", background='lightgreen').grid(column=4, row=11)
        ttk.Label(self.second_frame, text="   ").grid(column=4, row=12)
        ttk.Label(self.second_frame, text="SCA+2", background='lightgreen').grid(column=8, row=11, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="SCA+1", background='lightgreen').grid(column=10, row=11, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="SCA", background='lightgreen').grid(column=12, row=11, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA-1", background='lightgreen').grid(column=14, row=11, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="SCA-2", background='lightgreen').grid(column=16, row=11, sticky="EW", padx=2,
                                                                           pady=1) \
            # Put_Value
        ttk.Label(self.second_frame, text="FPA+2", background='lightgreen').grid(column=18, row=11, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="FPA+1", background='lightgreen').grid(column=20, row=11, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="FPA", background='lightgreen').grid(column=22, row=11, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="FPA-1", background='lightgreen').grid(column=24, row=11, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="FPA-2", background='lightgreen').grid(column=26, row=11, sticky="EW", padx=2,
                                                                           pady=1)
        # # Final_output
        ttk.Label(self.second_frame, text="SCAFPA", background='violet').grid(column=4, row=13, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="     ").grid(column=4, row=14, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="SCAFPA+2", background='violet').grid(column=8, row=13, sticky="EW", padx=2,
                                                                                pady=1)
        ttk.Label(self.second_frame, text="SCAFPA+1", background='violet').grid(column=10, row=13, sticky="EW", padx=2,
                                                                                pady=1)
        ttk.Label(self.second_frame, text="SCAFPA", background='violet').grid(column=12, row=13, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="SCAFPA-1", background='violet').grid(column=14, row=13, sticky="EW", padx=2,
                                                                                pady=1)
        ttk.Label(self.second_frame, text="SCAFPA-2", background='violet').grid(column=16, row=13, sticky="EW", padx=2,
                                                                                pady=1)
        # # Far MONTH
        ttk.Label(self.second_frame, text="Far_Month", background='yellow').grid(column=2, row=15)
        ttk.Label(self.second_frame, text="Spot_Value", background='orange').grid(column=4, row=16)
        ttk.Label(self.second_frame, text="Future_Value", background='orange').grid(column=6, row=16, sticky="EW",
                                                                                    padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA+2", background='orange').grid(column=8, row=16, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="CA+1", background='orange').grid(column=10, row=16, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="CA", background='orange').grid(column=12, row=16, sticky="EW", padx=2,
                                                                          pady=1)
        ttk.Label(self.second_frame, text="CA-1", background='orange').grid(column=14, row=16, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="CA-2", background='orange').grid(column=16, row=16, sticky="EW", padx=2,
                                                                            pady=1)

        # # Put_Value
        ttk.Label(self.second_frame, text="PA+2", background='orange').grid(column=18, row=16, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="PA+1", background='orange').grid(column=20, row=16, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="PA", background='orange').grid(column=22, row=16, sticky="EW", padx=2,
                                                                          pady=1)
        ttk.Label(self.second_frame, text="PA-1", background='orange').grid(column=24, row=16, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="PA-2", background='orange').grid(column=26, row=16, sticky="EW", padx=2,
                                                                            pady=1)
        # Result_output
        ttk.Label(self.second_frame, text="SED", background='lightgreen').grid(column=4, row=18)
        ttk.Label(self.second_frame, text="   ").grid(column=4, row=19)
        ttk.Label(self.second_frame, text="SCA+2", background='lightgreen').grid(column=8, row=18, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="SCA+1", background='lightgreen').grid(column=10, row=18, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="SCA", background='lightgreen').grid(column=12, row=18, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA-1", background='lightgreen').grid(column=14, row=18, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="SCA-2", background='lightgreen').grid(column=16, row=18, sticky="EW", padx=2,
                                                                           pady=1)
        # Put_Value
        ttk.Label(self.second_frame, text="FPA+2", background='lightgreen').grid(column=18, row=18, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="FPA+1", background='lightgreen').grid(column=20, row=18, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="FPA", background='lightgreen').grid(column=22, row=18, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="FPA-1", background='lightgreen').grid(column=24, row=18, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="FPA-2", background='lightgreen').grid(column=26, row=18, sticky="EW", padx=2,
                                                                           pady=1)
        # Final_output
        ttk.Label(self.second_frame, text="SCAFPA", background='violet').grid(column=4, row=20, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="     ").grid(column=4, row=21, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="SCAFPA+2", background='violet').grid(column=8, row=20, sticky="EW", padx=2,
                                                                                pady=1)
        ttk.Label(self.second_frame, text="SCAFPA+1", background='violet').grid(column=10, row=20, sticky="EW", padx=2,
                                                                                pady=1)
        ttk.Label(self.second_frame, text="SCAFPA", background='violet').grid(column=12, row=20, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="SCAFPA-1", background='violet').grid(column=14, row=20, sticky="EW", padx=2,
                                                                                pady=1)
        ttk.Label(self.second_frame, text="SCAFPA-2", background='violet').grid(column=16, row=20, sticky="EW", padx=2,
                                                                                pady=1)
        # # ***BANKNIFTY***#
        ttk.Label(self.second_frame, text="BANK_NIFTY", background='red').grid(column=0, row=22)
        ttk.Label(self.second_frame, text="Current_Month", background='yellow').grid(column=2, row=23)
        ttk.Label(self.second_frame, text="Spot_Value", background='orange').grid(column=4, row=24)
        ttk.Label(self.second_frame, text="Future_Value", background='orange').grid(column=6, row=24, sticky="EW",
                                                                                    padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA+2", background='orange').grid(column=8, row=24, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="CA+1", background='orange').grid(column=10, row=24, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="CA", background='orange').grid(column=12, row=24, sticky="EW", padx=2,
                                                                          pady=1)
        ttk.Label(self.second_frame, text="CA-1", background='orange').grid(column=14, row=24, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="CA-2", background='orange').grid(column=16, row=24, sticky="EW", padx=2,
                                                                            pady=1)
        # Put_Value
        ttk.Label(self.second_frame, text="PA+2", background='orange').grid(column=18, row=24, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="PA+1", background='orange').grid(column=20, row=24, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="PA", background='orange').grid(column=22, row=24, sticky="EW", padx=2,
                                                                          pady=1)
        ttk.Label(self.second_frame, text="PA-1", background='orange').grid(column=24, row=24, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="PA-2", background='orange').grid(column=26, row=24, sticky="EW", padx=2,
                                                                            pady=1)
        # Result_output
        ttk.Label(self.second_frame, text="SED", background='lightgreen').grid(column=4, row=26)
        ttk.Label(self.second_frame, text="   ").grid(column=4, row=27)
        ttk.Label(self.second_frame, text="SCA+2", background='lightgreen').grid(column=8, row=26, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="SCA+1", background='lightgreen').grid(column=10, row=26, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="SCA", background='lightgreen').grid(column=12, row=26, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA-1", background='lightgreen').grid(column=14, row=26, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="SCA-2", background='lightgreen').grid(column=16, row=26, sticky="EW", padx=2,
                                                                           pady=1)
        # Put_Value
        ttk.Label(self.second_frame, text="FPA+2", background='lightgreen').grid(column=18, row=26, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="FPA+1", background='lightgreen').grid(column=20, row=26, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="FPA", background='lightgreen').grid(column=22, row=26, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="FPA-1", background='lightgreen').grid(column=24, row=26, sticky="EW", padx=2,
                                                                           pady=1)
        ttk.Label(self.second_frame, text="FPA-2", background='lightgreen').grid(column=26, row=26, sticky="EW", padx=2,
                                                                           pady=1)

        # Final_output

        ttk.Label(self.second_frame, text="SCAFPA", background='violet').grid(column=4, row=28, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="     ").grid(column=4, row=29, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="SCAFPA+2", background='violet').grid(column=8, row=28, sticky="EW", padx=2,
                                                                                pady=1)
        ttk.Label(self.second_frame, text="SCAFPA+1", background='violet').grid(column=10, row=28, sticky="EW", padx=2,
                                                                                pady=1)
        ttk.Label(self.second_frame, text="SCAFPA", background='violet').grid(column=12, row=28, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="SCAFPA-1", background='violet').grid(column=14, row=28, sticky="EW", padx=2,
                                                                                pady=1)
        ttk.Label(self.second_frame, text="SCAFPA-2", background='violet').grid(column=16, row=28, sticky="EW", padx=2,
                                                                                pady=1)
        # NEAR MONTH
        ttk.Label(self.second_frame, text="Near_Month", background='yellow').grid(column=2, row=30)
        ttk.Label(self.second_frame, text="Spot_Value", background='orange').grid(column=4, row=31)
        ttk.Label(self.second_frame, text="Future_Value", background='orange').grid(column=6, row=31, sticky="EW",
                                                                                    padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA+2", background='orange').grid(column=8, row=31, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="CA+1", background='orange').grid(column=10, row=31, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="CA", background='orange').grid(column=12, row=31, sticky="EW", padx=2,
                                                                          pady=1)
        ttk.Label(self.second_frame, text="CA-1", background='orange').grid(column=14, row=31, sticky="EW", padx=2,
                                                                            pady=1)
        ttk.Label(self.second_frame, text="CA-2", background='orange').grid(column=16, row=31, sticky="EW", padx=2,
                                                                            pady=1)
        # Put_Value
        ttk.Label(self.second_frame, text="PA+2", background='orange').grid(column=18, row=31, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA+1", background='orange').grid(column=20, row=31, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA", background='orange').grid(column=22, row=31, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA-1", background='orange').grid(column=24, row=31, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA-2", background='orange').grid(column=26, row=31, sticky="EW", padx=2, pady=1)
        # Result_output
        ttk.Label(self.second_frame, text="SED", background='lightgreen').grid(column=4, row=33)
        ttk.Label(self.second_frame, text="   ").grid(column=4, row=34)
        ttk.Label(self.second_frame, text="SCA+2", background='lightgreen').grid(column=8, row=33, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA+1", background='lightgreen').grid(column=10, row=33, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA", background='lightgreen').grid(column=12, row=33, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA-1", background='lightgreen').grid(column=14, row=33, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA-2", background='lightgreen').grid(column=16, row=33, sticky="EW", padx=2, pady=1)
        # Put_Value
        ttk.Label(self.second_frame, text="FPA+2", background='lightgreen').grid(column=18, row=33, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="FPA+1", background='lightgreen').grid(column=20, row=33, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="FPA", background='lightgreen').grid(column=22, row=33, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="FPA-1", background='lightgreen').grid(column=24, row=33, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="FPA-2", background='lightgreen').grid(column=26, row=33, sticky="EW", padx=2, pady=1)
        # Final_output
        ttk.Label(self.second_frame, text="SCAFPA", background='violet').grid(column=4, row=35, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, text="     ").grid(column=4, row=36, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="SCAFPA+2", background='violet').grid(column=8, row=35, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, text="SCAFPA+1", background='violet').grid(column=10, row=35, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, text="SCAFPA", background='violet').grid(column=12, row=35, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, text="SCAFPA-1", background='violet').grid(column=14, row=35, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, text="SCAFPA-2", background='violet').grid(column=16, row=35, sticky="EW", padx=2,pady=1)
        # Far MONTH
        ttk.Label(self.second_frame, text="Far_Month", background='yellow').grid(column=2, row=37)
        ttk.Label(self.second_frame, text="Spot_Value", background='orange').grid(column=4, row=38)
        ttk.Label(self.second_frame, text="Future_Value", background='orange').grid(column=6, row=38, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, text="CA+2", background='orange').grid(column=8, row=38, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA+1", background='orange').grid(column=10, row=38, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA", background='orange').grid(column=12, row=38, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA-1", background='orange').grid(column=14, row=38, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="CA-2", background='orange').grid(column=16, row=38, sticky="EW", padx=2, pady=1)
        # Put_Value
        ttk.Label(self.second_frame, text="PA+2", background='orange').grid(column=18, row=38, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA+1", background='orange').grid(column=20, row=38, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA", background='orange').grid(column=22, row=38, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA-1", background='orange').grid(column=24, row=38, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="PA-2", background='orange').grid(column=26, row=38, sticky="EW", padx=2, pady=1)
        # Result_output
        ttk.Label(self.second_frame, text="SED", background='lightgreen').grid(column=4, row=41)
        ttk.Label(self.second_frame, text="   ").grid(column=4, row=42)
        ttk.Label(self.second_frame, text="SCA+2", background='lightgreen').grid(column=8, row=41, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA+1", background='lightgreen').grid(column=10, row=41, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA", background='lightgreen').grid(column=12, row=41, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA-1", background='lightgreen').grid(column=14, row=41, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="SCA-2", background='lightgreen').grid(column=16, row=41, sticky="EW", padx=2, pady=1)
        # Put_Value
        ttk.Label(self.second_frame, text="FPA+2", background='lightgreen').grid(column=18, row=41, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="FPA+1", background='lightgreen').grid(column=20, row=41, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="FPA", background='lightgreen').grid(column=22, row=41, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="FPA-1", background='lightgreen').grid(column=24, row=41, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, text="FPA-2", background='lightgreen').grid(column=26, row=41, sticky="EW", padx=2, pady=1)
        # Final_output
        ttk.Label(self.second_frame, text="SCAFPA", background='violet').grid(column=4, row=43, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, text="     ").grid(column=4, row=44, sticky="EW", padx=2,
                                                                              pady=1)
        ttk.Label(self.second_frame, text="SCAFPA+2", background='violet').grid(column=8, row=43, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, text="SCAFPA+1", background='violet').grid(column=10, row=43, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, text="SCAFPA", background='violet').grid(column=12, row=43, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, text="SCAFPA-1", background='violet').grid(column=14, row=43, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, text="SCAFPA-2", background='violet').grid(column=16, row=43, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, text="   ").grid(column=4, row=45, sticky="EW", padx=2,pady=1)
        ttk.Label(self.second_frame, width=15, text='   ').grid(column=4, row=3, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, width=15, text='   ').grid(column=4, row=10, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, width=15, text='   ').grid(column=4, row=17, sticky="EW", padx=2, pady=1)
        # BANKNIFTY
        ttk.Label(self.second_frame, width=15, text='   ').grid(column=4, row=25, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, width=15, text='   ').grid(column=4, row=32, sticky="EW", padx=2, pady=1)
        ttk.Label(self.second_frame, width=15, text='   ').grid(column=4, row=39, sticky="EW", padx=2, pady=1)
        self.root.after(2000,threading.Thread(target=self.Data_Upadting).start())
        self.root.mainloop()
    def Data_Upadting(self):
        if self.stop_Thread.is_set():
            return
        global token
        ltp=10
        getMultiQuotesLTP = thefirstock.firstock_getMultiQuoteLTP(dataToken=[{"exchange": "NSE", "token": "26000"}])
        try:
            ltp = int(float(getMultiQuotesLTP['data'][0]['result']['lastTradedPrice']))
        except:
            ttk.Label(self.bot, text="Please Login to the First Account", background='Yellow').grid(column=0, row=3, pady=2, padx=2)
        self.spot = ltp
        if (int(str(ltp)[-2:])) <= 50:
            Find_Value = ltp + (50 - (int(str(ltp)[-2:])))
        else:
            Find_Value = ltp + (100 - (int(str(ltp)[-2:])))
        getMultiQuotesLTP = thefirstock.firstock_getMultiQuoteLTP(dataToken=[{"exchange": "NSE", "token": "26009"}])
        bltp = int(float(getMultiQuotesLTP['data'][0]['result']['lastTradedPrice']))
        self.bspot = bltp
        Bfind_Value = bltp + (100 - (int(str(bltp)[-2:])))
        df = pd.read_csv(self.path+"\\NFOSymbol.csv")
        self.next = 0
        # if str(date.today())[-2:] >= str((date(2023, int(datetime.now().strftime("%m")[1]), 1) + relativedelta(day=0, weekday=TH(-1))))[8:10]:
        #     self.next += 1
        # else:
        #     self.next = 0
        testdate = datetime.now()
        weekly_thursday = []
        market_last = [week for week in calendar.monthcalendar(testdate.year, testdate.month) if
                       week[3] != 0 and weekly_thursday.append(week[3])]
        self.CUR_Year_Month_DATE = str(str((weekly_thursday[-1]))) + datetime.strptime(
            str(int(datetime.now().strftime("%m"))), "%m").strftime("%b").upper() + datetime.now().strftime(
            "%y").upper() + "C"
        self.Cur_Future = list(dict(df[df.eq(
            "NIFTY" + str(weekly_thursday[-1]) + datetime.strptime(str(int(datetime.now().strftime("%m")) + self.next),
                                                                   "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + 'F').any(1)]['Token']).values())
        if list(dict(
                df[df.eq("NIFTY" + self.CUR_Year_Month_DATE + str(Find_Value - 100)).any(1)]['Token']).values()) == []:
            self.CUR_Year_Month_DATE = str(str((weekly_thursday[-1] - 1))) + datetime.strptime(
                str(int(datetime.now().strftime("%m"))), "%m").strftime("%b").upper() + datetime.now().strftime(
                "%y").upper() + "C"
            self.Cur_Future = list(dict(df[df.eq("NIFTY" + str(weekly_thursday[-1] - 1) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + 'F').any(1)]['Token']).values())
        else:
            pass
        self.ATM_4CC = list(
            dict(df[df.eq("NIFTY" + self.CUR_Year_Month_DATE + str(Find_Value - 100)).any(1)]['Token']).values())
        self.ATM_3CC = list(
            dict(df[df.eq("NIFTY" + self.CUR_Year_Month_DATE + str(Find_Value - 50)).any(1)]['Token']).values())
        self.ATM_CC = list(
            dict(df[df.eq("NIFTY" + self.CUR_Year_Month_DATE + str(Find_Value)).any(1)]['Token']).values())
        self.ATM_1CC = list(
            dict(df[df.eq("NIFTY" + self.CUR_Year_Month_DATE + str(Find_Value + 50)).any(1)]['Token']).values())
        self.ATM_2CC = list(
            dict(df[df.eq("NIFTY" + self.CUR_Year_Month_DATE + str(Find_Value + 100)).any(1)]['Token']).values())
        # Near Month Call Values
        testdate = datetime.now()
        weekly_thursday = []
        market_last = [week for week in calendar.monthcalendar(testdate.year, testdate.month + 1) if
                       week[3] != 0 and weekly_thursday.append(week[3])]
        self.NEAR_Year_Month_DATE = str(str(weekly_thursday[-1])) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + 1 + self.next), "%m").strftime(
            "%b").upper() + datetime.now().strftime("%y").upper() + "C"
        self.Near_Future = list(dict(df[df.eq("NIFTY" + str(weekly_thursday[-1]) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + 1 + self.next), "%m").strftime(
            "%b").upper() + datetime.now().strftime("%y").upper() + 'F').any(1)]['Token']).values())
        if list(dict(
                df[df.eq("NIFTY" + self.NEAR_Year_Month_DATE + str(Find_Value - 100)).any(1)]['Token']).values()) == []:
            self.NEAR_Year_Month_DATE = str(str(weekly_thursday[-1] - 1)) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + 1 + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + "C"
            self.Near_Future = list(dict(df[df.eq("NIFTY" + str(weekly_thursday[-1] - 1) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + 1 + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + 'F').any(1)]['Token']).values())
        else:
            pass
        self.ATM_4NC = list(
            dict(df[df.eq("NIFTY" + self.NEAR_Year_Month_DATE + str(Find_Value - 100)).any(1)]['Token']).values())
        self.ATM_3NC = list(
            dict(df[df.eq("NIFTY" + self.NEAR_Year_Month_DATE + str(Find_Value - 50)).any(1)]['Token']).values())
        self.ATM_NC = list(
            dict(df[df.eq("NIFTY" + self.NEAR_Year_Month_DATE + str(Find_Value)).any(1)]['Token']).values())
        self.ATM_1NC = list(
            dict(df[df.eq("NIFTY" + self.NEAR_Year_Month_DATE + str(Find_Value + 50)).any(1)]['Token']).values())
        self.ATM_2NC = list(
            dict(df[df.eq("NIFTY" + self.NEAR_Year_Month_DATE + str(Find_Value + 100)).any(1)]['Token']).values())
        # For Month Call Values
        testdate = datetime.now()
        weekly_thursday = []
        market_last = [week for week in calendar.monthcalendar(testdate.year, testdate.month + 2) if
                       week[3] != 0 and weekly_thursday.append(week[3])]
        self.Far_Future = list(dict(df[df.eq("NIFTY" + str(weekly_thursday[-1]) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + 2 + self.next), "%m").strftime(
            "%b").upper() + datetime.now().strftime("%y").upper() + 'F').any(1)]['Token']).values())
        self.FOR_YEAR_MONTH_DATE = str(str(weekly_thursday[-1])) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + 2 + self.next), "%m").strftime(
            "%b").upper() + datetime.now().strftime("%y").upper() + "C"
        if list(dict(
                df[df.eq("NIFTY" + self.FOR_YEAR_MONTH_DATE + str(Find_Value - 100)).any(1)]['Token']).values()) == []:
            self.FOR_YEAR_MONTH_DATE = str(str(weekly_thursday[-1] - 1)) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + 2 + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + "C"
            self.Far_Future = list(dict(df[df.eq("NIFTY" + str(weekly_thursday[-1]) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + 2 + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + 'F').any(1)]['Token']).values())
        else:
            pass
        self.ATM_4FC = list(
            dict(df[df.eq("NIFTY" + self.FOR_YEAR_MONTH_DATE + str(Find_Value - 100)).any(1)]['Token']).values())
        self.ATM_3FC = list(
            dict(df[df.eq("NIFTY" + self.FOR_YEAR_MONTH_DATE + str(Find_Value - 50)).any(1)]['Token']).values())
        self.ATM_FC = list(
            dict(df[df.eq("NIFTY" + self.FOR_YEAR_MONTH_DATE + str(Find_Value)).any(1)]['Token']).values())
        self.ATM_1FC = list(
            dict(df[df.eq("NIFTY" + self.FOR_YEAR_MONTH_DATE + str(Find_Value + 50)).any(1)]['Token']).values())
        self.ATM_2FC = list(
            dict(df[df.eq("NIFTY" + self.FOR_YEAR_MONTH_DATE + str(Find_Value + 100)).any(1)]['Token']).values())

        # *******Puts Values Token Find******
        # Current Month
        testdate = datetime.now()
        weekly_thursday = []
        market_last = [week for week in calendar.monthcalendar(testdate.year, testdate.month) if
                       week[3] != 0 and weekly_thursday.append(week[3])]
        self.CUR_Year_Month_DATEP = str(str((weekly_thursday[-1]))) + datetime.strptime(
            str(int(datetime.now().strftime("%m"))), "%m").strftime("%b").upper() + datetime.now().strftime(
            "%y").upper() + "P"
        if list(dict(
                df[df.eq("NIFTY" + self.CUR_Year_Month_DATEP + str(Find_Value - 100)).any(1)]['Token']).values()) == []:
            self.CUR_Year_Month_DATEP = str(str((weekly_thursday[-1] - 1))) + datetime.strptime(
                str(int(datetime.now().strftime("%m"))), "%m").strftime("%b").upper() + datetime.now().strftime(
                "%y").upper() + "P"
        else:
            pass
        self.ATM_4CP = list(
            dict(df[df.eq("NIFTY" + self.CUR_Year_Month_DATEP + str(Find_Value - 100)).any(1)]['Token']).values())
        self.ATM_3CP = list(
            dict(df[df.eq("NIFTY" + self.CUR_Year_Month_DATEP + str(Find_Value - 50)).any(1)]['Token']).values())
        self.ATM_CP = list(
            dict(df[df.eq("NIFTY" + self.CUR_Year_Month_DATEP + str(Find_Value)).any(1)]['Token']).values())
        self.ATM_1CP = list(
            dict(df[df.eq("NIFTY" + self.CUR_Year_Month_DATEP + str(Find_Value + 50)).any(1)]['Token']).values())
        self.ATM_2CP = list(
            dict(df[df.eq("NIFTY" + self.CUR_Year_Month_DATEP + str(Find_Value + 100)).any(1)]['Token']).values())

        # Near Month Puts Values
        testdate = datetime.now()
        weekly_thursday = []
        market_last = [week for week in calendar.monthcalendar(testdate.year, testdate.month + 1) if
                       week[3] != 0 and weekly_thursday.append(week[3])]
        self.NEAR_Year_Month_DATEP = str(str(weekly_thursday[-1])) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + 1 + self.next), "%m").strftime(
            "%b").upper() + datetime.now().strftime("%y").upper() + "P"
        if list(dict(df[df.eq("NIFTY" + self.NEAR_Year_Month_DATEP + str(Find_Value - 100)).any(1)][
                         'Token']).values()) == []:
            self.NEAR_Year_Month_DATEP = str(str(weekly_thursday[-1])) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + 1 + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + "P"
        else:
            pass
        self.ATM_4NP = list(
            dict(df[df.eq("NIFTY" + self.NEAR_Year_Month_DATEP + str(Find_Value - 100)).any(1)]['Token']).values())
        self.ATM_3NP = list(
            dict(df[df.eq("NIFTY" + self.NEAR_Year_Month_DATEP + str(Find_Value - 50)).any(1)]['Token']).values())
        self.ATM_NP = list(
            dict(df[df.eq("NIFTY" + self.NEAR_Year_Month_DATEP + str(Find_Value)).any(1)]['Token']).values())
        self.ATM_1NP = list(
            dict(df[df.eq("NIFTY" + self.NEAR_Year_Month_DATEP + str(Find_Value + 50)).any(1)]['Token']).values())
        self.ATM_2NP = list(
            dict(df[df.eq("NIFTY" + self.NEAR_Year_Month_DATEP + str(Find_Value + 100)).any(1)]['Token']).values())

        # For Month Puts Values
        testdate = datetime.now()
        weekly_thursday = []
        market_last = [week for week in calendar.monthcalendar(testdate.year, testdate.month + 2) if
                       week[3] != 0 and weekly_thursday.append(week[3])]
        self.FOR_YEAR_MONTH_DATEP = str(str(weekly_thursday[-1])) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + 2 + self.next), "%m").strftime(
            "%b").upper() + datetime.now().strftime("%y").upper() + "P"
        if list(dict(
                df[df.eq("NIFTY" + self.FOR_YEAR_MONTH_DATEP + str(Find_Value - 100)).any(1)]['Token']).values()) == []:
            self.FOR_YEAR_MONTH_DATEP = str(str(weekly_thursday[-1] - 1)) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + 2 + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + "P"
        else:
            pass
        self.ATM_4FP = list(
            dict(df[df.eq("NIFTY" + self.FOR_YEAR_MONTH_DATEP + str(Find_Value - 100)).any(1)]['Token']).values())
        self.ATM_3FP = list(
            dict(df[df.eq("NIFTY" + self.FOR_YEAR_MONTH_DATEP + str(Find_Value - 50)).any(1)]['Token']).values())
        self.ATM_FP = list(
            dict(df[df.eq("NIFTY" + self.FOR_YEAR_MONTH_DATEP + str(Find_Value)).any(1)]['Token']).values())
        self.ATM_1FP = list(
            dict(df[df.eq("NIFTY" + self.FOR_YEAR_MONTH_DATEP + str(Find_Value + 50)).any(1)]['Token']).values())
        self.ATM_2FP = list(
            dict(df[df.eq("NIFTY" + self.FOR_YEAR_MONTH_DATEP + str(Find_Value + 100)).any(1)]['Token']).values())
        # BANKNIFTY
        testdate = datetime.now()
        weekly_thursday = []
        market_last = [week for week in calendar.monthcalendar(testdate.year, testdate.month) if
                       week[3] != 0 and weekly_thursday.append(week[3])]
        self.BCUR_Year_Month_DATE = str(str((weekly_thursday[-1]))) + datetime.strptime(
            str(int(datetime.now().strftime("%m"))), "%m").strftime("%b").upper() + datetime.now().strftime(
            "%y").upper() + "C"
        self.BCur_Future = list(dict(df[df.eq("BANKNIFTY" + str(weekly_thursday[-1]) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + self.next), "%m").strftime("%b").upper() + datetime.now().strftime(
            "%y").upper() + 'F').any(1)]['Token']).values())
        if list(dict(df[df.eq("BANKNIFTY" + self.CUR_Year_Month_DATE + str(Bfind_Value - 100)).any(1)][
                         'Token']).values()) == []:
            self.BCUR_Year_Month_DATE = str(str((weekly_thursday[-1] - 1))) + datetime.strptime(
                str(int(datetime.now().strftime("%m"))), "%m").strftime("%b").upper() + datetime.now().strftime(
                "%y").upper() + "C"
            self.BCur_Future = list(dict(df[df.eq("BANKNIFTY" + str(weekly_thursday[-1] - 1) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + 'F').any(1)]['Token']).values())
        else:
            pass
        self.BATM_4CC = list(
            dict(df[df.eq("BANKNIFTY" + self.BCUR_Year_Month_DATE + str(Bfind_Value - 200)).any(1)]['Token']).values())
        self.BATM_3CC = list(
            dict(df[df.eq("BANKNIFTY" + self.BCUR_Year_Month_DATE + str(Bfind_Value - 100)).any(1)]['Token']).values())
        self.BATM_CC = list(
            dict(df[df.eq("BANKNIFTY" + self.BCUR_Year_Month_DATE + str(Bfind_Value)).any(1)]['Token']).values())
        self.BATM_1CC = list(
            dict(df[df.eq("BANKNIFTY" + self.BCUR_Year_Month_DATE + str(Bfind_Value + 100)).any(1)]['Token']).values())
        self.BATM_2CC = list(
            dict(df[df.eq("BANKNIFTY" + self.BCUR_Year_Month_DATE + str(Bfind_Value + 200)).any(1)]['Token']).values())
        # Near Month Call Values
        testdate = datetime.now()
        weekly_thursday = []
        market_last = [week for week in calendar.monthcalendar(testdate.year, testdate.month + 1) if
                       week[3] != 0 and weekly_thursday.append(week[3])]
        self.BNEAR_Year_Month_DATE = str(str(weekly_thursday[-1])) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + 1 + self.next), "%m").strftime(
            "%b").upper() + datetime.now().strftime("%y").upper() + "C"
        self.BNear_Future = list(dict(df[df.eq("BANKNIFTY" + str(weekly_thursday[-1]) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + 1 + self.next), "%m").strftime(
            "%b").upper() + datetime.now().strftime("%y").upper() + 'F').any(1)]['Token']).values())
        if list(dict(df[df.eq("BANKNIFTY" + self.BNEAR_Year_Month_DATE + str(Bfind_Value - 100)).any(1)][
                         'Token']).values()) == []:
            self.BNEAR_Year_Month_DATE = str(str(weekly_thursday[-1] - 1)) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + 1 + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + "C"
            self.BNear_Future = list(dict(df[df.eq("BANKNIFTY" + str(weekly_thursday[-1]) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + 1 + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + 'F').any(1)]['Token']).values())
        else:
            pass
        self.BATM_4NC = list(
            dict(df[df.eq("BANKNIFTY" + self.BNEAR_Year_Month_DATE + str(Bfind_Value - 200)).any(1)]['Token']).values())
        self.BATM_3NC = list(
            dict(df[df.eq("BANKNIFTY" + self.BNEAR_Year_Month_DATE + str(Bfind_Value - 100)).any(1)]['Token']).values())
        self.BATM_NC = list(
            dict(df[df.eq("BANKNIFTY" + self.BNEAR_Year_Month_DATE + str(Bfind_Value)).any(1)]['Token']).values())
        self.BATM_1NC = list(
            dict(df[df.eq("BANKNIFTY" + self.BNEAR_Year_Month_DATE + str(Bfind_Value + 100)).any(1)]['Token']).values())
        self.BATM_2NC = list(
            dict(df[df.eq("BANKNIFTY" + self.BNEAR_Year_Month_DATE + str(Bfind_Value + 200)).any(1)]['Token']).values())
        # For Month Call Values
        testdate = datetime.now()
        weekly_thursday = []
        market_last = [week for week in calendar.monthcalendar(testdate.year, testdate.month + 2) if
                       week[3] != 0 and weekly_thursday.append(week[3])]
        self.BFar_Future = list(dict(df[df.eq("BANKNIFTY" + str(weekly_thursday[-1]) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + 2 + self.next), "%m").strftime(
            "%b").upper() + datetime.now().strftime("%y").upper() + 'F').any(1)]['Token']).values())
        self.BFOR_YEAR_MONTH_DATE = str(str(weekly_thursday[-1])) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + 2 + self.next), "%m").strftime(
            "%b").upper() + datetime.now().strftime("%y").upper() + "C"
        if list(dict(df[df.eq("BANKNIFTY" + self.BFOR_YEAR_MONTH_DATE + str(Bfind_Value - 100)).any(1)][
                         'Token']).values()) == []:
            self.BFOR_YEAR_MONTH_DATE = str(str(weekly_thursday[-1] - 1)) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + 2 + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + "C"
            self.Future_BFar = list(dict(df[df.eq("BANKNIFTY" + str(weekly_thursday[-1]) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + 2 + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + 'F').any(1)]['Token']).values())
        else:
            pass
        self.BATM_4FC = list(
            dict(df[df.eq("BANKNIFTY" + self.BFOR_YEAR_MONTH_DATE + str(Bfind_Value - 200)).any(1)]['Token']).values())
        self.BATM_3FC = list(
            dict(df[df.eq("BANKNIFTY" + self.BFOR_YEAR_MONTH_DATE + str(Bfind_Value - 100)).any(1)]['Token']).values())
        self.BATM_FC = list(
            dict(df[df.eq("BANKNIFTY" + self.BFOR_YEAR_MONTH_DATE + str(Bfind_Value)).any(1)]['Token']).values())
        self.BATM_1FC = list(
            dict(df[df.eq("BANKNIFTY" + self.BFOR_YEAR_MONTH_DATE + str(Bfind_Value + 100)).any(1)]['Token']).values())
        self.BATM_2FC = list(
            dict(df[df.eq("BANKNIFTY" + self.BFOR_YEAR_MONTH_DATE + str(Bfind_Value + 200)).any(1)]['Token']).values())
        # *******Puts Values Token Find******
        # Current Month
        testdate = datetime.now()
        weekly_thursday = []
        market_last = [week for week in calendar.monthcalendar(testdate.year, testdate.month) if
                       week[3] != 0 and weekly_thursday.append(week[3])]
        self.BCUR_Year_Month_DATEP = str(str((weekly_thursday[-1]))) + datetime.strptime(
            str(int(datetime.now().strftime("%m"))), "%m").strftime("%b").upper() + datetime.now().strftime(
            "%y").upper() + "P"
        if list(dict(df[df.eq("BANKNIFTY" + self.BCUR_Year_Month_DATEP + str(Bfind_Value - 100)).any(1)][
                         'Token']).values()) == []:
            self.BCUR_Year_Month_DATEP = str(str((weekly_thursday[-1] - 1))) + datetime.strptime(
                str(int(datetime.now().strftime("%m"))), "%m").strftime("%b").upper() + datetime.now().strftime(
                "%y").upper() + "P"
        else:
            pass
        self.BATM_4CP = list(
            dict(df[df.eq("BANKNIFTY" + self.BCUR_Year_Month_DATEP + str(Bfind_Value - 200)).any(1)]['Token']).values())
        self.BATM_3CP = list(
            dict(df[df.eq("BANKNIFTY" + self.BCUR_Year_Month_DATEP + str(Bfind_Value - 100)).any(1)]['Token']).values())
        self.BATM_CP = list(
            dict(df[df.eq("BANKNIFTY" + self.BCUR_Year_Month_DATEP + str(Bfind_Value)).any(1)]['Token']).values())
        self.BATM_1CP = list(
            dict(df[df.eq("BANKNIFTY" + self.BCUR_Year_Month_DATEP + str(Bfind_Value + 100)).any(1)]['Token']).values())
        self.BATM_2CP = list(
            dict(df[df.eq("BANKNIFTY" + self.BCUR_Year_Month_DATEP + str(Bfind_Value + 200)).any(1)]['Token']).values())

        # Near Month Puts Values
        testdate = datetime.now()
        weekly_thursday = []
        market_last = [week for week in calendar.monthcalendar(testdate.year, testdate.month + 1) if
                       week[3] != 0 and weekly_thursday.append(week[3])]
        self.BNEAR_Year_Month_DATEP = str(str(weekly_thursday[-1])) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + 1 + self.next), "%m").strftime(
            "%b").upper() + datetime.now().strftime("%y").upper() + "P"
        if list(dict(df[df.eq("BANKNIFTY" + self.BNEAR_Year_Month_DATEP + str(Bfind_Value - 100)).any(1)][
                         'Token']).values()) == []:
            self.BNEAR_Year_Month_DATEP = str(str(weekly_thursday[-1])) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + 1 + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + "P"
        else:
            pass
        self.BATM_4NP = list(dict(
            df[df.eq("BANKNIFTY" + self.BNEAR_Year_Month_DATEP + str(Bfind_Value - 200)).any(1)]['Token']).values())
        self.BATM_3NP = list(dict(
            df[df.eq("BANKNIFTY" + self.BNEAR_Year_Month_DATEP + str(Bfind_Value - 100)).any(1)]['Token']).values())
        self.BATM_NP = list(
            dict(df[df.eq("BANKNIFTY" + self.BNEAR_Year_Month_DATEP + str(Bfind_Value)).any(1)]['Token']).values())
        self.BATM_1NP = list(dict(
            df[df.eq("BANKNIFTY" + self.BNEAR_Year_Month_DATEP + str(Bfind_Value + 100)).any(1)]['Token']).values())
        self.BATM_2NP = list(dict(
            df[df.eq("BANKNIFTY" + self.BNEAR_Year_Month_DATEP + str(Bfind_Value + 200)).any(1)]['Token']).values())

        # For Month Puts Values
        testdate = datetime.now()
        weekly_thursday = []
        market_last = [week for week in calendar.monthcalendar(testdate.year, testdate.month + 2) if
                       week[3] != 0 and weekly_thursday.append(week[3])]
        self.BFOR_YEAR_MONTH_DATEP = str(str(weekly_thursday[-1])) + datetime.strptime(
            str(int(datetime.now().strftime("%m")) + 2 + self.next), "%m").strftime(
            "%b").upper() + datetime.now().strftime("%y").upper() + "P"
        if list(dict(df[df.eq("BANKNIFTY" + self.BFOR_YEAR_MONTH_DATEP + str(Bfind_Value - 100)).any(1)][
                         'Token']).values()) == []:
            self.BFOR_YEAR_MONTH_DATEP = str(str(weekly_thursday[-1] - 1)) + datetime.strptime(
                str(int(datetime.now().strftime("%m")) + 2 + self.next), "%m").strftime(
                "%b").upper() + datetime.now().strftime("%y").upper() + "P"
        else:
            pass
        self.BATM_4FP = list(
            dict(df[df.eq("BANKNIFTY" + self.BFOR_YEAR_MONTH_DATEP + str(Bfind_Value - 200)).any(1)]['Token']).values())
        self.BATM_3FP = list(
            dict(df[df.eq("BANKNIFTY" + self.BFOR_YEAR_MONTH_DATEP + str(Bfind_Value - 100)).any(1)]['Token']).values())
        self.BATM_FP = list(
            dict(df[df.eq("BANKNIFTY" + self.BFOR_YEAR_MONTH_DATEP + str(Bfind_Value)).any(1)]['Token']).values())
        self.BATM_1FP = list(
            dict(df[df.eq("BANKNIFTY" + self.BFOR_YEAR_MONTH_DATEP + str(Bfind_Value + 100)).any(1)]['Token']).values())
        self.BATM_2FP = list(
            dict(df[df.eq("BANKNIFTY" + self.BFOR_YEAR_MONTH_DATEP + str(Bfind_Value + 200)).any(1)]['Token']).values())
        lst=[self.Cur_Future,self.Near_Future,self.Far_Future,self.BCur_Future,self.BNear_Future,self.BFar_Future,self.ATM_4CC,self.ATM_3CC,self.ATM_CC,self.ATM_2CC,self.ATM_1CC,self.ATM_4CP,self.ATM_3CP,self.ATM_CP,self.ATM_2CP,self.ATM_1CP,self.ATM_4NC,self.ATM_3NC,self.ATM_NC,self.ATM_2NC,self.ATM_1NC,self.ATM_4NP,self.ATM_3NP,self.ATM_NP,self.ATM_2NP,self.ATM_1NP,self.ATM_4FC,self.ATM_3FC,self.ATM_FC,self.ATM_2FC,self.ATM_1FC,self.ATM_4FP,self.ATM_3FP,self.ATM_FP,self.ATM_2FP,self.ATM_1FP,self.BATM_4CC,self.BATM_3CC,self.BATM_CC,self.BATM_2CC,self.BATM_1CC,self.BATM_4CP,self.BATM_3CP,self.BATM_CP,self.BATM_2CP,self.BATM_1CP,self.BATM_4NC,self.BATM_3NC,self.BATM_NC,self.BATM_2NC,self.BATM_1NC,self.BATM_4NP,self.BATM_3NP,self.BATM_NP,self.BATM_2NP,self.BATM_1NP,self.BATM_4FC,self.BATM_3FC,self.BATM_FC,self.BATM_2FC,self.BATM_1FC,self.BATM_4FP,self.BATM_3FP,self.BATM_FP,self.BATM_2FP,self.BATM_1FP]
        for i in lst:
            try:
                getMultiQuotesLTP = thefirstock.firstock_getMultiQuoteLTP(dataToken=[{"exchange": "NFO","token": str(i[0])}])
                token = getMultiQuotesLTP["data"][0]['token']
                ltp = int(float(getMultiQuotesLTP['data'][0]['result']['lastTradedPrice']))
            except:
                pass
            print(ltp)
            #NIFTY
            ttk.Label(self.second_frame, width=15, text=self.spot).grid(column=4, row=3, sticky="EW", padx=2, pady=1)
            ttk.Label(self.second_frame, width=15, text=self.spot).grid(column=4, row=10, sticky="EW", padx=2, pady=1)
            ttk.Label(self.second_frame, width=15, text=self.spot).grid(column=4, row=17, sticky="EW", padx=2, pady=1)
            #BANKNIFTY
            ttk.Label(self.second_frame, width=15, text=self.bspot).grid(column=4, row=25, sticky="EW", padx=2, pady=1)
            ttk.Label(self.second_frame, width=15, text=self.bspot).grid(column=4, row=32, sticky="EW", padx=2, pady=1)
            ttk.Label(self.second_frame, width=15, text=self.bspot).grid(column=4, row=39, sticky="EW", padx=2, pady=1)
            # Future values
            if token== str(self.Cur_Future[0]):
                self.Future_Cur = ltp
                ttk.Label(self.second_frame, width=15, text=self.Future_Cur).grid(column=6, row=3, sticky="EW", padx=2, pady=1)
            elif token== str(self.Near_Future[0]):
                self.Future_Near = ltp
                ttk.Label(self.second_frame, width=15, text=self.Future_Near).grid(column=6, row=10, sticky="EW", padx=2,pady=1)
            elif token== str(self.Far_Future[0]):
                self.Future_Far = ltp
                ttk.Label(self.second_frame, width=15, text=self.Future_Far).grid(column=6, row=17, sticky="EW", padx=2,pady=1)
            elif token== str(self.BCur_Future[0]):
                self.Future_BCur = ltp
                ttk.Label(self.second_frame, width=15, text=self.Future_BCur).grid(column=6, row=25, sticky="EW", padx=2,pady=1)
            elif token== str(self.BNear_Future[0]):
                self.Future_BNear = ltp
                ttk.Label(self.second_frame, width=15, text=self.Future_BNear).grid(column=6, row=32, sticky="EW", padx=2,pady=1)
            elif token== str(self.BFar_Future[0]):
                self.Future_BFar = ltp
                ttk.Label(self.second_frame, width=15, text=self.Future_BFar).grid(column=6, row=39, sticky="EW", padx=2,pady=1)
            elif token== str(self.ATM_4CC[0]):
                self.ATM_4CC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_4CC_1,background='yellow').grid(column=16, row=3, sticky="EW", padx=2, pady=1)
                time.sleep(0.5)
                ttk.Label(self.second_frame, width=15, text=self.ATM_4CC_1).grid(column=16, row=3,sticky="EW",padx=2, pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_4CC_1 + self.spot).grid(column=16, row=5, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.ATM_4CP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Cur + self.ATM_4CP_1) - (self.spot + self.ATM_4CC_1)).grid(column=16,row=7,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_3CC[0]):
                self.ATM_3CC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_3CC_1).grid(column=14, row=3, sticky="EW", padx=2, pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_3CC_1 + self.spot).grid(column=14, row=5, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.ATM_3CP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Cur + self.ATM_3CP_1) - (self.spot + self.ATM_3CC_1)).grid(column=14,row=7,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_CC[0]):
                self.ATM_CC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_CC_1).grid(column=12, row=3, sticky="EW", padx=2, pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_CC_1 + self.spot).grid(column=12, row=5, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.ATM_CP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Cur + self.ATM_CP_1) - (self.spot + self.ATM_CC_1)).grid(column=12,row=7,sticky="EW",padx=2, pady=1)
                else:
                    pass
            elif token== str(self.ATM_1CC[0]):
                self.ATM_1CC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_1CC_1).grid(column=10, row=3, sticky="EW", padx=2, pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_1CC_1 + self.spot).grid(column=10, row=5, sticky="EW",               padx=2, pady=1)
                else:
                    pass
                if self.ATM_1CP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Cur + self.ATM_1CP_1) - (self.spot + self.ATM_1CC_1)).grid(column=10,row=7,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_2CC[0]):
                self.ATM_2CC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_2CC_1).grid(column=8, row=3, sticky="EW", padx=2, pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_2CC_1 + self.spot).grid(column=8, row=5, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.ATM_2CP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Cur + self.ATM_2CP_1) - (self.spot + self.ATM_2CC_1)).grid(column=8,row=7,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_4CP[0]):
                self.ATM_4CP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_4CP_1).grid(column=26, row=3, sticky="EW", padx=2, pady=1)
                if self.Future_Cur:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_4CP_1 + self.Future_Cur).grid(column=26, row=5,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.ATM_4CC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Cur + self.ATM_4CP_1) - (self.spot + self.ATM_4CC_1)).grid(column=16,row=7,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_3CP[0]):
                self.ATM_3CP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_3CP_1).grid(column=24, row=3, sticky="EW", padx=2, pady=1)
                if self.Future_Cur:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_3CP_1 + self.Future_Cur).grid(column=24, row=5,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.ATM_3CC_1:
                    ttk.Label(self.second_frame, width=15,
                              text=(self.Future_Cur + self.ATM_3CP_1) - (self.spot + self.ATM_3CC_1)).grid(column=14,row=7,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_CP[0]):
                self.ATM_CP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_CP_1).grid(column=22, row=3, sticky="EW", padx=2, pady=1)
                if self.Future_Cur:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_CP_1 + self.Future_Cur).grid(column=22, row=5,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.ATM_CC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Cur + self.ATM_CP_1) - (self.spot + self.ATM_CC_1)).grid(column=12,         row=7,         sticky="EW",         padx=2, pady=1)
                else:
                    pass
            elif token== str(self.ATM_1CP[0]):
                self.ATM_1CP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_1CP_1).grid(column=20, row=3, sticky="EW", padx=2, pady=1)
                if self.Future_Cur:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_1CP_1 + self.Future_Cur).grid(column=20, row=5,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.ATM_1CC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Cur + self.ATM_1CP_1) - (self.spot + self.ATM_1CC_1)).grid(column=10,row=7,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_2CP[0]):
                self.ATM_2CP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_2CP_1).grid(column=18, row=3, sticky="EW", padx=2, pady=1)
                if self.Future_Cur:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_2CP_1 + self.Future_Cur).grid(column=18, row=5,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.ATM_2CC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Cur + self.ATM_2CP_1) - (self.spot + self.ATM_2CC_1)).grid(column=8,row=7,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_4NC[0]):
                self.ATM_4NC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_4NC_1).grid(column=16, row=10, sticky="EW", padx=2,pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_4NC_1 + self.spot).grid(column=16, row=12,sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.ATM_4NP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Near + self.ATM_4NP_1) - (self.spot + self.ATM_4NC_1)).grid(column=16, row=14, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.ATM_3NC[0]):
                self.ATM_3NC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_3NC_1).grid(column=14, row=10, sticky="EW", padx=2,pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_3NC_1 + self.spot).grid(column=14, row=12,sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.ATM_3NP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Near + self.ATM_3NP_1) - (self.spot + self.ATM_3NC_1)).grid(column=14, row=14, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.ATM_NC[0]):
                self.ATM_NC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_NC_1).grid(column=12, row=10, sticky="EW", padx=2, pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_NC_1 + self.spot).grid(column=12, row=12, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.ATM_NP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Near + self.ATM_NP_1) - (self.spot + self.ATM_NC_1)).grid(column=12,          row=14,          sticky="EW",          padx=2,          pady=1)
                else:
                    pass
            elif token== str(self.ATM_1NC[0]):
                self.ATM_1NC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_1NC_1).grid(column=10, row=10, sticky="EW", padx=2,pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_1NC_1 + self.spot).grid(column=10, row=12,sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.ATM_1NP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Near + self.ATM_1NP_1) - (self.spot + self.ATM_1NC_1)).grid(column=10, row=14, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.ATM_2NC[0]):
                self.ATM_2NC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_2NC_1).grid(column=8, row=10, sticky="EW", padx=2, pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_2NC_1 + self.spot).grid(column=8, row=12, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.ATM_2NP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Near + self.ATM_2NP_1) - (self.spot + self.ATM_2NC_1)).grid(column=8, row=14, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.ATM_4NP[0]):
                self.ATM_4NP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_4NP_1).grid(column=26, row=10, sticky="EW", padx=2,pady=1)
                if self.Future_Near:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_4NP_1 + self.Future_Near).grid(column=26, row=12, sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.ATM_4NC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Near + self.ATM_4NP_1) - (self.spot + self.ATM_4NC_1)).grid(column=16, row=14, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.ATM_3NP[0]):
                self.ATM_3NP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_3NP_1).grid(column=24, row=10, sticky="EW", padx=2,pady=1)
                if self.Future_Near:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_3NP_1 + self.Future_Near).grid(column=24, row=12, sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.ATM_3NC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Near + self.ATM_3NP_1) - (self.spot + self.ATM_3NC_1)).grid(column=14, row=14, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.ATM_NP[0]):
                self.ATM_NP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_NP_1).grid(column=22, row=10, sticky="EW", padx=2, pady=1)
                if self.Future_Near:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_NP_1 + self.Future_Near).grid(column=22, row=12,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.ATM_NC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Near + self.ATM_NP_1) - (self.spot + self.ATM_NC_1)).grid(column=12,          row=14,          sticky="EW",          padx=2,          pady=1)
                else:
                    pass
            elif token== str(self.ATM_1NP[0]):
                self.ATM_1NP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_1NP_1).grid(column=20, row=10, sticky="EW", padx=2,pady=1)
                if self.Future_Near:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_1NP_1 + self.Future_Near).grid(column=20, row=12, sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.ATM_1NC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Near + self.ATM_1NP_1) - (self.spot + self.ATM_1NC_1)).grid(column=10, row=14, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.ATM_2NP[0]):
                self.ATM_2NP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_2NP_1).grid(column=18, row=10, sticky="EW", padx=2,pady=1)
                if self.Future_Near:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_2NP_1 + self.Future_Near).grid(column=18, row=12, sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.ATM_2NC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Near + self.ATM_2NP_1) - (self.spot + self.ATM_2NC_1)).grid(column=8, row=14, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.ATM_4FC[0]):
                self.ATM_4FC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_4FC_1).grid(column=16, row=17, sticky="EW", padx=2,pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_4FC_1 + self.spot).grid(column=16, row=19,sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.ATM_4FC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Far + self.ATM_4FP_1) - (self.spot + self.ATM_4FC_1)).grid(column=16,row=21,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_3FC[0]):
                self.ATM_3FC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_3FC_1).grid(column=14, row=17, sticky="EW", padx=2,pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_3FC_1 + self.spot).grid(column=14, row=19,sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.ATM_3FP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Far + self.ATM_3FP_1) - (self.spot + self.ATM_3FC_1)).grid(column=14,row=21,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_FC[0]):
                self.ATM_FC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_FC_1).grid(column=12, row=17, sticky="EW", padx=2, pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_FC_1 + self.spot).grid(column=12, row=19, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.ATM_FP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Far + self.ATM_FP_1) - (self.spot + self.ATM_FC_1)).grid(column=12,row=21,sticky="EW",padx=2, pady=1)
                else:
                    pass
            elif token== str(self.ATM_1FC[0]):
                self.ATM_1FC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_1FC_1).grid(column=10, row=17, sticky="EW", padx=2,pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_1FC_1 + self.spot).grid(column=10, row=19,sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.ATM_1FP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Far + self.ATM_1FP_1) - (self.spot + self.ATM_1FC_1)).grid(column=10,row=21,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_2FC[0]):
                self.ATM_2FC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_2FC_1).grid(column=8, row=17, sticky="EW", padx=2, pady=1)
                if self.spot:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_2FC_1 + self.spot).grid(column=8, row=19, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.ATM_2FP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Far + self.ATM_2FP_1) - (self.spot + self.ATM_2FC_1)).grid(column=8,row=21,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_4FP[0]):
                self.ATM_4FP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_4FP_1).grid(column=26, row=17, sticky="EW", padx=2,pady=1)
                if self.Future_Far:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_4FP_1 + self.Future_Far).grid(column=26, row=19,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.ATM_4FC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Far + self.ATM_4FP_1) - (self.spot + self.ATM_4FC_1)).grid(column=16,row=21,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_3FP[0]):
                self.ATM_3FP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_3FP_1).grid(column=24, row=17, sticky="EW", padx=2,pady=1)
                if self.Future_Far:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_3FP_1 + self.Future_Far).grid(column=24, row=19,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.ATM_3FC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Far + self.ATM_3FP_1) - (self.spot + self.ATM_3FC_1)).grid(column=14,row=21,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.ATM_FP[0]):
                self.ATM_FP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_FP_1).grid(column=22, row=17, sticky="EW", padx=2, pady=1)
                if self.Future_Far:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_FP_1 + self.Future_Far).grid(column=22, row=19,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.ATM_FC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Far + self.ATM_FP_1) - (self.spot + self.ATM_FC_1)).grid(column=12,row=21,sticky="EW",padx=2, pady=1)
                else:
                    pass
            elif token== str(self.ATM_1FP[0]):
                self.ATM_1FP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_1FP_1).grid(column=20, row=17, sticky="EW", padx=2,pady=1)
                if self.Future_Far:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_1FP_1 + self.Future_Far).grid(column=20, row=19,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.ATM_1FC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Far + self.ATM_1FP_1) - (self.spot + self.ATM_1FC_1)).grid(column=10,row=21,sticky="EW",padx=2,pady=1)

                else:
                    pass
            elif token== str(self.ATM_2FP[0]):
                self.ATM_2FP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.ATM_2FP_1).grid(column=18, row=17, sticky="EW", padx=2,pady=1)
                if self.Future_Far:
                    ttk.Label(self.second_frame, width=15, text=self.ATM_2FP_1 + self.Future_Far).grid(column=18, row=19,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.ATM_2FC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_Far + self.ATM_2FP_1) - (self.spot + self.ATM_2FC_1)).grid(column=8,row=21,sticky="EW",padx=2,pady=1)
                else:
                    pass
            # #BANKNIFTY
            # Call Value far current month
            elif token== str(self.BATM_4CC[0]):
                self.BATM_4CC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_4CC_1).grid(column=16, row=25, sticky="EW", padx=2,pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.spot + self.BATM_4CC_1).grid(column=16, row=27, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_4CP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BCur + self.BATM_4CP_1) - (self.bspot + self.BATM_4CC_1)).grid(column=16,row=29,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.BATM_3CC[0]):
                self.BATM_3CC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_3CC_1).grid(column=14, row=25, sticky="EW", padx=2,pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.spot + self.BATM_3CC_1).grid(column=14, row=27, sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.BATM_3CP_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BCur + self.BATM_3CP_1) - (self.bspot + self.BATM_3CC_1)).grid(column=14, row=29, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_CC[0]):
                self.BATM_CC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_CC_1).grid(column=12, row=25, sticky="EW", padx=2,pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_CC_1).grid(column=12, row=27, sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.BATM_CP_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BCur + self.BATM_CP_1) - (self.bspot + self.BATM_CC_1)).grid(column=12,row=29,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.BATM_1CC[0]):
                self.BATM_1CC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_1CC_1).grid(column=10, row=25, sticky="EW", padx=2,pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_1CC_1).grid(column=10, row=27, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_1CP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BCur + self.BATM_1CP_1) - (self.bspot + self.BATM_1CC_1)).grid(column=10, row=29,sticky="EW",padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_2CC[0]):
                self.BATM_2CC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_2CC_1).grid(column=8, row=25, sticky="EW", padx=2,pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_2CC_1).grid(column=8, row=27, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_2CP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BCur + self.BATM_2CP_1) - (self.bspot + self.BATM_2CC_1)).grid(column=8, row=29,sticky="EW",padx=2, pady=1)
                else:
                    pass
            # Puts Value far current month
            elif token== str(self.BATM_4CP[0]):
                self.BATM_4CP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_4CP_1).grid(column=26, row=25, sticky="EW", padx=2,pady=1)
                if self.Future_BCur:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BCur + self.BATM_4CP_1).grid(column=26, row=27,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.BATM_4CC_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BCur + self.BATM_4CP_1) - (self.bspot + self.BATM_4CC_1)).grid(column=16, row=29, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_3CP[0]):
                self.BATM_3CP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_3CP_1).grid(column=24, row=25, sticky="EW", padx=2,pady=1)
                if self.Future_BCur:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BCur + self.BATM_3CP_1).grid(column=24, row=27, sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.BATM_3CC_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BCur + self.BATM_3CP_1) - (self.bspot + self.BATM_3CC_1)).grid(column=14, row=29, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_CP[0]):
                self.BATM_CP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_CP_1).grid(column=22, row=25, sticky="EW", padx=2,pady=1)
                if self.Future_BCur:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BCur + self.BATM_CP_1).grid(column=22, row=27, sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.BATM_CC_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BCur + self.BATM_CP_1) - (self.bspot + self.BATM_CC_1)).grid(column=12, row=29, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_1CP[0]):
                self.BATM_1CP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_1CP_1).grid(column=20, row=25, sticky="EW", padx=2,pady=1)
                if self.Future_BCur:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BCur + self.BATM_1CP_1).grid(column=20, row=27, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_1CC_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BCur + self.BATM_1CP_1) - (self.bspot + self.BATM_1CC_1)).grid(column=10, row=29, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_2CP[0]):
                self.BATM_2CP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_2CP_1).grid(column=18, row=25, sticky="EW", padx=2,pady=1)
                if self.Future_BCur:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BCur + self.BATM_2CP_1).grid(column=18, row=27,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.BATM_2CC_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BCur + self.BATM_2CP_1) - (self.bspot + self.BATM_2CC_1)).grid(column=8, row=29, sticky="EW", padx=2, pady=1)
                else:
                    pass
            #CALL VALUE
            elif token== str(self.BATM_4NC[0]):
                self.BATM_4NC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_4NC_1).grid(column=16, row=32, sticky="EW", padx=2, pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_4NC_1).grid(column=16, row=34, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_4NP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BNear + self.BATM_4NP_1) - (self.bspot + self.BATM_4NC_1)).grid(column=16,row=36,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.BATM_3NC[0]):
                self.BATM_3NC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_3NC_1).grid(column=14, row=32, sticky="EW", padx=2, pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_3NC_1).grid(column=14, row=34, sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.BATM_3NP_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BNear + self.BATM_3NP_1) - (self.bspot + self.BATM_3NC_1)).grid(column=14, row=36, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_NC[0]):
                self.BATM_NC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_NC_1).grid(column=12, row=32, sticky="EW", padx=2, pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_NC_1).grid(column=12, row=34, sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.BATM_NP_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BNear + self.BATM_NP_1) - (self.bspot + self.BATM_NC_1)).grid(column=12,row=36,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.BATM_1NC[0]):
                self.BATM_1NC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_1NC_1).grid(column=10, row=32, sticky="EW", padx=2, pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_1NC_1).grid(column=10, row=34, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_1NP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BNear + self.BATM_1NP_1) - (self.bspot + self.BATM_1NC_1)).grid(column=10, row=36,sticky="EW",padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_2NC[0]):
                self.BATM_2NC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_2NC_1).grid(column=8, row=32, sticky="EW", padx=2,pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_2NC_1).grid(column=8, row=34,sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.BATM_2NP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BNear + self.BATM_2NP_1) - (self.bspot + self.BATM_2NC_1)).grid(column=8, row=36,sticky="EW",padx=2, pady=1)
                else:
                    pass
            # Puts Value
            elif token== str(self.BATM_4NP[0]):
                self.BATM_4NP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_4NP_1).grid(column=26, row=32, sticky="EW", padx=2,pady=1)
                if self.Future_BNear:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BNear + self.BATM_4NP_1).grid(column=18, row=34, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_4NC_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BNear + self.BATM_4NP_1) - (self.bspot + self.BATM_4NC_1)).grid(column=16, row=36, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_3NP[0]):
                self.BATM_3NP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_3NP_1).grid(column=24, row=32, sticky="EW", padx=2,pady=1)
                if self.Future_BNear:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BNear + self.BATM_3NP_1).grid(column=20, row=34, sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.BATM_3NP_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BNear + self.BATM_3NP_1) - (self.bspot + self.BATM_3NC_1)).grid(column=14, row=36, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_NP[0]):
                self.BATM_NP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_NP_1).grid(column=22, row=32, sticky="EW", padx=2,pady=1)
                if self.Future_BNear:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BNear + self.BATM_NCP_1).grid(column=22, row=34, sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.BATM_NC_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BNear + self.BATM_NP_1) - (self.bspot + self.BATM_NC_1)).grid(column=12, row=36, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_1NP[0]):
                self.BATM_1NP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_1NP_1).grid(column=20, row=32, sticky="EW", padx=2,pady=1)
                if self.Future_BNear:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BNear + self.BATM_1NP_1).grid(column=24, row=34, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_1NC_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BNear + self.BATM_1NP_1) - (self.bspot + self.BATM_1NC_1)).grid(column=10, row=36, sticky="EW", padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_2NP[0]):
                self.BATM_2NP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_2NP_1).grid(column=18, row=32, sticky="EW", padx=2,pady=1)
                if self.Future_BNear:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BNear + self.BATM_2NP_1).grid(column=26, row=34,sticky="EW", padx=2, pady=1)
                else:
                    pass
                if self.BATM_2NC_1:
                    ttk.Label(self.second_frame, width=15, text=(self.Future_BNear + self.BATM_2NP_1) - (self.bspot + self.BATM_2NC_1)).grid(column=8, row=36, sticky="EW", padx=2, pady=1)
                else:
                    pass
            #FUTURE VALUE
            # Call Value
            elif token== str(self.BATM_4FC[0]):
                self.BATM_4FC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_4FC_1).grid(column=16, row=39, sticky="EW", padx=2,pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_4FC_1).grid(column=16, row=42, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_4FP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BFar + self.BATM_4FP_1) - (self.bspot + self.BATM_4FC_1)).grid(column=16,row=44,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.BATM_3FC[0]):
                self.BATM_3FC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_3FC_1).grid(column=14, row=39, sticky="EW", padx=2,pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_3FC_1).grid(column=14, row=42, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_3FP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BFar + self.BATM_3FP_1) - (self.bspot + self.BATM_3FC_1)).grid(column=14, row=44,sticky="EW",padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_FC[0]):
                self.BATM_FC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_FC_1).grid(column=12, row=39, sticky="EW", padx=2,pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_FC_1).grid(column=12, row=42, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_FP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BFar + self.BATM_FP_1) - (self.bspot + self.BATM_FC_1)).grid(column=12, row=44,sticky="EW", padx=2,pady=1)
                else:
                    pass
            elif token== str(self.BATM_1FC[0]):
                self.BATM_1FC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_1FC_1).grid(column=10, row=39, sticky="EW", padx=2,pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_1FC_1).grid(column=10, row=42, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_1FP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BFar + self.BATM_1FP_1) - (self.bspot + self.BATM_1FC_1)).grid(column=10, row=44,sticky="EW",padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_2FC[0]):
                self.BATM_2FC_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_2FC_1).grid(column=8, row=39, sticky="EW", padx=2,pady=1)
                if self.bspot:
                    ttk.Label(self.second_frame, width=15, text=self.bspot + self.BATM_2FC_1).grid(column=8, row=42, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_2FP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BFar + self.BATM_2FP_1) - (self.bspot + self.BATM_2FC_1)).grid(column=8,row=44,sticky="EW",padx=2,pady=1)
                else:
                    pass
            # Puts Value
            elif token== str(self.BATM_4FP[0]):
                self.BATM_4FP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_4FP_1).grid(column=26, row=39, sticky="EW", padx=2,pady=1)
                if self.Future_BFar:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BFar + self.BATM_4FP_1).grid(column=26, row=42,sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_4FC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BFar + self.BATM_4FP_1) - (self.bspot + self.BATM_4FC_1)).grid(column=16,row=44,sticky="EW",padx=2,pady=1)
                else:
                    pass
            elif token== str(self.BATM_3FP[0]):
                self.BATM_3FP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_3FP_1).grid(column=24, row=39, sticky="EW", padx=2, pady=1)
                if self.Future_BFar:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BFar + self.BATM_3FP_1).grid(column=24, row=42, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_3FP_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BFar + self.BATM_3FP_1) - (self.bspot + self.BATM_3FC_1)).grid(column=14, row=44,sticky="EW",padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_FP[0]):
                self.BATM_FP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_FP_1).grid(column=22, row=39, sticky="EW", padx=2, pady=1)
                if self.Future_BFar:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BFar + self.BATM_FP_1).grid(column=22, row=42, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_FC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BFar + self.BATM_FP_1) - (self.bspot + self.BATM_FC_1)).grid(column=12, row=44,sticky="EW", padx=2,pady=1)
                else:
                    pass
            elif token== str(self.BATM_1FP[0]):
                self.BATM_1FP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_1FP_1).grid(column=20, row=39, sticky="EW", padx=2, pady=1)
                if self.Future_BFar:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BFar + self.BATM_1FP_1).grid(column=20, row=42, sticky="EW",padx=2, pady=1)
                else:
                    pass
                if self.BATM_1FC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BFar + self.BATM_1FP_1) - (self.bspot + self.BATM_1FC_1)).grid(column=10, row=44,sticky="EW",padx=2, pady=1)
                else:
                    pass
            elif token== str(self.BATM_2FP[0]):
                self.BATM_2FP_1 = ltp
                ttk.Label(self.second_frame, width=15, text=self.BATM_2FP_1).grid(column=18, row=39, sticky="EW", padx=2, pady=1)
                if self.Future_BFar:
                    ttk.Label(self.second_frame, width=15, text=self.Future_BFar + self.BATM_2FP_1).grid(column=18, row=42,sticky="EW", padx=2,pady=1)
                else:
                    pass
                if self.BATM_2FC_1:
                    ttk.Label(self.second_frame, width=15,text=(self.Future_BFar + self.BATM_2FP_1) - (self.bspot + self.BATM_2FC_1)).grid(column=8,row=44,sticky="EW",padx=2,pady=1)
                else:
                    pass
            else:
                pass
            time.sleep(0.3)
        self.root.after(20000,threading.Thread(target=self.Data_Upadting).start())
        self.root.after(20000, threading.Thread(target=self.Scheduled_DataSaving).start())
    def Scheduled_DataSaving(self):
        if self.stop_Thread.is_set():
            return
        def start_save():
            # Data_Saving
            self.Cdf1 = self.Cdf1._append(
                {'DATE_TIME':time.strftime("%d/%m/%Y-%H:%M:%S"),'Equities Derivatives': 'SCAFPA-Current',
                 'SCAFPA-2': (self.Future_Cur + self.ATM_2CP_1) - (self.spot + self.ATM_2CC_1),
                 'SCAFPA-1': (self.Future_Cur + self.ATM_1CP_1) - (self.spot + self.ATM_1CC_1),
                 'SCAFPA': (self.Future_Cur + self.ATM_CP_1) - (self.spot + self.ATM_CC_1),
                 'SCAFPA+1': (self.Future_Cur + self.ATM_3CP_1) - (self.spot + self.ATM_3CC_1),
                 'SCAFPA+2': (self.Future_Cur + self.ATM_4CP_1) - (self.spot + self.ATM_4CC_1)},ignore_index=True)
            self.Ndf1 =self.Ndf1._append(
                {'DATE_TIME': time.strftime("%d/%m/%Y-%H:%M:%S"),'Equities Derivatives': 'SCAFPA-Near',
                 'SCAFPA-2': (self.Future_Near + self.ATM_2NP_1) - (self.spot + self.ATM_2NC_1),
                 'SCAFPA-1': (self.Future_Near + self.ATM_1NP_1) - (self.spot + self.ATM_1NC_1),
                 'SCAFPA': (self.Future_Near + self.ATM_NP_1) - (self.spot + self.ATM_NC_1),
                 'SCAFPA+1': (self.Future_Near + self.ATM_3NP_1) - (self.spot + self.ATM_3NC_1),
                 'SCAFPA+2': (self.Future_Near + self.ATM_4NP_1) - (self.spot + self.ATM_4NC_1)},ignore_index=True)
            self.Fdf1 =self.Fdf1._append(
                {'DATE_TIME': time.strftime("%d/%m/%Y-%H:%M:%S"),'Equities Derivatives': 'SCAFPA-Far',
                 'SCAFPA-2': (self.Future_Far + self.ATM_2FP_1) - (self.spot + self.ATM_2FC_1),
                 'SCAFPA-1': (self.Future_Far + self.ATM_1FP_1) - (self.spot + self.ATM_1FC_1),
                 'SCAFPA': (self.Future_Far + self.ATM_FP_1) - (self.spot + self.ATM_FC_1),
                 'SCAFPA+1': (self.Future_Far + self.ATM_3FP_1) - (self.spot + self.ATM_3FC_1),
                 'SCAFPA+2': (self.Future_Far + self.ATM_4FP_1) - (self.spot + self.ATM_4FC_1)},ignore_index=True)
            df = (self.Cdf1, self.Ndf1, self.Fdf1)
            concat = pd.concat(df,ignore_index=True, sort=False)
            concat.to_csv(self.path + "\\Nifty_Data.csv")
            self.BCdf1 = self.BCdf1._append(
                {'DATE_TIME': time.strftime("%d/%m/%Y-%H:%M:%S"), 'Equities Derivatives': 'SCAFPA-Current',
                 'SCAFPA-2': (self.Future_BCur + self.BATM_2CP_1) - (self.bspot + self.BATM_2CC_1),
                 'SCAFPA-1': (self.Future_BCur + self.BATM_1CP_1) - (self.bspot + self.BATM_1CC_1),
                 'SCAFPA': (self.Future_BCur + self.BATM_CP_1) - (self.bspot + self.BATM_CC_1),
                 'SCAFPA+1': (self.Future_BCur + self.BATM_3CP_1) - (self.bspot + self.BATM_3CC_1),
                 'SCAFPA+2': (self.Future_BCur + self.BATM_4CP_1) - (self.bspot + self.BATM_4CC_1)}, ignore_index=True)
            self.BNdf1 = self.BNdf1._append(
                {'DATE_TIME': time.strftime("%d/%m/%Y-%H:%M:%S"),'Equities Derivatives': 'SCAFPA-Near',
                 'SCAFPA-2': (self.Future_BNear + self.BATM_2NP_1) - (self.bspot + self.BATM_2NC_1),
                 'SCAFPA-1': (self.Future_BNear + self.BATM_1NP_1) - (self.bspot + self.BATM_1NC_1),
                 'SCAFPA': (self.Future_BNear + self.BATM_NP_1) - (self.bspot + self.BATM_NC_1),
                 'SCAFPA+1': (self.Future_BNear + self.BATM_3NP_1) - (self.bspot + self.BATM_3NC_1),
                 'SCAFPA+2': (self.Future_BNear + self.BATM_4NP_1) - (self.bspot + self.BATM_4NC_1)}, ignore_index=True)
            self.BFdf1 = self.BFdf1._append(
                {'DATE_TIME': time.strftime("%d/%m/%Y-%H:%M:%S"),'Equities Derivatives': 'SCAFPA-Far',
                 'SCAFPA-2': (self.Future_BFar + self.BATM_2FP_1) - (self.bspot + self.BATM_2FC_1),
                 'SCAFPA-1': (self.Future_BFar + self.BATM_1FP_1) - (self.bspot + self.BATM_1FC_1),
                 'SCAFPA': (self.Future_BFar + self.BATM_FP_1) - (self.bspot + self.BATM_FC_1),
                 'SCAFPA+1': (self.Future_BFar + self.BATM_3FP_1) - (self.bspot + self.BATM_3FC_1),
                 'SCAFPA+2': (self.Future_BFar + self.BATM_4FP_1) - (self.bspot + self.BATM_4FC_1)}, ignore_index=True)

            Bdf = [self.BCdf1 ,self.BNdf1 ,self.BFdf1]
            concat1 = pd.concat(Bdf, ignore_index=True, sort=False)
            concat1.to_csv(self.path + "\\BANKNifty_Data.csv")
        schedule.every().day.at('09:30').do(start_save)
        schedule.every().day.at('12:30').do(start_save)
        schedule.every().day.at('01:30').do(start_save)
        schedule.every().day.at('03:30').do(start_save)
        try:
            schedule.every().day.at(self.hour+':'+self.minute).do(start_save)
        except:
            pass
        while True:
            if self.stop_Thread.is_set():
                return
            schedule.run_pending()
            time.sleep(1)

object=Smart_Analogy()
object.Firststock_login()
