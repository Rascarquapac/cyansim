import streamlit as st
import pandas as pd
import json as json
from descriptor import Descriptor
from user_interface import Pool, Sidebar, ViewCamera, ViewNetwork, ViewLens
from case import Case
from gear     import Cyangear
from message  import Messages
from draw     import Draw

def ui_init():
    # PARAMETERS
    casefile  = "./data/xcase_initcase.json"
    gsheet    = True if st.secrets.parameters.gsheet    == "True" else False
    case_init = True if st.secrets.parameters.case_init == "True" else False
    # Load objects once
    descriptor = Descriptor(updateFromGsheet=gsheet)
    camera     = ViewCamera(descriptor)
    pool       = Pool()
    case       = Case(camera=camera,pool=pool,active=case_init,filename=casefile)
    network    = ViewNetwork(pool)
    lens       = ViewLens(pool)
    cyangear   = Cyangear(pool)
    # set running toggle avoiding multiple intialisations
    st.session_state.running    = True
    # Define session_state objects
    st.session_state.camera   = camera
    st.session_state.pool     = pool
    st.session_state.case     = case
    st.session_state.network  = network
    st.session_state.lens     = lens
    st.session_state.cyangear = cyangear
    st.session_state.messages = Messages()
    st.session_state.sidebar  = Sidebar()
    st.session_state.draw     = Draw()
    # 
    st.session_state.analyze_done = False

     
# User Interface initialisation
if 'running' not in st.session_state:
    ui_init()
# Set title
st.header('Cyanview Gear Simulator V0.0')
# Logo
st.logo("images/cyan-logo-letters-light_background.png")
# Set sidebar
st.session_state.sidebar.display()
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
            on_change   = st.session_state.camera.select)
    with col2:
        brand = st.selectbox(
            label   = "Select Brand:",
            options = st.session_state.camera.brand_df,
            index   = None,
            key     = "brand_selector",
            placeholder = "Choose an option",
            on_change   = st.session_state.camera.select)
    with col3:
        camtype = st.selectbox(
            label   = "Select Camera Type:",
            options = st.session_state.camera.type_df,
            index   = None,
            key     = "type_selector",
            placeholder = "Choose an option",
            on_change   = st.session_state.camera.select)
    st.session_state.camera.edit_number()
    st.divider()
    st.caption("Your Current Cameras Pool")
    camera_pool = st.session_state.camera.display_selected()
    st.session_state.pool.build(camera_pool)
    with st.expander("More info about selected cameras",expanded=False):
        message = st.session_state.messages.camera_comments(st.session_state.camera)
        st.write(message)
with networkSelection:
    if not st.session_state.pool.df.empty :
        st.subheader('Select networks (optional):')
        st.session_state.network.edit()
        st.session_state.analyze_done = True
        with st.expander("Required equipment for use case",expanded=False):
            message = st.session_state.messages.gear_list(st.session_state.cyangear)
            print("Message:",message)
            st.write(message)
with lensSelection:
    if not st.session_state.pool.df.empty :
        st.session_state.lens.edit()
        st.session_state.cyangear.analyze()
        st.session_state.analyze_done = True
with motivations:
    if st.button("Motivation"):
        st.rerun()
with mermaid:
    if st.session_state.analyze_done :
        # MERMAID RENDERING
        html = st.session_state.draw.mermaidize(st.session_state.cyangear)
        st.write("test")
        st.write(html, unsafe_allow_html=True)
st.session_state.case.save_case()
