import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to PálmaVillApp! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This project is designed to help the Bajdor family with their tax administrative tasks.

    **👈 Select a demo from the sidebar** to see some examples
    of what this project can do!

    Or alternatively, click on these links below:"""
)
st.page_link(
    "pages/1_Find_missing_accounts.py", label="Find missing accounts", icon="🔍"
)
st.page_link("pages/2_Create_documents.py", label="Create documents", icon="📄")
st.markdown(
    """    ### Want to learn more?
    - Check out the project's [GitHub repository](https://github.com/jrysztv/palmavillapp)
"""
)
