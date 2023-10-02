
import dash
from dash import dcc
from dash import html
from dash import html, Input, Output, callback_context, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px  # yesid - new line
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import date

# sql project
import pandas as pd
from sqlalchemy.engine import create_engine

# graphs
# import altair as alt
import dash_alternative_viz as dav
import numpy as np

# model packages
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
import itertools
from itertools import cycle
import ast
import random

remote = True
if remote == True:
    URL = 'postgresql://london:as3fgd6@databaseinstance.c8611n47i7sr.us-east-1.rds.amazonaws.com:5432/database_ds4a'
    engine = create_engine(URL)
else:
    URL = 'postgresql://postgres:xxxx@localhost:5432/ds4a'
    engine = create_engine(URL)


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
    update_title='Loading...')

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.title = "SmartEnerx Dashboard"

server = app.server


app.layout = html.Div(
    children=[
        dcc.ConfirmDialog(
            id='danger',
            message='Error!, ¡Dashboard filters entered incorrectly!',
            displayed=False
        ),
        dcc.ConfirmDialog(
            id='danger2',
            message='Error!, ¡Dashboard filters entered incorrectly!',
            displayed=False
        ),
        dcc.ConfirmDialog(
            id='danger3',
            message='Error!, ¡Dashboard filters entered incorrectly!',
            displayed=False
        ),
        # header
        html.Div(
            [
                # first part
                html.Div(
                    [
                        html.H4("SmartEnerx Dashboard",
                                className="app__header__title--black"),
                        html.P(
                            "This app shows a Dashboard about Energy consumption in London",
                            className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                ),
                # second Part
                html.Div(
                    [
                        html.A(
                            html.Img(
                                src=app.get_asset_url("ukPowerNetworks.png"),
                                className="app__menu__img",

                            ),
                            href="https://www.ukpowernetworks.co.uk/",
                            target="_blank"
                        ),
                        html.A(
                            html.Img(
                                src=app.get_asset_url("C1.png"),
                                className="app__menu__img",

                            ),
                            href="https://www.correlation-one.com/data-science-for-all-colombia",
                            target="_blank"
                        ),
                    ],
                    className="app__header__logo",
                ),
            ],
            className="app__header",
        ),
        html.Div(
            [
                dcc.Tabs(
                    id="tabs",
                    value="TAB01",
                    children=[
                        dcc.Tab(
                            label="INTRODUCTION",
                            value="TAB01",
                            className="app__text",
                            children=[
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.Img(
                                                                    src=app.get_asset_url("ukPowerNetworks.png"), className="plotly-logo2"
                                                                ),
                                                            ], className="container__logo"
                                                        )

                                                    ]
                                                ), dbc.Col(
                                                    [
                                                        html.H1("Dashboard Details",
                                                                className="app__content")
                                                    ]
                                                ),


                                            ]
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        dbc.Row(
                                            [
                                                html.H3(
                                                    "This app is composed in 3 sections: ", className="app__content")


                                            ]),
                                        dbc.Row(
                                            [

                                                dbc.Col(

                                                    html.Div(
                                                        [
                                                            html.H2(
                                                                "MAIN ", className="app__content")
                                                        ], className="app__content_titles"
                                                    )
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.H5(""" In the first tab, you will find different figures and charts that shows the historical behaviour of households energy consumption by ACORN category.. All charts could be filter by season or by time period. 
Just select the category. 
season.
 or time period you want to see. and click on “Process”. 
All charts will updated automatically.

At the top, you will find KPis with the mean energy consumption per category. 

Scrolling down, you can see the historical data of daily energy demand of the selected category. If you selected more than one category, they will be displayed here in different colors. 

And, a chart with the relationship between temperature and daily energy consumption per category, which shows as the temperature decreases, the energy consumption increases.Nevertheless, regardless of temperature, the largest consumers of energy are the affluent achievers. 
""", className="app__content_black")
                                                    ]
                                                )



                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.H2(
                                                                    "DETAILS ", className="app__content")
                                                            ]
                                                        )

                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.H5(
                                                            """ On this tab shows two graphs detailing the energy consumption of the groups in the selected category. It can be displayed by season of the year or by a specific date range to carry out the respective analysis.""", className="app__content_black")
                                                    ]
                                                )



                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.H2(
                                                                    "FORECASTING ", className="app__content")
                                                            ]
                                                        )

                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.H5(
                                                            """ Here, you could adjust and create a forecast model in order to obtain a prediction of the daily energy consumption for your category and  group of interest, considering in advance the effect of metereological variables on consumption. 

Just indicate the number of periods in future that you want to predict, the category of interest, adjust the hyperparameters and that’s all, you will have a forecast of the households energy consumption. 

At the top will be the forecast time serie for the ACORN category, as well as a graphic with the behavious of the historical  tendency and sesonality. 

At the bottom, there will be the same information for each selected group. If you have selected more than one group, each will be displayed in a different color. 
 """, className="app__content_black")
                                                    ]
                                                )



                                            ]
                                        )





                                    ],
                                    className="container__2"
                                ),

                            ],
                        ),
                        dcc.Tab(
                            label="MAIN",
                            value="TAB0",
                            className="app__text",
                            children=[
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Img(
                                                    src=app.get_asset_url("ukPowerNetworks.png"), className="plotly-logo"
                                                ),
                                                html.Label(children="Filters", style={
                                                    'font-size': '18px', 'color': '#C62110', 'font-weight': 'bold'}),

                                                html.Br(),
                                                html.Br(),
                                                html.Div(
                                                    [
                                                        html.Label(
                                                            children="Category :", className="label_date")
                                                    ]
                                                ),

                                                html.Div(
                                                    [
                                                        dcc.Dropdown(
                                                            id="select-category",
                                                            options=[
                                                                {"label": i,
                                                                 "value": i}
                                                                for i in ['Financially Stretched',
                                                                          'Rising Prosperity',
                                                                          'Affluent Achievers',
                                                                          'Comfortable Communities',
                                                                          'Urban Adversity', 'Not Private Households']

                                                            ],
                                                            multi=True,
                                                            value=['Financially Stretched',
                                                                   'Rising Prosperity',
                                                                   'Affluent Achievers',
                                                                   'Comfortable Communities',
                                                                   'Urban Adversity', 'Not Private Households'],
                                                            placeholder="Select a Category",
                                                            className="reag__select",
                                                        ),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Br(),

                                                    ]
                                                ),
                                                html.Div(
                                                    [
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Label(
                                                            children="Time :", className="label_date"),
                                                        html.Label(
                                                            children="Select one of these time options  :", className="messages_filters"),
                                                    ]
                                                ),
                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        dcc.RadioItems(
                                                                            id='radioTime',
                                                                            options=[
                                                                                {"label": i,
                                                                                 "value": i}
                                                                                for i in ['Seasons',
                                                                                          'Date']
                                                                            ],
                                                                            value='Seasons',


                                                                        )
                                                                    ], className='radiobutton-group'
                                                                ),
                                                                html.Br(),
                                                                html.Div(
                                                                    [
                                                                        dcc.Dropdown(
                                                                            id="select-season",
                                                                            options=[
                                                                                {"label": i,
                                                                                 "value": i}
                                                                                for i in [
                                                                                    "Spring",
                                                                                    "Summer",
                                                                                    "Autumn",
                                                                                    "Winter",
                                                                                ]

                                                                            ],

                                                                            disabled=False,
                                                                            multi=True,
                                                                            value=[
                                                                                "Spring",
                                                                                "Summer",
                                                                                "Autumn",
                                                                                "Winter",
                                                                            ],
                                                                            placeholder="Select a season",
                                                                            className="reag__select",
                                                                            style={
                                                                                'opacity': '100%'}
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Br(),
                                                                html.Br(),

                                                            ]),

                                                        html.Div(
                                                            [
                                                                html.Div(
                                                                    [

                                                                        html.Div(
                                                                            [
                                                                                dcc.DatePickerRange(
                                                                                    id='my-date-picker-range',
                                                                                    min_date_allowed=date(
                                                                                        2013, 1, 1),
                                                                                    max_date_allowed=date(
                                                                                        2014, 3, 20),
                                                                                    initial_visible_month=date(
                                                                                        2013, 1, 1),
                                                                                    start_date=date(
                                                                                        2013, 1, 1),
                                                                                    end_date=date(
                                                                                        2014, 3, 20),
                                                                                    disabled=False,
                                                                                    clearable=True,

                                                                                    number_of_months_shown=5,
                                                                                    with_portal=True,
                                                                                    style={
                                                                                        'opacity': '100%'}
                                                                                )
                                                                            ], className="date_field"
                                                                        )
                                                                    ],
                                                                ),

                                                            ],
                                                            className="mobile_buttons",
                                                        ),
                                                        html.Div(
                                                            [

                                                                html.Div(
                                                                    id='output-container-date-picker-range',
                                                                    hidden=True,
                                                                    style={
                                                                        'text-align': 'center', 'color': 'black', 'font-size': '10px'}
                                                                )
                                                            ]
                                                        ),
                                                    ], className='container__4'
                                                ),
                                                html.Br(),
                                                html.Br(),
                                                html.Br(),
                                                html.Br(),
                                                html.Button(
                                                    "Process", id="button-send", n_clicks=0, className="button_process"
                                                ),
                                                html.Br(),
                                            ],
                                            className="two columns instruction",

                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [

                                                        html.Div(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        html.Div(
                                                                            html.H5(
                                                                                "Below you will find the KPI's of the visualization dashboard which indicates the average energy consumed by category in relation to the filters selected on the left side of the dashboard", className="app__content_red_right")
                                                                        ),

                                                                        dbc.Col(
                                                                            [
                                                                                html.H1("MAIN DATA VISUALIZATION",
                                                                                        className="app__header__tab--blue"),
                                                                            ], className="container__targetTitle",
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                html.H6("Average Energy Consumption",
                                                                                        className="app__text"),
                                                                                html.H6("Financially Stretched",
                                                                                        className="app__text2"),

                                                                                html.Div(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            dbc.Spinner(
                                                                                                html.Div(id='fs_number',
                                                                                                         className="app__target_numbers")
                                                                                            )
                                                                                        ),
                                                                                        dbc.Col(
                                                                                            html.Div(
                                                                                                'KWh', className="app__target_units")
                                                                                        )
                                                                                    ]
                                                                                ),
                                                                            ], className="container__target",
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                html.H6("Average Energy Consumption",
                                                                                        className="app__text"),
                                                                                html.H6("Affluent Achievers",
                                                                                        className="app__text2"),
                                                                                dbc.Col(
                                                                                    dbc.Spinner(
                                                                                        html.Div(id='aa_number',
                                                                                                 className="app__target_numbers")
                                                                                    )

                                                                                ),
                                                                                dbc.Col(
                                                                                    html.Div(
                                                                                        'KWh', className="app__target_units")
                                                                                )

                                                                            ], className="container__target",
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                html.H6("Average Energy Consumption",
                                                                                        className="app__text"),
                                                                                html.H6("Urban Adversity",
                                                                                        className="app__text2"),

                                                                                html.Div(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            dbc.Spinner(
                                                                                                html.Div(id='ua_number',
                                                                                                         className="app__target_numbers")
                                                                                            )
                                                                                        ),
                                                                                        dbc.Col(
                                                                                            html.Div(
                                                                                                'KWh', className="app__target_units")
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ], className="container__target",
                                                                        )


                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [

                                                                        dbc.Col(
                                                                            [

                                                                            ], className="container__targetTitle",
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                html.H6("Average Energy Consumption",
                                                                                        className="app__text"),
                                                                                html.H6("Rising Prosperity",
                                                                                        className="app__text2"),

                                                                                html.Div(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            dbc.Spinner(
                                                                                                html.Div(id='rp_number',
                                                                                                         className="app__target_numbers")
                                                                                            )
                                                                                        ),
                                                                                        dbc.Col(
                                                                                            html.Div(
                                                                                                'KWh', className="app__target_units")
                                                                                        )
                                                                                    ]
                                                                                ),
                                                                            ], className="container__target",
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                html.H6("Average Energy Consumption",
                                                                                        className="app__text"),
                                                                                html.H6("Comfortable Communities",
                                                                                        className="app__text2"),

                                                                                html.Div(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            dbc.Spinner(
                                                                                                html.Div(id='cc_number',
                                                                                                         className="app__target_numbers")
                                                                                            )
                                                                                        ),
                                                                                        dbc.Col(
                                                                                            html.Div(
                                                                                                'KWh', className="app__target_units")
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ], className="container__target",
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                html.H6("Average Energy Consumption",
                                                                                        className="app__text"),
                                                                                html.H6("Not private Households",
                                                                                        className="app__text2"),


                                                                                html.Div(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            dbc.Spinner(
                                                                                                html.Div(id='nph_number',
                                                                                                         className="app__target_numbers")
                                                                                            )
                                                                                        ),
                                                                                        dbc.Col(
                                                                                            html.Div(
                                                                                                'KWh', className="app__target_units")
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ], className="container__target",
                                                                        ),


                                                                    ]
                                                                ),
                                                                html.Br(),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Spinner(
                                                                            html.Div(
                                                                                [
                                                                                    html.H5(
                                                                                        "This graph shows the trend over time of the average consumption of the categories selected in the filters section", className="app__content_red"),
                                                                                    
                                                                                    dcc.Graph(
                                                                                        id="graph11"),
                                                                                ]
                                                                            )
                                                                        )
                                                                    ], className="container__graph11",
                                                                ),
                                                                html.Br(),
                                                                dbc.Row(
                                                                    [

                                                                        dbc.Spinner(
                                                                            html.Div(
                                                                                [
                                                                                    html.H5(
                                                                                        "This graph shows the comparison of the average energy consumption with temperature. At the times selected in the filters section.", className="app__content_red"),
                                                                                    dcc.Graph(
                                                                                        id="graph13"),
                                                                                ]
                                                                            )

                                                                        )
                                                                    ], className="container__graph11",
                                                                ),
                                                                html.Br(),
                                                                dbc.Row(
                                                                    [

                                                                        dbc.Spinner(
                                                                            html.Div([
                                                                                html.H5(
                                                                                    "This graph shows the comparison of the average energy consumption of the selected categories.", className="app__content_red"),
                                                                                dcc.Graph(
                                                                                    id="graph12"),
                                                                            ])

                                                                        )

                                                                    ], className="container__graph13",
                                                                )
                                                            ],
                                                        ),

                                                    ],
                                                    className="container"
                                                )

                                            ],
                                            className="container__secondy"
                                        )
                                    ],
                                    className="container__2"
                                ),

                            ],
                        ),
                        dcc.Tab(
                            label="DETAILS",
                            value="TAB1",
                            className="app__text",
                            children=[html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H5(
                                                'On this tab shows two graphs detailing the energy consumption of the groups in the selected category. It can be displayed by season of the year or by a specific date range to carry out the respective analysis.', className="app__content_red"),
                                        ], className='containera__info'
                                    ),
                                    html.Br(),
                                    html.Div(
                                        [

                                            html.Div(
                                                [
                                                    html.Img(
                                                        src=app.get_asset_url("ukPowerNetworks.png"), className="plotly-logo"
                                                    ),
                                                    html.Label(children="Filters", style={
                                                        'font-size': '18px', 'color': '#C62110', 'font-weight': 'bold'}),

                                                    html.Br(),
                                                    html.Br(),
                                                    html.Div(
                                                        [
                                                            html.Label(
                                                                children="Category :", className="label_date")
                                                        ]
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Div(
                                                                        [
                                                                            dcc.RadioItems(
                                                                                id='radio3',
                                                                                options=[{'label': x, 'value': x}
                                                                                         for x in ['Affluent Achievers', 'Comfortable Communities', 'Financially Stretched', 'Urban Adversity', 'Rising Prosperity', 'Not Private Households']],
                                                                                value='Affluent Achievers',



                                                                            )
                                                                        ], className='radiobutton-group'
                                                                    ),
                                                                    html.Div(
                                                                        [
                                                                            dcc.Dropdown(
                                                                                id='dropdown2', placeholder="Select a group", multi=True, className="reag__select",),
                                                                        ]
                                                                    ),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                ], className='container__4'
                                                            ),
                                                            html.Br(),
                                                            html.Br(),
                                                            html.Br(),
                                                            html.Br(),
                                                            html.Br(),

                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Label(
                                                                children="Time :", className="label_date"),
                                                            html.Label(
                                                                children="Select one of these time options :", className="messages_filters"),
                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Div(
                                                                        [
                                                                            dcc.RadioItems(
                                                                                id='radioTime2',
                                                                                options=[
                                                                                    {"label": i,
                                                                                     "value": i}
                                                                                    for i in ['Seasons',
                                                                                              'Date']
                                                                                ],
                                                                                value='Seasons',


                                                                            )
                                                                        ], className='radiobutton-group'
                                                                    ),

                                                                    html.Br(),
                                                                    html.Div(
                                                                        [
                                                                            dcc.Dropdown(
                                                                                id="select-season2",
                                                                                options=[
                                                                                    {"label": i,
                                                                                     "value": i}
                                                                                    for i in [
                                                                                        "Spring",
                                                                                        "Summer",
                                                                                        "Autumn",
                                                                                        "Winter",
                                                                                    ]

                                                                                ],

                                                                                disabled=False,
                                                                                multi=True,
                                                                                value=[
                                                                                    "Spring",
                                                                                    "Summer",
                                                                                    "Autumn",
                                                                                    "Winter",
                                                                                ],
                                                                                placeholder="Select a season",
                                                                                className="reag__select",
                                                                                style={
                                                                                    'opacity': '100%'}
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    html.Br(),
                                                                    html.Br(),

                                                                ]),

                                                            html.Div(
                                                                [


                                                                    html.Div(
                                                                        [
                                                                            dcc.DatePickerRange(
                                                                                id='my-date-picker-range2',
                                                                                min_date_allowed=date(
                                                                                    2013, 1, 1),
                                                                                max_date_allowed=date(
                                                                                    2014, 3, 20),
                                                                                initial_visible_month=date(
                                                                                    2013, 1, 1),
                                                                                start_date=date(
                                                                                    2013, 1, 1),
                                                                                end_date=date(
                                                                                    2014, 3, 20),
                                                                                disabled=False,
                                                                                clearable=True,

                                                                                number_of_months_shown=5,
                                                                                with_portal=True,
                                                                                style={
                                                                                    'opacity': '100%'}
                                                                            )
                                                                        ], className="date_field"
                                                                    )


                                                                ],
                                                                className="mobile_buttons",
                                                            ),
                                                            html.Div(
                                                                [

                                                                    html.Div(
                                                                        id='output-container-date-picker-range2',
                                                                        hidden=True,
                                                                        style={
                                                                            'text-align': 'center', 'color': 'black', 'font-size': '10px'}
                                                                    )
                                                                ]
                                                            ),
                                                        ], className='container__4'
                                                    ),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Button(
                                                        "Process", id="button-send2", n_clicks=0, className="button_process"
                                                    ),
                                                    html.Br(),
                                                ],
                                                className="two columns instruction",

                                            ),
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            dbc.Row(
                                                                [
                                                                    dbc.Spinner(
                                                                        html.Div(
                                                                            [
                                                                                html.Div(
                                                                                    [
                                                                                        html.H5(
                                                                                            'The first graph shows us the difference in daily energy consumption for the groups selected in the filters section.', className="app__content_red"),
                                                                                    ], className='containera__info'
                                                                                ),
                                                                                dcc.Graph(
                                                                                    id="graph21"),
                                                                            ]
                                                                        )
                                                                    )
                                                                ], className="container__graph11",
                                                            ),
                                                            html.Br(),
                                                            dbc.Row(
                                                                [
                                                                    dbc.Spinner(
                                                                        html.Div(
                                                                            [
                                                                                html.Div(
                                                                                    [
                                                                                        html.H5(
                                                                                            'The second graph indicates the trend over time of energy consumption.', className="app__content_red"),
                                                                                    ], className='containera__info'
                                                                                ),
                                                                                dcc.Graph(
                                                                                    id="graph22"),
                                                                            ]
                                                                        )
                                                                    )
                                                                ], className="container__graph11",
                                                            )

                                                        ],
                                                        className="container"
                                                    )

                                                ],
                                                className="container__secondy"
                                            )
                                        ]
                                    )
                                ],
                                className="container__2"
                            ),

                            ],
                        ),
                        dcc.Tab(
                            label="FORECASTING",
                            value="TAB2",
                            className="app__text",
                            children=[html.Div(
                                [
                                    html.Div(
                                        [
                                            
                                            html.H5("On this tab, the Prophet time series forecasting model was used to predict the daily energy consumption of the specified ACORN category and the groups of interest. The documentation of the model with the details of its implementation procedure can be found :", className="app__content_red_left"),
                                            html.A("Here", href='https://facebook.github.io/prophet/',
                                                   target="_blank", className="app__link_black"),
                                            html.H5("""Main hyperparameters can be adjusted to effectively tune the category model, such as the trend and seasonality flexibility. It is also possible to change the forecast horizon and display its outcome with the selected uncertainty level. 
                                                        The displayed forecast of each group is the result of a model fitted with the optimum hyperparameters; these were obtained by applying the grid search method using cross-validation for each group dataset.
                                                        The high-quality forecast is displayed with its uncertainty interval (error bands) and its corresponding historical data on the time series plot. In addition, the trend and yearly seasonality time components of the forecast of each category and group are included on the tab.
                                                        """, className="app__content_red"),
                                        ], className='containera__info'
                                    ),
                                    html.Br(),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Img(
                                                        src=app.get_asset_url("ukPowerNetworks.png"), className="plotly-logo"
                                                    ),
                                                    html.Label(children="Filters", style={
                                                        'font-size': '18px', 'color': '#C62110', 'font-weight': 'bold'}),

                                                    html.Br(),
                                                    html.Br(),
                                                    html.Div(
                                                        [
                                                            html.Label(
                                                                children="Category :", className="label_date")
                                                        ]
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Div(
                                                                        [
                                                                            dcc.RadioItems(
                                                                                id='radio4',
                                                                                options=[{'label': x, 'value': x}
                                                                                         for x in ['Affluent Achievers', 'Comfortable Communities', 'Financially Stretched', 'Urban Adversity', 'Rising Prosperity', 'Not Private Households']],
                                                                                value='Affluent Achievers',
                                                                            )
                                                                        ], className='radiobutton-group'
                                                                    ),
                                                                    html.Div(
                                                                        [
                                                                            dcc.Dropdown(
                                                                                id='dropdown3', placeholder="Select a group", multi=True, className="reag__select"),
                                                                        ]
                                                                    ),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                ], className='container__4'
                                                            ),
                                                            html.Br(),
                                                            html.Br(),
                                                            html.Br(),
                                                            html.Br(),
                                                            html.Br(),

                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Label(
                                                                children="Hyperparameter Model :", className="label_date"),
                                                            html.Label(
                                                                children="Select the hyperparameter  needed :", className="messages_filters"),
                                                        ]
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Label(
                                                                children="Forecast  Uncertainty  interval:", className="label_texto"),
                                                            dcc.Slider(0, 100,
                                                                       step=None,
                                                                       marks={
                                                                           0: '0',
                                                                           25: '25',
                                                                           50: '50',
                                                                           75: '75',
                                                                           85: '85',
                                                                           95: '95'
                                                                       },
                                                                       value=85,
                                                                       id='hp1'
                                                                       ),
                                                            html.Label(
                                                                children="Forecast period (days):", className="label_texto"),
                                                            dcc.Slider(0, 180,
                                                                       step=None,
                                                                       marks={
                                                                           0: '0',
                                                                           30: '30',
                                                                           60: '60',
                                                                           90: '90',
                                                                           120: '120',
                                                                           150: '150',
                                                                           180: '180'
                                                                       },
                                                                       value=90,
                                                                       id='hp2'
                                                                       ),
                                                            html.Label(
                                                                children="Flexibility of the trend:", className="label_texto"),
                                                            dcc.Slider(0.001, 0.5, 0.01,
                                                                       marks={
                                                                           0.001: '0.001',
                                                                           0.01: '0.01',
                                                                           0.1: '0.1',
                                                                           0.5: '0.5'
                                                                       },
                                                                       value=0.1,
                                                                       id='hp3'
                                                                       ),
                                                            html.Label(
                                                                children="Flexibility of the seasonality:", className="label_texto"),
                                                            dcc.Slider(0.01, 10,
                                                                       step=None,
                                                                       marks={
                                                                           0.01: '0.01',
                                                                           0.1: '0.1',
                                                                           1: '1',
                                                                           10: '10'
                                                                       },
                                                                       value=0.1,
                                                                       id='hp4'
                                                                       )
                                                        ], className='container__4'
                                                    ),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Button(
                                                        "Process", id="button-send3", n_clicks=0, className="button_process"
                                                    ),
                                                    html.Br(),
                                                ],
                                                className="two columns instruction",

                                            ),
                                            html.Div(
                                                [

                                                    dbc.Row(
                                                        [

                                                            dbc.Spinner(
                                                                html.Div(
                                                                    [
                                                                        html.H5('Projection of average energy consumption by category selected in the filters section.',className='app__content_red'),
                                                                        dcc.Graph(
                                                                            id="graph31")
                                                                    ]
                                                                ),
                                                            ),
                                                            dbc.Spinner(
                                                                html.Div(

                                                                    [
                                                                        html.H5('Trend graph: Shows the behavior of the trend over time shown in the upper graph. The color range shown in the projection is the uncertainty interval',className='app__content_red'),
                                                                        html.H5('Seasonality graph: Shows how seasonality is affected over time with respect to the average value of energy consumption shown in the upper graph.',className='app__content_red'),
                                                                        dcc.Graph(
                                                                            id="graph32")
                                                                    ]
                                                                ),
                                                            )


                                                        ], className="container__graphtab3",
                                                    ),
                                                    html.Br(),
                                                    dbc.Row([

                                                        dbc.Spinner(
                                                            html.Div(
                                                                [
                                                                    html.H5('Projection of average energy consumption by category selected in the filters section.',className='app__content_red'),
                                                                    dcc.Graph(
                                                                        id="graph33")
                                                                ]
                                                            ),
                                                        ),
                                                        dbc.Spinner(
                                                            html.Div(

                                                                [
                                                                    html.H5('Trend graph: Shows the behavior of the trend over time shown in the upper graph. The color range shown in the projection is the uncertainty interval.',className='app__content_red'),
                                                                    html.H5('Seasonality graph: Shows how seasonality is affected over time with respect to the average value of energy consumption shown in the upper graph.',className='app__content_red'),
                                                                    dcc.Graph(
                                                                        id="graph34")
                                                                ]
                                                            ),
                                                        )

                                                    ], className="container__graphtab3",
                                                    ),

                                                ],
                                                className="container__secondy"
                                            )
                                        ],
                                        className="container__2_tab3"
                                    )
                                ]
                            ),

                            ],
                        ),
                    ],
                )
            ],
            className="tabs__container",
        ),
    ],
    className="app__container",
)






