"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import (
    load_songs,
    recommend_songs,
    BalancedStrategy,
    GenreFirstStrategy,
    MoodFirstStrategy,
    EnergyFocusedStrategy,
)
from tabulate import tabulate


def format_recommendations_table(recommendations: list) -> str:
    """Format recommendations as a readable table with scoring breakdown."""
    table_data = []
    for rank, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        table_data.append([
            rank,
            song['title'],
            song['artist'],
            song['genre'],
            f"{score:.2f}",
            explanation
        ])

    headers = ["#", "Song", "Artist", "Genre", "Score", "Reasons"]
    return tabulate(table_data, headers=headers, tablefmt="grid")


def main() -> None:
    songs = load_songs("data/songs.csv")

    # User profile
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.75,
        "danceability": 0.7,
    }

    # Available scoring strategies
    strategies = [
        ("Balanced (Default)", BalancedStrategy()),
        ("Genre-First (Priority)", GenreFirstStrategy()),
        ("Mood-First (Discovery)", MoodFirstStrategy()),
        ("Energy-Focused (Workout)", EnergyFocusedStrategy()),
    ]

    print("\n" + "=" * 100)
    print("🎵 MUSIC RECOMMENDER - MULTIPLE SCORING STRATEGIES 🎵")
    print("=" * 100)
    print(f"\nUser Preferences: Genre={user_prefs['genre']}, Mood={user_prefs['mood']}, Energy={user_prefs['energy']}")
    print("\nComparing recommendations across 4 different scoring strategies...\n")

    for strategy_name, strategy in strategies:
        print(f"\n{'━' * 100}")
        print(f"📌 STRATEGY: {strategy_name}")
        print(f"{'━' * 100}\n")

        recommendations = recommend_songs(user_prefs, songs, k=3, strategy=strategy)
        print(format_recommendations_table(recommendations))
        print()

    # Demonstrate diversity penalties
    print("\n" + "=" * 100)
    print("🔄 DIVERSITY & FAIRNESS PENALTIES 🔄")
    print("=" * 100)
    print("\nDemonstrating how diversity penalties prevent filter bubbles...\n")

    print(f"{'━' * 100}")
    print("WITHOUT Diversity Penalties (Standard Balanced Scoring)")
    print(f"{'━' * 100}\n")
    recommendations_normal = recommend_songs(user_prefs, songs, k=5, strategy=BalancedStrategy(), use_diversity=False)
    print(format_recommendations_table(recommendations_normal))

    print(f"\n{'━' * 100}")
    print("WITH Diversity Penalties (Fair Representation)")
    print(f"{'━' * 100}\n")
    recommendations_diverse = recommend_songs(user_prefs, songs, k=5, strategy=BalancedStrategy(), use_diversity=True)
    print(format_recommendations_table(recommendations_diverse))

    # Summary
    print("\n" + "=" * 100)
    print("📊 IMPACT ANALYSIS")
    print("=" * 100)
    print("\nWithout diversity: Recommendations may cluster around popular songs/artists")
    print("With diversity: Different artists and genres get fair representation in top 5\n")


if __name__ == "__main__":
    main()
