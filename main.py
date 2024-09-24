import operations as op
import pandas as pd

var_id = op.get_variable_id("P2412")  # FINANSE PUBLICZNE / DOCHODY BUDŻETÓW WOJEWÓDZTW / DOCHODY NA 1 MIESZKAŃCA
op.print_list(var_id)

years = [str(year) for year in range(2010, 2023)]
var_data = op.get_variable_data("60508", years)
op.print_list(var_data)

var_data_df = pd.DataFrame(var_data)
print(var_data_df)