@ app.callback(
    [
        Output("fs_number", "children"),
        Output("rp_number", "children"),
        Output("aa_number", "children"),
        Output("cc_number", "children"),
        Output("ua_number", "children"),
        Output("nph_number", "children")
    ],
    [
        Input('button-send', 'n_clicks')
    ],
    [
        State("select-category", "value"),
        State("radioTime", "value"),
        State("select-season", "value"),
        State("my-date-picker-range", "start_date"),
        State("my-date-picker-range", "end_date"),

    ],
)
def button(btn1, category, radioTime, season, start_date, end_date):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    try:
        if 'button-send' in changed_id:
            results = []
            season = str(str(season).replace('[', '(').replace(']', ')'))
            category_list = str(str(category).replace('[', '(').replace(']', ')'))


            if radioTime == 'Seasons':
                if remote == False:
                    query_target = """select  acorn_category , cast(sum(sum_energy)/1000000 as decimal(10,2)) sum_energy
                    from public.daily_consumption"""+' where season in '+season+' and acorn_category in '+category_list+' group by acorn_category'

                else:
                    query_target = """select  acorn_category , cast(avg(day_avg_consumption) as decimal(10,2)) avg_energy
                    from staging.daily_consumption_group"""+' where season in '+season.lower()+' and acorn_category in '+category_list+' group by acorn_category'

            else:
                if remote == False:
                    query_target = """select  acorn_category , cast(sum(sum_energy)/1000000 as decimal(10,2)) sum_energy
                from public.daily_consumption"""+" where  cast(date_c as date)  between '"+start_date+"' and '"+end_date+"' and acorn_category in "+category_list+' group by acorn_category'
                else:
                    query_target = """select  acorn_category , cast(avg(day_avg_consumption) as decimal(10,2)) avg_energy
                    from staging.daily_consumption_group"""+" where  cast(date_ as date)  between '"+start_date+"' and '"+end_date+"' and acorn_category in "+category_list+' group by acorn_category'

            df_avg_energy = pd.read_sql(query_target, engine)
            categories = list(df_avg_energy.acorn_category)

            order = {'Financially Stretched': '-', 'Rising Prosperity': '-', 'Affluent Achievers': '-',
                        'Comfortable Communities': '-', 'Urban Adversity': '-', 'Not Private Households': '-'}

            for i in categories:
                if i in category:
                    value = float(
                        df_avg_energy[df_avg_energy['acorn_category'] == i]['avg_energy'])
                    if i in order.keys():
                        order[i] = value
                    results = [order['Financially Stretched'], order['Rising Prosperity'], order['Affluent Achievers'],
                                order['Comfortable Communities'], order['Urban Adversity'], order['Not Private Households']]
                else:
                    order[i] = '-'
            results.append(round(df_avg_energy.avg_energy.sum(), 2))

            msg = [results[0], results[1], results[2],
                    results[3], results[4], results[5]]

        else:
            msg = ['-', '-', '-', '-', '-', '-']
    except:
        msg = ['-', '-', '-', '-', '-', '-']
    return msg


