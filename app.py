import streamlit as st
from st_pages import Page, show_pages, add_page_title



add_page_title("ALab Leuven Streamlit App")

# Object notatio

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("pages/visualization.py", " Descriptive Dashboard", "🏠"),
        Page("pages/test.py", " Optimization Model Output", "📊"),
    ]
)


