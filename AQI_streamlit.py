"""
# Breathe Mongolia State of the Air Report
The first SOA Report for Mongolia:
"""

import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

#Load Data and cache it so that it doesn't have to be loaded everytime I update the site
@st.cache_data()
def load_data():
    daily_avg = pd.read_csv('Data/daily_avg.csv')
    AQI_final = pd.read_csv('Data/AQI_final.csv')
    #mng_shp = gpd.read_file("/Users/turbold/Documents/Projects/Green Summer DS/mng-administrative-divisions-shapefiles/mng_admbndp_admALL_nso_itos_20201019.shp")
    #mng_shp.drop(['ADM2_PCODE', 'ADM2_REF', 'ADM2ALT1EN','ADM2ALT2EN', 'ADM2ALT1MN', 'ADM2ALT2MN', 'ADM1_PCODE', 'date', 'validOn', 'validTo'], axis=1, inplace=True)
    #mng_bd = gpd.read_file("/Users/turbold/Documents/Projects/Green Summer DS/mng-administrative-divisions-shapefiles/mng_admbnda_adm1_nso_20201019.shp")
    return daily_avg, AQI_final, #mng_shp, mng_bd

#mng_shp, mng_bd
daily_avg, AQI_final = load_data()

st.title("State of the Air Report Mongolia")

# Add an expandable section with multiple subsections
with st.expander('More Information'):
    # Add an "About" subsection
    st.markdown('### About The Project')
    st.write('Breathe Mongolia\'s Air Quality Report strives to fill a critical gap in our understanding of the air we breathe in this vast and beautiful country. Inspired by the American Lung Association\'s \"State of the Air\" report, our mission is to bring a comprehensive assessment of air quality in Mongolia, raising awareness and advocating for cleaner, healthier air for all. This report is a culmination of meticulous data analysis, showcasing the tangible impact of air quality on public health and the environment. With the nomadic spirit and determination that define Mongolia, we are committed to providing a reliable and insightful resource that will empower individuals and decision-makers alike. Together, let\'s take a deep breath and work towards a greener and cleaner future for Mongolia.')

    # Add a subsection on air quality in Mongolia
    st.markdown('### Air Quality in Mongolia')
    st.write('Mongolia faces a pressing issue when it comes to air quality. With the harsh winters and traditional reliance on coal for heating, air pollution has become a significant concern. Ulaanbaatar, the capital city, is often ranked among the most polluted cities globally, particularly during the winter months. This pollution, primarily from coal and vehicle emissions, poses serious health risks, especially to children and the elderly. However, it\'s important to note that Ulaanbaatar is not the only city impacted. Many other Mongolian cities face similar air quality challenges, and the issue extends throughout the country. Breathe Mongolia is dedicated to shedding light on the severity of this problem, advocating for cleaner alternatives, and working toward a future where every breath of Mongolian air is a breath of fresh, clean life.')

    # Add a subsection on the source code
    st.markdown('### Clean Air for Mongolia')
    st.write('Our goal is to improve awareness and facilitate effective collaboration by offering easily accessible air quality data. This strategy encourages well-informed initiatives, enabling individuals to work together toward the common goal of enhancing air quality. This aligns with Breathe Mongolia\'s core mission of promoting public engagement for a cleaner and healthier environment.')

    # Add a subsection on the source code
    st.markdown('### Source Code')
    st.write('The source code for this project is written in Python and uses the Streamlit and Plotly libraries to create a web-based user-friendly interface. The code is available on GitHub: https://github.com/Puturbold/SOA-Breathe-Mongolia')

    # Add a subsection on the source code
    st.markdown('### Data')
    st.write('The data was obtained by querying the OpenAQ API, a platform that collects air quality information from government agencies and various other data sources. Source: https://openaq.org/')

# Convert the date column to a datetime object
daily_avg['utc_time'] = pd.to_datetime(daily_avg['utc_time'], format='%Y-%m-%d')

year = AQI_final.year.unique()
cities = AQI_final.city.unique()

##### TABLE OF CITIES #####

# Define a CSS style for centering text in a column
css_style = """
<style>
    td:nth-child(2) {
        text-align: center;
    }
</style>
"""

# Display the acceptable levels as a table without row numbers
st.markdown(f'## Air Pollution Grades')

# Transpose the DataFrame without resetting the index
AQI_Report = AQI_final.pivot(index=['city', 'sum_mn'], columns='year', values='Grade')

# Display the transposed DataFrame in a table
st.write(AQI_Report)

###### Select Cities ######

# Create a multiselect widget to allow the user to select the pollutants to display
selected_cities = st.multiselect('Select Cities', cities)

# Filter the data for the selected cities
filtered_data = daily_avg[daily_avg['city'].isin(selected_cities)]
AQI_final_filtered = AQI_final[AQI_final['city'].isin(selected_cities)]

# Display the acceptable levels as a table without row numbers
st.markdown(f'## Population Impacted')

# Transpose the DataFrame without resetting the index
if selected_cities:
    pop_count = AQI_final_filtered.pivot(index=['city', 'sum_mn'], columns='year', values='pop_count')
    # Display the transposed DataFrame in a table
    st.write(pop_count)
else:
    st.write('Please select at least one city.')


###### SCATTER PLOT ######

# Create a scatter plot to display the PM2.5 pollution over time for each city
if selected_cities:
    fig = px.scatter(filtered_data, x='utc_time', y='pm25_µg/m³', color='city')

    # Set the plot title
    fig.update_layout(title=f'Air Quality for Selected Cities')
    
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.write('Please select at least one city.')


st.write(AQI_final)