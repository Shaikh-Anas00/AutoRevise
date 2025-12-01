# AutoRevise — Final Evaluation

Date: 2025-11-14

This document is the final evaluation for the AutoRevise project. It collects the working process, system diagrams, the database ER model, sequence/process flowcharts, how to run and test the main paths, and a deep, practical explanation of the spaced repetition algorithm (SM-2) as implemented in the code.

## Contents
- Project summary
- Working process (flowchart + narrative)
- Database ER Diagram (entities, attributes, keys)
- Sequence diagrams / data flows for core features
- Spaced Repetition (SM-2) — detailed explanation, math, and examples
- Where SM-2 is used in the code (file + function references)
- Testing and verification steps (Fast checks)
- Edge cases, limitations, and recommended improvements

---

## Project summary

AutoRevise is a web-based flashcard and MCQ learning system with user accounts, decks, cards, MCQs, gamification (points, achievements), and a spaced repetition engine that schedules reviews. The backend is a Flask application (`Backened/App1.py`) with a MySQL data store. The frontend includes static pages and JS that call the backend API (e.g., `Frontened 1/js/study-session-connected.js`).

Core features used in evaluations:
- User registration/login, persistent sessions
- Deck and card creation (single & bulk CSV upload)
- Study sessions for flashcards and MCQs
- Spaced repetition scheduling with SM-2 for flashcards
- Simpler adaptive scheduling for MCQs
- Achievement awarding and points system

---

## Working process (flowchart + narrative)

High-level user flow (ASCII flowchart):

```
User
  │
  │ (1) Register / Login
  ▼
 Dashboard ─────────────┐
  │                     │
  │ (2) Select Deck      │
  ▼                     ▼
 Deck View            Create/Edit Deck / Cards
  │
  │ (3) Start Study Session (GET /study-session)
  ▼
 Study Session UI <─── Backend returns due cards (CardPerformance.next_review_date <= today OR no record)
  │
  │ (4) Show card front → user flips → rates (forgot/hard/good/easy)
  ▼
 Submit review (POST /submit-review) ──> Backend updates CardPerformance using SM-2
  │
  │ (5) Backend returns next_review_date, interval, points awarded
  ▼
 Next card (repeat) or session complete
```

Narrative of what happens when a user reviews a card:
1. Frontend requests due cards via `/study-session`. The backend selects cards where `CardPerformance.next_review_date` is NULL or <= current date, returning a prioritized set.
2. The user studies each card and, after revealing the answer, rates their recall: `forgot`, `hard`, `good`, or `easy`.
3. The frontend calls `/submit-review` with `card_id` and `rating`.
4. The backend retrieves the user's current CardPerformance for that card (if any), then calls `calculate_sm2(rating, current_interval, current_ease)` to compute new interval and ease factor.
5. Backend stores/updates the `CardPerformance` row with `next_review_date`, `interval`, and `ease_factor`. Points and StudyLog are updated, and achievements checked.

---

## Database ER Diagram (textual)

Below are the primary tables with key columns and relationships. This mirrors schema files and queries used inside `App1.py`.

- Users (user_id PK)
  - user_id (PK)
  - username
  - email
  - password_hash
  - points
  - is_admin
  - created_at

- Decks (deck_id PK)
  - deck_id (PK)
  - user_id (FK -> Users.user_id)
  - deck_name
  - description
  - created_at

- Cards (card_id PK)
  - card_id (PK)
  - deck_id (FK -> Decks.deck_id)
  - front_content
  - back_content
  - created_at

- CardPerformance (composite unique: user_id+card_id)
  - cp_id (PK)
  - user_id (FK -> Users.user_id)
  - card_id (FK -> Cards.card_id)
  - next_review_date (DATE)
  - interval (INT)  -- days
  - ease_factor (FLOAT)

- StudyLog
  - user_id (FK)
  - study_date (DATE) -- PK combined with user_id
  - cards_reviewed (INT)

- Achievements
  - achievement_id (PK)
  - name, description, icon_url

- UserAchievements
  - user_id (FK), achievement_id (FK), earned_at

- MCQ_Categories, MCQ_Questions, MCQ_Performance, MCQ_Upload_Log (similar structure for MCQ features)

ER relationships (summary):
- Users 1--* Decks
- Decks 1--* Cards
- Users *--* Cards via CardPerformance (user-card performance records)
- Users 1--* StudyLog
- Users *--* Achievements via UserAchievements

ASCII relationship sketch:

```
Users (1)──<(user_id) Decks (n)──<(deck_id) Cards (n)
  │                                  │
  └──<(user_id) CardPerformance (n)──┘

StudyLog(user_id, study_date)
Achievements <-- UserAchievements --> Users
MCQ_Categories --> MCQ_Questions --> MCQ_Performance
```

---

