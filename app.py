import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px 

df = pd.read_csv("data/opening_stats_summary.csv")

sns.set(style="whitegrid")
st.set_page_config(page_title="Opening Advantage Analyzer", layout="centered")

st.title("♟️Chess Opening Analyzer")
st.caption("Analyzed from 2.4 million+ Lichess tournament games.")

tabs = st.tabs([
    "🧠 Intro", "📊 Top Openings", "⚪⚫ Win Rates", 
    "⚖️ Balanced Openings", "📈 Scatter Plot", "💬 Your Move"
])

with tabs[0]:
    st.markdown("## Ever wondered which chess openings *win* more?")
    st.markdown("This app explores patterns in millions of tournament games.")
    st.image("assets/chess_banner.jpg", use_container_width=True)

with tabs[1]:
    st.subheader("Top 10 Most Played Openings")
    top = df.sort_values(by="Total", ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(data=top, y="Opening", x="Total", palette="Blues", ax=ax)
    st.pyplot(fig)

with tabs[2]:
    st.subheader("Is White Still Dominating?")
    total = df[["white", "black", "draw"]].sum()

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        total,
        labels=["White Wins", "Black Wins", "Draws"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#f7f7f7", "#222222", "#999999"],
        textprops={'color': 'black'}, 
    )

    for autotext in autotexts:
        autotext.set_color("#a6eff3") 

    ax.axis("equal")
    st.pyplot(fig)

with tabs[3]:
    st.subheader("Most Balanced (Fair) Openings")
    balanced = df.sort_values(by="WinRate_StdDev").head(5)
    st.dataframe(balanced[["ECO", "Opening", "White_Win_%", "Black_Win_%", "Draw_%", "WinRate_StdDev"]])

with tabs[4]:
    st.subheader("Relationship Between Popularity and Balance")
    fig = px.scatter(
        df,
        x="Total",
        y="WinRate_StdDev",
        color="Draw_%",
        size="Total",
        hover_name="Opening",  
        color_continuous_scale="Bluered_r",
        title="Opening Popularity vs Balance"
    )
    st.plotly_chart(fig)

with tabs[5]:
    st.subheader("Which Opening Do You Use?")
    
    # Cleaner dropdown with ECO codes
    opening_options = df.apply(lambda row: f"{row['ECO']} – {row['Opening']}", axis=1).unique()
    selected_opening = st.selectbox("Pick your favorite opening 🏁", sorted(opening_options))
    st.markdown(f"✅ You selected: **{selected_opening}**")

    st.caption("Made with ❤️ by Af • GitHub: [Afsheen25](https://github.com/Afsheen25)")
