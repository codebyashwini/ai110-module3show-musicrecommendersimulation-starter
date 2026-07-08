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

### Experiment 1: Stress Test with Diverse User Profiles

Tested the recommender across 5 distinct user profiles to evaluate robustness and identify edge cases:

#### Profile 1: High-Energy Pop Lover
**Preferences:** genre=pop, mood=happy, energy=0.9, valence=0.85, danceability=0.8

```
Top 5 Recommendations:

1. Sunrise City by Neon Echo - Score: 20.73
   Genre: pop | Mood: happy | Energy: 0.82
   Because: genre match (+10.0) | mood match (+5.0) | energy similarity (2.76) | valence similarity (1.98) | danceability similarity (0.99)

2. Gym Hero by Max Pulse - Score: 15.67
   Genre: pop | Mood: intense | Energy: 0.93
   Because: genre match (+10.0) | energy similarity (2.91) | valence similarity (1.84) | danceability similarity (0.92)

3. Rooftop Lights by Indigo Parade - Score: 10.48
   Genre: indie pop | Mood: happy | Energy: 0.76
   Because: mood match (+5.0) | energy similarity (2.58) | valence similarity (1.92) | danceability similarity (0.98)

4. EDM Festival by Pulse Collective - Score: 5.81
   Genre: edm | Mood: euphoric | Energy: 0.92
   Because: energy similarity (2.94) | valence similarity (1.98) | danceability similarity (0.89)

5. Neon Nights by Synth Wave Collective - Score: 5.60
   Genre: electronic | Mood: energetic | Energy: 0.87
   Because: energy similarity (2.91) | valence similarity (1.74) | danceability similarity (0.95)
```

**Observation:** System works well for mainstream preferences. Genre + mood matches dominate rankings. Sunrise City is an excellent fit, and Gym Hero ranks high despite mood mismatch because of strong energy alignment.

---

#### Profile 2: Chill Lofi Student
**Preferences:** genre=lofi, mood=chill, energy=0.35, valence=0.6, danceability=0.6

```
Top 5 Recommendations:

1. Library Rain by Paper Lanterns - Score: 20.98
   Genre: lofi | Mood: chill | Energy: 0.35
   Because: genre match (+10.0) | mood match (+5.0) | energy similarity (3.00) | valence similarity (2.00) | danceability similarity (0.98)

2. Midnight Coding by LoRoom - Score: 20.69
   Genre: lofi | Mood: chill | Energy: 0.42
   Because: genre match (+10.0) | mood match (+5.0) | energy similarity (2.79) | valence similarity (1.92) | danceability similarity (0.98)

3. Focus Flow by LoRoom - Score: 15.83
   Genre: lofi | Mood: focused | Energy: 0.40
   Because: genre match (+10.0) | energy similarity (2.85) | valence similarity (1.98) | danceability similarity (1.00)

4. Spacewalk Thoughts by Orbit Bloom - Score: 10.50
   Genre: ambient | Mood: chill | Energy: 0.28
   Because: mood match (+5.0) | energy similarity (2.79) | valence similarity (1.90) | danceability similarity (0.81)

5. Coffee Shop Stories by Slow Stereo - Score: 5.66
   Genre: jazz | Mood: relaxed | Energy: 0.37
   Because: energy similarity (2.94) | valence similarity (1.78) | danceability similarity (0.94)
```

**Observation:** Excellent recommendations. Both top songs are near-perfect matches on all five factors. Focus Flow ranks #3 despite mood mismatch (focused ≠ chill) because lofi + low energy are strong enough. This shows the system handles focused, study-oriented users well.

---

#### Profile 3: Deep Intense Rocker
**Preferences:** genre=rock, mood=intense, energy=0.9, valence=0.45, danceability=0.65

```
Top 5 Recommendations:

1. Storm Runner by Voltline - Score: 20.90
   Genre: rock | Mood: intense | Energy: 0.91
   Because: genre match (+10.0) | mood match (+5.0) | energy similarity (2.97) | valence similarity (1.94) | danceability similarity (0.99)

2. Gym Hero by Max Pulse - Score: 10.04
   Genre: pop | Mood: intense | Energy: 0.93
   Because: mood match (+5.0) | energy similarity (2.91) | valence similarity (1.36) | danceability similarity (0.77)

3. Metal Thunder by Iron Forge - Score: 5.49
   Genre: metal | Mood: aggressive | Energy: 0.94
   Because: energy similarity (2.88) | valence similarity (1.68) | danceability similarity (0.93)

4. Night Drive Loop by Neon Echo - Score: 5.39
   Genre: synthwave | Mood: moody | Energy: 0.75
   Because: energy similarity (2.55) | valence similarity (1.92) | danceability similarity (0.92)

5. Neon Nights by Synth Wave Collective - Score: 5.17
   Genre: electronic | Mood: energetic | Energy: 0.87
   Because: energy similarity (2.91) | valence similarity (1.46) | danceability similarity (0.80)
```