@ app.callback(

    [
    Output("graph11", "figure"),
    Output('graph11', 'style'),
    Output('danger', 'displayed')
    ],
    [
        Input('button-send', 'n_clicks')
    ],
    [
        State("select-category", "value"),
        State("radioTime", "value"),
        State("select-season", "value"),
        State("my-date-picker-range", "start_date"),
        State("my-date-picker-range", "end_date"),

    ],
)
def graph11(btn1, category, radioTime, season, start_date, end_date):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    try:
        if 'button-send' in changed_id:

            season = str(str(season).replace('[', '(').replace(']', ')'))
            category_list = str(str(category).replace('[', '(').replace(']', ')'))
            if radioTime == 'Seasons':
                if remote == False:
                    query = """select  date_, cast(total_consumption as decimal(10,2)) total_consumption, acorn_category
                    from public.daily_group_consumption"""+' where season in '+season.lower()+' and acorn_category in '+category_list

                else:  # yesid - else changed
                    query = """select date_, day_avg_consumption, acorn_category
                    from staging.daily_consumption_category"""+' where season in '+season.lower()+' and acorn_category in '+category_list

            else:
                if remote == False:
                    query = """select  date_, cast(sum_energy as decimal(10,2)) total_consumption, acorn_category
                from public.daily_group_consumption"""+" where  cast(date_c as date)  between '"+start_date+"' and '"+end_date+"' and acorn_category in "+category_list
                else:  # yesid - else changed
                    query = """select date_, day_avg_consumption, acorn_category
                    from staging.daily_consumption_category"""+" where  cast(date_ as date)  between '"+start_date+"' and '"+end_date+"' and acorn_category in "+category_list

            # yesid - changed lines from here to the 'return None'
            daily_consumption_category = pd.read_sql(query, engine)
            daily_consumption_category = daily_consumption_category.sort_values(
                by='date_')

            figure = px.line(daily_consumption_category,
                            x='date_',
                            y='day_avg_consumption',
                            color='acorn_category',
                            labels=dict(date_="Date", day_avg_consumption="Daily energy consume (kWh)",
                                        acorn_category='Category'),
                            title="Energy Consumption By Acorn Category",
                            # width=1200, height=400
                            )
            figure.update_layout(template=go.layout.Template())

            figure.update_yaxes(rangemode='tozero')

            return figure,{'display': 'block'},False
        else:
            df = pd.DataFrame({'date_': [0, 4], 'day_avg_consumption': [0, 2]})
            figure = px.line(df,
                            x='date_',
                            y='day_avg_consumption')
            return figure,{'display': 'None'},False
    except:
        df = pd.DataFrame({'date_': [0, 4], 'day_avg_consumption': [0, 2]})
        figure = px.line(df,
                        x='date_',
                        y='day_avg_consumption')
        return figure,{'display': 'None'},True



