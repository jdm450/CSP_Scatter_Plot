import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import plotly.express as px

Tk().withdraw()
file_path = askopenfilename(title="Select CSV file", filetypes=[("CSV Files", "*.csv")])
df = pd.read_csv(file_path)

# Remove percent signs and convert to float
df['OTM Prob'] = df['OTM Prob'].str.replace('%', '').astype(float)
df['Ann Rtn'] = df['Ann Rtn'].str.replace(',', '').replace({r'%': ''}, regex=True).astype(float)
df['IV'] = df['IV'].str.replace('%', '').astype(float)
df['Moneyness'] = df['Moneyness'].str.replace('%', '').str.replace('-', '').astype(float)

# Deleting unnecessary rows and columns
columns_to_delete = ['Ptnl Rtn', 'Time', 'Bid', 'BE (Bid)']
df.drop(columns=columns_to_delete, inplace=True, errors='ignore')
df = df.dropna(subset=['Moneyness'])

# Function to get a value from Probability - annual return
def put_value(row):
    result = row['OTM Prob'] + row['Ann Rtn']
    if result != 100:
        return result - 100

# Apply the function to create the new column
df['Put Value'] = df.apply(put_value, axis=1)

# Filter to Ann Rtrn between 20 and 50
filtered_df1 = df[(df['Ann Rtn'] >= 20) & (df['Ann Rtn'] <= 70)]

# Filter to Put Value that are positive
filtered_df2 = filtered_df1[filtered_df1['Put Value'] > 0]

filtered_df3 = filtered_df2[filtered_df2['IV'] <= 90]

df = filtered_df3


# Create a Scatter Plot with Trendline
fig = px.scatter(
    df,
    x='Put Value',
    y='Ann Rtn',
    title='CSP filtered Value',
    labels={
        'Put Value': 'Put Value',
        'Ann Rtn': 'Annual Return (%)'
    },
    hover_data=df.columns,
    trendline='ols',  # Adds a linear trendline using OLS regression
    size='Moneyness',
    color='IV'
)
fig.update_layout(
    xaxis=dict(title='Put Value'),
    yaxis=dict(title='Annual Return %'),
    template='plotly_dark'
)
fig.show()