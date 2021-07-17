import requests as req
import datetime as dt
import csv
from PIL import Image
from urllib.parse import quote
from IPython.display import display


url = 'https://api.covid19api.com/dayone/country/brazil'
r = req.get(url)

# print(r.status_code) checando se deu tudo certo !

raw_data = r.json()  # guardar dados retornados da api

# print(raw_data[0])  # verificar os dados q quero armazenar

final_data = []
for obs in raw_data:
    final_data.append([obs['Confirmed'], obs['Deaths'],
                       obs['Recovered'], obs['Active'], obs['Date']])


final_data.insert(0, ['CONFIRMADOS', 'OBITOS',
                      'RECUPERADOS', 'ATIVOS', 'DATA'])

CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4

# pegando apenas os 10 f char de DATA
for i in range(1, len(final_data)):
    final_data[i][DATA] = final_data[i][DATA][:10]

# guardar arquivo em csv
with open('brasil_covid.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)

# transformar str data em datetime
for i in range(1, len(final_data)):
    final_data[i][DATA] = dt.datetime.strptime(
        final_data[i][DATA], '%Y-%m-%d')

print(final_data)


def get_datasets(y, labels):
    if type(y[0]) == list:  # verificar se é lista ou valor comum
        datasets = []  # iniciar lista
        for i in range(len(y)):
            datasets.append({  # jogar len y na lista um dict
                # chave label contem label na posicao atual
                'label': labels[i],
                'data': y[i]  # contem y na posicao atual
            })
        return datasets
    else:  # caso y nao seja uma lista de listas
        return[{
            'label': labels[0],  # unica valor
            'data': y
        }]


def set_title(title=''):
    if title != '':
        display = 'true'
    else:
        display = 'false'
    return{
        'title': title,
        'display': display
    }


def create_chart(x, y, labels, kind='bar', title=''):
    datasets = get_datasets(y, labels)
    options = set_title(title)

    chart = {  # dict que representa o grafico
        'type': kind,
        'data': {
            'labels': x,  # valores de x
            'datasets': datasets  # valores de datasets
        },
        'options': options
    }
    return chart

# retonar arquivo de imagem


def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    resp = req.get(f'{url_base}?c={str(chart)}')
    return resp.content


def save_image(path, content):
    with open(path, 'wb') as img:
        img.write(content)


def display_img(path):
    img_pil = Image.open(path)
    display(img_pil)


y_data_1 = []
for obs in final_data[1::10]:
    y_data_1.append(obs[CONFIRMADOS])

y_data_2 = []
for obs in final_data[1::10]:
    y_data_2.append(obs[RECUPERADOS])

labels = ['Confirmados', 'Recuperados']

x = []
for obs in final_data[1::10]:
    x.append(obs[DATA].strftime('%d/%m/%Y'))

chart = create_chart(x, [y_data_1, y_data_2], labels,
                     title='Confirmados vs Recuperados')
chart_content = get_api_chart(chart)
save_image('first_graph.png', chart_content)
display_img('first_graph.png')

# QR CODE


def get_api_qrcode(link):
    text = quote(link)
    url_base = 'https://quickchart.io/qr'
    r = req.get(f'{url_base}?text={text}')
    return r.content


url_base = 'https://quickchart.io/chart'
link = f'{url_base}?c={str(chart)}'
save_image('qr-code.png', get_api_qrcode(link))
display_img('qr-code.png')
