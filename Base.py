import xml.etree.ElementTree as ET

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
    <OI NAME="M-Bus_Contori" TYPE="modbus.point.ModdbusRegisterGroup">'''

template_2 = '''<OI DESC="{Description}" NAME="{Name}" TYPE="{Type}">
    <PI Name="Gain" Value="1"/>
    <PI Name="Offset" Value="0"/>
    <PI Name="RegisterNumber" Value="{ModReg}"/>
    <PI Name="RegisterType" Value="{RegType}"/>
  </OI>'''

file = input('Enter the file name: ')
tree = ET.parse(file)
root = tree.getroot()

convertorCode = input("What is the code of the convertor: ")
MSType = int(input('''What is the type of the convertor: 
               1. Master   2. Slave'''))
MSTypeMapping = {1: "Master", 2: "Slave"}
MSType = MSTypeMapping.get(MSType, "Master")

report = template_1.format(ConvertorCode=convertorCode, MSType=MSType)

nodo = root.find('Nodo')

if nodo is not None:
    for variable in nodo.findall('Variabile'):
        ModReg = variable.attrib.get('ModReg')
        RegType = variable.attrib.get('Type')
        Description = variable.attrib.get('Desc')
        Name = input("A name for a variable: ")
        Type = int(input('''Select the type of the variable: 
                         1. Analog Input    2. Analog Output
                         3. Digital Input   4. Digital Output 
                         '''))
        TypeMapping = {1: "modbus.point.AnalogInput", 2: "modbus.point.AnalogOutput", 3: "modbus.point.DigitalInput", 4: "modbus.point.DigitalOutput"}
        TypeStr = TypeMapping.get(Type, "modbus.point.AnalogInput")
        
        report += template_2.format(Description=Description, Name=Name, Type=TypeStr, ModReg=ModReg, RegType=RegType)

report += '''</OI>
</OI></ExportedObjects></ObjectSet>'''\

output_file = input("Enter the output file name: ")
if not output_file.endswith(".xml"):
    output_file += ".xml"
with open(output_file, "w") as f:
    f.write(report)

print(f"File saved to {output_file}")