## Sequence / Data flow for the study-review path

1. Frontend GET /study-session
   - Backend selects cards:
     - For each card: left join CardPerformance for the user
     - WHERE cp.next_review_date IS NULL OR cp.next_review_date <= CURDATE()
     - ORDER BY cp.next_review_date ASC, c.created_at ASC

2. Frontend displays card, user flips and rates.

3. Frontend POST /submit-review { card_id, rating }
   - Backend verifies ownership
   - Loads current CardPerformance (interval, ease_factor)
   - Calls calculate_sm2(rating, current_interval, current_ease)
   - Computes next_review_date = today + new_interval days
   - Inserts or updates CardPerformance
   - Updates Users.points
   - Inserts/updates StudyLog
   - Commits transaction and returns next_review_date and interval

---

## Spaced Repetition (SM-2) — detailed explanation and math

This project implements a variant of the SM-2 algorithm (originally developed for SuperMemo). SM-2 schedules reviews using two state variables per (user, card): interval and ease factor (EF). The implementation is in `Backened/App1.py` as `calculate_sm2`.

Contract for calculate_sm2 (inputs/outputs):
- Inputs:
  - rating: one of ['forgot', 'hard', 'good', 'easy'] (maps to quality 0—5)
  - current_interval: integer number of days since last interval (0 if never reviewed)
  - current_ease: float ease factor (defaults to 2.5 for new cards)
- Outputs:
  - new_interval (int): number of days until next review
  - new_ease (float rounded to 2 decimals)

Implementation details (from code):

1) Rating → quality mapping (0–5 scale used by SM-2):
   - 'forgot' -> 0
   - 'hard'   -> 3
   - 'good'   -> 4
   - 'easy'   -> 5

2) Ease factor update formula (standard SM-2 variant used here):
   new_ease = current_ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
   then new_ease = max(1.3, new_ease)

   Explanation: This is the original SM-2 EF update formula. It rewards high-quality recalls by slightly increasing EF and heavily penalizes low-quality responses. The floor of 1.3 ensures spacing doesn't collapse to unrealistic values.

3) Interval update rules (implementation choice in code):
   - If quality < 3 (i.e., forgot), treat as failed — new_interval = 1 (restart learning)
   - Otherwise:
       - If current_interval == 0 → new_interval = 1 (first successful review)
       - If current_interval == 1 → new_interval = 6 (second successful review)
       - Else → new_interval = round(current_interval * new_ease)

   These match SM-2's early-step special cases (1, 6) and then a multiplicative growth using EF.

Notes about types and storage
- `ease_factor` is stored in DB as a float but the code rounds to 2 decimals for readability/storage.
- `interval` is stored as integer days.
- `next_review_date` = today + new_interval (computed with datetime.date + timedelta(days=new_interval)).

Worked numeric examples

Example A — New card, user answers 'good':
- Starting state: current_interval = 0, current_ease = 2.5
- quality = 4 (good)
- new_ease = 2.5 + (0.1 - (5 - 4) * (0.08 + (5 - 4) * 0.02))
           = 2.5 + (0.1 - 1 * (0.08 + 1 * 0.02))
           = 2.5 + (0.1 - (0.08 + 0.02))
           = 2.5 + (0.1 - 0.1) = 2.5
- new_interval: current_interval == 0 → new_interval = 1
- next_review_date = today + 1 day

Example B — After 2 successful reviews: current_interval = 6, current_ease = 2.5, user answers 'easy'
- quality = 5
- new_ease = 2.5 + (0.1 - (5 - 5)*(...)) = 2.5 + 0.1 = 2.6
- new_interval = round(6 * 2.6) = round(15.6) = 16 days

Example C — Known card where user forgets (quality = 0)
- current_interval = 16, current_ease = 2.6
- quality = 0
- new_ease = 2.6 + (0.1 - (5 - 0)*(0.08 + (5 - 0)*0.02))
           = 2.6 + (0.1 - 5*(0.08 + 5*0.02))
           = 2.6 + (0.1 - 5*(0.08 + 0.1))
           = 2.6 + (0.1 - 5*(0.18))
           = 2.6 + (0.1 - 0.9) = 2.6 - 0.8 = 1.8
           -> floor 1.3 not triggered (1.8 > 1.3)
- quality < 3 → new_interval = 1 (restart)

Implications
- EF slowly adapts to user's demonstrated recall quality. Higher EF accelerates future intervals multiplicatively.
- A failed review quickly reduces the interval (restart) and may reduce EF, forcing more frequent reviews.

Why this works
- SM-2 encodes the human forgetting curve: items that are easily recalled should be reviewed after exponentially increasing intervals; items that are hard or forgotten should be reviewed much sooner.

---

## Where SM-2 is used in the code (concrete references)