**Observation:** Storm Runner is perfect. Gym Hero ranks #2 because "intense" mood match overcomes the pop genre penalty. Metal Thunder ranks #3 despite genre mismatch because energy and aggressive mood are strong signals.

---

#### Profile 4: Edge Case - Conflicting Preferences
**Preferences:** genre=classical, mood=happy, energy=0.9, valence=0.8, danceability=0.2

```
Top 5 Recommendations:

1. Classical Dreams by Symphony Hall - Score: 14.26
   Genre: classical | Mood: sophisticated | Energy: 0.45
   Because: genre match (+10.0) | energy similarity (1.65) | valence similarity (1.76) | danceability similarity (0.85)

2. Sunrise City by Neon Echo - Score: 10.09
   Genre: pop | Mood: happy | Energy: 0.82
   Because: mood match (+5.0) | energy similarity (2.76) | valence similarity (1.92) | danceability similarity (0.41)

3. Rooftop Lights by Indigo Parade - Score: 9.94
   Genre: indie pop | Mood: happy | Energy: 0.76
   Because: mood match (+5.0) | energy similarity (2.58) | valence similarity (1.98) | danceability similarity (0.38)

4. Gym Hero by Max Pulse - Score: 5.17
   Genre: pop | Mood: intense | Energy: 0.93
   Because: energy similarity (2.91) | valence similarity (1.94) | danceability similarity (0.32)

5. EDM Festival by Pulse Collective - Score: 5.11
   Genre: edm | Mood: euphoric | Energy: 0.92
   Because: energy similarity (2.94) | valence similarity (1.88) | danceability similarity (0.29)
```

**⚠️ CRITICAL OBSERVATION - BIAS DISCOVERED:**

Classical Dreams ranks #1 despite a *catastrophic* mismatch: the user wants high energy (0.9) but Classical Dreams has energy 0.45 (50% lower). The user wants a happy mood but gets "sophisticated." Why?

**Answer:** Genre dominance. The +10 genre match bonus is so large (47.6% of max score) that it overpowers all continuous attributes. This reveals the system struggles with non-mainstream preference combinations—someone who genuinely wants "high-energy classical music" (e.g., baroque concerto for workout) gets locked into low-energy classical instead.

---

#### Profile 5: Balanced Music Explorer  
**Preferences:** genre=indie pop, mood=relaxed, energy=0.5, valence=0.7, danceability=0.6

```
Top 5 Recommendations:

1. Rooftop Lights by Indigo Parade - Score: 14.78
   Genre: indie pop | Mood: happy | Energy: 0.76
   Because: genre match (+10.0) | energy similarity (2.22) | valence similarity (1.78) | danceability similarity (0.78)

2. Sunset in Jamaica by Reggae Vibes - Score: 10.75
   Genre: reggae | Mood: relaxed | Energy: 0.52
   Because: mood match (+5.0) | energy similarity (2.94) | valence similarity (1.92) | danceability similarity (0.89)

3. Coffee Shop Stories by Slow Stereo - Score: 10.53
   Genre: jazz | Mood: relaxed | Energy: 0.37
   Because: mood match (+5.0) | energy similarity (2.61) | valence similarity (1.98) | danceability similarity (0.94)

4. Classical Dreams by Symphony Hall - Score: 5.56
   Genre: classical | Mood: sophisticated | Energy: 0.45
   Because: energy similarity (2.85) | valence similarity (1.96) | danceability similarity (0.75)

5. Folk Campfire by Acoustic Hearts - Score: 5.56
   Genre: folk | Mood: nostalgic | Energy: 0.41
   Because: energy similarity (2.73) | valence similarity (1.98) | danceability similarity (0.85)
```

**Observation:** Solid recommendations. Rooftop Lights wins with genre match. Mood-mismatched songs (relaxed vs. happy) still rank well because energy/valence alignment is close. This profile shows the system works well for "balanced" explorers.

---

### Experiment 2: Weight Sensitivity Test

**Question:** How sensitive are rankings to changes in feature weights?

**Test:** Compared original weights (Genre=10, Energy=3) vs. balanced weights (Genre=5, Energy=6)

#### High-Energy Pop Lover

**Original Weights (Genre=10, Energy=3):**
```
1. Sunrise City              | Score: 20.73
2. Gym Hero                  | Score: 15.67
3. Rooftop Lights            | Score: 10.48
4. EDM Festival              | Score:  5.81
5. Neon Nights               | Score:  5.60
```

