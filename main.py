import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


csv_path = 'company.csv'
df = pd.read_csv(csv_path) # read csv

notfound = []
url = 'https://www.findcompany.com.tw/search/'

#chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument('--disable-gpu') # windowsd必須加入此行
#chrome_options.headless = True # also works

company_name = df[352:1049]['公司名稱'].tolist()
#company_name = df[350:1049]['公司名稱'].tolist()
#--------------------------------------------------------------------------
def search(name):
    csv_path = 'company.csv'
    df = pd.read_csv(csv_path) # read csv

    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    
    element = driver.find_element_by_css_selector(".home-search-input")
    element.send_keys(name)
    print(name)
    
    search_click = driver.find_element_by_css_selector(".button").click()
    
    try:
        first_click = driver.find_element_by_css_selector(".searchItem:nth-child(1) > .company-name").click()
    except Exception:
        print('not found')
        notfound.append(name)
        driver.close()
        return
    
    
    #print(driver.page_source)
    
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    f = soup.find("table",{"class":"table-condensed"}).find('tbody').find_all('td')
    
    result = []
    
    
    for s in f:
        result.append(str(s.text.replace(" ","").replace("\n","")))
    
    
    #公司住址	
    try:
        address = result[result.index('登記地址')+1]
    except Exception:
        address = ''
    
    
    #公司E-mail	
    try:
        email = result[result.index('官方信箱')+1]
    except Exception:
        email = ''
    
    
    #公司負責人	
    try:
        Responsible_person = result[result.index('負責人')+1]
    except Exception:
        Responsible_person = ''
    
    
    #公司負責人E-amil	
    
    #公司(高階主管, ex.總經理)
    #董事長
    try:
        Chairman  = result[result.index('董事長')+1]
    except Exception:
        Chairman  = ''
    
    #總經理
    try:
        General_manager = result[result.index('總經理')+1]
    except Exception:
        General_manager = ''
    
    comma = ','

    if (Chairman=='' and General_manager==''):
        comma = ''
    elif(Chairman!='' and General_manager!='' and Chairman==General_manager):
        comma = ''
        General_manager = ''

    index=df[df['公司名稱'].isin([name])].index[0]
    df.loc[index,'公司住址']=address
    df.loc[index,'公司負責人']=email
    df.loc[index,'公司負責人E-amil']=Responsible_person
    df.loc[index,'公司(高階主管, ex.總經理)']=Chairman+comma+General_manager
    
    try:
        df.to_csv(csv_path,index=False,sep=',',encoding='utf-8-sig')
        print('save to csv')
    except Exception:
        print('save error ! try again !')

    driver.close()

for i in company_name:
    search(i)


