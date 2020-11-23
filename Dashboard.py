import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import pandas as pd

#Criação de listas que irão armazenar os dados
datas_totais = []
voos_domesticos = []
voos_internacionais = []
total_de_buscas_voos = []
dados = open('Gráfico 1.csv', 'r') #Arquivo .CSV é colocado em uma lista
for linha in dados: #Leitura de linha por linha do arquivo
    data, domes, inter, total = linha.split(';')  #Sepação de cada elemento da linha em outras quatro variáveis
    datas_totais.append(data) #Adição da data de cada linha a lista
    voos_domesticos.append(domes) #Adição da porcentagem de domésticas de cada linha a lista
    voos_internacionais.append(inter) #Adição da porcentagem de internacionais de cada linha a lista
    total_de_buscas_voos.append(total) #Adição da porcentagem do total de buscas de cada linha a lista
#Deleta-se o primeiro elemento de cada lista por ser utilizado apenas para denominar as colunas no arquivo
del voos_domesticos[0]
del voos_internacionais[0]
del datas_totais[0]
del total_de_buscas_voos[0]

meses = ['Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', #É definida uma lista de valores para o filtro
 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Total']

#Função que ira receber um período escolhido no filtro e devolver os valores a serem exibidos
def escolhe_meses(mes_do_filtro):
    meses_abreviados = ['fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'total'] #Lista com as abreviações dos meses para facilitar a leitura do arquivo
    datas_x = [] #Lista que ira receber as datas filtradas a serem exibidas em X
    domesticas_y = [] #Lista que ira receber a porcentagem de buscas domésticas a serem exibidas no eixo Y
    internacionais_y = [] #Semelhante a lista anterior, só que com buscas internacionais
    total_de_buscas_y = [] #Semelhante a busca anterior, só que com o total de buscas

    #Ira ler a lista de meses e meses_abreviados ao mesmo tempo por meio da função "ZIP"
    for mes, abreviação in zip(meses, meses_abreviados): 
        if mes_do_filtro == mes: #Caso o mês escolhido para o parâmetro da função for igual ao mês lido pela função "FOR"...
            mes_escolhida = abreviação #É guardado em uma variável a abreviação correspondente ao mês escolhido
    for data in datas_totais: #Lê data por data
        posição = datas_totais.index(data) #Localiza e guarda em uma variável a posição de uma data específica 
        data = data.split() #Os elementos dessa data são divididos em uma lista de três elementos("15 de fev"->["15","de","fev"])
        if data[2] == mes_escolhida: #Se o último elemento dessa lista anteriormente criada for correspondente ao a abreviação do mês escolhido...
            data = " ".join(data) #Transforma-se e se armazena em uma variável os 3 elementos em um separados por um espaço, por meio do comando "JOIN"
            datas_x.append(data) #A lista com as datas filtradas recebe a data correspondente ao mês escolhido
            #A posição anteriormente definidade é usada para adicionar os dados restantes em suas listas, uma vez que todas as posições são correspondentes ao mesmo dado
            domesticas_y.append(voos_domesticos[posição])
            internacionais_y.append(voos_internacionais[posição])
            total_de_buscas_y.append(total_de_buscas_voos[posição])
        #Caso seja escolhido o total, são atribuidos todos os dados as suas respectivas listas
        if mes_escolhida == 'total':
            datas_x = datas_totais
            domesticas_y = voos_domesticos
            internacionais_y = voos_internacionais
            total_de_buscas_y = total_de_buscas_voos
    return datas_x, domesticas_y, internacionais_y, total_de_buscas_y #Retorna-se as quatro listas de dados filtradas


abreviaçao_regioes = ['CO', 'N', 'S', 'SE', 'NE'] #Lista que será usada como valor para os filtros
regioes = ['Centro Oeste', 'Norte', 'Sul', 'Sudeste', 'Nordeste'] #Lista que será usada como nome para os filtros

#Criação de listas que armazenarão os tipos de dados
total_regioes = []
total_cidades = []
antes_pandemia = []
pos_pandemia = []
dados = open('dadosgrafico3.csv', 'r') #Leitura do arquivo .CSV que contém os dados

#Será lida linha por linha do arquivo
for linha in dados: 
    regiao, cidade, antes, depois = linha.split(',') #Cada elemento da lista separado por vírgula é separado por .SPLIT e armazenado em uma variável
    #Cada variável com o dado correspondente é armazenada em sua respectiva lista
    total_regioes.append(regiao)
    total_cidades.append(cidade)
    antes_pandemia.append(antes)
    pos_pandemia.append(depois)

#Função ESCOLHE_REGIAO receberá como parãmetro uma região para filtrar seus dados
def escolhe_regiao(regiao_escolhida): #Recebe como parâmetro "regiao_escolhida", que será alguma abreviação escolhida posteriormente no filtro
    #Listas que irão armazenar e devolver os dados filtrados
    cidades_filtradas = []
    medias_anterior_filtrada = []
    media_posterior_filtrada = []
    x = 0 #Variável que será utilizada para escolher a localização dos dados
    for reg in total_regioes: #Serão lidas todas as regiões (primeira coluna do arquivo)
        if reg == regiao_escolhida: #Caso a região que está sendo lida seja igual a abreviação da região escolhida (Parâmetro da função)...
            posiçao = total_regioes.index(reg) + x #É localizada a PRIMEIRA aparição abreviação da região na lista com todas as regiões(0, 1, 2 ,3 ...)
            #Uma vez que todas as listas correspondem ao mesmo número de elementos, utiliza-se a posição anteriormente definida para localizar todos os elementos correspondentes 
            cidades_filtradas.append(total_cidades[posiçao])
            medias_anterior_filtrada.append(antes_pandemia[posiçao])
            media_posterior_filtrada.append(pos_pandemia[posiçao])
            x = x + 1 #É somado um a variável X, para que na escolha de posição possa se escolher sempre a linha de dados seguinte a primeira incidência da abreviação da região
    return cidades_filtradas, medias_anterior_filtrada, media_posterior_filtrada #Devolve-se as três listas com os dados filtrados


df = pd.read_csv('Gráfico2(01.11).csv', encoding='UTF-8', sep=';')
cidades = df['CIDADE'].unique()
#Função que irá criar as linhas do gráfico caso sejam escolhidos no filtro mais de uma cidade
def cria_linhas(cidade):
    dados = df.values #O data frame é tranformado em um array(uma lista que armazena só um tipo de elemento, string, int float, etc. Além disso seu tamanho não pode ser modificado)
    porcentagens = [] #Lista que armazenará as porcentagens filtradas
    semanas = [] #Lista que armazenará as semanas filtradas
    for dado in dados: #Serão lidas as listas detro do array(correspondentes as linhas do arquivo)
        if dado[1] == cidade: #Se o dado[1] (posição da cidade), for igual a cidade escolhida como parâmetro...
            semanas.append(dado[0]) #O dado correspondente a semana é guardado na lista correspondente
            porcentagens.append(dado[2]) #O dado referente a porcentagem é guardado na lista correspondente
    #Se cria a linha que será exibida no gráfico
    linhas = go.Scatter(
        x = semanas,
        y = porcentagens,
        name = cidade #A cidade escolhida como parâmetro será o nome da linha
        )
    return linhas

#Configurações layout Dash
external_stylesheets = ['https://bootswatch.com/4/lux/bootstrap.css']
cores = ['#f7f7f9', '#007bff', '#d9534f', '#f0ad4e', '#1a1a1a']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Nav([
            #html.Img(src = app.get_asset_url('Rectangle.png')),
           # html.Img(src = app.get_asset_url('Aero Trends.png')),
            html.H3(children = 'Variação na procura de viagens aéreas no Brasil Pandemia COVID19', className = "navbar-brand"),
            ], className = "navbar navbar-expand-lg navbar-dark bg-primary"),
    html.Div([
    html.Div([html.H5('Descrição')], className = "card-header"),
    html.Div([
        html.P(children ='Devido a pandemia da COVID-19, houve uma grande interrupção no mercado de viagens e turismo no Brasil, fazendo com que o setor de viagens aéreas tivessem que alterar abruptamente suas fontes de recursos. Dito isso, nosso dashboard busca demonstrar de forma gráfica dados que podem ser úteis para tomadas de decisões nesse novo panorama da indústria. Tendo enfoque no total de buscas de voos domésticos e internacionais, em destinos com maior aumento nas buscas e na porcentagem de procura por região, nosso objetivo é atingir companhias aéreas, empresas de turismo e aplicativos de viagem de forma a demonstrar uma alternativa de otimização a seus recursos e estratégias.', className = "card-text")
    ], className = "card-body"),
    ], className = "card border-primary mb-3"),
    html.Div([
        html.Div([
            html.H4(
                children = 'Variação na procura por vôos nacionais e internacionais'),
            dcc.Dropdown(
                id = "filtro gráfico1",
                options = [{'label': mes, 'value': mes}for mes in meses],
                value = 'Total',
                clearable = False),
        ], className = 'dropdown-menu-sm-left'),
        dcc.Graph(
            id = "Gráfico1")
    ], className = "jumbotron"),
    html.Br(),
    html.Div([
        html.H4(
                children='A procura por vôos no Brasil'),
            html.Label(['Escolha as cidades para comparar:'],
                    style={'font-weight': 'bold', 'color' : cores[4]}),
            dcc.Dropdown(id='cidades',
                        options=[{'label': cidade, 'value': cidade}
                                for cidade in cidades],
                        value='Brasil',
                        multi=True,
                        disabled=False,
                        clearable=False,
                        searchable=True,
                        placeholder='Escolha a cidade...'),
            dcc.Graph(id='Gráfico2')
    ], className ="jumbotron"),
    html.Br(),
    html.Div([
        html.H4(
            children = 'A procura por voos nacionais antes e durante a Pandemia COVID19'),
        dcc.Dropdown(
            id = "filtro gráfico3",
            #Será criado uma opção de filtro para cada elemento das listas REGIOES('Nordeste', 'Sul'...)
            options = [{'label': regiao, 'value': abreviaçao}for regiao, abreviaçao in zip(regioes, abreviaçao_regioes)], #O nome do filtro recebe o nome da região e o valor do filtro recebe sua respectiva abreviação, sendo lidas duas listas ao mesmo tempo através do comando ZIP 
            value = 'NE', #Valor inicial a ser exibido é o Nordeste 
            clearable = False
        ),
        dcc.Graph(
            id = "Gráfico3"),
    ], className = "jumbotron"),
], style = {'margin': '8%','font-family': '"Nunito Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"', 'font-size': '0.875rem', 'font-weight': '400', 'line-height': '1.5', 'color': '#55595c', 'text-align': 'left', 'background-color': '#fff'})


