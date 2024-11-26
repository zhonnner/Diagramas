import pandas as pd
import plotly.express as px
from datetime import datetime

# Load data
file_path = 'TranscripcionManual.xlsx'
df = pd.read_excel(file_path, sheet_name='Hoja 1')

df['speaker'] = df['speaker'].str.strip().str.upper()
# Convert start_time and end_time to string format if they're datetime.time
if df['start_time'].dtype == 'object':
    df['start_time'] = df['start_time'].astype(str)
if df['end_time'].dtype == 'object':
    df['end_time'] = df['end_time'].astype(str)

# Convert start_time and end_time to timedelta if needed
df['start_time'] = pd.to_timedelta(df['start_time'], errors='coerce')
df['end_time'] = pd.to_timedelta(df['end_time'], errors='coerce')

# Drop rows where conversion failed
df.dropna(subset=['start_time', 'end_time'], inplace=True)

# Set a reference date
reference_date = datetime(2023, 1, 1)

# Convert timedelta to datetime by adding the reference date
df['start_time'] = reference_date + df['start_time']
df['end_time'] = reference_date + df['end_time']

# Map speaker labels to Speaker 1, Speaker 2, etc.
speaker_mapping = {
    'SPEAKER_00': 'Speaker 1',
    'SPEAKER_01': 'Speaker 2',
    'SPEAKER_02': 'Speaker 3',
    'SPEAKER_03': 'Speaker 4'
}
df['speaker'] = df['speaker'].replace(speaker_mapping)

# Verify mapping has no missing values
df.dropna(subset=['speaker'], inplace=True)

# Define a color map for speakers
color_map = {"Speaker 1": "blue", "Speaker 2": "orange", "Speaker 3": "green", "Speaker 4": "red"}

# Generate a timeline plot for each group and save as HTML
for group in df['Grupo'].unique():
    group_df = df[df['Grupo'] == group]
    
    # Create the timeline plot with Plotly
    fig = px.timeline(
        group_df,
        x_start='start_time',
        x_end='end_time',
        y='speaker',
        color='speaker',  # Use speaker as color
        color_discrete_map=color_map,  # Apply custom colors
        title=f'Speaker Timeline for Group {group}',
        labels={'speaker': 'Speaker', 'Grupo': 'Group'},
        category_orders={'speaker': ["Speaker 1", "Speaker 2", "Speaker 3", "Speaker 4"]}
    )

    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Speaker',
        xaxis_tickformat='%H:%M:%S',
        showlegend=False  # Hide legend for a cleaner look
    )
    
    # Save each figure as an HTML file
    fig.write_html(f'intervalos/Group_{group}_Timeline.html')
