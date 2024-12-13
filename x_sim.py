import streamlit as st
import pandas as pd
from pprint import pprint
from pool  import Pool
from camera  import Camera
from x_network import Network
from x_lens    import Lens
from view      import View
from x_cyangear  import Cyangear
from message   import Messages
from draw      import Draw

def ui_init():
    # Define first state
    st.session_state.running = True
    st.session_state.camera   = Camera(update=True)
    st.session_state.pool     = Pool()
    st.session_state.network  = Network(st.session_state.pool)
    st.session_state.lens     = Lens(st.session_state.pool)
    st.session_state.cyangear = Cyangear(st.session_state.pool)
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
cameraSelection,networkSelection,lensSelection, mermaid, motivations = st.tabs(["Cameras","IP Network" ,"Lens", "Scheme","Motivations"])
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
    camera_pool = st.session_state.camera.view.display_selected()
    st.session_state.pool.update(camera_pool)
    with st.expander("More info about selected cameras",expanded=False):
        message = st.session_state.messages.display(object=st.session_state.camera.view)
        st.write(message)
with networkSelection:
    if not st.session_state.pool.df.empty :
        st.subheader('Select networks (optional):')
        st.session_state.network.edit()
        st.session_state.analyze_done = True
        with st.expander("Required equipment for use case",expanded=False):
            message = st.session_state.messages.display(object=st.session_state.cyangear)
            st.write(message)
with lensSelection:
    if not st.session_state.pool.df.empty :
        st.session_state.lens.edit()
        #st.session_state.cyangear.setdf(lens_df)
        st.session_state.cyangear.analyze()
        st.session_state.analyze_done = True
with motivations:
    if st.button("Motivation"):
        st.rerun()
with mermaid:
    if st.session_state.analyze_done :
        # MERMAID RENDERING
        html = st.session_state.draw.mermaidize(st.session_state.cyangear)
        st.write(html, unsafe_allow_html=True)
