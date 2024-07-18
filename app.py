from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from data_process import df
import pandas as pd
import re
from plotly.subplots import make_subplots
import plotly.graph_objects as go

load_figure_template("united")


unidades = [unidade for unidade in sorted(df['unidade'].unique()) if unidade != 'nan']
areas_cnpq = [area for area in sorted(df['gde_area'].unique()) if area != 'nan']
areas_extensao = [area for area in sorted(df['area_extensao'].unique()) if area != 'nan']
tipos = ['extensão', 'ensino', 'pesquisa']
vinculos = df.vinculo.unique().tolist()

# stylesheet with the .dbc class to style  dcc, DataTable and AG Grid components with a Bootstrap theme
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.UNITED, dbc.icons.FONT_AWESOME, dbc_css], title="Mapeamento Divulgação Científica UFMG",
           suppress_callback_exceptions=True)

server = app.server

header = html.Div(
    dbc.Row(
        [
            dbc.Col(html.H4("Resultados Parciais do Mapeamento da Divulgação Científica na UFMG", className="bg-primary text-white p-2 mb-2 text-center"), width=10),
            dbc.Col(html.Img(src="assets/principal_completa_ufmg.jpg", className="float-end ms-auto", style={"height": "150px", "margin-right": "160px"}), width=2, align="end"),
        ],
        align="center",
        className="bg-primary"
    )
)

titulo_controls = html.H4("Use estes controles para filtrar os dados apresentados", className="text-left bg-primary text-white p-2 mb-2", style={"margin": "-15"})

dropdown_unidade = html.Div(
    [
        dbc.Label("Unidade"),
        dcc.Dropdown(
            options=[{"label": "Todas", "value": "Todas"}] + [{"label": unidade, "value": unidade} for unidade in unidades],
            value="Todas",
            id="unidade",
            clearable=False,
        ),
    ],
    className="mb-4",
)

dropdown_areas_cnpq = html.Div(
    [
        dbc.Label("Grande Área CNPq"),
        dcc.Dropdown(
            options=[{"label": "Todas", "value": "Todas"}] + [{"label": area, "value": area} for area in areas_cnpq],
            value="Todas",
            id="gde_area",
            clearable=False,
        ),
    ],
    className="mb-4",
)

dropdown_areas_extensao = html.Div(
    [
        dbc.Label("Área de Extensão"),
        dcc.Dropdown(
            options=[{"label": "Todas", "value": "Todas"}] + [{"label": area, "value": area} for area in areas_extensao],
            value="Todas",
            id="area_extensao",
            clearable=False,
        ),
    ],
    className="mb-4",
)

checklist_tipos = html.Div(
    [
        dbc.Label("Tipo de ação de Divulgação Científica"),
        dbc.Checklist(
            id="tipo",
            options=tipos,
            value=tipos,
            inline=True,
        ),
    ],
    className="mb-4",
)

checklist_vinculos = html.Div(
    [
        dbc.Label("Vínculo com a UFMG"),
        dbc.Checklist(
            id="vinculo",
            options=vinculos,
            value=vinculos,
            inline=True,
        ),
    ],
    className="mb-4",
)

posgrad = html.Div(
    [
        dbc.Label("Vínculo com Programa de Pós-Graduação?"),
        dbc.RadioItems(
            id="posgrad",
            options=[
                {"label": "Sim", "value": "Sim"},
                {"label": "Não", "value": "Não"},
                {"label": "Qualquer", "value": "Qualquer"}
            ],
            value="Qualquer",
            inline=True,
        ),
    ],
    className="mb-4",
)


controls = dbc.Card(
    [titulo_controls, checklist_tipos, dropdown_areas_cnpq, dropdown_areas_extensao, checklist_vinculos, dropdown_unidade, posgrad],
    body=True,
)