- File: `Backened/App1.py`
  - Function: `calculate_sm2(rating, current_interval, current_ease)` — implements the EF update and interval logic described above.
  - Endpoint: `@app.route('/submit-review', methods=['POST'])` — verifies card ownership, loads or initializes `CardPerformance`, calls `calculate_sm2`, computes `next_review_date`, updates/inserts `CardPerformance`, awards points and updates `StudyLog`, then commits to DB.
  - Endpoint: `@app.route('/study-session', methods=['GET'])` — selects cards where `CardPerformance.next_review_date IS NULL OR <= CURDATE()`; these are the due cards the SM-2 scheduling created.

- Frontend: `Frontened 1/js/study-session-connected.js`
  - Calls backend `api.getStudySession()` and `api.submitReview(card_id, rating)` (wrappers around the endpoints). The frontend uses the rating buttons ('forgot','hard','good','easy') that map to the server's SM-2 implementation.

Database columns involved:
- CardPerformance.next_review_date (DATE)
- CardPerformance.interval (INT)
- CardPerformance.ease_factor (FLOAT)

---

## Testing and verification steps (quick)

Prerequisites:
- Python 3.8+ and required packages in `Backened/requirements.txt` (Flask, mysql-connector-python, bcrypt, python-dotenv, flask-cors).
- MySQL server accessible and database `autorevise_db` created using provided schema SQL files (`schema_mcq_categories.sql`, `schema_mcq_update.sql`, `schema2.sql`).

Environment setup (PowerShell examples):

```powershell
# from project root (where App1.py is located)
cd 'd:\New folder\DBMS\Backened'
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Set DB env vars (example values)
$env:DB_HOST = 'localhost'; $env:DB_USER = 'root'; $env:DB_PASSWORD='Root123'; $env:DB_NAME='autorevise_db';
$env:SECRET_KEY = 'change-this-in-prod'

# Run the Flask backend (if App1.py contains run block) or use flask run with FLASK_APP
python App1.py
```

Quick API checks (PowerShell/curl style):

1) Register a test user (POST /register) — ensure response 201 and session cookie returned.
2) Create a deck (POST /decks) — returns deck_id.
3) Add a card to the deck (POST /decks/{deck_id}/cards) — returns card_id.
4) Request study session (GET /study-session) — card should be returned as due (first-time reviews have no CardPerformance record).
5) Submit a review (POST /submit-review) with rating 'good' — server should return next_review_date and interval = 1.

Using Postman or the frontend `study-session` page provides the same flows interactively.

---

## Edge cases, limitations, and recommended improvements

1. Timezones / date semantics
   - The code uses server-side DATE and CURDATE() comparisons. If your users are in different timezones or you run the server in UTC, consider storing timestamps in UTC (DATETIME/TIMESTAMP) and computing due items relative to the user's timezone.

2. Multiple reviews per day
   - The current logic uses integer `interval` days; multiple reviews in a single day will still set next_review_date = today + interval. If you want intra-day scheduling, store timestamps and use fractional-day logic or minimum-hour granularity.

3. Recalibration strategies
   - When ease factor drifts very low or very high, consider capping EF to a reasonable band (e.g., [1.3, 3.5]). Code currently enforces a lower bound of 1.3 only.

4. Warm-start/initial learning steps
   - SM-2 assumes that the user marks the quality; to support richer learning, you can add an explicit learning phase for new cards (e.g., 3 short exposures before starting SM-2 scheduling).

5. Bulk / concurrency safety
   - Ensure DB writes in `/submit-review` are performed transactionally as they are currently committed; consider retry/backoff for transient DB errors.

6. Adaptive UX
   - Provide users with a review history per card and an option to manually reschedule a card if they feel the algorithm scheduled it incorrectly.

7. Analytics
   - Use stored `StudyLog` and `CardPerformance` to compute machine learning models for personalized scheduling in the future.

---

## Final notes and quick checklist

- Files referenced while preparing this final evaluation:
  - `Backened/App1.py` (SM-2 implementation and endpoints)
  - `Frontened 1/js/study-session-connected.js` (frontend usage)
  - `Documentation/COMPLETE_PROJECT_DOCUMENTATION.md` and `Documentation/SYSTEM_DIAGRAMS.md` (existing project docs)

- Quick checklist to verify the core flow is working:
  1. Start backend and confirm `/session-check` returns expected session data.
  2. Register/login, create a deck, create a card.
  3. GET `/study-session` returns the card.
  4. POST `/submit-review` with 'good' and observe interval 1 and next_review_date = tomorrow.

If you'd like, I can also:
- Generate a printable PDF version of this final evaluation.
- Create visualization images (flowchart and ER diagram) in SVG/PNG and add them to `Documentation/`.
- Add a short automated test script that performs the quick checklist end-to-end using `requests` (Python) and asserts expected responses.

---

End of final evaluation.
