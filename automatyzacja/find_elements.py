import lxml.etree as ET

# open the input file
input = ET.parse('nr 1.xml')

# xpath variables
idDocument_xpath = '//p[@rend="Title"]'
placeName_xpath = '//hi[@rend="<placeName>_Znak"]'
dateDoc_xpath = '//hi[@rend="<date>_Znak"]'
abstract_xpath = '//p[@rend="abstract"]'

# element finding by xpath
def findElementByXpath(xpath):
    return input.find(xpath).xpath("string()")

# variables to
idDocument = findElementByXpath(idDocument_xpath)
placeName = findElementByXpath(placeName_xpath)
dateDoc = findElementByXpath(dateDoc_xpath)
abstract = findElementByXpath(abstract_xpath)

#printing
print(abstract)



#print(ET.tostring(tag, pretty_print=True, encoding="unicode"))
