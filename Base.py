import xml.etree.ElementTree as ET
import os
import ipaddress
import tkinter as tk
from tkinter import filedialog, messagebox

# input("!! This version of the app is made for the EBO version 5.0.3.117 !! \nIf you want to use it for newer versions of EBO please change the RuntimeVersion and SourceVersion to your version.")
template_1 = '''<?xml version="1.0" encoding="UTF-8"?>
<ObjectSet ExportMode="Standard" Note="TypesFirst" SemanticsFilter="Standard" Version="5.0.3.117">
  <MetaInformation>
    <ExportMode Value="Standard"/>
    <SemanticsFilter Value="None"/>
    <RuntimeVersion Value="5.0.3.117"/>
    <SourceVersion Value="5.0.3.117"/>
    <ServerFullPath Value="/Server 1"/>
  </MetaInformation>
<ExportedObjects>
      <OI NAME="{DeviceName}" TYPE="modbus.network.MasterDevice">'''
template_2='''
        <OI DESCR="{Descrizione}" NAME="{RegisterGroupName}" TYPE="modbus.point.ModbusRegisterGroup">
    '''

template_3 = '''       <OI DESCR="{Description}" NAME="{Name}" TYPE="{Type}">
            <PI Name="Gain" Value="1"/>
            <PI Name="Offset" Value="0"/>
            <PI Name="RegisterNumber" Value="{ModReg}"/>
            <PI Name="RegisterType" Value="{RegType}"/>
          </OI>
   '''

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
        
def generate_report():
    file = file_entry.get()
    tree = ET.parse(file)

    root = tree.getroot()
    DeviceName = device_name_entry.get()
    report = template_1.format(DeviceName=DeviceName)
    for nodo in root.findall('Nodo'):
       RegisterGroupName = 'ID ' + nodo.attrib.get('ID_Primary')
       Descrizione = nodo.attrib.get('Descrizione')
       report += template_2.format(RegisterGroupName=RegisterGroupName, Descrizione=Descrizione)
       counter = 0
       for variable in nodo.findall('Variabile'):
           counter += 1
           ModReg = variable.attrib.get('ModReg')
           dim = int(variable.attrib.get('Dim'))
           if dim == 0:
               RegType = 1
           elif dim == 1:
               RegType = 2
           elif dim == 2:
               RegType = 4
           elif dim == 3:
               RegType = 19
           elif dim == 4:
               RegType = 3
           elif dim == 5:
               RegType = 18
           elif dim == 6:
               RegType = 8
           else:
               RegType = 1
           Description = variable.attrib.get('Desc')
           Name = variable.attrib.get('Desc','').split(' ')[0] + ' ' + str(counter)
           TypeStr = "modbus.point.AnalogInput"
           report += template_3.format(Description=Description, Name=Name, Type=TypeStr, ModReg=int(ModReg)+1, RegType=RegType)
       report +='''     </OI>'''
    

    report += ''' 
         </OI>
   </ExportedObjects>

   </ObjectSet>'''

    try:
       output_file = output_file_entry.get()
       if not output_file.endswith(".xml"):
           output_file += ".xml"
       desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
       full_path = os.path.join(desktop_path, output_file)

       with open(full_path, "w") as f:
           f.write(report)
       messagebox.showinfo("Success",f"File saved to {full_path}")
    except IOError as e:
       messagebox.showerror("Error",f"Error occurred while saving the file: {e}")

#GUI Part

root = tk.Tk()
root.geometry("700x150")
root.title("MBus to EBO Converter")

messagebox.showwarning("Warning", "  !! This version of the app is made for EBO 5.0.3.117 !!\n\nIf you want to use it for newer versions of EBO please change the RuntimeVersion and SourceVersion to your version.")

label = tk.Label(root, text="Select the XML file to convert:", font=("Arial", 10))
label.grid(row=0, column=0, padx=10, pady=5)
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, width= 10, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Device name:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5)
device_name_entry = tk.Entry(root, width=50)
device_name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Output file name:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5)
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Generate Report", command=generate_report).grid(row=3, column=1, padx=10, pady=5)

root.mainloop()


