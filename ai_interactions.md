# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

### Challenge 4: Visual Summary Table

**What task did you give the agent?**

Create a formatted table output for music recommendations that displays song details (title, artist, genre, score) alongside a scoring breakdown showing why each song was recommended.

**Prompts used:**

> "How can I improve the terminal output of my music recommender to show recommendations in a formatted table instead of plain text? I want to display each recommendation with its score, and importantly, the breakdown of HOW the score was calculated (genre match, energy similarity, etc.). Suggest a library and implementation approach. The table should be readable and include all scoring reasons."

**What did the agent generate or change?**

- Added `tabulate` library to `requirements.txt` for ASCII table formatting
- Created `format_recommendations_table()` function in `src/main.py` that:
  - Takes recommendations list and converts to table data with columns: Rank, Song, Artist, Genre, Score, Reasons
  - Uses tabulate with "grid" format for clean ASCII output
  - Formats scores to 2 decimal places for readability
- Updated `main()` to:
  - Display user preferences header
  - Call `format_recommendations_table()` to render output
  - Add emoji decoration (🎵) for visual appeal

**What did you verify or fix manually?**

- Tested the output with default "pop/happy" user profile ✓ Works perfectly
- Verified all scoring reasons are displayed in the "Reasons" column
- Confirmed the table is readable and doesn't overflow in terminal (uses grid layout which wraps text)
- Checked that score formatting is consistent (2 decimals)
- **Manual improvement:** Added the "Reasons" column explanation in headers to make scoring breakdown crystal clear

---

## Advanced Song Features (SF9 - Challenge 1)

**What task did you give the agent?**

Design and implement 5+ new song attributes that extend the basic music recommender features (genre, mood, energy, etc.). These should enable richer preference matching and demonstrate how real recommenders handle complex user profiles.

**Prompts used:**

> "I want to add advanced song attributes to my music recommender beyond just genre, mood, and energy. What are 5-6 meaningful attributes that would make recommendations more nuanced? Consider things like: popularity levels, era/era-based preferences, detailed mood descriptors, vocal vs. instrumental balance, instrumentation types, and audience familiarity. Suggest values/ranges that make sense for each, then show me how to update my CSV schema and Python code to load and score these new features."

**What did the agent generate or change?**

**Data Schema Updates (data/songs.csv):**
- Added 6 new columns to all 18 songs:
  1. **popularity** (0-100) - how mainstream/well-known each song is
  2. **release_decade** - era classification (1800s, 1970s, 1980s, etc.)
  3. **detailed_mood_tags** - comma-separated descriptors (e.g., "lo-fi,ambient,study")
  4. **vocal_presence** (0-1) - focus on vocals vs instrumental
  5. **instrumentation** - type classification (acoustic, electronic, orchestral, guitar-driven, hybrid)
  6. **familiarity_level** - audience reach (niche, mainstream, universal)

**Code Changes (src/recommender.py):**
- Updated `Song` dataclass with 6 new fields
- Enhanced `load_songs()` to parse new CSV columns with appropriate types
- Extended `score_song()` with optional scoring rules for:
  - Popularity bonus: `(popularity / 100) × 1.5` points if `prefer_popular=True`
  - Vocal presence similarity: `(1 - |user_vocal - song_vocal|) × 1.0` if user has `target_vocal_presence`
  - Familiarity matching: `+1.5` points if song's familiarity matches user's `preferred_familiarity`

**User Profile Extension (src/main.py):**
- Created two example profiles showing new features:
  - "Mainstream Pop Fan" (uses `prefer_popular` and `target_vocal_presence`)
  - "Niche Lo-Fi Listener" (uses `preferred_familiarity` and `target_vocal_presence`)

**What did you verify or fix manually?**

- ✅ Verified all 18 songs load without errors with new fields
- ✅ Confirmed popularity bonus appears in scoring breakdown for "Mainstream" profile
- ✅ Validated vocal presence similarity calculations (e.g., Sunrise City 0.85 vs user 0.85 = full 1.0 bonus)
- ✅ Tested familiarity matching: Niche lo-fi songs (Midnight Coding) correctly receive +1.5 bonus for niche listener
- ✅ Confirmed scores changed appropriately: Midnight Coding jumps from ~20.7 (baseline) to 23.0 with familiarity match
- ✅ Manually reviewed data: Popularity values are realistic (82 for Sunrise City, 45 for Midnight Coding), instrumentation is descriptive
- ✅ **Manual improvement:** Added detailed_mood_tags to CSV with meaningful descriptors that could drive future feature matching (currently loaded but not yet scored)

---

## Design Pattern - Strategy Pattern (SF10 - Challenge 2)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

**Strategy Pattern** – A behavioral design pattern that encapsulates different scoring algorithms and allows runtime selection.

**How did AI help you brainstorm or implement it?**

Prompt used:

> "I want to support multiple scoring modes in my music recommender (Genre-First, Mood-First, Energy-Focused, etc.). How should I structure this so I can switch between different scoring algorithms without duplicating code? Should I use a design pattern? Which one and how would it look in Python?"

**AI Suggestion:** Strategy Pattern is ideal here. Create:
1. Abstract base class `ScoringStrategy` with `score_song()` method
2. Concrete implementations for each strategy
3. Pass strategy to `recommend_songs()` function

**How does the pattern appear in your final code?**

**In `src/recommender.py`:**

- `ScoringStrategy` (ABC) - abstract base with `score_song()` method
- `BalancedStrategy` - original weighting (genre 10 + mood 5 + energy 3 + valence 2 + danceability 1)
- `GenreFirstStrategy` - heavy genre weighting (15 pts) + higher energy weight (4.0)
- `MoodFirstStrategy` - mood priority (12 pts), elevated valence weight (3.0)
- `EnergyFocusedStrategy` - energy dominance (5.0 multiplier) for workout/focus scenarios

Functions updated:
- `score_song(user_prefs, song, strategy=None)` - accepts optional strategy, defaults to Balanced
- `recommend_songs(user_prefs, songs, k=5, strategy=None)` - passes strategy through

**Flexibility gained:**
- ✅ Easy to add new strategies without modifying existing code (Open/Closed Principle)
- ✅ Runtime strategy selection in `main.py` - can test all 4 strategies on same user profile
- ✅ Advanced features (popularity, vocal presence) apply to ALL strategies uniformly
- ✅ Clear separation: strategy defines core weighting, advanced features are layered on top

**Example comparison showing power of Strategy pattern:**
- Same user profile (pop, happy, energy 0.8) generates different top 3 across strategies:
  - Balanced: Sunrise City → Gym Hero → Rooftop Lights
  - Genre-First: Sunrise City → Gym Hero → Rooftop Lights (similar, but stronger scores)
  - Mood-First: Sunrise City → Rooftop Lights → Gym Hero (Rooftop Lights moves up due to mood match)
  - Energy-Focused: Sunrise City → Rooftop Lights → Gym Hero (same mood boost effect)

---

## Diversity & Fairness Logic (SF11 - Challenge 3)

**What task did you give the agent?**

Implement a diversity penalty system that prevents the same artist or genre from dominating the top recommendations. This addresses the "filter bubble" problem observed in the model card evaluation where Gym Hero appeared in 3/5 test profiles.

**Prompts used:**

> "I want to add a diversity penalty to my recommender so that if an artist or genre already appears in the top recommendations, subsequent songs from that artist/genre get a penalty. This should prevent filter bubbles and ensure users discover different artists. How should I structure the penalty? Should it scale with how many duplicates there already are?"

**What did the agent generate or change?**

**New function in `src/recommender.py`:**
- `apply_diversity_penalty(scored_songs, max_same_artist=2, max_same_genre=2)` - Post-processing step that:
  - Tracks artist and genre representation as it iterates through scored songs
  - Applies progressive penalties: first duplicate gets base penalty, second gets 2x, etc.
  - Artist penalty: 2.0 points per duplicate (after threshold of 2)
  - Genre penalty: 1.5 points per duplicate (after threshold of 2)
  - Appends penalty notes to explanation so users see why scores changed

**Updated `recommend_songs()` function:**
- Added `use_diversity` parameter (default False for backward compatibility)
- If enabled, applies diversity penalties before final ranking and re-sorts

**In `src/main.py`:**
- Added demonstration section showing before/after diversity penalties
- Comparison with lofi/chill profile shows:
  - WITHOUT diversity: Focus Flow (LoRoom #2) scores 15.73
  - WITH diversity: Focus Flow drops to 14.23 (1.5 point genre duplicate penalty)

**What did you verify or fix manually?**

- ✅ Verified penalty calculation: LoRoom's second song gets -1.5 penalty (genre duplicate, 1 over threshold of 2)
- ✅ Confirmed penalties appear in explanation: users can see "genre duplicate penalty (-1.5)"
- ✅ Tested with multiple artists/genres: penalties apply independently for artist AND genre duplicates
- ✅ Verified re-sorting works: after penalties applied, highest-scoring songs still rank first
- ✅ Backward compatibility: `use_diversity=False` (default) maintains original behavior
- ✅ **Manual observation:** In pop/happy profile, Neon Echo appears twice (Sunrise City #1, Night Drive Loop #5), but Night Drive Loop is 5th anyway—diversity penalties prevent it from rising if it scores higher

**Real-world impact:**
- Filter bubble reduction: Without diversity, catalog could return same 5 artists repeatedly
- Fair artist representation: Users discover broader palette while still getting quality matches
- Configurable thresholds: `max_same_artist=2` means 3rd song gets penalty, flexible per use case