@app.callback(
    Output(component_id='Gráfico1', component_property= 'figure'),
    [Input(component_id='filtro gráfico1', component_property='value')]
)

def update_gráfico(filtro):
    dados = escolhe_meses(filtro) #filtra-se os dados pela função "escolhe meses" e armazena-se em uma lista
    datas = dados[0] #A lista de datas filtradas(primeiro elemento da lista "dados") são armazenadas em uma variável
    domesticas = dados[1]
    internacionais = dados[2]
    total_de_buscas = dados[3]
    #Criação das linhas do gráfico
    trace1 = go.Scatter(x = datas, #As datas são atribuídas ao eixo X 
                    y = domesticas, #As porcentagens de busca por voos domésticos são atribuídos ao eixo Y
                    name = 'Nacionais', #Definido um nome a linha
                    text = datas, #Variável recebe os valores de X para exibição na função HOVER 
                    mode = 'lines', #É definido o tipo do gráfico
                    line = dict(color = '#1e3799', width = 3), #Atribuido uma cor para a linha 'Domésticas'
                    hovertemplate = '%{y}'.center(8) + '<br>'  + '%{text}' #São utilizados o as informações de Y e de X para vizualização do dado
                    )

    trace2 = go.Scatter(x = datas,
                    y = internacionais,
                    mode = 'lines',
                    name = 'Internacionais',
                    text = datas,
                    line = dict(color = '#e58e26', width = 3),
                    hovertemplate = '%{y}'.center(8) + '<br>'  + '%{text}'
                    )

    trace3 = go.Scatter(x = datas,
                    y = total_de_buscas,
                    mode = 'lines',
                    name = 'Total de buscas',
                    text = datas,
                    line = dict(color = '#6ab04c', width = 3),                
                    hovertemplate = '%{y}'.center(8) + '<br>'  + '%{text}'
    )

    gráfico_de_linhas = [trace1, trace2, trace3] #Todas as linhas do gráfico são armazenadas em uma lista

    fig = go.Figure(gráfico_de_linhas) #A lista com as variáveis é transformada em um objeto para ser vizualizada na forma do gráfico

    #Definição do passo para exibição da legenda em X
    if len(datas) > 18: #Caso a quantidade de Datas for maior que 18...
        variação_legenda_x = len(datas)//18 #Divide-se a a quantidade de datas por 18, de forma que sejam exibidos no máximo 18 datas
    else: #Caso a quantidade de datas seja menor ou igual a 18...
        variação_legenda_x = 1 #Será atribuído passo 1 de forma a exibir todos as datas

    fig.update_layout( #Deifição das configurações de layout
        xaxis_title =dict( #Adição de um título que deixará mais claro que tipo de informação será exibida no eixo X
            text = "<b>Data<b>", #Texto que será exibido, colocado em negrito para maior destaque por meio do comando "<b><b>", da linguagem html
            font = dict( #São atribuídas algumas propriedades para o texto
                family = 'Arial', #A fonte do texto
                color = cores[4], #A cor do texto
                size = 16 #Tamanho do texto em pixels
            )
        ),
        legend = dict(font= dict(color = cores[4])),
        xaxis = dict( #São atribuídas propriedades para o eixo X e para seus dados
            rangeslider=dict(visible=True), #Um filtro do próprio Plotly
            showline = True, #Mostrar a linha do Eixo X
            tickcolor = cores[4],
            tickmode = "linear", #É atribuído 'linear' no tipo de 'tick' para que se possa definir um valor incial para a exibição dos valores em X(tick0) e um passo(dtick)
            tick0 = datas[0], #Primeiro dado a ser exibido na legenda de X, no caso a primeira data
            dtick = variação_legenda_x, #Passo no qual os dados serão exibidos por meio da variável anteriormente definida
            tickfont = dict(
                color = cores[4]
            ),
            showgrid = False, #Não mostrar a grade de linhas do eixo X
            linecolor = cores[4], #Cor da linha do eixo X
            linewidth = 2, #Espessura da linha do eixo X
            ticks = 'outside' #Adição de "traços" do lado de fora do gráfico para melhor vizualização dos dados
        ),
        yaxis = dict( #Atribuição de propriedades para o eixo Y e seus respectivos dados
            gridcolor = cores[4], #Definição da cor da grade de linhas do eixo Y
            zeroline = False, #Para que a linha zero do eixo Y se mostre é atribuido "False" ao comando "zeroline"
            linecolor = cores[4], #É atrbuído uma cor a linha do eixo Y
            showticklabels = False, #É dado o comando para não mostrar a legenda padrão do Plotly
            ticksuffix = '%' #É adicionado '%' ao final de todos os dados do eixo Y
        ),
        margin = dict( #Configurações com relação as margens do gráfico
            t = 50, #Distância do gráfico do topo da página em pixels
            l = 100 #Distância do gráfico da lateral esquerda em pixels
        ),
        height = 580, #Altura do gráfico em pixels
        plot_bgcolor = cores[0], #Definição de cor do background do gráfico
        paper_bgcolor = cores[0],
        hoverlabel = dict( #Atrubuição das propriedades para o HOVER
            bgcolor = '#3F3F3F', #Cor do background do HOVER
            align = 'auto', #Alinhamento do texto do hover automático
            font = dict( #Configurações para o texto do hover
                family = 'Arial', #Fonte do texto
                size = 16, #Tamanho do texto em pixels
                color = 'white' #Cor do texto
            )
        )
    )

    annotations = [] #Criação da lista anotações que ira ser utilizada pra duas legendas do eixo Y e a fonte de origem dos dados
    valores_de_y = [-50, 0, 50, 100] #Valores que serão exibidos no eixo Y

    for valor_y in valores_de_y: #Se percorre toda a lista anteriormente criada
        annotations.append(dict( #Cada valor da lista é adicionado com uma série de propriedades a lista "annotations"
            xref = 'paper', #Coordenada da informação no eixo X, recebe 'paper' que irá definir toda a extensão do gráfico como valendo 1
            x = 0.00005, #Coordenado do eixo X sendo definida entre 0 e 1, de acordo com a função 'paper' anteriormente definida
            y = valor_y, #A coordenada no eixo Y é definida de acordo com os elemntos da lista, uma vez que os mesmos são números
            xanchor = 'right', #Orientação do texto com relação ao eixo X
            yanchor = 'middle', #Orientação do texto com relação ao eixo Y
            text ='{}%'.format(valor_y), #Definição do texto que será exibido
            font = dict(color = cores[4]),
            showarrow = False #Não mostrar uma seta indicando a coordenada exata das anotações
        ))

    #Definição de uma legenda  no eixo Y para deixar claro a que se referem as informações
    annotations.append(dict(
        xref = 'paper', x = -0.07, y = -80,
        xanchor = 'right', yanchor = 'bottom',
        text ='<b>Porcentagem de busca por voos<b>',
        textangle = -90, #Inclinação do texto na vertical para melhor vizualização no eixo Y
        font = dict(
            family = 'Arial',
            size = 16,
            color = cores[4]
        ),
        showarrow = False 
        ))

    fig.update_layout(annotations = annotations) #A lista com todas as legendas e outras informações são atribuidas ao comando annotations, e adicionadas as configurações de layout
    return fig 

