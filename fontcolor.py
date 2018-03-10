from lxml import etree

import requests
import selenium

import urllib.request, urllib.error, urllib.parse


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.color import Color
import webcolors
import ast

#Note: Color of titles is darkcyan



def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def closest_colourXY(requested_colour):
    min_colours = {}
    for key, name in webcolors.html4_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = abs(r_c - requested_colour[0]) * 256
        gd = abs (g_c - requested_colour[1]) * 256
        bd = abs (b_c - requested_colour[2]) * 256
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name




#Find text by matching FOntSize
def match_fontColor(inpcolor = "darkcyan"):

    ids = driver.find_elements_by_xpath('//*[@id]')
    #Get unique tag names
    tag_name = {}
    for ii in ids:
        tag_name[ii.tag_name] = 1

    #One can iterate over tagname to get through all tags. Outer-loop unused now, currently looking at h2 tag only
    for each_tag in tag_name.keys():
        taglist = driver.find_elements_by_tag_name('h2')
        
        for tag in taglist:
            if len(tag.text):   
                classname = tag.get_attribute("class")
                classlst = classname.split()
                colorlst = []
                classfilter = []

                #Separate class that have color in their names
                for each_class in classlst:
                    if "color" in each_class:
                        classfilter.append(each_class)

                #If no color class exists, just search from entire classlst : Not always robust
                if len(classfilter) == 0:
                    classfilter = classlst
                

                for eclass in classfilter:  
                          
                    color = driver.find_element_by_class_name(eclass).value_of_css_property('color')
                    r,g,b, alpha = ast.literal_eval(color.strip("rgba"))
                    rgb = []
                    rgb.append(r)
                    rgb.append(g)
                    rgb.append(b)        
                    colname = get_colour_name(rgb) 
                    colorlst.append(colname[1])
                #print(colorlst)           
                if inpcolor in colorlst:
                    #print(tag.text, colorlst,classfilter)
                    print(tag.text)
        #Remove this break when running for all tags
        break
                    
                #tagxpath = driver.find_element_by_xpath('//*[@id]')            

##Copy-over from Xinyuan's code

driver = webdriver.Chrome()
driver.get("https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dgarden&field-keywords=computer")
print(driver.title)
assert "Amazon.com: computer: Home & Kitchen" in driver.title
#Get all dark colored text 
match_fontColor("darkcyan")

