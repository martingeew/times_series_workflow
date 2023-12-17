import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import combinations
import seaborn as sns
import numpy as np

class ExploratoryDataAnalysis:
    def __init__(self, df):
        self.df = df

    def plot_time_series_individual(self):
        if self.df.index.name != 'Month':
            print("The index of the DataFrame is not 'Month'. Please set the 'Month' column as the index.")
            return

        for column in self.df.columns:
            fig = go.Figure([go.Scatter(x=self.df.index, y=self.df[column], mode='lines', name=column)])
            fig.update_layout(title=f"Time Series Plot of {column}",
                              xaxis_title='Month',
                              yaxis_title='Value',
                              template='plotly_dark')
            fig.show()

    def plot_dual_axis_time_series(self, column1, column2, shift_periods=0):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=self.df.index, y=self.df[column1], name=column1),
            secondary_y=False,
        )

        shifted_column2 = self.df[column2].shift(shift_periods)

        fig.add_trace(
            go.Scatter(x=self.df.index, y=shifted_column2, name=f"{column2} (shifted by {shift_periods})"),
            secondary_y=True,
        )

        fig.update_layout(
            title_text="Time Series with Dual Y-Axis",
            xaxis_title="Month",
            yaxis_title=column1,
            yaxis2_title=f"{column2} (shifted)",
            template="plotly_dark"
        )

        fig.show()

    def check_missing_values(self):
        missing_count = self.df.isnull().sum()
        missing_percentage = (missing_count / len(self.df)) * 100
        missing_df = pd.DataFrame({
            'Missing Values': missing_count,
            'Percentage (%)': missing_percentage
        })
        return missing_df[missing_df['Missing Values'] > 0].sort_values(by='Missing Values', ascending=False)

    def plot_histograms(self):
        for column in self.df.columns:
            fig = go.Figure(data=[go.Histogram(x=self.df[column])])
            fig.update_layout(
                title_text=f'Histogram of {column}',
                xaxis_title_text=column,
                yaxis_title_text='Count',
                bargap=0.2,
                template='plotly_dark'
            )
            fig.show()

    def plot_boxplots(self):
        for column in self.df.columns:
            fig = go.Figure(data=[go.Box(y=self.df[column], name=column)])
            fig.update_layout(
                title_text=f'Boxplot of {column}',
                yaxis_title_text='Value',
                template='plotly_dark'
            )
            fig.show()

    def plot_all_scatter_combinations(self, col1=None, col2=None):
        if col1 is not None and col2 is not None:
            if col1 not in self.df.columns or col2 not in self.df.columns:
                raise ValueError("Specified columns are not in the DataFrame")
            column_pairs = [(col1, col2)]
        else:
            column_pairs = combinations(self.df.columns, 2)

        for col1, col2 in column_pairs:
            fig = go.Figure(data=go.Scatter(x=self.df[col1], y=self.df[col2], mode='markers', name=f'{col1} vs {col2}'))
            fig.update_layout(
                title_text=f'Scatter Plot of {col1} vs {col2}',
                xaxis_title_text=col1,
                yaxis_title_text=col2,
                template='plotly_dark'
            )
            fig.show()

    def find_lead_lag_relationship(self, col1, col2, max_lag=12):
        if col1 not in self.df.columns or col2 not in self.df.columns:
            raise ValueError("Specified columns are not in the DataFrame")

        correlations = []
        for lag in range(-max_lag, max_lag + 1):
            shifted = self.df[col2].shift(lag)
            correlation = self.df[col1].corr(shifted)
            correlations.append(correlation)

        lags = np.arange(-max_lag, max_lag + 1)
        fig = go.Figure(data=go.Scatter(x=lags, y=correlations, mode='lines+markers'))
        fig.update_layout(
            title=f'Cross-Correlation between {col1} and {col2}',
            xaxis_title='Lag',
            yaxis_title='Correlation',
            template='plotly_dark'
        )
        fig.show()

    def create_pairgrid_plot_all_columns(self):
        g = sns.PairGrid(self.df)
        g.map(sns.scatterplot)
        g.fig.suptitle("PairGrid Plot for All Columns", fontsize=12, y=1.05)

