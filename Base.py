import xml.etree.ElementTree as ET
import os
import ipaddress

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
      <OI NAME="{DeviceName}" TYPE="modbus.network.{MSType}Device">'''
template_2='''
        <OI NAME="{RegisterGroupName}" TYPE="modbus.point.ModbusRegisterGroup">
    '''

template_3 = '''       <OI DESCR="{Description}" NAME="{Name}" TYPE="{Type}">
            <PI Name="Gain" Value="1"/>
            <PI Name="Offset" Value="0"/>
            <PI Name="RegisterNumber" Value="{ModReg}"/>
            <PI Name="RegisterType" Value="{RegType}"/>
          </OI>
   '''

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

# gatewayName = input("What is the name of the gateway: ")
DeviceName = input("What is the name of the device: ")

# while True:
#     try:
#         ip = input("What is the IP address of the gateway: ")
#         ipaddress.ip_address(ip)
#         print("Valid IP address.")
#         break 
#     except ValueError:
#         print("Invalid IP address. Please try again.")

while True:
    try:
        MSType = int(input('''What is the type of the device: 
               1. Master   2. Slave\n'''))
        if MSType not in [1, 2]:
            raise ValueError("Invalid selection. Please enter 1 or 2.")
        break
    except ValueError as e:
        print(e)
MSTypeMapping = {1: "Master", 2: "Slave"}
MSType = MSTypeMapping.get(MSType, "Master")

report = template_1.format(DeviceName=DeviceName, MSType=MSType)

# nodo = root.find('Nodo')

for nodo in root.findall('Nodo'):
    RegisterGroupName = input("Enter the name of the register group: ")
    report += template_2.format(RegisterGroupName=RegisterGroupName)
    counter = 0
    for variable in nodo.findall('Variabile'):
        counter += 1
        ModReg = variable.attrib.get('ModReg')
        RegType = variable.attrib.get('Type')
        Description = variable.attrib.get('Desc')
        Name = variable.attrib.get('Desc','').split(' ')[0] + ' ' + str(counter)
        TypeStr = "modbus.point.AnalogInput"
        # while True:    
        #       try:
        #           Type = int(input('''Select the type of the variable: 
        #                        1. Analog Input   2. Analog Output
        #                      '''))
        #           if Type not in [1, 2]:
        #               raise ValueError("Invalid selection. Please select an available type.")
        #           break
        #       except ValueError as e:
        #           print(e)
        # TypeMapping = {1: "modbus.point.AnalogInput", 2: "modbus.point.AnalogOutput"}
        # TypeStr = TypeMapping.get(Type)
        report += template_3.format(Description=Description, Name=Name, Type=TypeStr, ModReg=int(ModReg)+1, RegType=RegType)
    report +='''     </OI>'''
    

report += ''' 
      </OI>
</ExportedObjects>

</ObjectSet>'''

try:
    output_file = input("Enter the output file name: ")
    if not output_file.endswith(".xml"):
        output_file += ".xml"
    with open(output_file, "w") as f:
        f.write(report)
    print(f"File saved to {output_file}")
except IOError as e:
    print(f"Error occurred while saving the file: {e}")