import streamlit as st
import pickle
import pandas as pd
import requests
import os
from urllib.parse import quote_plus
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent


def get_omdb_api_key():
    api_key = os.getenv("OMDB_API_KEY")

    if api_key:
        return api_key

    return st.secrets["OMDB_API_KEY"]

st.set_page_config(
    page_title="FilmFinder",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def load_assets():
    movies_dict = pickle.load(open(BASE_DIR / 'model' / 'movies.pkl', 'rb'))
    movies_data = pd.DataFrame(movies_dict)
    vectors = pickle.load(open(BASE_DIR / 'model' / 'vectors.pkl', 'rb'))
    # similarity_matrix = cosine_similarity(vectors)
    return movies_data, vectors


@st.cache_data(show_spinner=False, ttl=24 * 60 * 60)
def fetch_movie_details(title):
    api_key = get_omdb_api_key()

    if not api_key:
        return {
            "poster": None,
            "plot": "Plot not available.",
            "year": "Unknown",
            "genre": "Unknown",
            "rating": "N/A",
            "runtime": "Unknown",
            "director": "Unknown",
        }

    url = f"https://www.omdbapi.com/?t={quote_plus(title)}&apikey={api_key}&plot=short"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("Response") == "True":
            return {
                "poster": data.get("Poster") if data.get("Poster") != "N/A" else None,
                "plot": data.get("Plot") if data.get("Plot") != "N/A" else "Plot not available.",
                "year": data.get("Year") if data.get("Year") != "N/A" else "Unknown",
                "genre": data.get("Genre") if data.get("Genre") != "N/A" else "Unknown",
                "rating": data.get("imdbRating") if data.get("imdbRating") != "N/A" else "N/A",
                "runtime": data.get("Runtime") if data.get("Runtime") != "N/A" else "Unknown",
                "director": data.get("Director") if data.get("Director") != "N/A" else "Unknown",
            }
    except Exception:
        pass

    return {
        "poster": None,
        "plot": "Plot not available.",
        "year": "Unknown",
        "genre": "Unknown",
        "rating": "N/A",
        "runtime": "Unknown",
        "director": "Unknown",
    }


movies, vectors = load_assets()


def recommend(movie, top_n=5):
    movie_matches = movies[movies['title'] == movie].index.tolist()

    if not movie_matches:
        return []

    movie_index = movie_matches[0]
    distances = cosine_similarity(vectors[movie_index], vectors).flatten()

    recommendations = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:top_n + 1]

    recommended_movies = []

    for index, score in recommendations:
        movie_title = movies.iloc[index].title
        details = fetch_movie_details(movie_title)

        recommended_movies.append(
            {
                "title": movie_title,
                "score": float(score),
                **details,
            }
        )

    return recommended_movies


