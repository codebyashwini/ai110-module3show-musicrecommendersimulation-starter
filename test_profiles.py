"""
Stress test script for Music Recommender Simulation.
Tests multiple user profiles to evaluate recommendation quality and identify edge cases.
"""

from src.recommender import load_songs, recommend_songs

def main() -> None:
    songs = load_songs("data/songs.csv")

    # Define diverse user profiles
    profiles = {
        "High-Energy Pop Lover": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "valence": 0.85,
            "danceability": 0.8
        },
        "Chill Lofi Student": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "valence": 0.6,
            "danceability": 0.6
        },
        "Deep Intense Rocker": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
            "valence": 0.45,
            "danceability": 0.65
        },
        "Edge Case: Conflicting Preferences": {
            "genre": "classical",
            "mood": "happy",  # Classical typically not "happy"
            "energy": 0.9,    # Classical typically low energy
            "valence": 0.8,
            "danceability": 0.2
        },
        "Balanced Music Explorer": {
            "genre": "indie pop",
            "mood": "relaxed",
            "energy": 0.5,
            "valence": 0.7,
            "danceability": 0.6
        }
    }

    for profile_name, user_prefs in profiles.items():
        print(f"\n{'='*70}")
        print(f"PROFILE: {profile_name}")
        print(f"{'='*70}")
        print(f"Preferences: {user_prefs}\n")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("Top 5 Recommendations:\n")
        for rank, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            print(f"{rank}. {song['title']} by {song['artist']}")
            print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']:.2f}")
            print(f"   Score: {score:.2f}")
            print(f"   Because: {explanation}\n")


if __name__ == "__main__":
    main()
