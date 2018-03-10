from lxml import etree
import requests
import selenium
import urllib2
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# some_xml_data = "<root>data</root>"
# root = etree.fromstring(some_xml_data)
driver = webdriver.Chrome()
driver.get("https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dgarden&field-keywords=computer")
print driver.title
assert "Amazon.com: computer: Home & Kitchen" in driver.title
elem = driver.find_elements_by_class_name("cfMarker")
print elem[0].value_of_css_property('height')[:-2]
print elem[0].find_element_by_xpath("..").get_attribute('class')


# elem.clear()




def _isSame(x, y):
	s = set([])
	for ele in x:

		s.add(ele.get_attribute(y))
	if len(s) == 1:
		return True
	else:
		return False


def all(x):
	return driver.find_elements_by_class_name(x)


def _count(l):
	return len(l)

def _sum_height(x):
	s = 0
	for ele in x:
		s += float(ele.value_of_css_property('height')[:-2])
	return s
print _sum_height(all("cfMarker"))




def _is_same_lowest_ancestor(x1, x2, y):
	y1 = x1.find_element_by_xpath("..").get_attribute(y)
	y2 = x2.find_element_by_xpath("..").get_attribute(y)
	return y1 == y2

# elem.send_keys("pycon")
# r = requests.get('https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=desktop', auth=('user', 'pass'))

# page = urllib2.urlopen('https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=desktop')
# soup = BeautifulSoup(r.content,"lxml")

# x = soup.body.find_all('div', attrs={'class' : 's-item-container'})
# for j in x:
	# print j.find_all(text = "$")
	
# print len(x)
# print root.tag

