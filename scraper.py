import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as ec
from selenium.webdriver.common.by import  By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from funciones import get_user_agent
from bs4 import BeautifulSoup

import time
import random


urls={

    "dominios":"http://ipv4info.com/tools/all-domains-on-ip/",
    "rangos":"http://ipv4info.com",
    "pwned":"https://pwndb2am4tzkvold.onion.ws"


}




PATH=r"./DRIVERS/geckodriver"

#tor
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", '127.0.0.1')
profile.set_preference("network.proxy.socks_port", 9050)
profile.set_preference("network.proxy.socks_remote_dns", False)
#cambia el useragent
#profile.set_preference("general.useragent.override",get_user_agent())
#headless
options=Options()
options.headless =True
profile.update_preferences()






def get_company_data(empresa,iniciorangos,finrangos,asn,organization):
    os.system("service tor reload")
    driver = webdriver.Firefox(executable_path=PATH, firefox_profile=profile, options=options)
    driver.get(urls['rangos'])

    WebDriverWait(driver, 10) \
        .until(ec.element_to_be_clickable((By.CSS_SELECTOR,
                                           'input#ipc4'))) \
        .send_keys(empresa)

    WebDriverWait(driver, 10) \
        .until(ec.element_to_be_clickable((By.XPATH,
                                           '//*[@id="wrap"]/form/button'))) \
        .click()

    body = driver.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    soup = BeautifulSoup(source, "html.parser")

    driver.close()

    tabla = soup.find_all("table", {"class": "TB2"})
    fila = tabla[0].find_all("tr")

    columna = fila[3].find_all("td")


    cont = 0

    for i in fila:
        if cont < 3:
            pass
        else:

            fila2 = i.find_all("td")

            iniciorangos.append(fila2[2].text)
            finrangos.append(fila2[3].text)
            asn.append(fila2[6].text)
            organization.append(fila2[8].text)

        cont = cont + 1





























