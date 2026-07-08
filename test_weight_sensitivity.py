"""
Weight sensitivity experiment for Music Recommender.
Tests how changes to scoring weights affect recommendation quality and diversity.
"""

import csv
from typing import List, Dict, Tuple


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file."""
    songs = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            }
            songs.append(song)
    return songs


def score_song_original(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Original scoring logic from recommender.py"""
    reasons = []
    score = 0.0

    if user_prefs.get('genre') == song['genre']:
        score += 10.0
        reasons.append("genre match (+10.0)")

    if user_prefs.get('mood') == song['mood']:
        score += 5.0
        reasons.append("mood match (+5.0)")

    energy_sim = (1.0 - abs(user_prefs.get('energy', 0.5) - song['energy'])) * 3.0
    score += energy_sim
    reasons.append(f"energy similarity ({energy_sim:.2f})")

    valence_sim = (1.0 - abs(user_prefs.get('valence', 0.5) - song['valence'])) * 2.0
    score += valence_sim
    reasons.append(f"valence similarity ({valence_sim:.2f})")

    danceability_sim = (1.0 - abs(user_prefs.get('danceability', 0.5) - song['danceability'])) * 1.0
    score += danceability_sim
    reasons.append(f"danceability similarity ({danceability_sim:.2f})")

    return score, reasons


def score_song_balanced(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Experimental: Reduce genre dominance by half; double energy importance."""
    reasons = []
    score = 0.0

    # Genre: reduced from 10.0 to 5.0
    if user_prefs.get('genre') == song['genre']:
        score += 5.0
        reasons.append("genre match (+5.0)")

    # Mood: unchanged
    if user_prefs.get('mood') == song['mood']:
        score += 5.0
        reasons.append("mood match (+5.0)")

    # Energy: doubled from 3.0 to 6.0
    energy_sim = (1.0 - abs(user_prefs.get('energy', 0.5) - song['energy'])) * 6.0
    score += energy_sim
    reasons.append(f"energy similarity ({energy_sim:.2f})")

    # Valence: unchanged
    valence_sim = (1.0 - abs(user_prefs.get('valence', 0.5) - song['valence'])) * 2.0
    score += valence_sim
    reasons.append(f"valence similarity ({valence_sim:.2f})")

    # Danceability: unchanged
    danceability_sim = (1.0 - abs(user_prefs.get('danceability', 0.5) - song['danceability'])) * 1.0
    score += danceability_sim
    reasons.append(f"danceability similarity ({danceability_sim:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int, score_fn) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return top k ranked by score."""
    scored_songs = []
    for song in songs:
        score, reasons = score_fn(user_prefs, song)
        explanation = " | ".join(reasons)
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Test profiles
    test_profiles = {
        "High-Energy Pop Lover": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "valence": 0.85,
            "danceability": 0.8
        },
        "Conflicting (Classical + High Energy)": {
            "genre": "classical",
            "mood": "happy",
            "energy": 0.9,
            "valence": 0.8,
            "danceability": 0.2
        }
    }

    for profile_name, user_prefs in test_profiles.items():
        print(f"\n{'='*80}")
        print(f"PROFILE: {profile_name}")
        print(f"{'='*80}")

        # Original weights
        print("\n[ORIGINAL WEIGHTS]")
        print("Weights: Genre=10.0, Mood=5.0, Energy=3.0, Valence=2.0, Danceability=1.0")
        print("Max possible score: 21.0\n")

        orig_recs = recommend_songs(user_prefs, songs, 5, score_song_original)
        for rank, (song, score, exp) in enumerate(orig_recs, 1):
            print(f"{rank}. {song['title']:<25} | Score: {score:5.2f}")

        # Balanced weights
        print("\n[BALANCED WEIGHTS]")
        print("Weights: Genre=5.0, Mood=5.0, Energy=6.0, Valence=2.0, Danceability=1.0")
        print("Max possible score: 19.0 (note: reduced max due to genre cut)\n")

        balanced_recs = recommend_songs(user_prefs, songs, 5, score_song_balanced)
        for rank, (song, score, exp) in enumerate(balanced_recs, 1):
            print(f"{rank}. {song['title']:<25} | Score: {score:5.2f}")

        # Compare changes
        print("\n[COMPARISON]")
        orig_titles = [rec[0]['title'] for rec in orig_recs]
        balanced_titles = [rec[0]['title'] for rec in balanced_recs]

        if orig_titles == balanced_titles:
            print("⚠️  SAME TOP 5 - Weight change did NOT affect top recommendations")
        else:
            print("✓ DIFFERENT - Weight change affected ranking")
            for i, (orig, balanced) in enumerate(zip(orig_titles, balanced_titles), 1):
                if orig != balanced:
                    print(f"  Position {i}: {orig} → {balanced}")


if __name__ == "__main__":
    main()
