import lxml.etree as ET

# open the input file
input = ET.parse('nr 1.xml')

# output template
templateXml = ET.parse('template.xml')

# element finding by xpath
def findElementByXpath(source, xpath):
    return source.find(xpath).xpath("string()")

# find and change text in output file
def insertText(xpath, newText):
    templateXml.find(xpath).text = newText

def insertAtrribut(xpath, newAttrName, newAttrValue):
    templateXml.find(xpath).set(newAttrName, newAttrValue)

# input variables
idDocument = findElementByXpath(input, '//p[@rend="Title"]')
placeName = findElementByXpath(input, '//hi[@rend="<placeName>_Znak"]')
dateDoc = findElementByXpath(input, '//hi[@rend="<date>_Znak"]')
abstract = findElementByXpath(input, '//p[@rend="abstract"]')

# xpath output variables
output_title_xpath = '//seriesStmt/title'
output_placeName_xpath = '//creation/placeName'
output_abstract_xpath = '//profileDesc/abstract'
output_date_xpath = '//creation/date'

# set title
insertText(output_title_xpath, idDocument)

# set place name
insertText(output_placeName_xpath, placeName)
if(placeName == 'Roma'):
    insertAtrribut(output_placeName_xpath, 'ana', 'Rzym')
else:
    print('placeName to nie Roma')

# set abstract
insertText(output_abstract_xpath, abstract)

# set date
insertText(output_date_xpath, dateDoc)


# printing output
print(ET.tostring(templateXml, pretty_print=True, encoding="unicode"))
