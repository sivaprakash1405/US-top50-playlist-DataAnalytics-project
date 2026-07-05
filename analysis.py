import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("--- [START] Step 2 & Step 3: Analysis & Visualization ---")

# 1. Load Data
df = pd.read_excel('Atlantic_United_States.xlsx', sheet_name='Sheet1')
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

# 2. Feature Engineering
df['duration_min'] = df['duration_ms'] / 60000

# Grouping by Song to find Longevity & Volatility
song_stats = df.groupby(['song', 'artist']).agg(
    days_on_chart=('date', 'count'),
    avg_rank=('position', 'mean'),
    best_rank=('position', 'min'),
    rank_volatility=('position', 'std')
).reset_index().fillna(0)

# Grouping by Artist to find Dominance
artist_stats = df.groupby('artist').agg(
    total_appearances=('date', 'count'),
    unique_songs=('song', 'nunique')
).reset_index()

# 3. Print Key Insights to Terminal
print("\n🔥 TOP 5 SONGS WITH LONGEST PRESENCE (LONGEVITY):")
print(song_stats.sort_values(by='days_on_chart', ascending=False).head(5)[['song', 'artist', 'days_on_chart']])

print("\n👑 TOP 5 DOMINANT ARTISTS IN THE US CHARTS:")
print(artist_stats.sort_values(by='total_appearances', ascending=False).head(5))

print("\n📢 CONTENT ATTRIBUTE SHARE (Explicit vs Clean Songs):")
explicit_share = df['is_explicit'].value_counts(normalize=True) * 100
print(f"Explicit Songs: {explicit_share.get(True, 0):.2f}%")
print(f"Clean Songs: {explicit_share.get(False, 0):.2f}%")

# 4. Create and Save a Chart
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df.sample(2000, random_state=42), x='duration_min', y='popularity', alpha=0.5, color='purple')
plt.title('Song Duration (Minutes) vs Popularity Score')
plt.xlabel('Duration in Minutes')
plt.ylabel('Popularity Score')
plt.grid(True)
plt.savefig('duration_vs_popularity.png')
print("\n📊 Chart saved successfully as 'duration_vs_popularity.png'!")

print("\n--- [SUCCESS] Step 2 and Step 3 Completed! ---")