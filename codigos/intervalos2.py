import json
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Load data from JSON
file_path = 'Transcription-18B.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Speaker mapping
speaker_mapping = {
    'SPEAKER_03': 'Speaker 4',
    'SPEAKER_01': 'Speaker 1',
    'SPEAKER_00': 'Speaker 2',
    'SPEAKER_02': 'Speaker 3'
}

# Process data into DataFrame
segments = data['segments']
rows = []
reference_date = datetime(2023, 1, 1)  # Reference date for datetime conversion

for segment in segments:
    speaker = speaker_mapping.get(segment['speaker'], segment['speaker'])
    
    # Convert start and end times from string to timedelta
    start_time = timedelta(
        hours=int(segment['start_time'].split(":")[0]),
        minutes=int(segment['start_time'].split(":")[1]),
        seconds=float(segment['start_time'].split(":")[2])
    )
    end_time = timedelta(
        hours=int(segment['end_time'].split(":")[0]),
        minutes=int(segment['end_time'].split(":")[1]),
        seconds=float(segment['end_time'].split(":")[2])
    )
    
    # Convert timedelta to datetime
    start_time = reference_date + start_time
    end_time = reference_date + end_time
    
    rows.append({'speaker': speaker, 'start_time': start_time, 'end_time': end_time})

df = pd.DataFrame(rows)
color_map = {"Speaker 1": "blue", "Speaker 2": "orange", "Speaker 3": "green", "Speaker 4": "red"}

# Create a timeline plot
fig = px.timeline(
    df,
    x_start='start_time',
    x_end='end_time',
    y='speaker',
    color='speaker',
    color_discrete_map=color_map,  # Apply custom colors
    title='Speaker Timeline for Group 18B',
    labels={'speaker': 'Speaker', 'start_time': 'Start Time', 'end_time': 'End Time'},
    category_orders={'speaker': ['Speaker 1', 'Speaker 2', 'Speaker 3', 'Speaker 4']}
)

# Customize layout
fig.update_layout(
    xaxis_title='Time',
    yaxis_title='Speaker',
    xaxis_tickformat='%H:%M:%S',
    showlegend=False  # Hide legend for a cleaner look
)

fig.write_html(f'intervalos/Group_18B_Timeline.html')