**Balanced Weights (Genre=5, Energy=6):**
```
1. Sunrise City              | Score: 18.49
2. Gym Hero                  | Score: 13.58
3. Rooftop Lights            | Score: 13.06
4. EDM Festival              | Score:  8.75
5. Neon Nights               | Score:  8.51
```

**Finding:** ⚠️ Same top 5, same order. Weight changes did NOT affect rankings for this user because genre already matches perfectly. Once a user's preferred genre is in the catalog, weight rebalancing doesn't help.

---

#### Edge Case: Conflicting Preferences (Classical + High Energy)

**Original Weights (Genre=10, Energy=3):**
```
1. Classical Dreams          | Score: 14.26
2. Sunrise City              | Score: 10.09
3. Rooftop Lights            | Score:  9.94
4. Gym Hero                  | Score:  5.17
5. EDM Festival              | Score:  5.11
```

**Balanced Weights (Genre=5, Energy=6):**
```
1. Sunrise City              | Score: 12.85
2. Rooftop Lights            | Score: 12.52
3. Classical Dreams          | Score: 10.91
4. Gym Hero                  | Score:  8.08
5. EDM Festival              | Score:  8.05
```

**✓ DRAMATIC CHANGE:** Sunrise City jumps from #2 to #1. This is better! A user who wants high energy + happy mood gets Sunrise City (energy 0.82, happy) instead of Classical Dreams (energy 0.45, sophisticated).

**Insight:** The system is robust for standard preference combinations but breaks for edge cases. Rebalancing weights fixes the edge case at the cost of leaving standard users unchanged—suggesting the real fix is not weight tuning but rethinking the categorical dominance entirely.

---

## Limitations and Risks

Our evaluation uncovered three critical limitations:

1. **Genre Dominance Bias (47.6% of max score):** The +10 point genre bonus is so heavy that it overpowers all continuous attributes combined. A user requesting "high-energy classical" gets locked into low-energy classical recommendations, even though Sunrise City (pop) would better match their actual energy preference. This shows that categorical weighting can *hide* what users actually want.

2. **Mood Cliff Effect (5-point penalty):** An exact mood mismatch costs exactly 5 points—larger than any single continuous metric can earn. This creates hard ranking boundaries where "same genre, different mood" loses to "different genre, same mood" even when energy/valence are better aligned. Users with non-standard mood preferences get systematically penalized.

3. **Filter Bubble / Limited Catalog Diversity:** "Gym Hero" appears in the top 5 for 3 out of 5 test profiles despite serving different musical tastes. Without diversity enforcement, the recommender converges toward objectively appealing songs (high valence, high danceability) rather than personalized picks. With only 18 songs in the catalog, serendipity is limited.

See the **model_card.md** for deeper analysis and proposed solutions.

---

## Reflection

Read the full evaluation in `model_card.md`:

[**Model Card**](model_card.md)

### Key Learning: How Categorical Weights Create Hidden Bias

Building and testing this recommender revealed something counterintuitive: **weighting scheme choices can invisibly exclude certain users.** I initially thought genre should be the most important feature—after all, a "pop lover" wouldn't want jazz, right? But in stress testing, I discovered someone could genuinely love both classical music *and* high-energy workouts. The moment I hardcoded "genre = 10 points," I mathematically locked that user out: even if another song perfectly matched their energy preference, the genre mismatch (10 points gone!) would always lose to a poorly-matched classical piece.

This mirrors real-world AI bias: decisions made at design time (what weights to assign, what categories to match on) become baked into the product and hide systemic unfairness. The recommender felt fair in code, but empirically failed for non-mainstream taste combinations. No one has to *intentionally* exclude users with atypical preferences—the math does it automatically.

### Why Recommendation Systems Are Harder Than They Look

The weight sensitivity experiment showed that you can't fix bias just by tuning numbers. Rebalancing weights (reducing genre from 10 → 5, raising energy from 3 → 6) fixed the edge case but left mainstream users unaffected because they already had perfect genre matches in the catalog. This suggests the real problem isn't the weights—it's the *categorical matching approach itself.* A truly fair system would recognize that "classical" and "pop" aren't categories but points in a musical space, where a user's taste can bridge both.

This is probably why Spotify uses deep learning instead of rule-based scoring: neural networks can learn that certain users genuinely like both classical and electronic, whereas hand-written rules force discrete boundaries (match or no match). Production systems also use diversity mechanisms and personalization from behavioral signals, not just content features, to avoid filter bubbles—something our simple content-based approach can't do.



