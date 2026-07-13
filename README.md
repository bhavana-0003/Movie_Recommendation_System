# FilmFinder
FilmFinder is a content-based movie recommendation system developed using Python, Streamlit, and Scikit-learn. The application recommends movies by analyzing features such as genres, cast, director, keywords, and movie descriptions. It also retrieves movie posters, IMDb ratings, genres, runtime, and plot summaries using the OMDb API to provide an engaging user experience.

## Live Demo
https://filmfinder-nxtt.onrender.com/

## Features
- Content-based movie recommendation system
- Interactive and responsive Streamlit web interface
- Live movie posters and metadata using the OMDb API
- Displays IMDb rating, runtime, genre, director, and plot
- TF-IDF vectorization for feature representation
- Cosine similarity for finding similar movies
- Fast and efficient recommendation generation

## Tech Stack
- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Requests
- Pickle
- OMDb API

## Dataset
TMDB 5000 Movies Dataset

The dataset includes movie information such as:
- Movie Title
- Genres
- Keywords
- Cast
- Crew
- Overview

## Project Structure
FilmFinder/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── model/
│   ├── movies.pkl
│   └── vectors.pkl
│
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
│
└── .streamlit/
    └── secrets.toml

## Workflow
TMDB Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
(Genres + Cast + Director + Keywords + Overview)
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Movie Feature Vectors
      │
      ▼
User Selects a Movie
      │
      ▼
Cosine Similarity
      │
      ▼
Top Similar Movies
      │
      ▼
OMDb API
      │
      ▼
Movie Posters & Details
      │
      ▼
Recommended Movies Displayed

## How It Works
1. Select a movie from the dropdown list.
2. The application retrieves the selected movie's TF-IDF vector.
3. Cosine similarity is calculated between the selected movie and all other movies.
4. The top similar movies are identified.
5. The OMDb API fetches posters and additional movie information.
6. Recommendations are displayed through the Streamlit interface.

## Installation

Clone the repository
git clone https://github.com/bhavana-0003/Movie_Recommendation_System.git

Navigate to the project folder
cd Movie_Recommendation_System

Install the required packages
pip install -r requirements.txt

Run the application
streamlit run app.py

## Future Enhancements
- Movie trailer integration
- Genre-based filtering
- Watchlist functionality
- User authentication
- Hybrid recommendation system
- Personalized recommendations
- Search autocomplete
- Sorting based on IMDb rating and release year

## Developed By
**Bhavana Sri**
GitHub: https://github.com/bhavana-0003

## Acknowledgements
- TMDB 5000 Movies Dataset
- OMDb API
- Streamlit
- Scikit-learn
