import time
import os
import folium
import chardet
import streamlit as st
from streamlit_folium import st_folium
import streamlit.components.v1 as components
from IPython.display import HTML
import pandas as pd


def get_city_names():
    with open("map_data.csv","rb") as f:
        encoding=chardet.detect(f.read())["encoding"]
    df=pd.read_csv("map_data.csv",encoding=encoding)
    df['lat']=df['lat'].astype(float)
    df['long']=df['long'].astype(float)
    HTML(df.to_html(render_links=True,escape=False))
    return list(df['city'].unique()),df


def generate_map(df, selected_city):
    new_df = df[df['city'] == selected_city]
    if new_df.empty:
        return folium.Map(location=[0, 0], zoom_start=30) 
    map_center = [new_df['lat'].mean(), new_df['long'].mean()]
    f_map = folium.Map(location=map_center, zoom_start=8)

    for _, row in new_df.iterrows():
        folium.Marker(
            location=[row['lat'], row['long']],
            popup=folium.Popup(row['name'], parse_html=True),
            icon=folium.Icon(color='darkpurple', icon='info-sign')
        ).add_to(f_map)
    
    return new_df, f_map._repr_html_()

def side_data(data):
    with st.sidebar:    
        for _,i in data.iterrows():
            base='https://www.google.com/maps/search/'
            place="".join(i['name'].split(" "))
            ne=os.path.join(base,place)
            with st.chat_message("assistant"):
                st.success(f"""
                    **{i['name']}**\n
                    {i['des']}\n
                    [Read more]{ne}
                """)


def main_int():
    #-------------------- main app interface --------------------

    st.title("📚Educational Resource Finder 🗺")
    df=get_city_names()[-1]
    names=['Select city']
    names+=get_city_names()[0]

    col1,col2=st.columns([2,1],gap="medium")
    with col1:
        city=st.selectbox("**Select your city**",options=names,key="choosen_city",on_change=callback_func)
    with col2:
        resource_type=st.radio("**Select resource type**",options=["Public Libary","Computer Center"],index=None)


    #--------------------- sidebar portion -------------------------
    with st.sidebar:
            with st.chat_message("assistant"):
                st.warning(f"Here's more about {resource_type} in your city {city}")


    #--------------------- map genration -------------------------

    generate=st.button("**Generate resource map** 🗺")
    if generate:
        if city!='Select city' and resource_type!=None:
            with st.spinner("Generating response...."):
                    with st.chat_message('ai'):
                        st.success(f"Please wait! I am fetching the best results for {resource_type}'s in {city}")
                    x,map=generate_map(df,city)
                    time.sleep(2)
            with st.container(height=400):
                components.html(map,height=370)
            side_data(x)
        else:
            with st.chat_message('ai'):
                st.error("Inapproiate selection. Please choose appropiate option from both city and resource type to filter results")
    else:
        with st.chat_message('ai'):
            st.info("Please select your city from the above list and resource type then click on above button to fetch appropiate results")
