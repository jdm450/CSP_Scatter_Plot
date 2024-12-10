from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import plotly.express as px

# Creating Tkinter root window
Tk().withdraw()

# Open Finder to select one of the CSV files
file_path = askopenfilename(title="Select CSV file", filetypes=[("CSV Files", "*.csv")])

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Removing commas and percent signs and converting integers to floats
df['OTM Prob'] = df['OTM Prob'].str.replace('%', '').astype(float)
df['Ann Rtn'] = df['Ann Rtn'].str.replace(',', '').replace({r'%': ''}, regex=True).astype(float)
df['IV'] = df['IV'].str.replace('%', '').astype(float)
df['Moneyness'] = df['Moneyness'].str.replace('%', '').str.replace('-', '').astype(float)

# Deleting unnecessary columns from the data frame
columns_to_delete = ['Time', 'Bid', 'BE (Bid)']
df.drop(columns=columns_to_delete, inplace=True, errors='ignore')
df = df.dropna(subset=['Moneyness'])

# Filtering out Options with an Implied Volotality over 100%
filtered_df = df[(df['IV'] < 100)]
df = filtered_df

fig = px.scatter(
    df,
    x='OTM Prob',
    y='Ann Rtn',
    title='Option Contracts Scatter Plot',
    labels={
        'OTM Prob': 'Out of the Money Probability',
        'Ann Rtn': 'Annualized Return (%)',
    },
    hover_data=df.columns,
    # Adding a trendline using OLS regression
    trendline='ols',
    size='Moneyness',
    color='IV'
)

fig.update_layout(
    xaxis=dict(title='OTM Probability %'),
    yaxis=dict(title='Annual Return %'),
    template='plotly_dark'
)

fig.show()