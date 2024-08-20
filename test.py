import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set page configuration
st.set_page_config(page_title="Device's data chart", page_icon="🔧", layout="wide", initial_sidebar_state="expanded")

# Mock data for multiple devices with a data point every 6 hours for one month
device_names = [f'MedDevice_{i:03d}' for i in range(10)]  # 10 devices with names like MedDevice_001, MedDevice_002, etc.
data = {
    'device_id': np.repeat(device_names, 120),  # 120 data points per device for a month with 6-hour intervals
    'datetime': pd.date_range('2023-01-01', periods=120, freq='6H').tolist() * 10,
    'voltage': np.random.uniform(210, 230, 1200),
    'current': np.random.uniform(0.1, 2.0, 1200),
    'temperature': np.random.uniform(22, 45, 1200),
    'humidity': np.random.uniform(30, 70, 1200),
    'vibration': np.random.uniform(0.0, 1.0, 1200)
}

# Introduce more abnormal data points as patterns
pattern_length = 10  # Length of the abnormal pattern
num_patterns = 5  # Number of patterns to introduce

for _ in range(num_patterns):
    start_index = np.random.randint(0, 1200 - pattern_length)
    end_index = start_index + pattern_length
    data['voltage'][start_index:end_index] = np.linspace(240, 250, pattern_length)  # Voltage pattern
    data['current'][start_index:end_index] = np.linspace(2.5, 3.0, pattern_length)  # Current pattern
    data['temperature'][start_index:end_index] = np.linspace(50, 60, pattern_length)  # Temperature pattern
    data['humidity'][start_index:end_index] = np.linspace(80, 90, pattern_length)  # Humidity pattern
    data['vibration'][start_index:end_index] = np.linspace(1.5, 2.0, pattern_length)  # Vibration pattern

# Convert to DataFrame
df = pd.DataFrame(data)

# Flag abnormal points based on allowable ranges
df['is_abnormal'] = (
    (df['voltage'] > 230) |
    (df['current'] > 2.0) |
    (df['temperature'] > 45) |
    (df['humidity'] > 70) |
    (df['vibration'] > 1.0)
)

# Device ID selection
selected_device_id = st.sidebar.selectbox('Select Device ID', device_names)

# Main content
t1, t2 = st.columns((3, 2))
t1.title("Device's data chart")

# Date range selection
start_date = st.sidebar.date_input("Start date", df['datetime'].min())
end_date = st.sidebar.date_input("End date", df['datetime'].max())

# Filter data based on selected device ID and date range
filtered_df = df[(df['device_id'] == selected_device_id) & (df['datetime'] >= pd.to_datetime(start_date)) & (df['datetime'] <= pd.to_datetime(end_date))]

# Mock prediction data
predicted_voltage = np.random.uniform(210, 230)
predicted_current = np.random.uniform(0.1, 2.0)
predicted_temperature = np.random.uniform(22, 45)
predicted_humidity = np.random.uniform(30, 70)
predicted_vibration = np.random.uniform(0.0, 1.0)

# Calculate the percentage of abnormal data points
total_points = len(filtered_df)
abnormal_points = filtered_df['is_abnormal'].sum()
abnormal_percentage = (abnormal_points / total_points) * 100
health_percentage = 100 - abnormal_percentage

# Calculate health percentages for each parameter
voltage_health = 100 - (filtered_df['voltage'] > 230).sum() / total_points * 100
current_health = 100 - (filtered_df['current'] > 2.0).sum() / total_points * 100
temperature_health = 100 - (filtered_df['temperature'] > 45).sum() / total_points * 100
humidity_health = 100 - (filtered_df['humidity'] > 70).sum() / total_points * 100
vibration_health = 100 - (filtered_df['vibration'] > 1.0).sum() / total_points * 100

# Display health status with progress bars
st.sidebar.markdown("### Device Health Status")
st.sidebar.progress(health_percentage / 100)
st.sidebar.markdown(f"**Overall Health Percentage:** {health_percentage:.2f}%")

st.sidebar.markdown("### Parameter Health Status")
st.sidebar.markdown("**Voltage Health**")
st.sidebar.progress(voltage_health / 100)
st.sidebar.markdown(f"{voltage_health:.2f}%")

st.sidebar.markdown("**Current Health**")
st.sidebar.progress(current_health / 100)
st.sidebar.markdown(f"{current_health:.2f}%")

st.sidebar.markdown("**Temperature Health**")
st.sidebar.progress(temperature_health / 100)
st.sidebar.markdown(f"{temperature_health:.2f}%")

st.sidebar.markdown("**Humidity Health**")
st.sidebar.progress(humidity_health / 100)
st.sidebar.markdown(f"{humidity_health:.2f}%")

st.sidebar.markdown("**Vibration Health**")
st.sidebar.progress(vibration_health / 100)
st.sidebar.markdown(f"{vibration_health:.2f}%")

def plot_and_display_stats(df, y_column, title, unit, col, y_min, y_max):
    y_axis_title = f"{title} ({unit})"
    
    # Check for abnormal points and display warning if necessary
    abnormal_points = df[df['is_abnormal']]
    if not abnormal_points.empty:
        col.warning(f"Warning: Detected abnormal points in {title}.")
        y_max = max(y_max, abnormal_points[y_column].max())
        y_min = min(y_min, abnormal_points[y_column].min())
    
    # Plot the chart
    fig = px.line(df, x='datetime', y=y_column, title=title, height=500)  # Set chart height
    fig.update_traces(line=dict(color='#1f77b4'), mode='lines')  # Set line color to soft blue and remove markers
    fig.update_layout(
        plot_bgcolor='#FFFFFF',  # Set plot background color to white
        paper_bgcolor='#FFFFFF',  # Set paper background color to white
        font=dict(color='#000000'),  # Set font color to black for better contrast
        title_font=dict(size=24, color='#000000', family='Arial'),  # Set title font
        xaxis=dict(showgrid=True, gridcolor='#E0E0E0', title='Datetime'),  # Show x-axis grid lines with light gray color and set x-axis title
        yaxis=dict(showgrid=True, gridcolor='#E0E0E0', title=y_axis_title, title_standoff=25, titlefont=dict(size=14), tickangle=0, range=[y_min, y_max])  # Show y-axis grid lines with light gray color and set y-axis title with standoff and horizontal alignment
    )
    fig.update_xaxes(rangeslider=dict(visible=True))
    
    # Highlight abnormal points
    fig.add_scatter(x=abnormal_points['datetime'], y=abnormal_points[y_column], mode='markers', marker=dict(color='red', size=10), name='Abnormal Points')
    
    col.plotly_chart(fig, use_container_width=True)

# Create a 3x3 grid layout for the charts
cols = st.columns(3)

# Display content with units in y-axis titles and specified min/max values
plot_and_display_stats(filtered_df, 'voltage', 'Voltage', 'V', cols[0], 100, 300)
plot_and_display_stats(filtered_df, 'current', 'Current', 'A', cols[1], 0, 5)
plot_and_display_stats(filtered_df, 'temperature', 'Temperature', '°C', cols[2], 10, 50)
plot_and_display_stats(filtered_df, 'humidity', 'Humidity', '%', cols[0], 0, 100)
plot_and_display_stats(filtered_df, 'vibration', 'Vibration', 'G', cols[1], -1, 1)