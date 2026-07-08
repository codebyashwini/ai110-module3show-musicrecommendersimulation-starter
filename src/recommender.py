import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

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
    popularity: int
    release_decade: str
    detailed_mood_tags: str
    vocal_presence: float
    instrumentation: str
    familiarity_level: str


class ScoringStrategy(ABC):
    """Base class for different scoring strategies."""
    @abstractmethod
    def score_song(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        """Score a song based on user preferences. Returns (score, reasons)."""
        pass


class BalancedStrategy(ScoringStrategy):
    """Original balanced scoring: Genre (10) + Mood (5) + Energy (3) + Valence (2) + Danceability (1)."""
    def score_song(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
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


class GenreFirstStrategy(ScoringStrategy):
    """Genre-focused: Heavily weights genre matching, then energy and mood."""
    def score_song(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        reasons = []
        score = 0.0

        if user_prefs.get('genre') == song['genre']:
            score += 15.0
            reasons.append("genre match (PRIORITY +15.0)")

        energy_sim = (1.0 - abs(user_prefs.get('energy', 0.5) - song['energy'])) * 4.0
        score += energy_sim
        reasons.append(f"energy similarity ({energy_sim:.2f})")

        if user_prefs.get('mood') == song['mood']:
            score += 3.0
            reasons.append("mood match (+3.0)")

        valence_sim = (1.0 - abs(user_prefs.get('valence', 0.5) - song['valence'])) * 1.5
        score += valence_sim
        reasons.append(f"valence similarity ({valence_sim:.2f})")

        return score, reasons


class MoodFirstStrategy(ScoringStrategy):
    """Mood-focused: Emphasizes emotional tone over genre, great for mood-based discovery."""
    def score_song(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        reasons = []
        score = 0.0

        if user_prefs.get('mood') == song['mood']:
            score += 12.0
            reasons.append("mood match (PRIORITY +12.0)")

        valence_sim = (1.0 - abs(user_prefs.get('valence', 0.5) - song['valence'])) * 3.0
        score += valence_sim
        reasons.append(f"valence similarity ({valence_sim:.2f})")

        energy_sim = (1.0 - abs(user_prefs.get('energy', 0.5) - song['energy'])) * 2.5
        score += energy_sim
        reasons.append(f"energy similarity ({energy_sim:.2f})")

        if user_prefs.get('genre') == song['genre']:
            score += 5.0
            reasons.append("genre match (+5.0)")

        return score, reasons


class EnergyFocusedStrategy(ScoringStrategy):
    """Energy-focused: Prioritizes energy level for workout, focus, or party modes."""
    def score_song(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        reasons = []
        score = 0.0

        energy_sim = (1.0 - abs(user_prefs.get('energy', 0.5) - song['energy'])) * 5.0
        score += energy_sim
        reasons.append(f"energy match (PRIORITY {energy_sim:.2f})")

        if user_prefs.get('mood') == song['mood']:
            score += 4.0
            reasons.append("mood match (+4.0)")

        danceability_sim = (1.0 - abs(user_prefs.get('danceability', 0.5) - song['danceability'])) * 2.0
        score += danceability_sim
        reasons.append(f"danceability similarity ({danceability_sim:.2f})")

        if user_prefs.get('genre') == song['genre']:
            score += 3.0
            reasons.append("genre match (+3.0)")

        return score, reasons


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
                'popularity': int(row['popularity']),
                'release_decade': row['release_decade'],
                'detailed_mood_tags': row['detailed_mood_tags'],
                'vocal_presence': float(row['vocal_presence']),
                'instrumentation': row['instrumentation'],
                'familiarity_level': row['familiarity_level'],
            }
            songs.append(song)
    print(f"Loaded {len(songs)} songs.")
    return songs

def score_song(user_prefs: Dict, song: Dict, strategy: Optional[ScoringStrategy] = None) -> Tuple[float, List[str]]:
    """Score a single song against user preferences using the specified strategy (default: Balanced)."""
    if strategy is None:
        strategy = BalancedStrategy()

    score, reasons = strategy.score_song(user_prefs, song)

    # Add optional advanced feature scoring (applies to all strategies)
    if user_prefs.get('prefer_popular', False):
        popularity_bonus = (song['popularity'] / 100.0) * 1.5
        score += popularity_bonus
        reasons.append(f"popularity bonus ({popularity_bonus:.2f})")

    if 'target_vocal_presence' in user_prefs:
        vocal_sim = (1.0 - abs(user_prefs['target_vocal_presence'] - song['vocal_presence'])) * 1.0
        score += vocal_sim
        reasons.append(f"vocal presence similarity ({vocal_sim:.2f})")

    if user_prefs.get('preferred_familiarity') and user_prefs['preferred_familiarity'] == song['familiarity_level']:
        score += 1.5
        reasons.append("familiarity match (+1.5)")

    return score, reasons

def apply_diversity_penalty(scored_songs: List[Tuple[Dict, float, str]], max_same_artist: int = 2, max_same_genre: int = 2) -> List[Tuple[Dict, float, str]]:
    """Apply diversity penalties to reduce filter bubbles.

    Penalizes songs if their artist or genre is already well-represented in top results.
    Returns adjusted scores while preserving original songs/explanations.
    """
    adjusted = []
    artist_counts = {}
    genre_counts = {}

    for song, score, explanation in scored_songs:
        adjusted_score = score
        penalties = []

        artist = song['artist']
        genre = song['genre']

        # Artist diversity: penalty if artist already has max_same_artist songs
        artist_count = artist_counts.get(artist, 0)
        if artist_count >= max_same_artist:
            artist_penalty = 2.0 * (artist_count - max_same_artist + 1)
            adjusted_score -= artist_penalty
            penalties.append(f"artist duplicate penalty (-{artist_penalty:.2f})")

        # Genre diversity: penalty if genre already has max_same_genre songs
        genre_count = genre_counts.get(genre, 0)
        if genre_count >= max_same_genre:
            genre_penalty = 1.5 * (genre_count - max_same_genre + 1)
            adjusted_score -= genre_penalty
            penalties.append(f"genre duplicate penalty (-{genre_penalty:.2f})")

        # Update counts
        artist_counts[artist] = artist_counts.get(artist, 0) + 1
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

        # Append penalty notes to explanation if any penalties applied
        final_explanation = explanation
        if penalties:
            final_explanation = explanation + " | " + " | ".join(penalties)

        adjusted.append((song, adjusted_score, final_explanation))

    return adjusted

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, strategy: Optional[ScoringStrategy] = None, use_diversity: bool = False) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return top k ranked by score (highest first).

    Args:
        user_prefs: User preference dict
        songs: List of song dicts to score
        k: Number of recommendations to return
        strategy: Scoring strategy (default: Balanced)
        use_diversity: If True, apply diversity penalties to reduce filter bubbles
    """
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, strategy)
        explanation = " | ".join(reasons)
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda x: x[1], reverse=True)

    # Apply diversity penalties if enabled
    if use_diversity:
        scored_songs = apply_diversity_penalty(scored_songs, max_same_artist=2, max_same_genre=2)
        scored_songs.sort(key=lambda x: x[1], reverse=True)

    return scored_songs[:k]