@ app.callback(
    Output(component_id='Gráfico2', component_property='figure'),
    [Input(component_id='cidades', component_property='value')]
)
def update_graph(cidades):
    gráfico = [] #Lista que irá armazenar as linhas do gráfico
    if type(cidades) == list: #Caso a opção de filtro escolhida for mais de uma cidade, o parâmetro será uma lista e o 'if' será executado
        for cidade in cidades: #Como são duas cidades ou mais, será lido elemento por elemento da lista
            gráfico.append(cria_linhas(cidade)) #Cada uma das cidades será colocada como parâmetro da função 'cria_linhas', anteriormente apresentada
    else: #Caso a opção de filtro escolhida for uma cidade apenas o comando 'else' é executado 
        gráfico.append(cria_linhas(cidades)) #Será criada apenas uma linha com a função 'cria_linhas'

    fig = go.Figure(gráfico) #Todas as linhas do gráfico (seja uma ou mais linhas) guardadas na lista 'gráfico' são tranformados em um objeto para serem exibidas como o gráfico em si
    fig.update_layout(xaxis = dict(
                        title = dict(
                            text = '<b>Semanas<b>',
                            font = dict(color = cores[4])),
                        tickfont = dict(color = cores[4])),
                    yaxis= dict(
                        linecolor = cores[4],
                        ticksuffix = '%',
                        title = dict(
                            text = '<b>Porcentagem da busca por voos (%)<b>',
                            font = dict(color = cores[4])),
                          tickfont = dict(color = cores[4])),
                      yaxis_zeroline = False,
                      yaxis_gridcolor = cores[4],
                      plot_bgcolor = cores[0],
                      paper_bgcolor = cores[0],
                      legend = dict(font = dict(color = cores[4])),
                      xaxis_showgrid = False)
    return fig

