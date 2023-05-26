from io import StringIO

import lxml.etree as ET

# open the input file
input = ET.parse('nr 1378053001.xml')

# output template
templateXml = ET.parse('template.xml')

# element finding by xpath
def findElementByXpath(source, xpath):
    return source.find(xpath).xpath("string()")

# find and change text in output file
def insertText(xpath, newText):
    templateXml.find(xpath).text = newText

def insertElement(xpath, newElement):
    templateXml.find(xpath).append(newElement)

def insertAtrribut(xpath, newAttrName, newAttrValue):
    templateXml.find(xpath).set(newAttrName, newAttrValue)

def changeYellowToPlaceName(inputPath):
    path = input.find(inputPath)
    path.attrib.pop("rend", None)
    path.attrib.pop("style", None)
    for elem in path:
        if(elem.attrib.get('rend')=='background(yellow)'):
            elem.tag = 'placeName'
            elem.attrib.pop("rend", None)
    return path

# input variables
idDocument = findElementByXpath(input, '//div/head')
placeName = findElementByXpath(input, '//hi[@rend="<placeName>_Znak"]')
dateDoc = findElementByXpath(input, '//hi[@rend="<date>_Znak"]')
abstract = changeYellowToPlaceName('//p[@rend="abstract"]')
nota = findElementByXpath(input, '//hi[@rend="nota_Znak"]')

# xpath output variables
output_title_xpath = '//titleStmt/title'
output_placeName_xpath = '//creation/placeName'
output_abstract_xpath = '//profileDesc/abstract'
output_date_xpath = '//msItem/note'

# set title
insertText(output_title_xpath, idDocument)

# set place name
insertText(output_placeName_xpath, placeName)
if(placeName == 'Roma'):
    insertAtrribut(output_placeName_xpath, 'ana', 'Rzym')
else:
    print('placeName to nie Roma')

# set abstract
insertElement(output_abstract_xpath, abstract)

# set date
insertText(output_date_xpath, dateDoc)

# set nota
insertText(output_date_xpath, nota)

# printing output
print(ET.tostring(templateXml, pretty_print=1, encoding="unicode"))
