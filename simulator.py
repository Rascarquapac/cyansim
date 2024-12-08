import streamlit as st
import pandas as pd
from x_camera  import Camera
from x_network import Network
from x_lens    import Lens
from view      import View
from cyangear  import Cyangear
from message   import Messages

def ui_init():
    # Define first state
    st.session_state.running = True
    st.session_state.camera   = Camera(update=True)
    st.session_state.network  = Network()
    st.session_state.lens     = Lens()
    st.session_state.cyangear = Cyangear()
    st.session_state.messages = Messages()
    st.session_state.view     = View(st.session_state)
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
    print("lensSelection:lens.df-->")
    print(st.session_state.lens.df)
    st.subheader("Setup Camera Pool X")
    col1, col2, col3  = st.columns([0.34,0.33,0.33])
    with col1:
        x_camera_pattern = st.text_input(
            label = "Camera Pattern:", 
            value = "",
            key   = "x_camera_pattern",
            placeholder = "Enter substring of camera name",
            on_change   = st.session_state.view.camera_select)
    with col2:
        brand = st.selectbox(
            label   = "Select Brand:",
            options = st.session_state.camera.brand_df,
            index   = None,
            key     = "x_brand_selector",
            placeholder = "Choose an option",
            on_change   = st.session_state.view.camera_select)
    with col3:
        camtype = st.selectbox(
            label   = "Select Camera Type:",
            options = st.session_state.camera.type_df,
            index   = None,
            key     = "x_type_selector",
            placeholder = "Choose an option",
            on_change   = st.session_state.view.camera_select)
    st.session_state.view.camera_edit_number()
    st.divider()
    st.caption("Your Current Cameras Pool")
    network_df = st.session_state.view.camera_display_selected()
    st.session_state.network.setdf(network_df)
    with st.expander("More info about selected cameras",expanded=False):
        message = st.session_state.messages.display(object=st.session_state.camera)
        st.write(message)

with networkSelection:
    if not st.session_state.network.df.empty :
        st.subheader('Select networks (optional):')
        protocol_df = st.session_state.view.network_edit_byblocks()
        st.session_state.lens.setdf(protocol_df)
        st.session_state.cyangear.analyze(st.session_state.lens.df)
        st.session_state.analyze_done = True
        with st.expander("Required equipment for use case",expanded=False):
            message = st.session_state.messages.display(object=st.session_state.cyangear)
            st.write(message)
with lensSelection:
    if not st.session_state.lens.df.empty:
        lens_df = st.session_state.view.lens_edit()
        #st.session_state.cyangear.setdf(lens_df)
        st.session_state.cyangear.analyze(lens_df)
        st.session_state.analyze_done = True
with motivations:
    if st.button("Motivation"):
        st.rerun()
with mermaid:
    if st.session_state.analyze_done and not st.session_state.lens.df.empty :
        # MERMAID RENDERING
        html = st.session_state.cyangear.mermaidize()
        st.write(html, unsafe_allow_html=True)
