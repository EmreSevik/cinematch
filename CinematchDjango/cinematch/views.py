from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pickle
import requests
from .models import FavoriteMovie


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/recommend/')  # Redirect to recommend page instead of homepage
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')  # Redirect to login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login')

# ------------------------------
# TMDB API Fonksiyonları
# ------------------------------

def fetch_poster(movie_id):
    api_key = "62c0cd7deeb424c46268a411e4e009bb"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url).json()
    poster_path = response.get("poster_path", "")
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return ""

def fetch_popular_movies():
    api_key = "62c0cd7deeb424c46268a411e4e009bb"
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1"
    response = requests.get(url).json()
    popular_movies = []
    
    for movie in response.get("results", [])[:6]:
        popular_movies.append({
            "title": movie.get("title", ""),
            "poster_url": f"https://image.tmdb.org/t/p/w500/{movie.get('poster_path', '')}",
            "year": movie.get("release_date", "")[:4] if movie.get("release_date") else "",
            "rating": round(movie.get("vote_average", 0), 1)
        })
    
    return popular_movies

def fetch_top_rated_movies():
    api_key = "62c0cd7deeb424c46268a411e4e009bb"
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=en-US&page=1"
    response = requests.get(url).json()
    top_rated_movies = []
    
    for movie in response.get("results", [])[:6]:
        top_rated_movies.append({
            "title": movie.get("title", ""),
            "poster_url": f"https://image.tmdb.org/t/p/w500/{movie.get('poster_path', '')}",
            "year": movie.get("release_date", "")[:4] if movie.get("release_date") else "",
            "rating": round(movie.get("vote_average", 0), 1)
        })
    
    return top_rated_movies

# ------------------------------
# Model ve Film Listesi
# ------------------------------

movies = pickle.load(open("cinematch/ml/movies_list.pkl", "rb"))
similarity = pickle.load(open("cinematch/ml/similarity.pkl", "rb"))
movie_titles = list(movies['title'].values)

# ------------------------------
# Öneri Fonksiyonu
# ------------------------------

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)
    recommendations = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        title = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_id)
        recommendations.append({
            "title": title,
            "poster_url": poster_url
        })
    return recommendations

# ------------------------------
# Anasayfa
# ------------------------------

def index_view(request):
    popular_movies = fetch_popular_movies()
    top_rated_movies = fetch_top_rated_movies()
    
    return render(request, "index.html", {
        "popular_movies": popular_movies,
        "top_rated_movies": top_rated_movies
    })

# ------------------------------
# Öneri Sayfası
# ------------------------------

@login_required
def recommend_view(request):
    example_ids = [497, 299536, 934433, 550, 531219]  # örnek posterler
    poster_urls = [fetch_poster(mid) for mid in example_ids]

    selected_movie = None
    recommendations = None

    # Handle like action
    if request.method == 'POST' and 'like_movie' in request.POST:
        title = request.POST.get('like_movie')
        poster_url = request.POST.get('like_poster_url')
        # Check if already liked
        if not FavoriteMovie.objects.filter(user=request.user, title=title).exists():
            FavoriteMovie.objects.create(user=request.user, title=title, poster_url=poster_url)
        # Show the same recommendations again
        selected_movie = request.POST.get('selected_movie')
        if selected_movie in movie_titles:
            recommendations = recommend(selected_movie)
    elif request.method == 'POST':
        selected_movie = request.POST.get("movie")
        if selected_movie in movie_titles:
            recommendations = recommend(selected_movie)
        else:
            recommendations = None

    return render(request, "recommend.html", {
        "poster_urls": poster_urls,
        "movies": movie_titles,
        "recommendations": recommendations,
        "selected_movie": selected_movie
    })

@login_required
def profile_view(request):
    if request.method == 'POST' and 'remove_movie' in request.POST:
        title = request.POST.get('remove_movie')
        FavoriteMovie.objects.filter(user=request.user, title=title).delete()
    favorite_movies = FavoriteMovie.objects.filter(user=request.user)
    return render(request, 'profile.html', {'favorite_movies': favorite_movies})
