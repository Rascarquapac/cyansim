import streamlit as st
import pandas as pd
from pprint import pprint
from camera  import Camera
from network import Network
from lens    import Lens
from view      import View
from cyangear  import Cyangear
from message   import Messages
from draw      import Draw

def ui_init():
    # Define first state
    st.session_state.running = True
    st.session_state.camera   = Camera(update=True)
    st.session_state.network  = Network()
    st.session_state.lens     = Lens()
    st.session_state.cyangear = Cyangear()
    st.session_state.messages = Messages()
    st.session_state.view     = View(st.session_state)
    st.session_state.draw     = Draw()
    # Initiate drawings
    st.session_state.analyze_done = False

# User Interface initialisation
if 'running' not in st.session_state:
    ui_init()
# Set title
st.header('Cyanview Gear Simulator V0.0')
# Logo
st.logo("images/cyan-logo-letters-light_background.png")
# Set sidebar
st.session_state.view.sidebar()
# Set tabs
cameraSelection,networkSelection,lensSelection, motivations, mermaid = st.tabs(["Cameras","IP Network" ,"Lens","Motivations", "Scheme"])
with cameraSelection :
    st.subheader("Setup Camera Pool X")
    col1, col2, col3  = st.columns([0.34,0.33,0.33])
    with col1:
        camera_pattern = st.text_input(
            label = "Camera Pattern:", 
            value = "",
            key   = "camera_pattern",
            placeholder = "Enter substring of camera name",
            on_change   = st.session_state.camera.view.select)
    with col2:
        brand = st.selectbox(
            label   = "Select Brand:",
            options = st.session_state.camera.view.brand_df,
            index   = None,
            key     = "brand_selector",
            placeholder = "Choose an option",
            on_change   = st.session_state.camera.view.select)
    with col3:
        camtype = st.selectbox(
            label   = "Select Camera Type:",
            options = st.session_state.camera.view.type_df,
            index   = None,
            key     = "type_selector",
            placeholder = "Choose an option",
            on_change   = st.session_state.camera.view.select)
    st.session_state.camera.view.edit_number()
    st.divider()
    st.caption("Your Current Cameras Pool")
    selected_df = st.session_state.camera.view.display_selected()
    st.session_state.network.setdf(selected_df)
    with st.expander("More info about selected cameras",expanded=False):
        message = st.session_state.messages.display(object=st.session_state.camera.view)
        st.write(message)
with networkSelection:
    if not st.session_state.network.df.empty :
        st.subheader('Select networks (optional):')
        network_df = st.session_state.network.view.edit(selected_df)
        st.session_state.lens.setdf(network_df)
        st.session_state.analyze_done = True
        with st.expander("Required equipment for use case",expanded=False):
            message = st.session_state.messages.display(object=st.session_state.cyangear)
            st.write(message)
with lensSelection:
    if not st.session_state.lens.df.empty:
        lens_df = st.session_state.lens.view.edit()
        #st.session_state.cyangear.setdf(lens_df)
        st.session_state.cyangear.analyze(lens_df)
        st.session_state.analyze_done = True
with motivations:
    if st.button("Motivation"):
        st.rerun()
with mermaid:
    if st.session_state.analyze_done and not st.session_state.lens.df.empty :
        # MERMAID RENDERING
        html = st.session_state.draw.mermaidize(st.session_state.cyangear)
        st.write(html, unsafe_allow_html=True)
