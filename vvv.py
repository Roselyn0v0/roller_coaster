"""
Name:       Roselyn Wang
CS230:      Section 4
Data:       RollerCoaster
URL:        Link to your web application on Streamlit Cloud (if posted)

Description:

This program ... (List all the features you included)
"""



import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt


tab1, tab2, tab3, tab4 = st.tabs(["Find <State> and <Design> ", "Find fastest speed in <Park>",
                            "Compare roller-coasters performance", "Don’t know what to ride? "
                                                                   "Find the roller-coaster that fits you "])

# Load data
def load_data():
    #path = "/Users/roselyn/Desktop/CS230pythonProject/final/"
    df = pd.read_csv("RCG.csv")
    return df

df = load_data()

with tab1:
    # User input
    st.title('Find all of the roller-coasters in <state> that is <Design>?')

    expander = st.expander('Description', expanded=False)
    expander.write("""
    This query is designed to help individuals locate specific roller coasters within a particular state. 
    This query utilizes a map interface to display the location of roller coasters that meet the specified design criteria. 
    The user can enter the name of a state and a roller coaster design type they are interested in (sit down, inverted, 
    stand up, flying, 4th dimension, wing) into the category bar. The map will then display markers that represent the 
    locations of all the roller coasters in that state that meet the specified design criteria. The map interface allows 
    users to zoom in and out of the map to view the markers more closely and click on individual markers to see additional 
    information about each roller coaster. This query is particularly useful for people who are planning a trip in a specific 
    state that meets their desired design criteria.
    """)

   # Add dropdowns for State, Design and Coaster
    selected_state = st.selectbox('Select a state', options=df['State'].unique())
    selected_design = st.selectbox('Select a design', options=df[df['State'] == selected_state]['Design'].unique())
    selected_coaster = st.selectbox('Select a coaster', options=df[(df['State'] == selected_state) & (df['Design'] == selected_design)]['Coaster'].unique())

   # Filter data for selected state, design, and coaster
    selected_data = df[(df['State'] == selected_state) & (df['Design'] == selected_design) & (df['Coaster'] == selected_coaster)]

   # Replace all NaN values with 0
    selected_data = selected_data.fillna(0)

   # Show map
    st.pydeck_chart(pdk.Deck(
       map_style='mapbox://styles/mapbox/light-v9',
       initial_view_state=pdk.ViewState(
           latitude=selected_data['Latitude'].mean(),
           longitude=selected_data['Longitude'].mean(),
           zoom=11,
           pitch=50,
       ),
       layers=[
           pdk.Layer(
              'ScatterplotLayer',
              data=selected_data,
              get_position='[Longitude, Latitude]',
              get_color='[200, 30, 0, 160]',
              get_radius=100,
           ),
       ],
   ))


with tab2:
    st.title("What’s the fastest <speed> roller-coasters in <park> ?")

    expander2 = st.expander('Description', expanded=False)
    expander2.write("""
    This query is designed to help individuals identify the fastest roller coasters in a particular park. 
    This query utilizes a bar chart interface to display the speed of various roller coasters in the park, 
    allowing users to compare and identify the fastest ones. The user can pick a park in the category drop-down. 
    The x-axis of the bar chart represents the roller coaster's name, and the y-axis represents the speed of the 
    roller coaster. The bar chart allows users to easily compare the speeds of different roller coasters in the park, 
    and identify the fastest ones. In addition to the bar chart, the top 3 in the bar chart. The user could use the 
    color picker to select color for the bars.
    """)

    state_list = df['State'].unique().tolist()
    state_list.sort()
    selected_state = st.selectbox("Please select a state", state_list)

    if selected_state:
        park_list = df[df["State"] == selected_state]['Park'].unique().tolist()
        park_list.sort()
        selected_park = st.selectbox("Please select a park", park_list)

    if selected_park:
        selected_coaster = df[(df["State"] == selected_state) & (df["Park"] == selected_park)]
        selected_coaster = selected_coaster.sort_values(by=["Top_Speed"], ascending=False)
        if not selected_coaster.empty:
            highest_speed_coaster = selected_coaster.iloc[0]
            st.write(f"The highest top speed coaster in {selected_park}, {selected_state} is {highest_speed_coaster['Coaster']} with a top speed of {highest_speed_coaster['Top_Speed']} mph.")

            # Add color picker
            bar_color = st.color_picker('Pick a bar color')

            # Bar chart showing top speed of all roller coasters in the selected park
            chart_data = selected_coaster[["Coaster", "Top_Speed"]]
            chart = alt.Chart(chart_data).mark_bar(color=bar_color).encode(
                x=alt.X('Coaster', sort=alt.EncodingSortField('Top_Speed', order='descending')),
                y='Top_Speed'
            ).properties(width=600, height=400, title=f"Top Speed of Coasters in {selected_park}")
            st.altair_chart(chart)

            # Pivot table showing various statistics for the selected park
            pivot_data = selected_coaster[["Coaster", "Top_Speed", "Max_Height", "Drop", "Length", "Duration", "Inversions", "Num_of_Inversions", "Design"]]
            pivot = pivot_data.pivot_table(index="Design", values=["Coaster", "Top_Speed", "Max_Height", "Drop", "Length", "Duration", "Inversions", "Num_of_Inversions"], aggfunc="max")
            st.write("### Pivot table showing various statistics for fastest roller coasters:")
            st.write(pivot)
        else:
            st.write("No coasters found in this park.")


