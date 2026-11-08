# Content Recommendation System (OOP)

A Python-based content recommendation system inspired by platforms like Netflix and YouTube. Built using **Object-Oriented Programming (OOP)**, it recommends movies, books, and courses based on user preferences and interaction history.

> **University Project:** Object-Oriented Programming  
> ENSA Berrechid — Hassan I University

## Features

- **Content Hierarchy:** A base class `Contenu` with specialized subclasses:
  - `Film` — stores movie duration.
  - `Livre` — stores book author.
  - `Cours` — stores course level.

- **User Profiles:** Three user types with different rating perceptions:
  - `User`
  - `UserExigeant` (Demanding User)
  - `UserGenereux` (Generous User)

- **Content Interactions:** Users can view and rate content, dynamically updating global ratings.

- **Operator Overloading:** Supports custom operations such as:
  - `user + content`
  - `content in user`
  - `==` and `<`

- **Content Similarity:** Calculates similarity based on content type, category, specific attributes, and ratings.

- **Personalized Recommendations:** Ranks content using a scoring formula combining:
  - **P:** User preference
  - **R:** Global content rating
  - **H:** Similarity to the user's interaction history

  Already-viewed content is excluded from recommendations.

### Recommendation Formula

```python
score = (0.5 * H + 0.3 * P + 0.2 * R) * exp(H - 1)
```

## Usage

Run the project using:

```bash
python mon_code.py
```

Example:

```python
u = User(["sci-fi"])
u.noter(Film("Inception", "sci-fi", 8, 148), 9)

for c in u.recommender(catalogue):
    print(c.title)
```

## Test Scenarios

1. **Sci-Fi Fan:** Similar content is ranked first.
2. **Demanding vs. Generous Users:** The same raw rating produces different recommendations depending on the user's profile.
3. **Mixed Tastes:** Recommendations balance multiple user interests.

## Technologies & Concepts

- Python
- Object-Oriented Programming
- Inheritance and Polymorphism
- Operator Overloading
- Recommendation Algorithms
- Similarity Scoring

## Author

**Your Name**  
ENSA Berrechid — Hassan I University