@ app.callback(
    [
    Output("graph12", "figure"),
    Output('graph12', 'style')
    ],
    [
        Input('button-send', 'n_clicks')
    ],
    [
        State("select-category", "value"),
        State("radioTime", "value"),
        State("select-season", "value"),
        State("my-date-picker-range", "start_date"),
        State("my-date-picker-range", "end_date"),


    ],
)
def graph12(btn1, category, radioTime, season, start_date, end_date):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    try:
        if 'button-send' in changed_id:
            season = str(str(season).replace('[', '(').replace(']', ')'))
            category_list = str(str(category).replace('[', '(').replace(']', ')'))
            if radioTime == 'Seasons':
                if remote == False:
                    query = """select  date_, cast(total_consumption as decimal(10,2)) total_consumption, acorn_category
                    from public.daily_group_consumption"""+' where season in '+season.lower()+' and acorn_category in '+category_list

                else:
                    query = """select date_, day_avg_consumption, acorn_category
                    from staging.daily_consumption_category"""+' where season in '+season.lower()+' and acorn_category in '+category_list

            else:
                if remote == False:
                    query = """select  date_, cast(sum_energy as decimal(10,2)) total_consumption, acorn_category
                from public.daily_group_consumption"""+" where  cast(date_c as date)  between '"+start_date+"' and '"+end_date+"' and acorn_category in "+category_list
                else:  # yesid - else changed
                    query = """select date_, day_avg_consumption, acorn_category
                    from staging.daily_consumption_category"""+" where  cast(date_ as date)  between '"+start_date+"' and '"+end_date+"' and acorn_category in "+category_list

            daily_consumption_category = pd.read_sql(query, engine)
            figure = px.bar(daily_consumption_category.sort_values('day_avg_consumption', ascending=False),
                            x='acorn_category',
                            y="day_avg_consumption",
                            color='acorn_category',
                            labels={'acorn_category': 'Category',
                                    'day_avg_consumption': 'Mean daily energy consumption (kw/h)'},
                            title="Categories Average"
                            # width=1200, height=400
                            )
            figure.update_layout(template=go.layout.Template())
            figure.update_yaxes(rangemode='tozero')

            return figure,{'display': 'block'}
        else:
            df = pd.DataFrame(
                {'acorn_category': [0, 4], 'day_avg_consumption': [0, 2]})

            figure = px.bar(df,
                            x='acorn_category',
                            y='day_avg_consumption')
            return figure,{'display': 'None'}
    except:
        df = pd.DataFrame(
                {'acorn_category': [0, 4], 'day_avg_consumption': [0, 2]})

        figure = px.bar(df,
                        x='acorn_category',
                        y='day_avg_consumption')
        return figure,{'display': 'None'}



