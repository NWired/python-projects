from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import webbrowser

#open google chrome
browser = webdriver.Chrome()
for i in range(1,3):
    #access the site
    browser.get('https://freebiesglobal.com/page/%s'%i)
#PS: there are free udemy coupons in freebiesglobal
    

    ##specify which part of the site to search
    target = browser.find_element_by_class_name(\
    'eq_grid.post_eq_grid.rh-flex-eq-height.col_wrap_fifth')
    #find items
    items = target.find_elements_by_class_name(\
    'img-centered-flex.rh-flex-center-align.rh-flex-justify-center')

    #open the tabs
    for a in items:
        webbrowser.open(a.get_attribute('href'))