# Conteúdo da aba "Sobre"
sobre_content = html.Div([
    html.H3("Sobre o Mapeamento"),
    html.P("""
        Este dashboard apresenta resultados paricias do Mapeamento de Divulgação Científica da UFMG.
        O mapeamento ainda está aberto para preenchimento de toda a comunidade acadêmica da UFMG
        que atua no âmbito do ensino, da pesquisa e da extensão em divulgação científica.
    """),
    html.P("""
        Através deste mapeamento, esperamos reunir informações que nos orientem na 
        elaboração de políticas institucionais e que contribuam para a promoção de 
        processos solidários e sinérgicos na divulgação científica.
    """),
    html.P("""
        Se você participa de alguma ação de ensino, pesquisa ou extensão que tenha como 
        objetivo o compartilhamento do conhecimento gerado na universidade com o público 
        não especializado, sua colaboração é fundamental. Por favor, responda ao 
        questionário clicando no botão abaixo.
    """),
    html.Div(
        dbc.Button("Clique aqui para responder", color="primary", className="me-1", href="https://questionarios.ufmg.br/index.php/286584?lang=pt-BR", target="_blank"),
        className="d-flex justify-content-center"
    )
])

sobre = dbc.Tab(label="Sobre", children=[sobre_content])

tab_vinculos = dbc.Tab([dcc.Graph(id="fig_vinculos", figure=px.bar(template="plotly"))], label="Vínculos")
tab_tipo = dbc.Tab([dcc.Graph(id="fig_tipo", figure=px.pie(template="plotly"))], label="Tipo")
tab_gde_area = dbc.Tab([dcc.Graph(id="fig_grande_area", figure=px.bar(template="plotly"))], label="Grande Área")
tab_area_ext = dbc.Tab([dcc.Graph(id="fig_area_extensao", figure=px.bar(template="plotly"))], label="Área de Extensão")
tab_publicos = dbc.Tab([dcc.Graph(id="fig_publicos", figure=px.bar(template="plotly"))], label="Públicos Alvo")
tab_unidades = dbc.Tab([dcc.Graph(id="fig_unidades", figure=px.bar(template="plotly"))], label="Unidades")
tab_redes = dbc.Tab([dcc.Graph(id="fig_socialmedia", figure=px.bar(template="plotly"))], label="Redes Sociais")

tabs = dbc.Card(dbc.Tabs([tab_tipo, tab_gde_area, tab_area_ext, tab_publicos, tab_unidades, tab_vinculos, tab_redes, sobre]))

card_n = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Resultados coletados até 02/07/2024"),
            html.H4("Nº de registros"),
            html.H5(f"Total: {len(df)}"),
            html.H5(id="n_filtrado"),
        ],
        className="text-center"
    ),
    color="primary",
    inverse=True
)

footer = html.Footer(
    dbc.Container(
        dbc.Row(
            dbc.Col(
                [html.P(
                    [
                        " Dashboard desenvolvido por ",
                        html.A("Marcelo Pereira", href="https://marcelo-pereira.notion.site/", target="_blank"),
                        " ",
                        html.I(className="fa-brands fa-creative-commons"),
                        ', 2024'
                    ],
                    className="text-center"
                ),
                ]
            )
        ),
        fluid=True,
        className="py-3"
    ),
    className="footer bg-light text-dark mt-auto"
)

app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col(controls, width=2),
                dbc.Col([tabs, card_n], width=10),
            ],
            className="mt-4",
        ),
        footer
    ],
    fluid=True,
    className="dbc dbc-ag-grid",
)



