# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0** – A preference-based music recommender using weighted attribute matching.

---

## 2. Intended Use  

VibeMatch recommends songs based on a user's preferred genre, mood, and audio characteristics (energy, valence, danceability). It's designed for classroom exploration of recommender systems to demonstrate how scoring weights and feature importance shape recommendations. This is not intended for production use, but rather as a learning tool to understand trade-offs in music discovery systems.

**Assumptions:** 
- Users have one primary preferred genre and mood
- Audio attributes (energy, valence, danceability) are numeric and comparable across songs
- Higher genre/mood matches are always better (no users want "wrong" genres)

---

## 3. How the Model Works  

The system scores each song by combining five factors:

1. **Genre Match** (+10 points if exact match): Does the song match your favorite genre?
2. **Mood Match** (+5 points if exact match): Does the song match your preferred mood (happy, chill, intense, etc.)?
3. **Energy Fit** (up to +3 points): Is the song's energy level close to what you want? A perfect match gets full points; bigger differences lose points.
4. **Valence Fit** (up to +2 points): Is the "positivity" of the song aligned with your preference?
5. **Danceability Fit** (up to +1 point): Does the song's groove match what you're looking for?

Think of it like a checklist: "Does this song match my genre? My mood? Is it the right energy level?" Each factor contributes to a total score, and the songs with the highest scores rise to the top.

**Maximum possible score: 21 points**

The algorithm is straightforward: calculate a score for every song in the catalog, sort by score, and return the top 5.

---

## 4. Data  

**Dataset:** 18 songs across 12 genres (pop, lofi, rock, ambient, jazz, indie pop, blues, electronic, reggae, hip-hop, classical, metal, folk, edm, synthwave)

**Genres represented:**
- High-energy / Dance: EDM, pop, electronic, hip-hop, synthwave (5 songs)
- Acoustic / Chill: lofi, jazz, folk, acoustic, ambient (5 songs)
- Intense / Alternative: rock, metal (2 songs)
- Specialized: blues, classical, reggae, indie pop (6 songs)

**Missing perspectives:** 
- Limited instrumental/background music diversity
- No country, R&B, or experimental genres
- Only 2 "aggressive/intense" songs vs. 5+ "chill" songs—the catalog is imbalanced

---

## 5. Strengths  

**Works well for:**
- Users with clear, mainstream preferences (e.g., "I like pop and happy songs") → Top recommendation is almost always a perfect or near-perfect match
- Energy-based filtering → Users seeking high-energy or chill music get appropriate recommendations
- Common genre/mood combinations → "Happy pop," "chill lofi," and "intense rock" all return intuitive top choices

**Examples from testing:**
- **Chill Lofi Student** (lofi + chill + low energy): Gets Library Rain and Midnight Coding—both exact genre and mood matches
- **High-Energy Pop Lover** (pop + happy + 0.9 energy): Gets Sunrise City—perfect on all three categorical factors
- **Deep Intense Rocker** (rock + intense + high energy): Gets Storm Runner—perfect match

These feel right. The system correctly penalizes recommendations that miss on genre.

---

## 6. Limitations and Bias 

**Critical Issue #1: Genre Dominance (47.6% of score)**
The 10-point genre bonus is larger than all continuous attributes combined. This means a song with the "right" genre but terrible energy fit will rank above a song with "wrong" genre but perfect energy fit. Example: "Conflicting user likes classical + happy + high energy (0.9)" receives Classical Dreams (energy 0.45, mood sophisticated) ranked #1, even though Sunrise City (pop/happy/energy 0.82) is far closer to what they actually want. The genre match alone overpowers all other factors.

**Critical Issue #2: Mood Cliff Effect**
Mood mismatches cost exactly 5 points—larger than any single continuous metric can earn (max 3 for energy). This creates discrete ranking cliffs where mood matters more than actual attribute alignment. In the High-Energy Pop test, "Gym Hero" (pop/intense/energy 0.93) loses to "Sunrise City" (pop/happy/energy 0.82) because the 5-point mood penalty is larger than the energy advantage, even though Gym Hero is objectively closer on energy.

**Issue #3: Recommendation Repetition (Filter Bubble)**
Without diversity enforcement, "universally appealing" songs (high valence, high danceability) like Gym Hero appear in the top 5 for 3 out of 5 test profiles, regardless of user taste. The system recommends the same songs to different users, reducing serendipity and niche discovery.

**Issue #4: No Acoustic/Instrumental Distinction**
Acousticness is loaded but never used in scoring. A user who values acoustic instruments (singer-songwriter feel) gets the same recommendations as someone seeking electronic sound.

---

## 7. Evaluation  

**Profiles Tested (5 total):**

1. **High-Energy Pop Lover** (genre: pop, mood: happy, energy: 0.9)
   - Top 5: Sunrise City, Gym Hero, Rooftop Lights, EDM Festival, Neon Nights
   - Assessment: ✓ Works well—genre/mood matches rank first

2. **Chill Lofi Student** (genre: lofi, mood: chill, energy: 0.35)
   - Top 5: Library Rain, Midnight Coding, Focus Flow, Spacewalk Thoughts, Coffee Shop Stories
   - Assessment: ✓ Excellent—near-perfect matches, strong energy alignment

3. **Deep Intense Rocker** (genre: rock, mood: intense, energy: 0.9)
   - Top 5: Storm Runner, Gym Hero, Metal Thunder, Night Drive Loop, Neon Nights
   - Assessment: ✓ Good—Storm Runner is perfect; Gym Hero ranks high due to intense mood

