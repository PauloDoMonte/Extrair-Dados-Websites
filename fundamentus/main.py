from urllib.request import urlopen, urlretrieve, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.fundamentus.com.br/resultado.php"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606 Safari/537.36"}

req = Request(url,headers=headers)
response = urlopen(req)
html = response.read()
soup = BeautifulSoup(html,'html.parser')

lista = soup.find('table')
qtd = soup.findAll('span',class_='tips')
qtd = range(int(len(qtd)-1))

resumo = []

papel = lista.find('td').find('span',class_='tips').getText()
cotacao = lista.find('td').findNext('td').contents[0]

for i in qtd:

    acoes = {}

    PL = cotacao.findNext('td').contents[0]
    PVP = PL.findNext('td').contents[0]
    PSR = PVP.findNext('td').contents[0]
    DividendYield = PSR.findNext('td').contents[0]
    PAtivo = DividendYield.findNext('td').contents[0]
    PCapGiro = PAtivo.findNext('td').contents[0]
    PEbit = PCapGiro.findNext('td').contents[0]
    PAtivoCirc = PEbit.findNext('td').contents[0]
    EVEbit = PAtivoCirc.findNext('td').contents[0]
    EVEbita = EVEbit.findNext('td').contents[0]
    MrgEbit = EVEbita.findNext('td').contents[0]
    MrgLiq = MrgEbit.findNext('td').contents[0]
    LiqCorrente = MrgLiq.findNext('td').contents[0]
    ROIC = LiqCorrente.findNext('td').contents[0]
    ROE = ROIC.findNext('td').contents[0]
    Liq2Meses = ROE.findNext('td').contents[0]
    PatriLiquido = Liq2Meses.findNext('td').contents[0]
    DivBruta_por_Patri = PatriLiquido.findNext('td').contents[0]
    Cresc_5a = DivBruta_por_Patri.findNext('td').contents[0]

    acoes['id'] = i
    acoes['Papel'] = papel
    acoes['Cotacao'] = cotacao
    acoes['PL'] = PL
    acoes['PVP'] = PVP
    acoes['PSR'] = PSR
    acoes['DividendYield'] = DividendYield
    acoes['PAtivo'] = PAtivo
    acoes['PCapGiro'] = PCapGiro
    acoes['PEbit'] = PEbit
    acoes['PAtivoCirc'] = PAtivoCirc
    acoes['EVEbit'] = EVEbit
    acoes['EVEbita'] = EVEbita
    acoes['MrgEbit'] = MrgEbit

    resumo.append(acoes)

    try:
        papel = Cresc_5a.findNext('td').span.a.contents[0]
        cotacao = papel.findPrevious('td').findNext('td').contents[0]

    except HTTPError as e:
        print(e.status, e.reason)

database = pd.DataFrame(resumo)
print(database.head())

# Tratamento de dados campo PL
database['PL'] = database['PL'].str.replace('.','',regex=True).replace(',','.',regex=True)
convert_dict = {'PL':float}
database['PL'] = database['PL'].astype(convert_dict)

# Tratamento de dados campo ROE
database['ROE'] = database['ROE'].str.replace('.','',regex=True).replace(',','.',regex=True).replace('%','',regex=True)
convert_dict = {'ROE': float}
database['ROE'] = database['ROE'].astype(convert_dict)/100

# Tratamento de dados campo MrgLiq
database['MrgLiq'] = database['MrgLiq'].str.replace('.','',regex=True).replace(',','.',regex=True).replace('%','',regex=True)
convert_dict = {'MrgLiq': float}
database['MrgLiq'] = database['MrgLiq'].astype(convert_dict)/100

# Tratamento de dados campo Divida Bruta/Patrimonio
database['DivBruta_por_Patri'] = database['DivBruta_por_Patri'].str.replace('.','',regex=True).replace(',','.',regex=True)
convert_dict = {'DivBruta_por_Patri': float}
database['DivBruta_por_Patri'] = database['DivBruta_por_Patri'].astype(convert_dict)

# Tratamento de dados campo CAGER
database['Cresc_5a'] = database['Cresc_5a'].str.replace('.',',',regex=True).replace(',','.',regex=True).replace('%','',regex=True)
convert_dict = {'Cresc_5a': float}
database['Cresc_5a'] = database['Cresc_5a'].astype(convert_dict)/100

# Tratamento de dados campo DividendYield
database['DividendYield'] = database['DividendYield'].str.replace('.','',regex=True).replace(',','.',regex=True).replace('%','',regex=True)
convert_dict = {'DividendYield':float}
database['DividendYield'] = database['DividendYield'].astype(convert_dict)/100

# Tratamento de dados campo ROIC
