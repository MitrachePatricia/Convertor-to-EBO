import xml.etree.ElementTree as ET
import os

template_1 = '''<ObjectSet ExportMode="Standard" Note="TypesFirst" SemanticsFilter="Standard" Version="5.0.3.117">
  <MetaInformation>
    <ExportMode Value="Standard"/>
    <SemanticsFilter Value="None"/>
    <RuntimeVersion Value="5.0.3.117"/>
    <SourceVersion Value="5.0.3.117"/>
    <ServerFullPath Value="/Server 1"/>
  </MetaInformation>
<ExportedObjects>
<OI NAME="Convertor {ConvertorCode}" TYPE="modbus.network.{MSType}Device">
    <OI NAME="M-Bus_Contori" TYPE="modbus.point.ModdbusRegisterGroup">
    '''

template_2 = '''<OI DESC="{Description}" NAME="{Name}" TYPE="{Type}">
    <PI Name="Gain" Value="1"/>
    <PI Name="Offset" Value="0"/>
    <PI Name="RegisterNumber" Value="{ModReg}"/>
    <PI Name="RegisterType" Value="{RegType}"/>
  </OI>'''

while True:
    file = input('Enter the file name: ')
    if not file.endswith(".xml"):
        file += ".xml"
    if not os.path.isfile(file):
        print(f"Error: The file '{file}' does not exist. Please try again.")
        continue
    tree = ET.parse(file)
    break

root = tree.getroot()

while True:
    try:
        convertorCode = input("What is the code of the convertor: ")
        if convertorCode[:5] != 'HD670':
            raise ValueError("Invalid convertor code. Please enter a valid convertor code.")
        break
    except ValueError as e:
        print(e)
while True:
    try:
        MSType = int(input('''What is the type of the convertor: 
               1. Master   2. Slave\n'''))
        if MSType not in [1, 2]:
            raise ValueError("Invalid selection. Please enter 1 or 2.")
        break
    except ValueError as e:
        print(e)
MSTypeMapping = {1: "Master", 2: "Slave"}
MSType = MSTypeMapping.get(MSType, "Master")

report = template_1.format(ConvertorCode=convertorCode, MSType=MSType)

nodo = root.find('Nodo')

if nodo is not None:
    counter = 0
    for variable in nodo.findall('Variabile'):
        counter += 1
        ModReg = variable.attrib.get('ModReg')
        RegType = variable.attrib.get('Type')
        Description = variable.attrib.get('Desc')
        Name = input(f"A name for variable {counter}: ")
        if int(RegType) > 2:
            Type = 1
        else:
            while True:    
               try:
                   Type = int(input('''Select the type of the variable: 
                              1. Analog Input   2. Digital Input   
                            '''))
                   if Type not in [1, 2]:
                      raise ValueError("Invalid selection. Please enter 1 or 2.")
                   break
               except ValueError as e:
                  print(e)

TypeMapping = {1: "modbus.point.AnalogInput", 2: "modbus.point.DigitalInput"}


TypeStr = TypeMapping.get(Type)
        
report += template_2.format(Description=Description, Name=Name, Type=TypeStr, ModReg=int(ModReg)+1, RegType=RegType)

report += '''</OI>
</OI></ExportedObjects></ObjectSet>'''

output_file = input("Enter the output file name: ")
if not output_file.endswith(".xml"):
    output_file += ".xml"
with open(output_file, "w") as f:
    f.write(report)

print(f"File saved to {output_file}")