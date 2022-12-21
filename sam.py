from funciones import *
from scraper import *
import sqlite3


print('''



   SSSSSSSSSSSSSSS              AAA               MMMMMMMM               MMMMMMMM
 SS:::::::::::::::S            A:::A              M:::::::M             M:::::::M
S:::::SSSSSS::::::S           A:::::A             M::::::::M           M::::::::M
S:::::S     SSSSSSS          A:::::::A            M:::::::::M         M:::::::::M
S:::::S                     A:::::::::A           M::::::::::M       M::::::::::M
S:::::S                    A:::::A:::::A          M:::::::::::M     M:::::::::::M
 S::::SSSS                A:::::A A:::::A         M:::::::M::::M   M::::M:::::::M
  SS::::::SSSSS          A:::::A   A:::::A        M::::::M M::::M M::::M M::::::M
    SSS::::::::SS       A:::::A     A:::::A       M::::::M  M::::M::::M  M::::::M
       SSSSSS::::S     A:::::AAAAAAAAA:::::A      M::::::M   M:::::::M   M::::::M
            S:::::S   A:::::::::::::::::::::A     M::::::M    M:::::M    M::::::M
            S:::::S  A:::::AAAAAAAAAAAAA:::::A    M::::::M     MMMMM     M::::::M
SSSSSSS     S:::::S A:::::A             A:::::A   M::::::M               M::::::M
S::::::SSSSSS:::::SA:::::A               A:::::A  M::::::M               M::::::M
S:::::::::::::::SSA:::::A                 A:::::A M::::::M               M::::::M
 SSSSSSSSSSSSSSS AAAAAAA                   AAAAAAAMMMMMMMM               MMMMMMMM








''')
print("escribe el dominio a analizar:")
dom = input("SAM 💀>")
print("escribe el nombre de la compañia:")
company = input("SAM 💀>")

subdominioslist=list()
puertosabiertos=list()
listaip=list()
iniciorango=list()
finalrango=list()
asnlista=list()
propietarios=list()
urls=list()
crawled=list()




con = sqlite3.connect(f'{company}_data.db')
cursorObj=con.cursor()


cursorObj.execute('DROP table if exists subdominios')
cursorObj.execute('DROP table if exists rangos')
try:
    ############FOTOS
    cursorObj.execute('''CREATE TABLE rangos(Inicio_rango TEXT, Final_rango TEXT, ASN TEXT,Propietario TEXT)''')
    cursorObj.execute('''CREATE TABLE Subdominios(Subdominio TEXT, IP TEXT, Dominio TEXT)''')

except:
    con.close()

def pasar_DB_rangos():

    i = 0

    while i < len(iniciorango):
        con.execute(f'INSERT INTO  rangos (Inicio_rango,Final_rango,ASN,Propietario) VALUES(?, ?, ?,?)',
                    (str(iniciorango[i]), str(finalrango[i]), str(asnlista[i]),str(propietarios[i])))

        con.commit()
        i = i + 1;
def pasar_DB_sub():

    i = 0
    while i < len(subdominioslist):
        con.execute(f'INSERT INTO  Subdominios(Subdominio,IP,Dominio) VALUES(?, ?, ?)',
                    (str(subdominioslist[i]), str(get_ip(subdominioslist[i])), str(dom)))

        con.commit()
        i = i + 1;



def mostrarmenu():
    print('''

    1-)INFORMACION DEL DOMINIO
    2-)SUBDOMINIOS
    3-)RANGOS DE IP
    4-)CRAWLING
    5-)informe completo
    Q-SALIR
    ''')


while 1:
    mostrarmenu()

    opcion = input("SAM>>")
    if opcion == '1':
        print("MOSTRANDO INFORMACION DEL DOMINIO \n")
        print(f"IP: {get_ip(dom)}")
        print("PUERTOS ABIERTOS")
        try:

            puertosabiertos=get_puertos(dom)
            for i in puertosabiertos:
                print(f"TCP: {i}")
            print("WHOIS")
            print(whois2(dom))
        except:
            print('No tiene puertos abiertos')
            print("WHOIS")
            print(whois2(dom))
    elif opcion == '2':
        print("MOSTRANDO LISTA DE SUBDOMINIOS \n")
        subdominioslist=get_subdomains(dom)
        for i in subdominioslist:
            print(i)
    elif opcion == '3':
        print("MOSTRANDO RANGOS\n")
        get_company_data(company,iniciorango,finalrango,asnlista,propietarios)
        for i in range(len(iniciorango)):
            print('******************************************')
            print(f" INICIO DEL RANGO:{iniciorango[i]}")
            print(f" FINAL DEL RANGO:{finalrango[i]}")
            print(f" ASN DEL RANGO:{asnlista[i]}")
            print(f" PROPIETARIO DEL RANGO:{propietarios[i]}")
            print('******************************************')
    elif opcion == '4':
        print("RESULTADO DEL CRAWLER\n")
        crawled=crawl(dom)
        for i in crawled:
            print(i)
    elif opcion == '5':
        print("GENERANDO INFORME")

        if len(subdominioslist)==0:
            subdominioslist=get_subdomains(dom)
            pasar_DB_sub()

        else:
            pasar_DB_sub()

        if len(iniciorango)==0:
            get_company_data(company, iniciorango, finalrango, asnlista, propietarios)

        pasar_DB_rangos()

        puerto='PUERTOS ABIERTOS: '
        try:

            puertosabiertos = get_puertos(dom)
            for i in puertosabiertos:
                puerto=puerto+f"TCP: {i}"
        except:

            puerto='PUERTOS:  No tiene puertos abiertos'


        archivo = open(f"{company}.txt", "w")
        archivo.write(f"IP: {get_ip(dom)}\n {puerto} \n WHOIS:{whois2(dom)}")
        archivo.close()

        archivo2 = open(f"{company}_crawling.txt", "w")
        archivo2.write(f"{crawl(dom)}")
        archivo2.close()




    elif opcion == 'Q':
        print("SESION CERRADA")
        break
