@app.callback(
    Output(component_id='Gráfico3', component_property= 'figure'),
    [Input(component_id='filtro gráfico3', component_property='value')]
)
#Função que irá receber o filtro e gerar o gráfico
def upgrade_graph(filtro):
    dados = escolhe_regiao(filtro) #Serão armazenados os dados filtrados pela função "escolhe_região" que receberá como parâmetro alguma das regiôes escolhidas no filtro 
    #Como a lista "dados" é uma lista de listas, serão separados seus elementos(no caso as listas filtradas) em outras listas para serem colocadas nos eixos X e Y
    cidades = dados[0]
    media1 = dados[1]
    media2 = dados[2]
    trace1 = go.Bar(x = cidades,
                    y = media1,
                    name = 'Antes da Pandemia',
                    marker = {'color': '#40407a'})
    trace2 = go.Bar(x = cidades,
                    y = media2,
                    name = 'Durante a Pandemia',
                    marker = {'color': '#cc8e35'})
    data = [trace1, trace2]
    layout = go.Layout(title = dict(
        font = dict(color = cores[4])),
                   plot_bgcolor = cores[0],
                   paper_bgcolor = cores[0],
                   legend = dict(font = dict(color = cores[4])),
                   yaxis=dict(
                       linecolor = cores[4],
                       gridcolor = cores[4],
                       zeroline = False,
                       tickfont = dict(color = cores[4]),
                       ticksuffix = '%',
                       title = dict(
                           text = '<b> Porcentagem de procura por vôos (%)<b>',
                           font = dict(color = cores[4]))),
                   xaxis=dict(
                       tickfont = dict(color = cores[4]),
                       title = dict(
                           text = '<b>Cidades<b>',
                           font = dict(color = cores[4]))))
    fig = go.Figure(data=data, layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)