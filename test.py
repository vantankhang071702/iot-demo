import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set page configuration
st.set_page_config(page_title="Device's health chart", page_icon="🔧", layout="wide", initial_sidebar_state="expanded")

# Mock data for multiple devices with a data point every hour for one month
device_names = [f'MedDevice_{i:03d}' for i in range(10)]  # 10 devices with names like MedDevice_001, MedDevice_002, etc.
data = {
    'device_id': np.repeat(device_names, 720),  # 720 data points per device for a month with hourly intervals
    'datetime': pd.date_range('2023-01-01', periods=720, freq='H').tolist() * 10,
    'voltage': np.random.uniform(210, 230, 7200),
    'current': np.random.uniform(0.1, 2.0, 7200),
    'temperature': np.random.uniform(22, 45, 7200),
    'humidity': np.random.uniform(30, 70, 7200),
    'vibration': np.random.uniform(0.0, 1.0, 7200)
}

# Introduce abnormal data points as patterns
pattern_length = 10  # Length of the abnormal pattern
num_patterns = 5  # Number of patterns to introduce

for _ in range(num_patterns):
    start_index = np.random.randint(0, 7200 - pattern_length)
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

# Set page background color to match the chart
st.markdown(
    """
    <style>
    .main {
        background-color: #FFFFFF;
        color: #000000;
    }
    .circle {
        display: inline-block;
        width: 60px;
        height: 60px;
        line-height: 60px;
        border-radius: 50%;
        background-color: #1f77b4;
        color: white;
        text-align: center;
        font-size: 16px;
        margin: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Device ID selection
selected_device_id = st.sidebar.selectbox('Select Device ID', device_names)

# Main content
t1, t2 = st.columns((3, 2))
t1.title("Predictive Maintenance Tool")
t1.markdown(f"<h3 style='font-size: 16px;'>Device: {selected_device_id}</h3>", unsafe_allow_html=True)

# Date range selection
start_date = st.sidebar.date_input("Start date", df['datetime'].min())
end_date = st.sidebar.date_input("End date", df['datetime'].max())

# Filter data based on selected device ID and date range
filtered_df = df[(df['device_id'] == selected_device_id) & (df['datetime'] >= pd.to_datetime(start_date)) & (df['datetime'] <= pd.to_datetime(end_date))]

# Prediction section in the sidebar
st.sidebar.header("Prediction")
# Mock prediction data
predicted_voltage = np.random.uniform(210, 230)
predicted_current = np.random.uniform(0.1, 2.0)
predicted_temperature = np.random.uniform(22, 45)
predicted_humidity = np.random.uniform(30, 70)
predicted_vibration = np.random.uniform(0.0, 1.0)

# Display predictions with progress bars
st.sidebar.markdown("### Voltage")
st.sidebar.progress((predicted_voltage - 210) / (230 - 210))
st.sidebar.markdown(f"{predicted_voltage:.2f} V")

st.sidebar.markdown("### Current")
st.sidebar.progress((predicted_current - 0.1) / (2.0 - 0.1))
st.sidebar.markdown(f"{predicted_current:.2f} A")

st.sidebar.markdown("### Temperature")
st.sidebar.progress((predicted_temperature - 22) / (45 - 22))
st.sidebar.markdown(f"{predicted_temperature:.2f} °C")

st.sidebar.markdown("### Humidity")
st.sidebar.progress((predicted_humidity - 30) / (70 - 30))
st.sidebar.markdown(f"{predicted_humidity:.2f} %")

st.sidebar.markdown("### Vibration")
st.sidebar.progress((predicted_vibration - 0.0) / (1.0 - 0.0))
st.sidebar.markdown(f"{predicted_vibration:.2f} G")

def plot_and_display_stats(df, y_column, title, unit):
    y_axis_title = f"{title} ({unit})"
    
    # Check for abnormal points and display warning if necessary
    abnormal_points = df[df['is_abnormal']]
    if not abnormal_points.empty:
        st.warning(f"Warning: Detected abnormal points in {title}.")
    
    # Plot the chart
    fig = px.line(df, x='datetime', y=y_column, title=f'{title} Over Time', height=500)  # Set chart height
    fig.update_traces(line=dict(color='#1f77b4'), mode='lines')  # Set line color to soft blue and remove markers
    fig.update_layout(
        plot_bgcolor='#FFFFFF',  # Set plot background color to white
        paper_bgcolor='#FFFFFF',  # Set paper background color to white
        font=dict(color='#000000'),  # Set font color to black for better contrast
        title_font=dict(size=24, color='#000000', family='Arial'),  # Set title font
        xaxis=dict(showgrid=True, gridcolor='#E0E0E0', title='Datetime'),  # Show x-axis grid lines with light gray color and set x-axis title
        yaxis=dict(showgrid=True, gridcolor='#E0E0E0', title=y_axis_title, title_standoff=25, titlefont=dict(size=14), tickangle=0)  # Show y-axis grid lines with light gray color and set y-axis title with standoff and horizontal alignment
    )
    fig.update_xaxes(rangeslider=dict(visible=True))
    
    # Highlight abnormal points
    fig.add_scatter(x=abnormal_points['datetime'], y=abnormal_points[y_column], mode='markers', marker=dict(color='red', size=10), name='Abnormal Points')
    
    st.plotly_chart(fig, use_container_width=True)

# Display content with units in y-axis titles
plot_and_display_stats(filtered_df, 'voltage', 'Voltage', 'V')
plot_and_display_stats(filtered_df, 'current', 'Current', 'A')
plot_and_display_stats(filtered_df, 'temperature', 'Temperature', '°C')
plot_and_display_stats(filtered_df, 'humidity', 'Humidity', '%')
plot_and_display_stats(filtered_df, 'vibration', 'Vibration', 'G')