@ app.callback(
    [
    Output("graph13", "figure"),
    Output('graph13', 'style')
    ],
    [
        Input('button-send', 'n_clicks')
    ],
    [
        State("select-category", "value"),
        State("radioTime", "value"),
        State("select-season", "value"),
        State("my-date-picker-range", "start_date"),
        State("my-date-picker-range", "end_date")
    ],
)
def graph13(btn1, category, radioTime, season, start_date, end_date):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    try:
        if 'button-send' in changed_id:
            season = str(str(season).replace('[', '(').replace(']', ')'))
            category_list = str(str(category).replace('[', '(').replace(']', ')'))

            if radioTime == 'Seasons':
                if remote == False:
                    query = """select  date_, cast(total_consumption as decimal(10,2)) total_consumption, acorn_category
                    from public.daily_group_consumption""" + ' where season in ' + season.lower() + ' and acorn_category in ' + category_list

                else:
                    query = '''SELECT * FROM staging.daily_consumption_category''' +\
                        ' WHERE season IN ' + season.lower() + ' AND acorn_category IN ' + category_list

            else:
                if remote == False:
                    query = """select  date_, cast(sum_energy as decimal(10,2)) total_consumption, acorn_category
                                from public.daily_group_consumption""" + " where  cast(date_c as date)  between '" + start_date + "' and '" + end_date + "' and acorn_category in " + category_list
                else:
                    query = '''SELECT * FROM staging.daily_consumption_category''' +\
                        "WHERE date_ BETWEEN '" + start_date + "' AND '" + \
                        end_date + "' AND acorn_category in " + category_list

            daily_consumption_category = pd.read_sql(query, engine)
            weather_daily = pd.read_sql(
                '''SELECT * FROM staging.weather_daily''', engine)
            weather_daily['date_'] = pd.DatetimeIndex(
                weather_daily['time'])  # Convert date in weather daily dataframe to day
            daily_consumption_category['date_'] = pd.DatetimeIndex(
                daily_consumption_category['date_'])  # Convert date in daily energy dataframe to day
            # Merge daily energy consumption and weather dataset
            daily_with_weather = pd.merge(daily_consumption_category.groupby(['date_', 'season', 'acorn_category'])[
                ['day_avg_consumption']].mean().reset_index(),
                weather_daily.groupby(
                    'date_')[['temperature_min']].mean().reset_index(),
                on='date_', how='left')

            figure = px.scatter(daily_with_weather,
                                x='temperature_min',
                                y='day_avg_consumption',
                                color='acorn_category',
                                labels=dict(temperature_min="Temperature (ºC)", day_avg_consumption="Daily energy consumption (kw/h)",
                                            acorn_category='Category'),
                                title="Energy Consumption By Acorn Category",
                                # width=1200, height=400
                                )

            figure.update_layout(template=go.layout.Template())
            figure.update_yaxes(rangemode='tozero')

            return figure,{'display': 'block'}
        else:
            df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
            figure = px.scatter(df,
                                x='temperature_min',
                                y='day_avg_consumption')
            return figure,{'display': 'None'}
    except:
        df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
        figure = px.scatter(df,
                            x='temperature_min',
                            y='day_avg_consumption')
        return figure,{'display': 'None'}


@ app.callback(

    [
    Output("graph21", "figure"),
    Output('graph21', 'style'),
    Output('danger2', 'displayed')
    ],


    [
        Input('button-send2', 'n_clicks')
    ],
    [

        State("dropdown2", "value"),
        State("radioTime2", "value"),
        State("select-season2", "value"),
        State("my-date-picker-range2", "start_date"),
        State("my-date-picker-range2", "end_date"),


    ],
)
def graph21(btn1, group, radioTime, season, start_date, end_date):

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    try:
        if 'button-send' in changed_id:
            season = str(str(season).replace('[', '(').replace(']', ')'))
            group_list = str(str(group).replace('[', '(').replace(']', ')'))
            print(group_list, season)
            if radioTime == 'Seasons':
                if remote == False:
                    query = """select  date_, cast(total_consumption as decimal(10,2)) total_consumption, acorn_category
                    from public.daily_group_consumption"""+' where season in '+season.lower()+' and acorn_category in '+group_list

                else:
                    query = """select date_, cast(day_avg_consumption as decimal(10,2)) avg_consumption, acorn_group_detail
                    from staging.daily_consumption_group"""+' where season in '+season.lower()+' and acorn_group_detail in '+group_list

            else:
                if remote == False:
                    query = """select  date_, cast(sum_energy as decimal(10,2)) total_consumption, acorn_category
                from public.daily_group_consumption"""+" where  cast(date_c as date)  between '"+start_date+"' and '"+end_date+"' and acorn_category in "+group_list
                else:
                    query = """select date_, cast(day_avg_consumption as decimal(10,2)) avg_consumption,acorn_group_detail
                    from staging.daily_consumption_group"""+" where  cast(date_ as date)  between '"+start_date+"' and '"+end_date+"' and acorn_group_detail in "+group_list

            daily_dataset = pd.read_sql(query, engine)

            #  yesid - new lines
            daily_dataset['date_'] = pd.to_datetime(daily_dataset['date_'])
            daily_dataset['weekday'] = pd.DatetimeIndex(
                daily_dataset['date_']).dayofweek
            daily_dataset["name_weekday"] = (daily_dataset['date_']).dt.day_name()

            figure = px.bar(daily_dataset,
                            x='name_weekday', y='avg_consumption', color='acorn_group_detail',
                            labels={'avg_consumption': 'Daily energy consume (Kw/h)', 'name_weekday': 'Weekday',
                                    'acorn_group_detail': 'Group'},
                            title="Daily Behavior By Group",
                            category_orders={
                                "name_weekday": ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
                                                'Sunday']})
            figure.update_layout(template=go.layout.Template())

            return figure,{'display': 'block'},False
        else:
            df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
            figure = px.scatter(df,
                                x='temperature_min',
                                y='day_avg_consumption')
            figure.update_layout(template=go.layout.Template())

            return figure,{'display': 'None'},False
    except:
        df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
        figure = px.scatter(df,
                            x='temperature_min',
                            y='day_avg_consumption')
        figure.update_layout(template=go.layout.Template())

        return figure,{'display': 'None'},True


