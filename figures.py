import matplotlib.pyplot as plt


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