with tab3:
   st.title("Compare the performance of different roller-coasters")

   expander3 = st.expander('Description', expanded=False)
   expander3.write("""
   This query design enables users to compare the performance of different roller coasters based on various attributes.
   The bar chart interface displays the values of top speed, max height, drop, length, and duration of each roller-
   coaster on the y-axis. And the x-axis represents the different roller-coaster names. This allows the users to 
   compare the performance of the different roller-coaster easily. 
   """)

   # Get unique list of states, parks, and coasters
   state_list = df['State'].unique().tolist()
   state_list.sort()
   park_list = df['Park'].unique().tolist()
   park_list.sort()
   coaster_list = df['Coaster'].unique().tolist()
   coaster_list.sort()

   # Create side-by-side selectboxes and chart
   left_col, right_col = st.columns(2)
   with left_col:
       selected_state = st.selectbox("Select a state", state_list, key="left_state")
       parks_in_state = df[df["State"] == selected_state]["Park"].unique().tolist()
       selected_park = st.selectbox("Select a park", parks_in_state, key="left_park")
       coasters_in_park = df[(df["State"] == selected_state) & (df["Park"] == selected_park)]["Coaster"].unique().tolist()
       selected_coaster = st.selectbox("Select a coaster", coasters_in_park, key="left_coaster")
   with right_col:
       selected_state_2 = st.selectbox("Select a state", state_list, key="right_state")
       parks_in_state_2 = df[df["State"] == selected_state_2]["Park"].unique().tolist()
       selected_park_2 = st.selectbox("Select a park", parks_in_state_2, key="right_park")
       coasters_in_park_2 = df[(df["State"] == selected_state_2) & (df["Park"] == selected_park_2)]["Coaster"].unique().tolist()
       selected_coaster_2 = st.selectbox("Select a coaster", coasters_in_park_2, key="right_coaster")

   # Create bar chart of coaster statistics
   left_chart_data = df[(df["Coaster"] == selected_coaster)][["Top_Speed", "Max_Height", "Drop", "Length", "Duration"]].fillna(0)
   left_chart_data = left_chart_data.melt(var_name="attribute", value_name="value")
   left_chart_data["coaster"] = selected_coaster
   right_chart_data = df[(df["Coaster"] == selected_coaster_2)][["Top_Speed", "Max_Height", "Drop", "Length", "Duration"]].fillna(0)
   right_chart_data = right_chart_data.melt(var_name="attribute", value_name="value")
   right_chart_data["coaster"] = selected_coaster_2
   chart_data = pd.concat([left_chart_data, right_chart_data])

   chart = alt.Chart(chart_data).mark_bar().encode(
       x=alt.X('coaster', axis=alt.Axis(title='')),
       y=alt.Y('value', axis=alt.Axis(title='')),
       color=alt.Color('coaster', scale=alt.Scale(range=['#339CFF', '#FF5733'])),
       column=alt.Column('attribute', header=alt.Header(title='Coaster Attribute'))
   ).properties(width=150, height=500, title=f"Comparison of {selected_coaster} and {selected_coaster_2}")

   # Display the chart
   st.altair_chart(chart)

with tab4:
   st.title('Find the roller-coaster that fits you')

   expander4 = st.expander('Description', expanded=False)
   expander4.write("""
   This query design aims to help users to choose the best roller-coaster ride based on their preferences. 
   There would be sliders where users can adjust the values of top speed, max height, drop, length, duration, 
   inversions, num of inversions, and design. Once the users set the preferred attributes, the interface will 
   display the name of the roller-coaster, and information about the park where the roller-coaster is located. 
   This interface also offers a map feature that allows the user to see the geographic location of the part on the map. 
   """)

   top_speed = st.slider("Top speed in mph", min_value=0, max_value=int(df['Top_Speed'].max()))
   max_height = st.slider("Max height in ft", min_value=0, max_value=int(df['Max_Height'].max()))
   drop = st.slider("Drop in ft", min_value=0, max_value=int(df['Drop'].max()))
   length = st.slider("Length in ft", min_value=0, max_value=int(df['Length'].max()))
   duration = st.slider("Duration in s", min_value=0, max_value=int(df['Duration'].max()))
   inversions = st.slider("Number of inversions", min_value=0, max_value=int(df['Num_of_Inversions'].max()))

   # Filter data
   mask = (df['Top_Speed'] <= top_speed) & (df['Max_Height'] <= max_height) & (df['Drop'] <= drop) & \
          (df['Length'] <= length) & (df['Duration'] <= duration) & (df['Num_of_Inversions'] <= inversions)
   filtered_data = df[mask]

   # Add dropdowns for Park and Coaster
   selected_park = st.selectbox('Select a park', options=filtered_data['Park'].unique())
   selected_coaster = st.selectbox('Select a coaster', options=filtered_data[filtered_data['Park'] == selected_park]['Coaster'])

   # Filter data for selected park and coaster
   selected_data = filtered_data[(filtered_data['Park'] == selected_park) & (filtered_data['Coaster'] == selected_coaster)]

   if not selected_data.empty:
       # Show map
       st.pydeck_chart(pdk.Deck(
           map_style='mapbox://styles/mapbox/light-v9',
           initial_view_state=pdk.ViewState(
               latitude=selected_data.iloc[0]['Latitude'],
               longitude=selected_data.iloc[0]['Longitude'],
               zoom=11,
               pitch=50,
           ),
           layers=[
               pdk.Layer(
                   'ScatterplotLayer',
                   data=selected_data,
                   get_position='[Longitude, Latitude]',
                   get_color='[200, 30, 0, 160]',
                   get_radius=100,
               ),
           ],
       ))
   else:
       st.write("No matching roller-coaster found for the selected filters.")