@ app.callback(
    [
        Output("graph22", "figure"),
        Output('graph22', 'style'),
    ],

    [
        Input('button-send2', 'n_clicks')
    ],
    [

        State("dropdown2", "value"),
        State("radioTime2", "value"),
        State("select-season2", "value"),
        State("my-date-picker-range2", "start_date"),
        State("my-date-picker-range2", "end_date"),


    ],
)
def graph22(btn1, group, radioTime, season, start_date, end_date):

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    try:
        if 'button-send' in changed_id:
            season = str(str(season).replace('[', '(').replace(']', ')'))
            group_list = str(str(group).replace('[', '(').replace(']', ')'))
            print(group_list, season)
            if radioTime == 'Seasons':
                if remote == False:
                    query = """select  date_, cast(total_consumption as decimal(10,2)) total_consumption, acorn_category
                    from public.daily_group_consumption"""+' where season in '+season.lower()+' and acorn_category in '+group_list

                else:
                    query = """select date_, cast(day_avg_consumption as decimal(10,2)) avg_consumption, acorn_group_detail
                    from staging.daily_consumption_group"""+' where season in '+season.lower()+' and acorn_group_detail in '+group_list

            else:
                if remote == False:
                    query = """select  date_, cast(sum_energy as decimal(10,2)) total_consumption, acorn_category
                from public.daily_group_consumption"""+" where  cast(date_c as date)  between '"+start_date+"' and '"+end_date+"' and acorn_category in "+group_list
                else:
                    query = """select date_, cast(day_avg_consumption as decimal(10,2)) avg_consumption,acorn_group_detail
                    from staging.daily_consumption_group"""+" where  cast(date_ as date)  between '"+start_date+"' and '"+end_date+"' and acorn_group_detail in "+group_list

            daily_dataset = pd.read_sql(query, engine)

            daily_dataset['date_'] = pd.to_datetime(daily_dataset['date_'])
            daily_dataset = daily_dataset.sort_values(by='date_')
            figure = px.line(daily_dataset,
                                x="date_",
                                y="avg_consumption",
                                labels=dict(
                                    date_="Date", avg_consumption="Daily energy consume (kWh)", acorn_group_detail='Group'),
                                hover_data={"date_": "|%B %d, %Y"},
                                color='acorn_group_detail',
                                title="Energy Consumption By Group"
                                )
            # yesid - new lines
            figure.update_layout(template=go.layout.Template())
            figure.update_yaxes(rangemode='tozero')

            return figure, {'display': 'block'}
        else:
            df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
            figure = px.line(df,
                                x="temperature_min",
                                y="day_avg_consumption")
            figure.update_layout(template=go.layout.Template())
            figure.update_yaxes(rangemode='tozero')
            return figure, {'display': 'None'}
    except:
        df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
        figure = px.line(df,
                            x="temperature_min",
                            y="day_avg_consumption")
        figure.update_layout(template=go.layout.Template())
        figure.update_yaxes(rangemode='tozero')
        return figure, {'display': 'None'}




# PLOTS TAB 3
# plot the historic data and the forecast with plotly
# function to plot a line with band errors
def line(error_y_mode=None, **kwargs):
    figure_with_error_bars = px.line(**kwargs)
    fig = px.line(**{arg: val for arg, val in kwargs.items()
                  if (arg != 'error_y') & (arg != 'error_x')})
    for data in figure_with_error_bars.data:
        x = list(data['x'])
        y_upper = list(data['error_y']['array'])
        y_lower = list(data['error_x']['array'])
        color = f"rgba({tuple(int(data['line']['color'].lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))},.3)".replace(
            '((', '(').replace('),', ',').replace(' ', '')
        fig.add_trace(
            go.Scatter(
                x=x + x[::-1],
                y=y_upper + y_lower[::-1],
                fill='toself',
                fillcolor=color,
                line=dict(
                    color='rgba(255,255,255,0)'
                ),
                hoverinfo="skip",
                showlegend=False,
                legendgroup=data['legendgroup'],
                xaxis=data['xaxis'],
                yaxis=data['yaxis'],
            )
        )
    # Reorder data as said here: https://stackoverflow.com/a/66854398/8849755
    reordered_data = []
    for i in range(int(len(fig.data) / 2)):
        reordered_data.append(fig.data[i + int(len(fig.data) / 2)])
        reordered_data.append(fig.data[i])
    fig.data = tuple(reordered_data)
    fig.update_layout(showlegend=False)

    return fig


@app.callback(
    [
    Output("graph31", "figure"),
    Output('graph31', 'style'),
    Output('danger3', 'displayed')
    ],

    [
        Input('button-send3', 'n_clicks')
    ],
    [
        State("dropdown3", "value"),
        State("hp1", "value"),
        State("hp2", "value"),
        State("hp3", "value"),
        State("hp4", "value")
    ]
)
def graph31(bt, group, conf_int, f_period, cps, sps):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    try:
        if 'button-send3' in changed_id:

            user_ps = dict(
                zip(['changepoint_prior_scale', 'seasonality_prior_scale'], [cps, sps]))
            acorn_class = pd.read_sql(
                """SELECT * FROM staging.classification""", engine)
            cat = acorn_class[acorn_class["acorn_group"].isin(
                group)]["acorn_category"].values[0]

            if remote == False:
                query = ""

            else:
                query = """SELECT * FROM staging.daily_consumption_category""" + \
                    " WHERE daily_consumption_category.acorn_category = '" + \
                        str(cat) + "';"

            df_daily_category = pd.read_sql(query, engine)
            df_daily_category.sort_values(["date_"], inplace=True)
            df_daily_category.rename(columns={'date_': 'ds', 'day_avg_consumption': 'y'},
                                    inplace=True)  # neccesary for Prophet
            df_temp = df_daily_category[['ds', 'y']]  # neccesary for Prophet

            if remote == False:
                query = ""

            else:
                query = """SELECT * FROM staging.params_cat""" + \
                    " WHERE params_cat.category = '" + str(cat) + "';"

            ps_ct = pd.read_sql(query, engine)
            ps = ast.literal_eval(ps_ct['params'].values[0])
            # update hyperparameters according to the user selection
            ps.update(user_ps)

            iw = conf_int / 100

            uk_holidays = pd.read_sql('''SELECT * FROM staging.holidays''', engine)
            uk_holidays.rename(columns={
                            "bank_holidays": "ds", "type": "holiday"}, inplace=True)  # neccesary for Prophet

            model = Prophet(interval_width=iw,  # custom
                            holidays=uk_holidays, yearly_seasonality=True, weekly_seasonality=True, **ps)  # Best parameters
            # montly seasonality
            model.add_seasonality(name='custom_monthly',
                                period=30.5, fourier_order=10)
            model.add_country_holidays(country_name='UK')  # additional holidays

            model.fit(df_temp)

            # Forecast
            future = model.make_future_dataframe(periods=f_period,  # custom
                                                freq='D', include_history=True)  # number of days to be forecast
            forecast = model.predict(future)
            forecast['category'] = str(cat)

            fig = go.Figure()
            colors = cycle(plotly.colors.qualitative.Plotly)

            fig.add_trace(
                go.Scatter(x=df_temp["ds"],
                        y=df_temp["y"],
                        mode="lines",
                        marker_color=next(colors),
                        showlegend=False)

            )

            fig2 = go.Figure(fig.add_traces(
                data=line(data_frame=forecast[forecast["ds"] > '26-02-2014'],  # forecast with error bands
                        x='ds', y='yhat', color='category',
                        error_y='yhat_upper', error_x='yhat_lower', error_y_mode='band')._data),
            )

            fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                            title={'text': 'Daily Energy Consumption in ' + cat + ' ACORN category',
                                    'font_family': "Arial",
                                    'y': 0.9,
                                    'x': 0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'},
                            xaxis_title="Date",
                            yaxis_title="Mean daily energy consumption (KWh)",
                            template=go.layout.Template(),
                            autosize=False,
                            font=dict(family="Arial", size=10))

            fig2.update_xaxes(tickformat="%b\n%Y")

            return fig2,{'display': 'block'},False
        else:
            df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
            figure = px.line(df,
                            x="temperature_min",
                            y="day_avg_consumption")
            figure.update_layout(template=go.layout.Template())
            figure.update_yaxes(rangemode='tozero')
            return figure,{'display': 'None'},False
    except:
        df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
        figure = px.line(df,
                        x="temperature_min",
                        y="day_avg_consumption")
        figure.update_layout(template=go.layout.Template())
        figure.update_yaxes(rangemode='tozero')
        return figure,{'display': 'None'},True


