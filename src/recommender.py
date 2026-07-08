import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored_songs = []
        for song in self.songs:
            score, _ = self._score_song_oop(user, song)
            scored_songs.append((song, score))
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored_songs[:k]]

    def _score_song_oop(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        reasons = []
        score = 0.0

        if user.favorite_genre == song.genre:
            score += 10.0
            reasons.append(f"genre match (+10.0)")

        if user.favorite_mood == song.mood:
            score += 5.0
            reasons.append(f"mood match (+5.0)")

        energy_sim = (1.0 - abs(user.target_energy - song.energy)) * 3.0
        score += energy_sim
        reasons.append(f"energy similarity ({energy_sim:.2f})")

        return score, reasons

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self._score_song_oop(user, song)
        return " | ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numerical values to proper types."""
    print(f"Loading songs from {csv_path}...")
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
    print(f"Loaded {len(songs)} songs.")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences using the algorithm recipe."""
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

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return top k ranked by score (highest first)."""
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]
