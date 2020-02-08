from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import webbrowser,bs4,requests
import pyinputplus as pyip
import openpyxl


#open google chrome
def freebiesglobal(n):
    browser = webdriver.Chrome()
    for i in range(1,n+1):
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

    browser.quit()

#open learnviral
def learnviral(n):
    browser = webdriver.Chrome()
    for i in range(1,n+1):
        browser.get('https://udemycoupon.learnviral.com/page/%s'%i) #a page
        target = browser.find_element_by_id('main')
        items = target.find_elements_by_class_name(\
            'coupon-code-link.btn.promotion')
        for a in items:
            webbrowser.open(a.get_attribute('href'))
    browser.quit()

#open couponscorpion.com
def couponscorpion(n):
    browser = webdriver.Chrome()
    for i in range(1,n+1): #per page
        browser.get('https://couponscorpion.com/page/%s'%i)
        target = browser.find_element_by_class_name(\
            'eq_grid.post_eq_grid.rh-flex-eq-height.col_wrap_three')
        items = target.find_elements_by_class_name(\
            'img-centered-flex.rh-flex-center-align.rh-flex-justify-center')
        
        for a in items: #per item in a page
            res = requests.get(a.get_attribute('href'))
            res.raise_for_status()
            soupitem = bs4.BeautifulSoup(res.text,'html.parser')
            elem = soupitem.select('a')
            for i in elem:
                webbrowser.open(i.get('href'))
    browser.quit()
            
#open guru99
def guru99(n):
    browser = webdriver.Chrome()
    browser.get('https://www.guru99.com/free-udemy-course.html') #a page
    items = browser.find_elements_by_link_text('Learn More')
    for a in range(n):
        webbrowser.open(items[a].get_attribute('href'))
    browser.quit()
    
#open couponscorpion.com
def couponscorpion(n):
    browser = webdriver.Chrome()
    for i in range(1,n+1): #per page
        browser.get('https://dailycoursereviews.com/page/%s'%i)
        target = browser.find_element_by_class_name(\
            'eq_grid.post_eq_grid.rh-flex-eq-height.col_wrap_three')
        items = target.find_elements_by_class_name(\
            'img-centered-flex.rh-flex-center-align.rh-flex-justify-center')
        
        for a in items: #per item in a page
            res = requests.get(a.get_attribute('href'))
            res.raise_for_status()
            soupitem = bs4.BeautifulSoup(res.text,'html.parser')
            elem = soupitem.select('a')
            for i in elem:
                webbrowser.open(i.get('href'))
    browser.quit()
    
def courses():
    browser = webdriver.Chrome()
    browser.get('https://freebiesglobal.com/22-free-udemy-python-courses')
    target = browser.find_element_by_tag_name('ol')
    items = target.find_elements_by_tag_name('a')
    for a in items:
         webbrowser.open(a.get_attribute('href'))
    browser.quit()


def courses2():
    browser = webdriver.Chrome()
    browser.get('https://freebiesglobal.com/89-free-courses-web-development-css-javascript-bootstrap-jquery-adobe-and-more')
    target = browser.find_element_by_tag_name('ol')
    items = target.find_elements_by_tag_name('a')
    for a in items:
         webbrowser.open(a.get_attribute('href'))
    browser.quit()

def main():
    sites = ['freebiesglobal','learnviral','couponscorpion','guru99','leave']
    item = ''
    while item != 'leave':
        item = pyip.inputMenu(sites,lettered = True)
        if item != 'leave':
            count = input('No of pages/items to show')
            if count.isdigit() and int(count) < 2:
                if count.isdigit() == False:
                    print('Key in a number')
                    continue
                elif int(count) < 2:
                    print('Pages must be 2 or more')
                    continue

                elif item == 'leave':
                    exit()
            else:
                eval('%s(%s)'%(item,count))

functions = ['main()','courses()','courses2()']
choice = pyip.inputMenu(functions,lettered = True)
eval(choice)
