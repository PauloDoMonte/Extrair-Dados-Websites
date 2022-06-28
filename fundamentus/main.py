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
    acoes['MrgLiq'] = MrgLiq
    acoes['LiqCorrente'] = LiqCorrente
    acoes['ROIC'] = ROIC
    acoes['ROE'] = ROE
    acoes['Liq2Meses'] = Liq2Meses
    acoes['PatriLiquido'] = PatriLiquido
    acoes['DivBruta_por_Patri'] = DivBruta_por_Patri
    acoes['Cresc_5a'] = Cresc_5a

    resumo.append(acoes)

    try:
        papel = Cresc_5a.findNext('td').span.a.contents[0]
        cotacao = papel.findPrevious('td').findNext('td').contents[0]

    except HTTPError as e:
        print(e.status, e.reason)

database = pd.DataFrame(resumo)

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
database['Cresc_5a'] = database['Cresc_5a'].str.replace('.','',regex=True).replace(',','.',regex=True).replace('%','',regex=True)
convert_dict = {'Cresc_5a': float}
database['Cresc_5a'] = database['Cresc_5a'].astype(convert_dict)/100

# Tratamento de dados campo DividendYield
database['DividendYield'] = database['DividendYield'].str.replace('.','',regex=True).replace(',','.',regex=True).replace('%','',regex=True)
convert_dict = {'DividendYield':float}
database['DividendYield'] = database['DividendYield'].astype(convert_dict)/100

# Tratamento de dados campo ROIC
database['ROIC'] = database['ROIC'].str.replace('.','',regex=True).replace(',','.',regex=True).replace('%','',regex=True)
convert_dict = {'ROIC': float}
database['ROIC'] = database['ROIC'].astype(convert_dict)/100

# Tratamento de dados campo PVP
database['PVP'] = database['PVP'].str.replace('.','',regex=True).replace(',','.',regex=True)
convert_dict = {'PVP': float}
database['PVP'] = database['PVP'].astype(convert_dict)

# Tratamento de dados campo EVEbit
database['EVEbit'] = database['EVEbit'].str.replace('.','',regex=True).replace(',','.',regex=True)
convert_dict = {'EVEbit': float}
database['EVEbit'] = database['EVEbit'].astype(convert_dict)

# Tratamento de dados campo EVEbita
database['EVEbita'] = database['EVEbita'].str.replace('.','',regex=True).replace(',','.',regex=True)
convert_dict = {'EVEbita': float}
database['EVEbita'] = database['EVEbita'].astype(convert_dict)

# Filtragem de dados para selecionar as melhores acoes
selecao = (database['PL'] >= 1) & (database['ROE'] > 0) & (database['ROE'] < 90) & (database['MrgLiq'] > 0) & (database['DivBruta_por_Patri']>1.3) & (database['Cresc_5a']>0.1)

melhores_acoes = database[selecao].sort_values('PL',ascending=False)
melhores_acoes.to_csv("melhores_acoes.csv")

# Visualização com gráficos
import matplotlib.pyplot as plt

plt.rc('figure',figsize=(30,10))
plt.rc('font',family='serif',size=8)
area = plt.figure()

dados_g1 = melhores_acoes.sort_values(by='PL', ascending=False)
plt.barh(dados_g1.Papel,dados_g1.PL)
plt.title('PL por ação')
plt.show()

dados_g2 = melhores_acoes.sort_values(by='PVP', ascending=False)
plt.barh(dados_g2.Papel,dados_g1.PVP)
plt.title('PVP por ação')
plt.show()

area