@app.callback(
    [
    Output("graph32", "figure"),
    Output('graph32', 'style')
    ],

    [
        Input('button-send3', 'n_clicks')
    ],
    [
        State("dropdown3", "value"),
        State("hp2", "value"),
        State("hp3", "value"),
        State("hp4", "value")
    ]
)
def graph32(bt, group, f_period, cps, sps):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    try:
        if 'button-send3' in changed_id:

            user_ps = dict(
                zip(['changepoint_prior_scale', 'seasonality_prior_scale'], [cps, sps]))
            acorn_class = pd.read_sql(
                """SELECT * FROM staging.classification""", engine)
            cat = acorn_class[acorn_class["acorn_group"].isin(
                group)]["acorn_category"].values[0]

            if remote == False:
                query = ""

            else:
                query = """SELECT * FROM staging.daily_consumption_category""" + " WHERE daily_consumption_category.acorn_category = '" + str(
                    cat) + "';"

            df_daily_category = pd.read_sql(query, engine)
            df_daily_category.sort_values(["date_"], inplace=True)
            df_daily_category.rename(columns={'date_': 'ds', 'day_avg_consumption': 'y'},
                                    inplace=True)  # neccesary for Prophet
            df_temp = df_daily_category[['ds', 'y']]  # neccesary for Prophet

            if remote == False:
                query = ""

            else:
                query = """SELECT * FROM staging.params_cat""" + \
                    " WHERE params_cat.category = '" + str(cat) + "';"

            ps_ct = pd.read_sql(query, engine)
            ps = ast.literal_eval(ps_ct['params'].values[0])
            # update hyperparameters according to the user selection
            ps.update(user_ps)

            uk_holidays = pd.read_sql('''SELECT * FROM staging.holidays''', engine)
            uk_holidays.rename(columns={
                            "bank_holidays": "ds", "type": "holiday"}, inplace=True)  # neccesary for Prophet

            model = Prophet(holidays=uk_holidays, yearly_seasonality=True,
                            weekly_seasonality=True, **ps)  # Best parameters
            # montly seasonality
            model.add_seasonality(name='custom_monthly',
                                period=30.5, fourier_order=10)
            model.add_country_holidays(country_name='UK')  # additional holidays

            model.fit(df_temp)

            # Forecast
            future = model.make_future_dataframe(periods=f_period,  # custom
                                                freq='D', include_history=True)  # number of days to be forecast
            forecast = model.predict(future)
            forecast['category'] = str(cat)

            fig = make_subplots(rows=1, cols=2)
            colors = cycle(plotly.colors.qualitative.Plotly)

            fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["trend"], mode="lines",
                                    marker_color=next(colors)), row=1, col=1)

            colors = cycle(plotly.colors.qualitative.Plotly)
            fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yearly"], mode="lines",
                                    marker_color=next(colors)), row=1, col=2)

            fig.update_layout(xaxis_title="Date", showlegend=False, template=go.layout.Template(),
                            autosize=False,  font=dict(family="Arial", size=10), yaxis_title="Mean daily energy consumption (KWh)", title={'text': 'Tendency and Seasonality ',
                                                                                                                                            'font_family': "Arial",
                                                                                                                                            'y': 0.9,
                                                                                                                                            'x': 0.5,
                                                                                                                                            'xanchor': 'center',
                                                                                                                                            'yanchor': 'top'})

            fig.update_xaxes(tickformat="%b\n%Y")
            figure = fig

            return figure,{'display': 'block'}
        else:
            df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
            figure = px.line(df,
                            x="temperature_min",
                            y="day_avg_consumption")
            figure.update_layout(template=go.layout.Template())
            figure.update_yaxes(rangemode='tozero')
            return figure,{'display': 'None'}
    except:
        df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
        figure = px.line(df,
                        x="temperature_min",
                        y="day_avg_consumption")
        figure.update_layout(template=go.layout.Template())
        figure.update_yaxes(rangemode='tozero')
        return figure,{'display': 'None'}