4. **Edge Case: Conflicting Preferences** (genre: classical, mood: happy, energy: 0.9)
   - Top 5: Classical Dreams (0.45 energy!), Sunrise City, Rooftop Lights, Gym Hero, EDM Festival
   - Assessment: ✗ Poor—Classical Dreams is ranked first despite catastrophic energy mismatch. Genre match overpowers all else.
   - **Surprise:** Doubling energy weight and halving genre weight makes Sunrise City rank first, which intuitively feels better for this user.

5. **Balanced Music Explorer** (genre: indie pop, mood: relaxed, energy: 0.5)
   - Top 5: Rooftop Lights, Sunset in Jamaica, Coffee Shop Stories, Classical Dreams, Folk Campfire
   - Assessment: ✓ Reasonable—Rooftop Lights matches genre; mood mismatches are penalized fairly

**Weight Sensitivity Experiment:**
- Changed weights from (Genre=10, Energy=3) to (Genre=5, Energy=6)
- **Result:** For high-quality matches (like High-Energy Pop Lover), no change—already perfect
- **Result:** For conflicting preferences, massive improvement—Sunrise City jumps from #2 to #1
- **Insight:** The system is robust to weight changes only when the catalog naturally contains good matches; otherwise, categorical weights determine all rankings

**Surprising Finding:** Gym Hero appears in 3 of 5 top-5 lists despite serving different user tastes (High-Energy Pop, Intense Rock, and Conflicting Preferences). This song has objectively high valence (0.77), energy (0.93), and danceability (0.88), making it a "universal" recommendation. The system has no mechanism to diversify away from such songs.

---

## 8. Future Work  

1. **Rebalance weights:** Reduce genre dominance from 10 → 6 points; raise energy importance from 3 → 4 points to better serve users with unusual genre/mood combinations
2. **Use acousticness:** Add a check for users who prefer acoustic instruments (likes_acoustic) to surface guitar-driven or stripped-down versions
3. **Add diversity enforcement:** Penalize songs that appear frequently across user profiles to encourage serendipity
4. **Expand mood recognition:** Instead of exact mood match, use mood similarity (e.g., "happy" and "euphoric" are similar) to reduce the harsh 5-point cliff
5. **Build a catalog:** Add 50+ more songs to reduce filter bubbles; ensure all genres have 3+ songs each
6. **Explain misses:** When recommending a song with a mood mismatch, explicitly flag it ("You liked rock, this is pop, but check it out because...") to set expectations

---

## 9. Personal Reflection  

### Biggest Learning Moment

Building this recommender revealed how easy it is to accidentally create biased systems **just by making design choices that seemed reasonable at the time.** I started thinking genre match was the most important factor, so I weighted it highest (10 points). But in testing, I discovered that genre dominance actually *hides* what users really want—someone who loves high-energy classical music gets locked out by the genre matching rules. This taught me that **fairness isn't baked into algorithms automatically; it requires testing against diverse user profiles.** The "edge case" of classical + high energy revealed a systemic bias that only appeared under stress testing. This is probably the most important lesson: your system will surprise you in ways that math alone can't predict.

### How AI Tools Helped (and Where I Double-Checked)

Working through this project, I used Claude to help structure the evaluation methodology, generate synthetic test profiles, and analyze the surprising patterns in the data (like Gym Hero appearing in 3 of 5 top-5 lists). **Where I double-checked Claude:** When Claude suggested rebalancing weights as a fix, I tested it myself rather than accepting the recommendation at face value. The weight sensitivity experiment showed that rebalancing helped the edge case but left mainstream users unchanged—revealing that weight tuning wasn't the real solution. This taught me to use AI for *ideation and analysis* but *verify results empirically* before accepting recommendations, especially for claims about how a system will behave.

### What Surprised Me About Simple Algorithms

The biggest surprise was how **"human" the recommendations feel even though the algorithm is just weighted math.** Users naturally understand "+10 for genre match" and can reason about why Sunrise City ranks above Storm Runner for a pop lover. Yet this simplicity masks profound complexity: Gym Hero appearing everywhere despite serving different users taught me that **simple scoring naturally creates filter bubbles.** Without diversity enforcement, the algorithm converges toward "universally appealing" songs rather than personalized picks. This made me realize why production systems (Spotify, Apple Music) explicitly use diversity mechanisms—it's not just a nice-to-have feature, it's essential to prevent mathematical convergence toward safety.

I was also surprised by how much the *explanation* matters. When a song ranks high due to a mismatch (e.g., high energy for a classical search), the breakdown helps users decide whether the system understood them or missed the mark. This taught me that recommendation systems are as much about **communicating reasoning** as about scoring accuracy.

### What I'd Try Next

If I extended this project, I'd focus on three things:

1. **Reframe categories as continuous features:** Instead of "genre: classical OR pop" (binary match), treat genre as a point in musical space where distance matters. This would let the algorithm naturally discover users who bridge classical and electronic without explicit rules.

2. **Add diversity enforcement:** Track which songs appear frequently across user profiles and penalize repetition. This would prevent Gym Hero from appearing everywhere while still ranking it high for profiles it genuinely fits.

3. **Incorporate user feedback loops:** In a real system, I'd track what users actually listened to vs. what I recommended, then use that signal to adjust weights per-user. The "edge case" user might teach the system over time that high energy matters more to them than genre purity.
