import operations as op
import pandas as pd
import requests
import os
import plot_viewer as pv
import figures as fig

# FINANSE PUBLICZNE / DOCHODY BUDŻETÓW WOJEWÓDZTW / DOCHODY NA 1 MIESZKAŃCA
var_id = op.get_variable_id('P2412')
op.print_list(var_id)

years = [str(year) for year in range(2010, 2023)]
var_data = op.get_variable_data('60508', years)
op.print_list(var_data)

var_data_df = pd.DataFrame(var_data)
print(var_data_df)

url = ('https://www.gis-support.pl/downloads/2022/wojewodztwa.zip?_gl=1*1ftvb4i*_ga*OTY5MTU5MDY4LjE3MTE2NTczMDA'
       '.*_ga_6DGXL861WD*MTcxNjEzMDU5Ni42LjAuMTcxNjEzMDU5Ni42MC4wLjA.')
resp = requests.get(url, allow_redirects=True)

current_dir = os.getcwd()
file_path = os.path.join(current_dir, 'wojewodztwa.zip')
with open(file_path, 'wb') as file:
    file.write(resp.content)

dbf_data = op.read_zipfile(file_path, 'wojewodztwa')
dbf_data = dbf_data.rename(columns={'JPT_NAZWA_': 'name'})
dbf_data['name'] = dbf_data['name'].str.upper()
dbf_data['name'] = dbf_data['name'].apply(op.normalize_text)

merged_df = pd.merge(dbf_data, var_data_df, on='name')
pv.run(merged_df, years)

# RYNEK NIERUCHOMOŚCI / RYNKOWA SPRZEDAŻ LOKALI MIESZKALNYCH / ŚREDNIA CENA ZA 1 M2 LOKALI MIESZKALNYCH SPRZEDANYCH
# W RAMACH TRANSAKCJI RYNKOWYCH
var_id = op.get_variable_id('P3788')
var_data = op.get_variable_data('633692', years)
var_data_df = pd.DataFrame(var_data)
# RYNEK NIERUCHOMOŚCI / RYNKOWA SPRZEDAŻ LOKALI MIESZKALNYCH / MEDIANA CEN ZA 1 M2 LOKALI MIESZKALNYCH SPRZEDANYCH
# W RAMACH TRANSAKCJI RYNKOWYCH
var_id_cmp = op.get_variable_id('P3787')
var_data_cmp = op.get_variable_data('633677', years)
var_data_cmp_df = pd.DataFrame(var_data_cmp)

fig.plot_01(var_data_df, var_data_cmp_df, years)

# PRZEMYSŁ I BUDOWNICTWO / BUDOWNICTWO MIESZKANIOWE / MIESZKANIA ODDANE DO UŻYTKOWANIA
var_id = op.get_variable_id('P3824')
var_data = op.get_variable_data('748601', years)
var_data_df = pd.DataFrame(var_data)

fig.plot_02(var_data_df)

# WYNAGRODZENIA I ŚWIADCZENIA SPOŁECZNE / WYNAGRODZENIA / PRZECIĘTNE MIESIĘCZNE WYNAGRODZENIA BRUTTO
var_id = op.get_variable_id('P2497')
var_data = op.get_variable_data('64428', years)
var_data_df = pd.DataFrame(var_data)
var_data_cmp = op.get_variable_data('64428', years, '0')
var_data_cmp_df = pd.DataFrame(var_data_cmp)

fig.plot_03(var_data_df, var_data_cmp_df)

# FINANSE PRZEDSIĘBIORSTW (DANE KWARTALNE) / WYNIKI FINANSOWE PRZEDSIĘBIORSTW / WYNIKI FINANSOWE (PKD 2007) - WSKAŹNIKI
var_id = op.get_variable_id('P3869')
var_data = op.get_variable_data('1548847', years)
var_data_df = pd.DataFrame(var_data)

fig.plot_04(var_data_df)
