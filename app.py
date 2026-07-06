import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(page_title="US Top 50 Playlist Performance Analytics", layout="wide")

st.title("🎧 United States Top 50 Playlist & Song Popularity Trend Analysis")
st.markdown("### Historical Playlist Performance Dashboard for Atlantic Recording Corporation")
@st.cache_data
def load_data():
    df = pd.read_excel('Atlantic_United_States.xlsx', sheet_name='Sheet1')
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df['duration_min'] = df['duration_ms'] / 60000
    return df

df = load_data()

st.sidebar.header("🎯 Filter Options")

min_date = df['date'].min().to_pydatetime()
max_date = df['date'].max().to_pydatetime()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

all_artists = sorted(df['artist'].unique())
selected_artist = st.sidebar.selectbox("Select Artist", ["All"] + all_artists)

all_album_types = df['album_type'].unique().tolist()
selected_album_types = st.sidebar.multiselect("Select Album Type", all_album_types, default=all_album_types)

filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
filtered_df = filtered_df[filtered_df['album_type'].isin(selected_album_types)]

if selected_artist != "All":
    filtered_df = filtered_df[filtered_df['artist'] == selected_artist]

st.markdown("---")
st.subheader("📊 Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Playlist Records", f"{len(filtered_df):,}")
with col2:
    st.metric("Unique Songs Tracked", filtered_df['song'].nunique())
with col3:
    st.metric("Unique Artists", filtered_df['artist'].nunique())
with col4:
    explicit_pct = (filtered_df['is_explicit'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric("Explicit Content Share", f"{explicit_pct:.1f}%")

st.markdown("---")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("👑 Artist Dominance Leaderboard")
    top_artists = filtered_df.groupby('artist').size().reset_index(name='Total Days on Chart').sort_values(by='Total Days on Chart', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top_artists, x='Total Days on Chart', y='artist', palette='viridis', ax=ax)
    ax.set_xlabel("Total Days on Chart (Appearances)")
    ax.set_ylabel("Artist")
    st.pyplot(fig)

with row1_col2:
    st.subheader("📈 Popularity vs Playlist Rank Scatter Plot")
    fig, ax = plt.subplots(figsize=(10, 5))
    sample_size = min(2000, len(filtered_df))
    if sample_size > 0:
        sns.scatterplot(data=filtered_df.sample(sample_size, random_state=42), x='position', y='popularity', alpha=0.6, color='dodgerblue', ax=ax)
    ax.set_xlabel("Playlist Position (Rank 1-50)")
    ax.set_ylabel("Popularity Score")
    ax.invert_xaxis()  
    st.pyplot(fig)

st.markdown("---")
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("🎵 Longest Presence (Top 10 Songs)")
    top_songs = filtered_df.groupby(['song', 'artist']).size().reset_index(name='Days on Chart').sort_values(by='Days on Chart', ascending=False).head(10)
    st.dataframe(top_songs, use_container_width=True)

with row2_col2:
    st.subheader("⚠️ Content Strategy Insight (Explicit vs Clean)")
    if len(filtered_df) > 0 and filtered_df['is_explicit'].nunique() > 0:
        fig, ax = plt.subplots(figsize=(6, 4))
        counts = filtered_df['is_explicit'].value_counts()
        
        labels = ['Explicit' if x else 'Clean' for x in counts.index]
        colors = ['#e74c3c' if x else '#2ecc71' for x in counts.index]
        
        ax.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_ylabel("")
        st.pyplot(fig)
    else:
        st.info("No sufficient explicit/clean mix data available for this selection.")

print("Streamlit app code is successfully written!")