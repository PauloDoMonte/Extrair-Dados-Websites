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

    resumo.append(acoes)

    try:
        papel = Cresc_5a.findNext('td').span.a.contents[0]
        cotacao = papel.findPrevious('td').findNext('td').contents[0]

    except HTTPError as e:
        print(e.status, e.reason)

database = pd.DataFrame(resumo)
print(database.head())
