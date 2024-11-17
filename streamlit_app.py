import streamlit as st

# Page setup 
about_page = st.Page(
    page="views/About.py",
    title="About",
    icon="😎",
    default=True
)
project_1_page= st.Page(
    page="views/StockDashBoard.py",
    title="Stock DashBoard",
    icon="🎯",
)
project_2_page=st.Page(
    page="views/NSEListing.py",
    title="Ticker Details",
    icon="✔"
)
project_3_page=st.Page(
    page="views/StockInINR.py",
    title="Stock in INR",
    icon="📣"
)
project_4_page=st.Page(
    page="views/TopPerformerNSE.py",
    title="Top Performer NSE",
    icon="💎"
)

# Navigation 
# app_pages = st.navigation(pages=[about_page, project_1_page, project_2_page, project_3_page, project_4_page])
app_pages = st.navigation(
    {
        "Info": [about_page],
        "Projects": [project_1_page, project_2_page, project_3_page, project_4_page]
    }
)

app_pages.run()

# share accross pages
github_url = "https://github.com/Siddharthbadal/"
linkedin_url = "https://www.linkedin.com/in/siddharthbadal/"
st.sidebar.text("Build by Siddharth")
st.sidebar.write(" [Github](%s) " % github_url , " [LinkedIn](%s)" % linkedin_url)