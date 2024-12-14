import streamlit as st

class Sidebar():
    def __init__(self) -> None:
        pass
    # SIDEBAR
    def display(self):
        # Sidebar
        st.sidebar.header(("Workflow"))
        st.sidebar.markdown((
            """
        1. Set **Cameras** pool
        2. Set **IP Network** mediums
        3. Set **Lenses**
        4. **Refine** your use-case
        """))
        st.sidebar.header(("Outputs"))
        st.sidebar.markdown((
            """
        1. **Schema** of use-case, 
        2. List of equipment for quote
        3. Tips, attention points, explanations
        """
        ))

        st.sidebar.header(("Resources"))
        st.sidebar.markdown((
            """
        - [Support Documentation](https://support.cyanview.com)
        - [Website](https://www.cyanview.com)
        - [Presentation](https://www.cyanview.com/presentation)
        - [Blog](https://www.cyanview.com/blog) (How to master Streamlit for data science)
        """
        ))

        st.sidebar.header(("About Cyanview"))
        st.sidebar.markdown((
            "[Cyanview](https://www.cyanview.com) is a company providing shading solutions for video productions."
        ))
        return 

 