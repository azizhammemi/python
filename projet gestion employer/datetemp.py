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
    if 'Date/Temps' in df.columns:
      df["entre"] = pd.NA
      df["sortie"] = pd.NA
      df.replace(pd.NA,'-' , inplace=True)


      for i, row in df.iterrows():
          if i % 2 == 0:  # Si le numéro de ligne est pair
              df.at[i, "entre"] = row["Date/Temps"]  # Remplacer "VotreColonne" par le nom de votre colonne à couper
          else:  # Si le numéro de ligne est impair
              df.at[i, "sortie"] = row["Date/Temps"]  # Remplacer "VotreColonne" par le nom de votre colonne à couper

  # Afficher le DataFrame avec les nouvelles colonnes "entre" et "sortie"
      
    

      mintesentre=sum(df['entre'].astype(str).str[14:16].replace({'': 0}).astype(int))
      hourentre=sum(df['entre'].astype(str).str[11:13].replace({'': 0}).astype(int))
      while mintesentre >59:
          mintesentre=mintesentre-60
          hourentre=hourentre+1


      mintesorties=sum(df['sortie'].astype(str).str[14:16].replace({'': 0}).astype(int))
      hoursortie=sum(df['sortie'].astype(str).str[11:13].replace({'': 0}).astype(int))
      while mintesorties >59:
          mintesorties=mintesorties-60
          hoursortie=hoursortie+1
      if(mintesentre>mintesorties):
          mintesorties=mintesorties+60
          hoursortie=hoursortie-1
      hourentree = df['entre'].astype(str).str[11:13].replace({'': '0'}).astype(int)
      hoursortiee = df['sortie'].astype(str).str[11:13].replace({'': '0'}).astype(int)
      mintesentree = df['entre'].astype(str).str[14:16].replace({'': '0'}).astype(int)
      mintesortiess = df['sortie'].astype(str).str[14:16].replace({'': '0'}).astype(int)
      totalheur = hoursortiee - hourentree
      totalminutes =(totalheur*60)+(mintesortiess - mintesentree)

      
      df['journe'] = totalminutes // 60 + ((totalminutes % 60) / 100)

      df['journe'] = df['journe'].shift() + df['journe']

      df.loc[df['journe'].apply(lambda x: x % 1 > 0.59), 'journe'] += 0.4
      df.loc[::2, 'journe'] = 00.00
      df.loc[0, "total"]=str(hoursortie-hourentre)+"h"+str(mintesorties-mintesentre)+"m"
      t1.delete('1.0',END)
      t2.delete('1.0',END) # Delete previous data from position 0 till end
      t1.insert(tk.END, df.to_string())
      t2.insert(tk.END, str(hoursortie-hourentre)+"h"+str(mintesorties-mintesentre)+"m")

      nom=df.loc[1, 'Nom']
      df.to_excel(nom+'export.xlsx', index=False)
 
# saving the excel
    else:
      t1.delete('1.0',END)
      t2.delete('1.0',END) # Delete previous data from position 0 till end
      t2.insert(tk.END, "n'est pas exixte")
      t1.insert(tk.END, df)


  



def upload_csv():
  try:
    global df
    file = filedialog.askopenfilename(filetypes=[("Csv file", ".csv")])

    df = pd.read_csv(file,encoding='ISO-8859-1' ,sep=';')
    if 'Date/Temps' in df.columns:
      
        df["entre"] = pd.NA
        df["sortie"] = pd.NA
        df.replace(pd.NA,'-' , inplace=True)


        for i, row in df.iterrows():
            if i % 2 == 0:  # Si le numéro de ligne est pair
                df.at[i, "entre"] = row["Date/Temps"]  # Remplacer "VotreColonne" par le nom de votre colonne à couper
            else:  # Si le numéro de ligne est impair
                df.at[i, "sortie"] = row["Date/Temps"]  # Remplacer "VotreColonne" par le nom de votre colonne à couper

          # Afficher le DataFrame avec les nouvelles colonnes "entre" et "sortie"
        
      

        mintesentre=sum(df['entre'].astype(str).str[14:16].replace({'': 0}).astype(int))
        hourentre=sum(df['entre'].astype(str).str[11:13].replace({'': 0}).astype(int))
        while mintesentre >=60:
            mintesentre=mintesentre-60
            hourentre=hourentre+1


        mintesorties=sum(df['sortie'].astype(str).str[14:16].replace({'': 0}).astype(int))
        hoursortie=sum(df['sortie'].astype(str).str[11:13].replace({'': 0}).astype(int))
        while mintesorties >= 60:
            mintesorties=mintesorties-60
            hoursortie=hoursortie+1
        if(mintesentre>mintesorties):
            mintesorties=mintesorties+60
            hoursortie=hoursortie-1
        hourentree = df['entre'].astype(str).str[11:13].replace({'': '0'}).astype(int)
        hoursortiee = df['sortie'].astype(str).str[11:13].replace({'': '0'}).astype(int)
        mintesentree = df['entre'].astype(str).str[14:16].replace({'': '0'}).astype(int)
        mintesortiess = df['sortie'].astype(str).str[14:16].replace({'': '0'}).astype(int)
        totalheur = hoursortiee - hourentree
        totalminutes =(totalheur*60)+(mintesortiess - mintesentree)

        
        df['journe'] = totalminutes // 60 + ((totalminutes % 60) / 100)

        df['journe'] = df['journe'].shift() + df['journe']

        df.loc[df['journe'].apply(lambda x: x % 1 > 0.59), 'journe'] += 0.4
        df.loc[::2, 'journe'] = 00.00
        df.loc[0, "total"]=str(hoursortie-hourentre)+"h"+str(mintesorties-mintesentre)+"m"
        t1.delete('1.0',END)
        t2.delete('1.0',END) # Delete previous data from position 0 till end
        t1.insert(tk.END, df.to_string())
        t2.insert(tk.END, str(hoursortie-hourentre)+"h"+str(mintesorties-mintesentre)+"m")
        nom=df.loc[1, 'Nom']
        df.to_excel(nom+'export.xlsx', index=False)
    else:
      t1.delete('1.0',END)
      t2.delete('1.0',END) # Delete previous data from position 0 till end
      t2.insert(tk.END, "n'est pas valide")
      t1.insert(tk.END, df)
  except:
      t1.delete('1.0',END)
      t2.delete('1.0',END) # Delete previous data from position 0 till end
      t2.insert(tk.END, "n'est pas exixte")
      t1.insert(tk.END, df)



my_w.mainloop()