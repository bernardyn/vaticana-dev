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

def createElement(tag, attrib, attribValue, value):
    newValue = ET.XML(f'<{tag}>{attrib}="{attribValue}"{value}</{tag}>')
    return newValue

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
title = findElementByXpath(input, '//div/head')
placeName = findElementByXpath(input, '//hi[@rend="<placeName>_Znak"]')
dateDoc = findElementByXpath(input, '//hi[@rend="<date>_Znak"]')
abstract = changeYellowToPlaceName('//p[@rend="abstract"]')
nota = findElementByXpath(input, '//hi[@rend="nota_Znak"]')
zrodlo = findElementByXpath(input, '//hi[@rend="Źródło_Znak"]')
bibl = findElementByXpath(input, '//p[@rend="bibl"]')

# xpath output variables
output_title = '//titleStmt/title'
output_placeName = '//creation/placeName'
output_dateDoc = '//creation/date'
output_abstract = '//profileDesc/abstract'
output_nota = '//msContents/msItem'
output_zrodlo = '//msIdentifier/msName'
output_bibl = '//msContents/msItem'

# set title
insertText(output_title, title)

# set place name
insertText(output_placeName, placeName)
if(placeName == 'Roma'):
    insertAtrribut(output_placeName, 'ana', 'Rzym')
else:
    print('placeName to nie Roma')

# set źródło
insertText(output_zrodlo, zrodlo)
sourceCheck = zrodlo.find('or.')
if('or.' in zrodlo):
    insertAtrribut(output_zrodlo, 'type', 'oryginał')
if('cop.' in zrodlo):
    insertAtrribut(output_zrodlo, 'type', 'kopia')

# set abstract
insertElement(output_abstract, abstract)

# set bibl
if(';' in bibl):
    splittedBibl = bibl.split('; ')
    for elem in splittedBibl:
        if('reg.' in elem):
            newElem = createElement('bibl', 'type', 'regest', elem)
            insertElement(output_bibl, newElem)
        elif('ed.' in elem):
            newElem = createElement('bibl', 'type', 'edycja', elem)
            insertElement(output_bibl, newElem)
        else:
            newElem = createElement('bibl', 'type', 'none', elem)
            insertElement(output_bibl, newElem)

# set date
insertText(output_dateDoc, dateDoc)

# set nota
insertText(output_nota, nota)

# printing output
print(ET.tostring(templateXml, pretty_print=1, encoding="unicode"))