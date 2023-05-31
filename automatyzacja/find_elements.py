import lxml.etree as ET

# open the input file
inputFileName = '1'
input = ET.parse('pliki/'+inputFileName+'.xml')

# output template
templateXml = ET.parse('template.xml')

#remove namespace http://www.tei-c.org/ns/1.0
def remove_namespace(doc, namespace):
    ns = u'{%s}' % namespace
    nsl = len(ns)
    for elem in doc.getiterator():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]

# element finding by xpath
def findElementByXpath(source, xpath):
    try:
        element = source.find(xpath).xpath("string()")
    except:
        element = 'error_not_found'
    return element

# find and change text in output file
def insertText(xpath, newText):
    templateXml.find(xpath).text = newText

def createElement(tag, attrib, attribValue, value):
    newValue = ET.XML(f'<{tag} {attrib}="{attribValue}">{value}</{tag}>')
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

# remove namespace
remove_namespace(input, u'http://www.tei-c.org/ns/1.0')

# input variables
title = findElementByXpath(input, '//div/head')
placeName = findElementByXpath(input, '//hi[@rend="<placeName>_Znak"]')
dateDoc = findElementByXpath(input, '//hi[@rend="<date>_Znak"]')
abstract = changeYellowToPlaceName('//p[@rend="abstract"]')
nota = findElementByXpath(input, '//hi[@rend="nota_Znak"]')
zrodlo = findElementByXpath(input, '//p[@rend="Źródło"]')
bibl = findElementByXpath(input, '//p[@rend="bibl"]')
content = findElementByXpath(input, '//p[@rend="content"]')

# xpath output variables
output_title = '//titleStmt/title'
output_placeName = '//creation/placeName'
output_dateDoc = '//creation/date'
output_abstract = '//profileDesc/abstract'
output_nota = '//msItem/note'
output_zrodlo = '//msIdentifier/msName'
output_bibl = '//msContents/msItem'
output_content = '//body/div/p'

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
else:
    newElem = createElement('bibl', 'type', 'none', bibl)
    insertElement(output_bibl, newElem)

# set date
insertText(output_dateDoc, dateDoc)

# set nota
insertText(output_nota, nota)

# set content
insertText(output_content, content)

# printing output
# print(ET.tostring(templateXml, pretty_print=1, encoding="unicode"))

# write to file
outputFileName = inputFileName+'-out.xml'
templateXml.write(outputFileName, encoding="utf-8")