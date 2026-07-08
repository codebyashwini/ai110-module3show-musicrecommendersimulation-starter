# 📊 Music Recommender System: Evaluation Summary

**Evaluation Date:** July 7, 2026  
**System:** VibeMatch 1.0 (Content-based music recommender)  
**Dataset:** 18 songs across 12 genres  
**Test Profiles:** 5 diverse user preference profiles

---

## Quick Overview

| Step | What We Did | Key Finding |
|------|-----------|-------------|
| **Stress Testing** | Tested 5 user profiles (pop lover, lofi student, rocker, edge cases, balanced explorer) | System works well for mainstream preferences but fails for non-standard combinations |
| **Accuracy Check** | Analyzed why specific songs ranked where they did | Genre dominance (47.6% of score) overpowers continuous attributes |
| **Weight Experiment** | Tested rebalancing genre weight (10→5) vs. energy weight (3→6) | Edge cases improved, but standard users unaffected—suggests categorical matching is the core issue |
| **Bias Analysis** | Identified three critical bias patterns | Genre cliff, mood cliff, filter bubble effect |
| **Documentation** | Compiled findings into model_card.md and README.md | Clear before/after comparison showing which profiles work well and which don't |

---

## Three Critical Biases Discovered

### 1. **Genre Dominance (47.6% of Score)**
**The Problem:** Genre match is worth 10 out of 21 max points, larger than all continuous metrics combined.

**Real-World Impact:**
- User: "I love classical music *and* high-energy workouts"
- System: "Classical Dreams (energy 0.45)" ranked #1
- User wanted: Sunrise City (energy 0.82) or Gym Hero (energy 0.93)
- Why it happened: Genre match (+10) > any energy mismatch penalty

**Evidence from Testing:**
```
Edge Case Profile (classical + happy + energy 0.9):
ORIGINAL WEIGHTS (Genre=10):
  1. Classical Dreams (energy 0.45) ← WRONG
     
BALANCED WEIGHTS (Genre=5, Energy=6):
  1. Sunrise City (energy 0.82)   ← CORRECT
```

### 2. **Mood Cliff Effect (5-Point Penalty)**
**The Problem:** Mood mismatch costs exactly 5 points—larger than any single continuous metric.

**Real-World Impact:**
- Gym Hero (pop + intense + energy 0.93) loses to Sunrise City (pop + happy + energy 0.82)
- Gym Hero is objectively closer on energy, but loses because mood mismatch (5 points) > energy advantage (0.15 points)
- Users with non-standard moods ("I want happy metal!" or "intense classical!") get systematically locked out

**Why This Matters:** Creates hard ranking boundaries instead of smooth gradients.

### 3. **Filter Bubble / Recommendation Repetition**
**The Problem:** Without diversity enforcement, high-valence songs appear in multiple users' top-5 lists.

**Real-World Impact:**
- "Gym Hero" appears in top 5 for 3 out of 5 test profiles
- Song has objectively high metrics (energy 0.93, valence 0.77, danceability 0.88)
- System recommends the same songs to different users, reducing serendipity

**Example:**
```
Gym Hero ranked in top 5 for:
  - High-Energy Pop Lover (#2)
  - Deep Intense Rocker (#2)
  - Conflicting Preferences (#4)
```

---

## Which Profiles Worked Well ✓

| Profile | Top Recommendation | Assessment | Why It Worked |
|---------|-------------------|-----------|---------------|
| **Chill Lofi Student** | Library Rain (perfect match) | Excellent | Genre + mood + energy all aligned perfectly |
| **High-Energy Pop Lover** | Sunrise City (perfect match) | Excellent | Genre + mood matched exactly |
| **Deep Intense Rocker** | Storm Runner (perfect match) | Excellent | Genre + mood + energy aligned |
| **Balanced Explorer** | Rooftop Lights (genre match) | Good | Mood mismatches tolerable with energy/valence alignment |

---

## Which Profiles Failed ✗

| Profile | Top Recommendation | Assessment | Why It Failed |
|---------|-------------------|-----------|---------------|
| **Conflicting Preferences** (classical + happy + 0.9 energy) | Classical Dreams (energy 0.45) | **POOR** | Genre match overpowered energy mismatch |

**Impact:** 1 out of 5 users (20%) received a genuinely poor recommendation due to genre dominance.

---

## Weight Sensitivity Results

**Hypothesis:** Rebalancing weights (Genre 10→5, Energy 3→6) would help edge cases.

**Result:** Partially correct.