st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(255, 179, 71, 0.14), transparent 28%),
                radial-gradient(circle at top right, rgba(110, 86, 207, 0.12), transparent 24%),
                linear-gradient(180deg, #0b1020 0%, #10192f 100%);
            color: #f5f7fb;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .hero-card {
            border-radius: 24px;
            padding: 1.4rem 1.6rem;
            background: linear-gradient(135deg, rgba(18, 28, 51, 0.96), rgba(34, 46, 80, 0.82));
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 24px 80px rgba(0, 0, 0, 0.32);
            margin-bottom: 0.9rem;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.28rem 0.7rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.08);
            color: #ffd58f;
            font-size: 0.72rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.7rem;
        }

        .hero-title {
            font-size: 2.15rem;
            line-height: 1.1;
            margin: 0;
            color: #ffffff;
            font-weight: 800;
        }

        .hero-copy {
            color: rgba(245, 247, 251, 0.78);
            font-size: 0.9rem;
            line-height: 1.55;
            max-width: 58rem;
            margin-top: 0.5rem;
        }

        .stat-card {
            padding: 1rem 1.1rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }

        .stat-label {
            color: rgba(245, 247, 251, 0.62);
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
        }

        .stat-value {
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 700;
        }

        .movie-card {
            height: 560px;
            display: flex;
            flex-direction: column;
            border-radius: 24px;
            padding: 0.9rem;
            background: linear-gradient(180deg, rgba(18, 26, 47, 0.94), rgba(14, 20, 37, 0.98));
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.24);
            overflow: hidden;
        }

        .movie-card img {
            flex-shrink: 0;
        }

        .movie-title {
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 700;
            margin-top: 0.6rem;
            margin-bottom: 0;
            display: -webkit-box;
            -webkit-line-clamp: end;
            -webkit-box-orient: vertical;
            overflow: hidden;
            height: 2.3rem;
            flex-shrink: 0;
        }

        .movie-meta {
            color: rgba(245, 247, 251, 0.7);
            font-size: 0.84rem;
            margin-bottom: 0.6rem;
            margin-top: 0.15rem;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
            overflow: hidden;
            flex-shrink: 0;
        }

        .movie-plot {
            color: rgba(245, 247, 251, 0.74);
            font-size: 0.9rem;
            line-height: 1.55;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
            flex-grow: 1;
        }

        .score-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.35rem;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            background: rgba(255, 213, 143, 0.12);
            color: #ffd58f;
            font-size: 0.8rem;
            font-weight: 700;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(11, 16, 32, 0.98), rgba(17, 25, 47, 0.98));
            border-right: 1px solid rgba(255, 255, 255, 0.07);
        }

        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {
            color: rgba(245, 247, 251, 0.88) !important;
        }

        div[data-testid="stSlider"] [role="slider"] {
            background-color: #3b82f6 !important;
            border-color: #3b82f6 !important;
            box-shadow: none !important;
        }

        div[data-testid="stSlider"] [style*="rgb(255, 75, 75)"],
        div[data-testid="stSlider"] [style*="rgba(255, 75, 75"],
        div[data-testid="stSlider"] [style*="#ff4b4b" i] {
            background-color: #3b82f6 !important;
            border-color: #3b82f6 !important;
            color: #3b82f6 !important;
        }

        div[data-testid="stThumbValue"] {
            color: #60a5fa !important;
        }

        div[data-testid="stTickBarMin"],
        div[data-testid="stTickBarMax"] {
            color: rgba(245, 247, 251, 0.6) !important;
        }

        div[data-baseweb="select"] > div {
            border-color: rgba(255, 255, 255, 0.15) !important;
        }
        div[data-baseweb="select"]:focus-within > div {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 1px #3b82f6 !important;
        }

        .stButton > button {
            background: #3b82f6 !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 700;
            box-shadow: none !important;
        }

        .stButton > button:hover {
            background: #3b82f6 !important;
            box-shadow: none !important;
        }

        .stButton > button:focus:not(:active) {
            color: #ffffff !important;
            border-color: #3b82f6 !important;
            box-shadow: none !important;
        }

        div[data-testid="column"] {
            display: flex;
        }
        div[data-testid="column"] > div {
            width: 100%;
        }
        div[data-testid="stVerticalBlock"]:has(> div .movie-card) {
            height: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("## FilmFinder")
st.sidebar.markdown("Discover Your Next Favorite Movie")

option = st.sidebar.selectbox(
    'Choose Your Movie',
    movies['title'].values,
)

top_n = st.sidebar.slider('Recommendation count', min_value=3, max_value=12, value=4, step=1)

selected_details = fetch_movie_details(option)

st.markdown(
    """
    <div class="hero-card">
        <div class="eyebrow">Movie recommendation system</div>
        <h1 class="hero-title">Discover movies that match your taste</h1>
        <p class="hero-copy">
            From timeless classics to modern blockbusters, discover movies that match your preferences with intelligent recommendations
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

hero_left, hero_right = st.columns([0.9, 1.3], gap="large")

with hero_left:
    poster = selected_details["poster"]
    if poster:
        st.image(poster, use_container_width=True)
    else:
        st.markdown(
            """
            <div class="movie-card" style="display:flex; align-items:center; justify-content:center; min-height: 520px; text-align:center;">
                <div>
                    <div style="font-size:4rem;">🎬</div>
                    <div class="movie-title">Poster unavailable</div>
                    <div class="movie-meta">A poster could not be fetched for this title.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with hero_right:
    st.markdown(f"## {option}")
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    st.markdown(selected_details["plot"])
    st.markdown("<div style='height:0.9rem'></div>", unsafe_allow_html=True)

    stat1, stat2, stat3 = st.columns(3)
    with stat1:
        st.markdown(
            f"<div class='stat-card'><div class='stat-label'>Year</div><div class='stat-value'>{selected_details['year']}</div></div>",
            unsafe_allow_html=True,
        )
    with stat2:
        st.markdown(
            f"<div class='stat-card'><div class='stat-label'>IMDb Rating</div><div class='stat-value'>{selected_details['rating']}</div></div>",
            unsafe_allow_html=True,
        )
    with stat3:
        st.markdown(
            f"<div class='stat-card'><div class='stat-label'>Runtime</div><div class='stat-value'>{selected_details['runtime']}</div></div>",
            unsafe_allow_html=True,
        )

    stat4, stat5 = st.columns(2)
    with stat4:
        st.markdown(
            f"<div class='stat-card'><div class='stat-label'>Genre</div><div class='stat-value'>{selected_details['genre']}</div></div>",
            unsafe_allow_html=True,
        )
    with stat5:
        st.markdown(
            f"<div class='stat-card'><div class='stat-label'>Director</div><div class='stat-value'>{selected_details['director']}</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:1.3rem'></div>", unsafe_allow_html=True)

    generate_clicked = st.button('Generate recommendations', type='primary', use_container_width=True)

if generate_clicked:
    with st.spinner('Building your recommendation list...'):
        recommend_movies = recommend(option, top_n=top_n)

    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)

    if recommend_movies:
        st.markdown("### You May Also Enjoy")
        rows = st.columns(4)

        for index, movie in enumerate(recommend_movies):
            with rows[index % 4]:
                st.markdown(
                    f"""
                    <div class="movie-card">
                        {f'<img src="{movie["poster"]}" style="width:100%; border-radius:18px; object-fit:cover; aspect-ratio: 2 / 3;" />' if movie["poster"] else '<div style="width:100%; border-radius:18px; aspect-ratio: 2 / 3; background: linear-gradient(135deg, rgba(255,255,255,0.14), rgba(255,255,255,0.03)); display:flex; align-items:center; justify-content:center; color: rgba(255,255,255,0.72); font-size:1.6rem;">No poster</div>'}
                        <div class="movie-title">{movie['title']}</div>
                        <div class="movie-meta">{movie['year']} • {movie['genre']}</div>
                        <div class="score-pill">Match score: {movie['score']:.3f}</div>
                        <div class="movie-plot" style="margin-top:0.85rem;">{movie['plot']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info('No recommendations were found for the selected title.')