@callback(
    Output("fig_vinculos", "figure"),
    Output("fig_tipo", "figure"),
    Output("fig_grande_area", "figure"),
    Output("fig_area_extensao", "figure"),
    Output("fig_publicos", "figure"),    
    Output("fig_unidades", "figure"),
    Output("fig_socialmedia", "figure"),
    Output("n_filtrado", "children"),
    Input("unidade", "value"),
    Input("gde_area", "value"),
    Input("area_extensao", "value"),
    Input("tipo", "value"),
    Input("vinculo", "value"),
    Input("posgrad", "value"),
)
def update(unidade="Todas", gde_area="Todas", area_extensao="Todas", tipo=tipos, vinculo=vinculos, posgrad="Qualquer"):

    dff = df.copy()
    
    if unidade != "Todas":
        dff = dff[dff['unidade'] == unidade]
    if gde_area != "Todas":
        dff = dff[dff['gde_area'] == gde_area]
    if area_extensao != "Todas":
        dff = dff[dff['area_extensao'] == area_extensao]
    if 'extensão' not in tipo:
        dff = dff[dff['extensão'] == 0]
    if 'ensino' not in tipo:
        dff = dff[dff['ensino'] == 0]
    if 'pesquisa' not in tipo:
        dff = dff[dff['pesquisa'] == 0]
    if vinculo:
        dff = dff[dff['vinculo'].isin(vinculo)]
    if posgrad != "Qualquer":
        dff = dff[dff['programas'] == posgrad]

    n_filtrado = f"Filtrado: {len(dff)}"

    # Construindo o gráfico de Vínculos
    dff_vinculo_counts = dff['vinculo'].value_counts(normalize=True).reset_index()
    dff_vinculo_counts.columns = ['vinculo', 'porcentagem']
    dff_vinculo_counts['tipo'] = "Filtrado"
    df_vinculo_counts = df['vinculo'].value_counts(normalize=True).reset_index()
    df_vinculo_counts.columns = ['vinculo', 'porcentagem']
    df_vinculo_counts['tipo'] = "Total"
    consolidado = pd.concat([dff_vinculo_counts, df_vinculo_counts])

    fig_vinculos = px.bar(
        consolidado,
        x='vinculo',
        y='porcentagem',
        labels={'vinculo': '', 'porcentagem': ''},
        color='tipo',
        facet_row = 'tipo',
        title='Distribuição de Vínculos (em %)',
        category_orders={'tipo': ['Total', 'Filtrado']},
        height=750
    )

    # Construindo o gráfico de Tipo de Ação
    contagens = dff[['extensão', 'ensino', 'pesquisa']].sum()
    data_filtrada = pd.DataFrame({
        'Tipo': ['Extensão', 'Ensino', 'Pesquisa'],
        'Contagem': [contagens['extensão'], contagens['ensino'], contagens['pesquisa']],
        'Conjunto': 'Filtrado'
    })
    contagens_gerais = df[['extensão', 'ensino', 'pesquisa']].sum()
    data_geral = pd.DataFrame({
        'Tipo': ['Extensão', 'Ensino', 'Pesquisa'],
        'Contagem': [contagens_gerais['extensão'], contagens_gerais['ensino'], contagens_gerais['pesquisa']],
        'Conjunto': 'Total'
    })
    data = pd.concat([data_geral, data_filtrada])
    obs = '*Cada respondente poderia mencionar até 5 ações de Divulgação Científica.<br> Os números aqui apresentados representam o somatório de todas as ações'

    fig_tipo = make_subplots(rows=1, cols=2, subplot_titles=("Total", "Filtrado"), specs=[[{'type': 'pie'}, {'type': 'pie'}]])

    fig_tipo.add_trace(
        go.Pie(
            labels=data_geral['Tipo'],
            values=data_geral['Contagem'],
            name="Total",
            title="Total",
            textinfo='label+percent'
        ),
        row=1, col=1
    )

    fig_tipo.add_trace(
        go.Pie(
            labels=data_filtrada['Tipo'],
            values=data_filtrada['Contagem'],
            name="Filtrado",
            title="Filtrado",
            textinfo='label+percent'
        ),
        row=1, col=2
    )

    fig_tipo.update_layout(
        title_text='Distribuição das ações* de divulgação científica por tipo',
        annotations=[
            dict(
                text=obs,
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=-0.25,
                align="center",
                font=dict(size=11),
            )
        ],
        margin=dict(b=100)
    )


    # Construindo o gráfico de Grande Área CNPq
    dff_grande_area_counts = dff['gde_area'].dropna().value_counts().reset_index()
    dff_grande_area_counts.columns = ['grande_area_cnpq', 'count']
    dff_grande_area_counts['tipo'] = 'Filtrado'
    df_grande_area_counts = df['gde_area'].dropna().value_counts().reset_index()
    df_grande_area_counts.columns = ['grande_area_cnpq', 'count']
    df_grande_area_counts['tipo'] = 'Total'
    consolidado_grande_area = pd.concat([dff_grande_area_counts, df_grande_area_counts])
    fig_grande_area = px.bar(consolidado_grande_area, x='grande_area_cnpq', y='count',
                                labels={'grande_area_cnpq': '', 'count': ''},
                                title='Distribuição de ações por Grande Área CNPq (números absolutos)',
                                facet_row='tipo',
                                category_orders={'tipo': ['Total', 'Filtrado']},
                                color='tipo',
                                height=750)


    # Construindo o gráfico de Area de Extensão	
    dff_area_counts = dff['area_extensao'].dropna().value_counts().reset_index()
    dff_area_counts.columns = ['area_extensao', 'count']
    dff_area_counts['tipo'] = 'Filtrado'
    df_area_counts = df['area_extensao'].dropna().value_counts().reset_index()
    df_area_counts.columns = ['area_extensao', 'count']
    df_area_counts['tipo'] = 'Total'
    consolidado_area = pd.concat([dff_area_counts, df_area_counts])
    fig_area_extensao = px.bar(consolidado_area, x='area_extensao', y='count',
                        labels={'area_extensao': '', 'count': ''},
                        title='Distribuição por Área de Extensão  (números absolutos)',
                        facet_row='tipo',
                        category_orders={'tipo': ['Total', 'Filtrado']},
                        color='tipo',
                        height=750)
    
    # Construindo o gráfico de Unidades
    mapeamento = {
    'Escola de Ciências da Informação': 'ECI',
    'Escola de Belas-Artes': 'EBA',
    'Faculdade de Filosofia e Ciências Humanas': 'FAFICH',
    'Escola de Enfermagem': 'Enfermagem',
    'Escola de Engenharia': 'Engenharia',
    'Faculdade de Ciências Econômicas': 'FACE',
    'Pró-Reitoria de Extensão': 'PROEX',
    'Instituto de Ciências Exatas': 'ICEX',
    'Instituto de Ciências Biológicas': 'ICB',
    'Instituto de Geociências': 'IGC',
    'Faculdade de Educação': 'FAE',
    'Escola de Arquitetura': 'Arquitetura',
    'Faculdade de Odontologia': 'Odonto',
    'Pró-Reitoria de Administração': 'PRA',
    'Faculdade de Letras': 'FALE',
    'Faculdade de Medicina': 'Medicina',
    'Pró-Reitoria de Recursos Humanos': 'PRORH',
    'Escola de Veterinária': 'Veterinária',
    'FUMP': 'FUMP',
    'Escola de Educação Física, Fisioterapia e Terapia Ocupacional': 'EEFFTO',
    'CEDECOM': 'CEDECOM',
    'Instituto de Ciências Agrárias': 'ICA',
    'Faculdade de Direito': 'Direito',
    'Gabinete da Reitoria': 'Gab. Reitoria',
    'Faculdade de Farmácia': 'Farmácia',
    'Colégio Técnico': 'COLTEC',
    'Escola de Música': 'Música',
    'Biblioteca Universitária': 'Biblioteca',
    'Centro Pedagógico': 'CP'
    }

    dff_unidade_counts = dff.unidade.value_counts().reset_index()
    dff_unidade_counts.columns = ['unidade', 'contagem']
    dff_unidade_counts['unidade'] = dff_unidade_counts['unidade'].map(mapeamento)
    dff_unidade_counts['tipo'] = 'Filtrado'
    df_unidade_counts = df.unidade.value_counts().reset_index()
    df_unidade_counts.columns = ['unidade', 'contagem']
    df_unidade_counts['unidade'] = df_unidade_counts['unidade'].map(mapeamento)
    df_unidade_counts['tipo'] = 'Total'
    consolidado_unidade = pd.concat([dff_unidade_counts, df_unidade_counts])
    fig_unidades = px.bar(consolidado_unidade, x='unidade', y='contagem',
                        labels={'unidade': '', 'contagem': ''},
                        title='Distribuição de ações por Unidade  (números absolutos)',
                        facet_row='tipo',
                        category_orders={'tipo': ['Total', 'Filtrado']},
                        color='tipo',
                        height=750)
    

    # Construindo o gráfico de Públicos Específicos
    dff_publicos = dff.filter(like="publicoespecifico").iloc[:, :-1]
    colunas = [
    'Crianças', 'Jovens', 'Adultos', 'Idosos', 
    'Educação Infantil', 'Ensino Fundamental', 'Ensino Médio',
    'Cadastro Único', 'Indígenas', 'Pessoas negras', 'Entorno', 
    'Trabalhadores UFMG', 'Pessoas com deficiência', 'Doenças crônicas',
    'Moradores vilas', 'Comunidades rurais', 'Comunidades quilombolas',
    'Mulheres', 'LGBTQIA+', 'Imigrantes', 'Moradores de rua'
]
    dff_publicos.columns = colunas
    dff_publicos = dff_publicos.apply(lambda col: col.value_counts().get('Sim', 0)).reset_index()
    dff_publicos.columns = ['Público', 'Contagem']
    dff_publicos['tipo'] = 'Filtrado'
    df_publicos = df.filter(like="publicoespecifico").iloc[:, :-1]
    df_publicos.columns = colunas
    df_publicos = df_publicos.apply(lambda col: col.value_counts().get('Sim', 0)).reset_index()
    df_publicos.columns = ['Público', 'Contagem']
    df_publicos['tipo'] = 'Total'
    consolidado_publicos = pd.concat([dff_publicos, df_publicos], ignore_index=True)
    fig_publicos = px.bar(consolidado_publicos, 
                          x='Público', 
                          y='Contagem',
                        labels={'Público': '', 'Contagem': ''},
                        title='Público Alvo Específico (números absolutos)<br><sup>Entre os respondentes que informaram públicos específicos</sup>',
                        facet_row='tipo',
                        category_orders={'tipo': ['Total', 'Filtrado']},
                        color='tipo',
                        height=750)
    
    # Construindo o gráfico de Redes Sociais
    url_pattern = re.compile(r'(https?|ftp)://[^\s/$.?#].[^\s]*', re.IGNORECASE)
    def is_valid_url(url):
        if pd.isna(url):
            return False
        return re.match(url_pattern, url) is not None
    websites = dff['links[SQ001]'].apply(is_valid_url).sum()
    facebook = dff['links[SQ002]'].apply(lambda x: "facebook" in str(x)).sum()
    instagram = dff['links[SQ004]'].apply(lambda x: "instagram" in str(x) or '@' in str(x)).sum()
    youtube = dff['links[SQ005]'].apply(lambda x: "youtu" in str(x)).sum()
    redes_sociais_filtrado = pd.DataFrame({'Rede Social': ['Websites', 'Facebook', 'Instagram', 'Youtube'],
                                           'Contagem': [websites, facebook, instagram, youtube],
                                             'Tipo': 'Filtrado'})
    websites = df['links[SQ001]'].apply(is_valid_url).sum()
    facebook = df['links[SQ002]'].apply(lambda x: "facebook" in str(x)).sum()
    instagram = df['links[SQ004]'].apply(lambda x: "instagram" in str(x) or '@' in str(x)).sum()
    youtube = df['links[SQ005]'].apply(lambda x: "youtu" in str(x)).sum()
    redes_sociais_total = pd.DataFrame({'Rede Social': ['Websites', 'Facebook', 'Instagram', 'Youtube'],
                                        'Contagem': [websites, facebook, instagram, youtube],
                                        'Tipo': 'Total'})
    redes_sociais = pd.concat([redes_sociais_total, redes_sociais_filtrado], ignore_index=True)


    fig_socialmedia = px.bar(redes_sociais, 
                             x='Rede Social', 
                             y='Contagem',
                            labels={'Rede Social':'', 'Contagem':''},
                            title='Uso de Redes Sociais nas ações de Divulgação Científica (números absolutos)',
                            facet_row='Tipo',
                            category_orders={'Tipo': ['Total', 'Filtrado']},
                            color='Tipo',
                            height=750)


    return fig_vinculos, fig_tipo, fig_grande_area, fig_area_extensao, fig_publicos, fig_unidades, fig_socialmedia, n_filtrado

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
