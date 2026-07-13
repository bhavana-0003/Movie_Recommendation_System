# FilmFinder
FilmFinder is a content-based movie recommendation system developed using Python, Streamlit, and Scikit-learn. The application recommends movies by analyzing features such as genres, cast, director, keywords, and movie descriptions. It also retrieves movie posters and additional information using the OMDb API to provide a better user experience.

## Features
- Content-based movie recommendations
- Movie posters and details using OMDb API
- IMDb rating, genre, runtime, and director information
- TF-IDF vectorization and cosine similarity
- Interactive and responsive Streamlit interface

## Tech Stack
- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Requests
- OMDb API

## Dataset
TMDB 5000 Movies Dataset

## How It Works
1. Select a movie from the list.
2. The system compares the selected movie with all other movies using TF-IDF vectors and cosine similarity.
3. The most similar movies are recommended.
4. Posters and movie details are fetched from the OMDb API and displayed in the application.

## Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Future Enhancements
- Trailer integration
- Genre-based filtering
- Watchlist functionality
- User authentication
- Hybrid recommendation system

## Developed By
Bhavana Sri