```
HIGH-ENERGY POP (Already has perfect genre match):
  Original:  [Sunrise City, Gym Hero, Rooftop Lights, ...]
  Balanced:  [Sunrise City, Gym Hero, Rooftop Lights, ...]
  Change: NONE ← Weight rebalancing doesn't help if catalog has genre match

CONFLICTING PREFS (Classical + happy + 0.9 energy):
  Original:  [Classical Dreams (0.45 energy), Sunrise City (0.82), ...]
  Balanced:  [Sunrise City (0.82), Rooftop Lights (0.76), Classical Dreams, ...]
  Change: DRAMATIC ✓ ← Weight rebalancing helps edge cases

Conclusion: System is insensitive to weight changes for standard users,
but fixing edge cases requires reducing genre weight—which is a
design trade-off, not a tuning solution.
```

---

## Recommendations for Improvement

### Quick Wins (Low Effort)
1. **Rebalance weights:** Reduce genre from 10→6, raise energy from 3→5
   - Fixes edge case users at minimal cost to mainstream users
   
2. **Implement mood similarity:** Instead of exact mood match (+5) vs. mismatch (0), use similarity scoring
   - "happy" and "euphoric" are closer than "happy" and "melancholic"
   - Smooths the 5-point cliff

3. **Add diversity penalty:** Track which songs appear frequently, penalize repetition
   - Reduces filter bubble, increases serendipity

### Medium Effort
4. **Use acousticness:** Currently loaded but unused
   - Add preference: "user_acoustic_preference" (0–1)
   - Helps distinguish "acoustic guitar singer-songwriter" from "electronic pop"

5. **Expand catalog:** Current 18 songs is too small
   - Aim for 50+ songs with balanced genre distribution
   - Ensures all preference combinations have quality matches

### Architectural Changes
6. **Replace categorical matching with similarity metrics**
   - Instead of "genre must match," use genre similarity (cosine distance in embedding space)
   - Allows "pop" and "indie pop" users to see each other's recommendations

7. **Add behavioral signals:** Listening history, skip rate, replay count
   - Content-based (this system) captures *intent* but misses *satisfaction*
   - Collaborative filtering can find serendipitous matches

---

## What We Learned

### Key Insight #1: Categorical Weights Create Invisible Bias
When you decide "genre is the most important," you're not just prioritizing—you're *excluding*. Any user whose taste bridges categories (classical + high-energy, pop + acoustic) gets mathematically locked out. No intentional exclusion needed; the math does it automatically.

### Key Insight #2: You Can't Test Only Happy Paths
Testing only mainstream preferences (pop lover, lofi student, rocker) would have missed the edge case entirely. The system felt fair and accurate until stress-tested with conflicting preferences. This is why adversarial testing (deliberately breaking assumptions) matters.

### Key Insight #3: Recommendation Systems Are Not Just About Accuracy
A system can be *accurate* (recommends songs users enjoy) but still introduce *bias* (certain user types are systematically underserved). Our edge case user might eventually like Classical Dreams, but they'll never discover the Sunrise City they're actually looking for—that's a bias problem, not an accuracy problem.

### Key Insight #4: Simple Rules Have Hidden Trade-Offs
The scoring logic looked clean: "match genre/mood, compute distance metrics, sum." But in practice, each design choice (what to weight, what to match on, what to exclude) has downstream fairness implications you can't predict without testing across diverse users.

---

## Testing Methodology Used

1. **Stress Testing:** Define diverse profiles that push boundaries (mainstream + edge cases + conflicting preferences)
2. **Sensitivity Analysis:** Change weights, observe impact on specific profiles
3. **Root Cause Analysis:** For each failure, trace it back to a specific scoring component
4. **Comparison:** Observe how the same song ranks for different users to detect filter bubbles
5. **Intuition Check:** Ask "does this feel right?" and validate against the algorithm's logic

---

## Next Steps

1. **Re-run evaluation after weight rebalancing:** Use the test_profiles.py script to verify that changing weights improves edge cases without breaking mainstream users
2. **Expand catalog:** Add 30+ more songs, re-test to see if filter bubbles disappear
3. **Implement mood similarity:** Replace exact mood matching with gradient-based scoring
4. **Document in PR:** Link this summary in a pull request to explain why changes were made

---

## Files Generated During Evaluation

- `test_profiles.py` – Stress test script with 5 diverse user profiles
- `test_weight_sensitivity.py` – Weight sensitivity experiment (original vs. balanced)
- `EVALUATION_SUMMARY.md` – This document
- `model_card.md` – Updated with full evaluation results
- `README.md` – Updated with experiments section and detailed findings
