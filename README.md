# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This is a **content-based music recommender** that scores songs based on their similarity to a user's taste profile. It uses a weighted scoring algorithm that matches categorical features (genre, mood) and computes proximity for numerical features (energy, valence, danceability). The system demonstrates how real-world recommenders turn user data and item attributes into personalized suggestions—a technique that underpins platforms like Spotify and Apple Music, though this version uses simple rules instead of machine learning.

---

## How The System Works

### Song Features
Each `Song` object uses these attributes to represent its musical "vibe":
- **genre** (categorical): pop, lofi, rock, ambient, jazz, etc.
- **mood** (categorical): happy, chill, intense, relaxed, focused, moody
- **energy** (0–1): how intense/upbeat the song is (0.3 = lazy, 0.9 = high-intensity)
- **valence** (0–1): emotional brightness (0.8 = uplifting, 0.2 = dark)
- **danceability** (0–1): how groove-oriented the track is
- **tempo_bpm** (numeric): beats per minute
- **acousticness** (0–1): organic vs. electronic sound

### UserProfile Preferences
A `UserProfile` stores a user's taste as:
- **genre** (string): their preferred genre
- **mood** (string): their preferred emotional tone
- **energy** (0–1): their preferred intensity level
- **valence** (0–1): their preferred emotional brightness
- **danceability** (0–1): whether they prefer groovy or introspective tracks

### Algorithm Recipe (Finalized Scoring Logic)

For each song in the catalog, the `Recommender` computes a weighted similarity score:

**Categorical Matches** (highest priority):
- **Genre match**: +10 points (exact match only)
- **Mood match**: +5 points (exact match only)

**Numerical Proximity** (rewards closeness on a 0–1 scale):
- **Energy similarity**: `(1 - |user_energy - song_energy|) × 3.0`
- **Valence similarity**: `(1 - |user_valence - song_valence|) × 2.0`
- **Danceability similarity**: `(1 - |user_danceability - song_danceability|) × 1.0`

**Example Calculation**:
- User: lofi, chill, energy=0.4, valence=0.6, danceability=0.5
- Song: "Library Rain" (lofi, chill, energy=0.35, valence=0.60, danceability=0.58)
  - Genre match: +10
  - Mood match: +5
  - Energy: (1 - |0.4 - 0.35|) × 3 = 0.95 × 3 = 2.85
  - Valence: (1 - |0.6 - 0.60|) × 2 = 1.0 × 2 = 2.0
  - Danceability: (1 - |0.5 - 0.58|) × 1 = 0.92 × 1 = 0.92
  - **Total score: 20.77** ← top recommendation

3. **Ranking**: Sort all songs by total score (highest first), return top 3–5

### Design Rationale
- **Heavy category weighting** (10 + 5 = 15 base points) ensures genre/mood are primary filters
- **Numerical weights** (3, 2, 1) prioritize energy > valence > danceability, reflecting that intensity is more noticeable than emotional nuance
- This allows differentiation: "intense rock" (high energy, rock) will score very differently from "chill lofi" (low energy, lofi) even if valence overlaps

### Data Flow

```
USER INPUT
   ↓
   UserProfile Dict
   { genre, mood, energy, valence, danceability }
   ↓
   ─────────────────────────────────────────────
   SCORING LOOP (for each song in catalog)
   │
   ├─ Match genre? +10
   ├─ Match mood? +5
   ├─ Compute energy distance × 3.0
   ├─ Compute valence distance × 2.0
   ├─ Compute danceability distance × 1.0
   │
   └─→ Total Score
   ─────────────────────────────────────────────
   ↓
   RANKING
   Sort by score (highest first)
   ↓
   OUTPUT
   Top 3–5 Recommendations
   (title, artist, score breakdown)
```

### Known Limitations & Potential Biases

This recommender has several important limitations:

- **Over-weighting genre**: The +10 categorical bonus for genre match is very heavy. A user who loves "lofi" will almost never see blues or classical recommendations, even if those match their mood and energy perfectly.
- **Mood mismatch**: Only exact mood matches count. "Energetic" songs won't be recommended to a user seeking "euphoric" songs, even if they have similar energy values.
- **Small catalog bias**: With only 18 songs, the system can't discover unexpected gems or niche recommendations.
- **Energy dominance**: The weight(3.0) on energy means a song with "perfect mood" but mismatched intensity might score lower than one with matched energy but wrong mood.
- **Missing contextual features**: No time-of-day, listening history, or user discovery intent. A song that's perfect for "focus work" might be recommended equally for "party mode."

### Why This Approach?
This mirrors how real-world recommenders work at their core: **represent items and users as vectors of features, then find the closest matches**. Production systems (Spotify, Apple Music) layer on collaborative filtering, behavioral signals, and deep learning, but the fundamental idea—proximity = similarity—is the same. Our version keeps it simple so we can understand, debug, and reason about why recommendations happen.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Here's a sample run with the default "pop/happy" user profile:

```
User profile: genre=pop, mood=happy, energy=0.8

Top recommendations:

1. Sunrise City - Score: 19.97
   Because: genre match (+10.0) | mood match (+5.0) | energy similarity (2.94) | valence similarity (1.32) | danceability similarity (0.71)

2. Gym Hero - Score: 14.69
   Because: genre match (+10.0) | energy similarity (2.61) | valence similarity (1.46) | danceability similarity (0.62)

3. Rooftop Lights - Score: 9.94
   Because: mood match (+5.0) | energy similarity (2.88) | valence similarity (1.38) | danceability similarity (0.68)

4. Night Drive Loop - Score: 5.60
   Because: energy similarity (2.85) | valence similarity (1.98) | danceability similarity (0.77)

5. Storm Runner - Score: 5.47
   Because: energy similarity (2.67) | valence similarity (1.96) | danceability similarity (0.84)
```

This demonstrates how the algorithm prioritizes genre and mood matches while using numerical proximity to differentiate songs with similar categorical features.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



