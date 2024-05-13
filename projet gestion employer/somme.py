import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pandas as pd 

my_w = tk.Tk()
my_w.geometry("1200x700")  # Size of the window 
my_w.title('employer')
my_font1=('times', 18, 'bold')
l1 = tk.Label(my_w,text='Compter le temp et le jour de travail',width=90,font=my_font1)  
l1.grid(row=0,column=1)
b1 = tk.Button(my_w, text='Upload Excel File', width=20,command = lambda:upload_file())
b1.grid(row=1,column=1) 


t2 = tk.Text(my_w,height=1, width=20,bg='white') # added one text box
t2.grid(row=2,column=1) # 
t3 = tk.Text(my_w,height=1, width=20,bg='white') # added one text box
t3.grid(row=3,column=1) # 
t1 = tk.Text(my_w, height=35, width=140,bg='white') # added one text box
t1.grid(row=5,column=1,pady=10) # 
b2 = tk.Button(my_w, text='Upload  csv File', width=20,command = lambda:upload_csv())
b2.grid(row=4,column=1) 

def upload_file():
  global df
  file = filedialog.askopenfilename(filetypes=[("Excel file", ".xls"), ("Excel file", ".xlsx")])

  df = pd.read_excel(file ,engine='xlrd')
  if 'Présence réelle.' in df.columns:
    hour=sum(df['Présence réelle.'].astype(str).str[:2].replace({'na': 0}).astype(int))
    mnites=sum(df["Présence réelle."].astype(str).str[3:5].replace({'': 0}).astype(int))
    while mnites >= 60:
        mnites=mnites-60
        hour=hour+1
    t2.delete('1.0',END) # Delete previous data from position 0 till end
    t2.insert(tk.END, str(hour)+"h"+str(mnites)+"m")

  else:
    t2.delete('1.0',END) # Delete previous data from position 0 till end
    t2.insert(tk.END, "n'est pas existe ")
  if 'Jr. travaillé.' in df.columns:
    df['Jr. travaillé.'] = df['Jr. travaillé.'].replace(',', '.', regex=True)
    jour=sum(df["Jr. travaillé."].astype(str).str[0:].replace({'nan': 0}).astype(float))
    t3.delete('1.0',END) # Delete previous data from position 0 till end
    t3.insert(tk.END, str(jour)+" jour travailler")
  else:
    t3.delete('1.0',END) # Delete previous data from position 0 till end
    t3.insert(tk.END, "n'est pas existe ")  
  t1.delete('1.0',END) # Delete previous data from position 0 till end

  t1.insert(tk.END, df)


def upload_csv():
  global df
  file = filedialog.askopenfilename(filetypes=[("Csv file", ".csv")])

  df = pd.read_csv(file,encoding='ISO-8859-1' ,sep=';')
  if 'Présence réelle.' in df.columns:
    hour=sum(df['Présence réelle.'].astype(str).str[:2].replace({'na': 0}).astype(int))
    mnites=sum(df["Présence réelle."].astype(str).str[3:5].replace({'': 0}).astype(int))
    while mnites >= 60:
        mnites=mnites-60
        hour=hour+1
    t2.delete('1.0',END) # Delete previous data from position 0 till end
    t2.insert(tk.END, str(hour)+"h"+str(mnites)+"m")

  else:
    t2.delete('1.0',END) # Delete previous data from position 0 till end
    t2.insert(tk.END, "n'est pas existe ")
  if 'Jr. travaillé.' in df.columns:
    df['Jr. travaillé.'] = df['Jr. travaillé.'].replace(',', '.', regex=True)
    jour=sum(df["Jr. travaillé."].astype(str).str[0:].replace({'nan': 0}).astype(float))
    t3.delete('1.0',END) # Delete previous data from position 0 till end
    t3.insert(tk.END, str(jour)+" jour travailler")
  else:
    t3.delete('1.0',END) # Delete previous data from position 0 till end
    t3.insert(tk.END, "n'est pas existe ")  
  t1.delete('1.0',END) # Delete previous data from position 0 till end

  t1.insert(tk.END, df)

my_w.mainloop()