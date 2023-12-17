import pandas as pd
from visualize import ExploratoryDataAnalysis

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------

data = pd.read_pickle("../../data/interim/merged_india_nz_arrivals_data.pkl")

# --------------------------------------------------------------
# Create plots
# --------------------------------------------------------------

plot = PlotData()
plot.motor_power(df=data)
plot.speed_vs_temp(df=data)


# Example usage
# df = pd.read_csv('your_data.csv')
# eda = ExploratoryDataAnalysis(df)
# eda.plot_time_series_individual()
# eda.plot_dual_axis_time_series('column1', 'column2')
# ... and so on for other methods

# Vizualise the data
plot_time_series_individual(data)
plot_dual_axis_time_series(data, 'india_arrivals_esimate', 'India_visa_search')

# Check missing values
check_missing_values(data)

# Check distribution
plot_histograms(data)
plot_boxplots(data)

# Check correlations
create_pairgrid_plot_all_columns(data)
plot_all_scatter_combinations(data)  # Plots all combinations
plot_all_scatter_combinations(data, 'india_arrivals_esimate', 'India_visa_search')  # Plots only col1 vs col3
find_lead_lag_relationship(data, 'india_arrivals_esimate', 'India_visa_search', max_lag=36)
plot_dual_axis_time_series(data, 'india_arrivals_esimate', 'India_visa_search', shift_periods=12)

