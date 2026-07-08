"""
Interactive Streamlit app for the Music Recommender System.
Demonstrates all four challenges with an interactive UI.
"""

import streamlit as st
from src.recommender import (
    load_songs,
    recommend_songs,
    BalancedStrategy,
    GenreFirstStrategy,
    MoodFirstStrategy,
    EnergyFocusedStrategy,
)
import pandas as pd

st.set_page_config(
    page_title="🎵 Music Recommender",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🎵 Music Recommender System")
st.markdown(
    "An interactive music recommendation engine with multiple strategies and diversity enforcement."
)

# Load songs
@st.cache_data
def load_data():
    return load_songs("data/songs.csv")

songs = load_data()

# Sidebar controls
st.sidebar.header("🎛️ User Preferences")

genre = st.sidebar.selectbox(
    "Favorite Genre",
    options=sorted(set(song["genre"] for song in songs)),
    index=0,
)

mood = st.sidebar.selectbox(
    "Favorite Mood",
    options=sorted(set(song["mood"] for song in songs)),
    index=0,
)

energy = st.sidebar.slider("Energy Level (0=Low, 1=High)", 0.0, 1.0, 0.5, 0.05)
valence = st.sidebar.slider("Valence/Positivity (0=Dark, 1=Uplifting)", 0.0, 1.0, 0.5, 0.05)
danceability = st.sidebar.slider("Danceability (0=Static, 1=Groovy)", 0.0, 1.0, 0.5, 0.05)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Advanced Options")

prefer_popular = st.sidebar.checkbox("Prefer Popular Songs", value=False)
target_vocal = st.sidebar.checkbox("Vocal Preference", value=False)
if target_vocal:
    vocal_presence = st.sidebar.slider("Vocal Presence", 0.0, 1.0, 0.5, 0.05)
else:
    vocal_presence = None

familiarity_pref = st.sidebar.selectbox(
    "Familiarity Level",
    options=["Any", "Mainstream", "Niche", "Universal"],
)

st.sidebar.markdown("---")
st.sidebar.header("🎯 Recommendation Settings")

strategy_name = st.sidebar.selectbox(
    "Scoring Strategy",
    options=["Balanced (Default)", "Genre-First", "Mood-First", "Energy-Focused"],
)

use_diversity = st.sidebar.checkbox("Enable Diversity Penalties", value=True)
k = st.sidebar.slider("Number of Recommendations", 1, 10, 5)

# Map strategy name to strategy object
strategies = {
    "Balanced (Default)": BalancedStrategy(),
    "Genre-First": GenreFirstStrategy(),
    "Mood-First": MoodFirstStrategy(),
    "Energy-Focused": EnergyFocusedStrategy(),
}
selected_strategy = strategies[strategy_name]

# Build user preferences dict
user_prefs = {
    "genre": genre,
    "mood": mood,
    "energy": energy,
    "valence": valence,
    "danceability": danceability,
    "prefer_popular": prefer_popular,
}

if target_vocal and vocal_presence is not None:
    user_prefs["target_vocal_presence"] = vocal_presence

if familiarity_pref != "Any":
    user_prefs["preferred_familiarity"] = familiarity_pref.lower()

# Get recommendations
recommendations = recommend_songs(user_prefs, songs, k=k, strategy=selected_strategy, use_diversity=use_diversity)

# Display user profile
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Genre", genre)
with col2:
    st.metric("Mood", mood)
with col3:
    st.metric("Energy", f"{energy:.2f}")
with col4:
    st.metric("Valence", f"{valence:.2f}")
with col5:
    st.metric("Danceability", f"{danceability:.2f}")

st.markdown("---")

# Display recommendations
st.subheader(f"🎧 Top {k} Recommendations")
st.markdown(f"**Strategy:** {strategy_name} | **Diversity Penalties:** {'✓ Enabled' if use_diversity else '✗ Disabled'}")

# Create recommendation table
rec_data = []
for rank, (song, score, explanation) in enumerate(recommendations, 1):
    rec_data.append({
        "#": rank,
        "Song": song["title"],
        "Artist": song["artist"],
        "Genre": song["genre"],
        "Mood": song["mood"],
        "Popularity": song["popularity"],
        "Score": f"{score:.2f}",
        "Instrumentation": song["instrumentation"],
    })

df_recs = pd.DataFrame(rec_data)

# Display as table
st.dataframe(
    df_recs,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Score": st.column_config.NumberColumn(format="%.2f"),
    },
)

# Display detailed breakdown
st.markdown("---")
st.subheader("📊 Detailed Score Breakdown")

cols = st.columns(len(recommendations) if len(recommendations) <= 5 else 5)

for idx, (song, score, explanation) in enumerate(recommendations):
    col_idx = idx % 5
    with cols[col_idx]:
        with st.container(border=True):
            st.markdown(f"### {idx + 1}. {song['title']}")
            st.markdown(f"**Artist:** {song['artist']}")
            st.markdown(f"**Genre:** {song['genre']} | **Mood:** {song['mood']}")
            st.markdown(f"**Score:** `{score:.2f}`")
            st.markdown("**Scoring Breakdown:**")

            # Parse and display reasons
            reasons = explanation.split(" | ")
            for reason in reasons:
                st.markdown(f"• {reason}")

# Compare strategies section
st.markdown("---")
st.subheader("🔄 Compare All Strategies")

if st.checkbox("Show strategy comparison", value=False):
    st.markdown("See how different strategies rank the same songs differently:")

    strategy_options = {
        "Balanced": BalancedStrategy(),
        "Genre-First": GenreFirstStrategy(),
        "Mood-First": MoodFirstStrategy(),
        "Energy-Focused": EnergyFocusedStrategy(),
    }

    comparison_data = []

    for strat_name, strat_obj in strategy_options.items():
        recs = recommend_songs(user_prefs, songs, k=3, strategy=strat_obj, use_diversity=False)
        for rank, (song, score, _) in enumerate(recs, 1):
            comparison_data.append({
                "Strategy": strat_name,
                "Rank": rank,
                "Song": song["title"],
                "Artist": song["artist"],
                "Score": f"{score:.2f}",
            })

    df_comparison = pd.DataFrame(comparison_data)

    # Pivot to show side-by-side
    for strategy_name in strategy_options.keys():
        st.markdown(f"#### {strategy_name}")
        strategy_recs = df_comparison[df_comparison["Strategy"] == strategy_name][["Rank", "Song", "Artist", "Score"]]
        st.dataframe(strategy_recs, use_container_width=True, hide_index=True)

# Song catalog section
st.markdown("---")
st.subheader("📚 Full Song Catalog")

if st.checkbox("View all songs", value=False):
    catalog_data = []
    for song in songs:
        catalog_data.append({
            "Title": song["title"],
            "Artist": song["artist"],
            "Genre": song["genre"],
            "Mood": song["mood"],
            "Energy": f"{song['energy']:.2f}",
            "Popularity": song["popularity"],
            "Era": song["release_decade"],
            "Instrumentation": song["instrumentation"],
        })

    df_catalog = pd.DataFrame(catalog_data)
    st.dataframe(df_catalog, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown(
    """
    ### 🎯 About This App

    This music recommender demonstrates four advanced features:
    - **Challenge 4:** Beautiful tabulate-style table output
    - **Challenge 1:** 6 advanced song attributes (popularity, era, instrumentation, etc.)
    - **Challenge 2:** 4 different scoring strategies using the Strategy pattern
    - **Challenge 3:** Diversity penalties to prevent filter bubbles

    Built with Python, Streamlit, and the Strategy design pattern.
    """
)