@app.callback(
    [
    Output("graph33", "figure"),
    Output('graph33', 'style')
    ],
    [
        Input('button-send3', 'n_clicks')
    ],
    [
        State("dropdown3", "value"),
        State("hp1", "value"),
        State("hp2", "value")
    ]
)
def graph33(bt, group, conf_int, f_period):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    try:
        if 'button-send3' in changed_id:
            group_list = str(str(group).replace('[', '(').replace(']', ')'))

            if remote == False:
                query = """select  date_, cast(sum_energy as decimal(10,2)) total_consumption, acorn_category
                from public.daily_group_consumption""" + " where  cast(date_c as date)  between '" + start_date + "' and '" + end_date + "' and acorn_category in " + group_list
            else:
                query = """SELECT * FROM staging.params_gp""" + \
                    " WHERE params_gp.group IN " + group_list

            ps_gp = pd.read_sql(query, engine)

            if remote == False:
                query = """select  date_, cast(sum_energy as decimal(10,2)) total_consumption, acorn_category
                from public.daily_group_consumption""" + " where  cast(date_c as date)  between '" + start_date + "' and '" + end_date + "' and acorn_category in " + group_list
            else:
                query = """select date_, cast(day_avg_consumption as decimal(10,2)) day_avg_consumption, acorn_group_detail
                    from staging.daily_consumption_group""" + ' where acorn_group_detail in ' + group_list

            df_daily_consumption_group = pd.read_sql(query, engine)
            df_daily_consumption_group.rename(columns={"date_": "ds", "day_avg_consumption": "y"},
                                            inplace=True)  # neccesary for Prophet
            df_daily_consumption_group.sort_values(
                ["acorn_group_detail", "ds"], inplace=True)
            uk_holidays = pd.read_sql('''SELECT * FROM staging.holidays''', engine)
            uk_holidays.rename(columns={
                            "bank_holidays": "ds", "type": "holiday"}, inplace=True)  # neccesary for Prophet

            grouped = df_daily_consumption_group.groupby(
                'acorn_group_detail')  # grouped df
            dfs = []
            iw = conf_int / 100

            for g in grouped.groups:
                # get the specific data from each group
                group_df = grouped.get_group(g)
                group_df = group_df.sort_values("ds")
                # get the tuned hyperparameters
                ps = ast.literal_eval(
                    ps_gp[ps_gp['group'] == g]['params'].values[0])
                model = Prophet(holidays=uk_holidays,  # holidays
                                interval_width=iw,  # custom
                                yearly_seasonality=True, weekly_seasonality=True, **ps)  # Best parameters
                # montly seasonality
                model.add_seasonality(name='custom_monthly',
                                    period=30.5, fourier_order=10)
                model.fit(group_df)  # Fit the model
                future_days = model.make_future_dataframe(periods=f_period,  # Input
                                                        freq='D', include_history=True)  # number of days to be forecast
                forecast = model.predict(future_days)
                forecast['group'] = g

                dfs.append(forecast)

            final_groups = pd.concat(dfs, ignore_index=True)
            colors = cycle(plotly.colors.qualitative.Plotly)

            fig = go.Figure()

            for g in grouped.groups:
                group_df = grouped.get_group(g)
                group_df = group_df.sort_values("ds")
                fig.add_trace(
                    go.Scatter(x=group_df["ds"],
                            y=group_df["y"],
                            mode="lines",
                            marker_color=next(colors),
                            showlegend=False))

            fig2 = go.Figure(
                fig.add_traces(
                    data=line(data_frame=final_groups[final_groups["ds"] > '26-02-2014'],
                            x='ds', y='yhat', error_y='yhat_upper', error_x='yhat_lower',
                            error_y_mode='band',  # Here you say `band` or `bar`.
                            color='group')._data),
            )

            fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                            template=go.layout.Template(),
                            autosize=False,
                            xaxis_title="Date",
                            yaxis_title="Mean daily energy consumption (KWh)",
                            font=dict(family="Arial", size=10),
                            title={'text': 'Daily Energy Consumption by ACORN groups',
                                    'font_family': "Arial",
                                    'y': 0.9,
                                    'x': 0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'})

            fig2.update_xaxes(tickformat="%b\n%Y")
            figura = fig2

            return figura,{'display': 'block'}
        else:
            df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
            figure = px.line(df,
                            x="temperature_min",
                            y="day_avg_consumption")
            figure.update_layout(template=go.layout.Template())
            figure.update_yaxes(rangemode='tozero')
            return figure,{'display': 'None'}
    except:
        df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
        figure = px.line(df,
                        x="temperature_min",
                        y="day_avg_consumption")
        figure.update_layout(template=go.layout.Template())
        figure.update_yaxes(rangemode='tozero')
        return figure,{'display': 'None'}


@app.callback(
    [
    Output("graph34", "figure"),
    Output('graph34', 'style')
    ],
    [
        Input('button-send3', 'n_clicks')
    ],
    [
        State("dropdown3", "value"),
        State("hp2", "value")
    ]
)
def graph34(bt, group, f_period):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    try:
        if 'button-send3' in changed_id:
            group_list = str(str(group).replace('[', '(').replace(']', ')'))

            if remote == False:
                query = ""
            else:
                query = """SELECT * FROM staging.params_gp""" + \
                    " WHERE params_gp.group IN " + group_list

            ps_gp = pd.read_sql(query, engine)

            if remote == False:
                query = ""
            else:
                query = """select date_, cast(day_avg_consumption as decimal(10,2)) day_avg_consumption, acorn_group_detail
                    from staging.daily_consumption_group""" + ' where acorn_group_detail in ' + group_list

            df_daily_consumption_group = pd.read_sql(query, engine)
            df_daily_consumption_group.rename(columns={"date_": "ds", "day_avg_consumption": "y"},
                                            inplace=True)  # neccesary for Prophet
            df_daily_consumption_group.sort_values(
                ["acorn_group_detail", "ds"], inplace=True)
            uk_holidays = pd.read_sql('''SELECT * FROM staging.holidays''', engine)
            uk_holidays.rename(columns={
                            "bank_holidays": "ds", "type": "holiday"}, inplace=True)  # neccesary for Prophet

            grouped = df_daily_consumption_group.groupby(
                'acorn_group_detail')  # grouped df
            dfs = []

            for g in grouped.groups:
                # get the specific data from each group
                group_df = grouped.get_group(g)

                # get the tuned hyperparameters
                ps = ast.literal_eval(
                    ps_gp[ps_gp['group'] == g]['params'].values[0])
                model = Prophet(holidays=uk_holidays,  # holidays
                                interval_width=0.95,  # custom
                                yearly_seasonality=True, weekly_seasonality=True, **ps)  # Best parameters
                # montly seasonality
                model.add_seasonality(name='custom_monthly',
                                    period=30.5, fourier_order=10)
                model.fit(group_df)  # Fit the model
                future_days = model.make_future_dataframe(periods=f_period,  # Input
                                                        freq='D', include_history=True)  # number of days to be forecast
                forecast = model.predict(future_days)
                forecast['group'] = g

                dfs.append(forecast)

            final_groups = pd.concat(dfs, ignore_index=True)

            fig = make_subplots(rows=1, cols=2)
            colors = cycle(plotly.colors.qualitative.Plotly)

            for group in final_groups.group.unique():
                dfc = final_groups[final_groups["group"] == group]
                fig.add_trace(go.Scatter(x=dfc["ds"],
                                        y=dfc["trend"],
                                        mode="lines",
                                        marker_color=next(colors)),
                            row=1, col=1)

            colors = cycle(plotly.colors.qualitative.Plotly)
            for group in final_groups.group.unique():
                dfc = final_groups[final_groups["group"] == group]
                fig.add_trace(go.Scatter(x=dfc["ds"],
                                        y=dfc["yearly"],
                                        mode="lines",
                                        marker_color=next(colors)),
                            row=1, col=2)

            fig.update_layout(xaxis_title="Date",
                            showlegend=False, template=go.layout.Template(),
                            autosize=False,
                            font=dict(family="Arial", size=10), yaxis_title="Mean daily energy consumption (KWh)", title={'text': 'Tendency and Seasonality ',
                                                                                                                            'font_family': "Arial",
                                                                                                                            'y': 0.9,
                                                                                                                            'x': 0.5,
                                                                                                                            'xanchor': 'center',
                                                                                                                            'yanchor': 'top'})

            fig.update_xaxes(tickformat="%b\n%Y")
            figura = fig

            return figura,{'display': 'block'}
        else:
            df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
            figure = px.line(df,
                            x="temperature_min",
                            y="day_avg_consumption")
            figure.update_layout(template=go.layout.Template())
            figure.update_yaxes(rangemode='tozero')
            return figure,{'display': 'None'}
    except:
        df = pd.DataFrame(
                {'temperature_min': [0, 4], 'day_avg_consumption': [0, 2]})
        figure = px.line(df,
                        x="temperature_min",
                        y="day_avg_consumption")
        figure.update_layout(template=go.layout.Template())
        figure.update_yaxes(rangemode='tozero')
        return figure,{'display': 'None'}


@ app.callback(
    [
        Output('select-season', 'disabled'),
        Output('my-date-picker-range', 'disabled'),
        Output('output-container-date-picker-range', 'hidden'),
        Output('select-season', 'style'),
        Output('my-date-picker-range', 'style'),
    ],
    Input('radioTime', 'value')
)
def time_selector(selection):
    if selection == 'Seasons':
        return False, True, True, {'opacity': '100%'}, {'opacity': '50%'}
    else:
        return True, False, False, {'opacity': '50%'}, {'opacity': '100%'}


@ app.callback(
    [
        Output('select-season2', 'disabled'),
        Output('my-date-picker-range2', 'disabled'),
        Output('output-container-date-picker-range2', 'hidden'),
        Output('select-season2', 'style'),
        Output('my-date-picker-range2', 'style'),
    ],
    Input('radioTime2', 'value')
)
def time_selector(selection):
    if selection == 'Seasons':
        return False, True, True, {'opacity': '100%'}, {'opacity': '50%'}
    else:
        return True, False, False, {'opacity': '50%'}, {'opacity': '100%'}


@ app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


@ app.callback(
    Output('output-container-date-picker-range2', 'children'),
    Input('my-date-picker-range2', 'start_date'),
    Input('my-date-picker-range2', 'end_date'))
def update_output(start_date, end_date):

    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


@ app.callback(
    [Output('dropdown2', 'options'),
     Output('dropdown2', 'value')],
    Input('radio3', 'value'))
def dropdown_options(radio_value):
    aa_list = ['Executive Wealth', 'Lavish Lifestyles', "Mature Money"]
    cc_list = ["Comfortable Seniors", "Countryside Communities",
               "Starting Out", "Steady Neighbourhoods ", "Successful Suburbs"]
    fs_list = ["Modest Means", "Poorer Pensioners",
               "Striving Families", "Student Life"]
    nph_list = ["Not Private Households"]
    rp_list = ["Career Climbers", "City Sophisticates"]
    ua_list = ["Difficult Circumstances",
               "Struggling Estates", 'Young Hardship']

    if radio_value == 'Affluent Achievers':
        options = [{'label': x, 'value': x} for x in aa_list]
        value = "['"+aa_list[0]+"']"
    elif radio_value == "Comfortable Communities":
        options = [{'label': x, 'value': x} for x in cc_list]
        value = "['"+cc_list[0]+"']"
    elif radio_value == "Financially Stretched":
        options = [{'label': x, 'value': x} for x in fs_list]
        value = "['"+fs_list[0]+"']"
    elif radio_value == "Not Private Households":
        options = [{'label': x, 'value': x} for x in nph_list]
        value = "['"+nph_list[0]+"']"
    elif radio_value == "Rising Prosperity":
        options = [{'label': x, 'value': x} for x in rp_list]
        value = "['"+rp_list[0]+"']"
    elif radio_value == "Urban Adversity":
        options = [{'label': x, 'value': x} for x in ua_list]
        value = "['"+ua_list[0]+"']"

    return options, value


@ app.callback(
    [Output('dropdown3', 'options'),
     Output('dropdown3', 'value')],
    Input('radio4', 'value'))
def dropdown_options(radio_value):
    aa_list = ['Executive Wealth', 'Lavish Lifestyles', "Mature Money"]
    cc_list = ["Comfortable Seniors", "Countryside Communities",
               "Starting Out", "Steady Neighbourhoods ", "Successful Suburbs"]
    fs_list = ["Modest Means", "Poorer Pensioners",
               "Striving Families", "Student Life"]
    nph_list = ["Not Private Households"]
    rp_list = ["Career Climbers", "City Sophisticates"]
    ua_list = ["Difficult Circumstances",
               "Struggling Estates", 'Young Hardship']

    if radio_value == 'Affluent Achievers':
        options = [{'label': x, 'value': x} for x in aa_list]
        value = "['"+aa_list[0]+"']"
    elif radio_value == "Comfortable Communities":
        options = [{'label': x, 'value': x} for x in cc_list]
        value = "['"+cc_list[0]+"']"
    elif radio_value == "Financially Stretched":
        options = [{'label': x, 'value': x} for x in fs_list]
        value = "['"+fs_list[0]+"']"
    elif radio_value == "Not Private Households":
        options = [{'label': x, 'value': x} for x in nph_list]
        value = "['"+nph_list[0]+"']"
    elif radio_value == "Rising Prosperity":
        options = [{'label': x, 'value': x} for x in rp_list]
        value = "['"+rp_list[0]+"']"
    elif radio_value == "Urban Adversity":
        options = [{'label': x, 'value': x} for x in ua_list]
        value = "['"+ua_list[0]+"']"

    return options, value


if __name__ == "__main__":
    app.run_server(
        host='0.0.0.0', port=8050,
        debug=False, dev_tools_hot_reload=True  # recargar pagina
    )
