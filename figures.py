import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


def generate_plots(_df, years_list):
    for year in years_list:
        _df.sort_values(str(year), ascending=False)
        _fig, ax = plt.subplots(figsize=(9, 9))
        _df.plot(column=str(year), cmap='Purples', linewidth=1.5, ax=ax)

        vmin, vmax = _df[str(year)].min(), _df[str(year)].max()
        sm = plt.cm.ScalarMappable(cmap='Purples', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        sm._A = []
        _fig.colorbar(sm, shrink=0.5, ax=ax)

        ax.grid(True)
        ax.set_axis_off()
        ax.set_title(f'Dochody budżetów województw na 1 mieszkańca [PLN] - rok: {year}')

        plt.tight_layout()
        plt.show()
        _fig.savefig(f'plot_{year}.png')


def plot_01(_df, __df, years_list):
    fig = go.Figure()
    for year in years_list:
        _df_year = _df[['name', year]].rename(columns={year: 'value'})
        _df_year['source'] = 'ŚREDNIA'

        __df_year = __df[['name', year]].rename(columns={year: 'value'})
        __df_year['source'] = 'MEDIANA'

        year_data = pd.concat([_df_year, __df_year])
        fig.add_trace(go.Bar(
            x=year_data[year_data['source'] == 'ŚREDNIA']['name'],
            y=year_data[year_data['source'] == 'ŚREDNIA']['value'],
            name=f'{year} ŚREDNIA',
            visible=(year == '2010'),
            marker_color='blueviolet'
        ))
        fig.add_trace(go.Bar(
            x=year_data[year_data['source'] == 'MEDIANA']['name'],
            y=year_data[year_data['source'] == 'MEDIANA']['value'],
            name=f'{year} MEDIANA',
            visible=(year == '2010'),
            marker_color='crimson'
        ))

    steps = []
    for i, year in enumerate(years_list):
        step = dict(
            method='update',
            args=[{'visible': [False] * len(fig.data)}],
            label=year
        )
        for j in range(i * 2, i * 2 + 2):
            step['args'][0]['visible'][j] = True
        steps.append(step)

    sliders = [dict(
        active=0,
        steps=steps,
        x=0.0,
        y=-0.5,
        currentvalue={'prefix': 'Rok: ', 'font': {'size': 20}},
        pad={'t': 50},
    )]
    fig.update_layout(
        sliders=sliders,
        title='Średnia i mediana cen za 1 m2 lokali mieszkalnych sprzedanych w ramach transakcji rynkowych',
        xaxis_title='Województwo',
        yaxis_title='Cena za 1 m2 [PLN]',
        barmode='group',
        height=600,
        xaxis=dict(
            tickangle=-90,
            tickmode='array',
            tickvals=list(range(len(_df['name']))),
            ticktext=_df['name']
        )
    )
    fig.show()


def plot_02(_df):
    _df = _df.melt(id_vars=['name'], var_name='year', value_name='value')
    names = _df['name'].unique()
    global_min = _df['value'].min()
    global_max = _df['value'].max()

    fig = go.Figure()
    for name in names:
        name_data = _df[_df['name'] == name]
        fig.add_trace(go.Bar(
            x=name_data['year'],
            y=name_data['value'],
            name=name,
            visible=(name == 'MAŁOPOLSKIE'),
            marker_color='blueviolet'
        ))

    steps = []
    for i, name in enumerate(names):
        step = dict(
            method='update',
            label=name,
            args=[{'visible': [False] * len(fig.data)}, {'yaxis': {'range': [global_min, global_max]}}]
        )
        step['args'][0]['visible'][i] = True
        steps.append(step)

    sliders = [dict(
        active=0,
        steps=steps,
        x=0.0,
        y=-0.1
    )]
    fig.update_layout(
        sliders=sliders,
        title='Liczba mieszkań oddanych do użytkowania w latach 2010 - 2022',
        xaxis_title='',
        yaxis_title='',
        yaxis=dict(range=[global_min, global_max]),
        height=600
    )
    fig.show()


def plot_03(_df, __df):
    _df_melted = _df.melt(id_vars=['name'], var_name='Year', value_name='Value')
    __df_melted = __df.melt(id_vars=['name'], var_name='Year', value_name='Value')

    fig = px.scatter(_df_melted, x='Year', y='Value', color='name',
                     title='Przeciętne miesięczne wynagrodzenia brutto')

    fig.add_trace(go.Scatter(
        x=__df_melted['Year'],
        y=__df_melted['Value'],
        mode='markers',
        name='POLSKA',
        marker=dict(color='black', size=10, symbol='x')
    ))
    fig.update_yaxes(range=[2000, 8500])
    fig.update_layout(
        xaxis_title='Rok',
        yaxis_title='Kwota [PLN]',
        legend_title=''
    )
    fig.show()


def plot_04(_df):
    fig = go.Figure()
    for year in range(2010, 2023):
        _df_sorted = _df.sort_values(str(year))

        fig.add_trace(
            go.Bar(
                y=_df_sorted['name'],
                x=_df_sorted[str(year)],
                orientation='h',
                visible=False,
                name=str(year)
            )
        )

    fig.data[0].visible = True
    steps = []
    for i, year in enumerate(range(2010, 2023)):
        step = dict(
            method='update',
            args=[{'visible': [False] * len(fig.data)}],
            label=str(year)
        )
        step['args'][0]['visible'][i] = True
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={'prefix': 'Rok: '},
        pad={'t': 50},
        steps=steps
    )]
    fig.update_traces(marker_color='blueviolet')
    fig.update_layout(
        sliders=sliders,
        xaxis_title='Zyskowność sprzedaży brutto [%]',
        yaxis_title='Województwo',
        title='Wyniki finansowe przedsiębiorstw (PKD 2007) - wskaźniki',
        barmode='stack',
        autosize=False,
        height=600,
        width=1700
    )
    fig.show()
