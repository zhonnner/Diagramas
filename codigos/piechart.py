import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser

# Load the JSON data
file_path = 'Transcription-18B.json'
data = pd.read_json(file_path)

# Mapping speakers
speaker_mapping = {
    'SPEAKER_00': 'speaker 2',
    'SPEAKER_01': 'speaker 1',
    'SPEAKER_02': 'speaker 3',
    'SPEAKER_03': 'speaker 4'
}

# Convert start_time and end_time to timedelta and calculate duration
def calculate_duration(start_time, end_time):
    start_dt = parser.parse(start_time)
    end_dt = parser.parse(end_time)
    duration = (end_dt - start_dt).total_seconds()
    return duration

# Extract relevant information
durations = {'speaker 1': 0, 'speaker 2': 0, 'speaker 3': 0, 'speaker 4': 0}
for segment in data['segments']:
    speaker = speaker_mapping[segment['speaker']]
    start_time = segment['start_time']
    end_time = segment['end_time']
    durations[speaker] += calculate_duration(start_time, end_time)

# Plotting pie chart
speakers = list(durations.keys())
time_spoken = list(durations.values())

plt.figure(figsize=(6, 6))
plt.pie(time_spoken, labels=speakers, autopct='%1.1f%%', startangle=90)
plt.title('Percentage of Time Spoken by Each Speaker')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Show the pie chart
plt.show()
