import requests
from django.shortcuts import render,redirect,get_object_or_404
from .form import MovieForm,ReviewForm,MovieTypeForm
from .models import Movie,Review
from django.contrib.auth.decorators import login_required


movie_key = "e35b8f1415cec2229f2b61f89ea5db75"
movie_url = "https://api.themoviedb.org/3/search/movie"
 
def home(request):
    if request.user.is_authenticated:
        user_movies = Movie.objects.filter(user=request.user)
        response = requests.get("https://api.themoviedb.org/3/movie/now_playing",params={"api_key":"e35b8f1415cec2229f2b61f89ea5db75"})
        data = response.json()['results'][0:10]
        action_movie = []
        scifi_movie = []
        love_movie = []
        for i in user_movies:
             if i.category == 'action':
                action_movie.append(i)
             if i.category == 'sci-fi':
                scifi_movie.append(i)
             if i.category == 'love':
                love_movie.append(i) 
        return render(request, 'home.html', {'movie': user_movies,'now_playing' : data,"action_movie" : action_movie,"scifi_movie":scifi_movie,"love_movie":love_movie})          
    else: 
        response = requests.get("https://api.themoviedb.org/3/movie/now_playing",params={"api_key":"e35b8f1415cec2229f2b61f89ea5db75"})
        data = response.json()['results'][0:10]
    return render(request, 'home.html', {'now_playing' : data})

@login_required
def search(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            movie_name = form.cleaned_data["movie_name"]
            response = requests.get(movie_url, params={"api_key": movie_key, "query": movie_name})
            data = response.json()["results"]
            return render(request, "search.html", {"results": data})
    else:
        form = MovieForm()
    return render(request, "search.html", {"form": form})
   
def display(request,movie_id):
        m_id = movie_id
        movie_api_url = f"https://api.themoviedb.org/3/movie/{m_id}"
        response = requests.get(movie_api_url,params={"api_key":movie_key,"language": "en-US"})
        data = response.json()
        reviews = Review.objects.filter(movie = data['id'])
        return render(request,"list.html",{"details":data,'review':reviews})

def display_home(request,movie_id):
        m_id = movie_id
        movie_api_url = f"https://api.themoviedb.org/3/movie/{m_id}"
        response = requests.get(movie_api_url,params={"api_key":movie_key,"language": "en-US"})
        data = response.json()
        reviews = Review.objects.filter(movie = data['id'])
        return render(request,"display.html",{"details":data,'reviews':reviews})

def delete(request,movie_id):
        movie = Movie.objects.get(pk = movie_id)
        movie.delete()
        return redirect('home')


def add(request,movie_id):
    m_id = movie_id
    movie_api_url = f"https://api.themoviedb.org/3/movie/{m_id}"
    response = requests.get(movie_api_url,params={"api_key":movie_key,"language": "en-US"})
    data = response.json()
    instance = Movie(
                id = data["id"],
                title = data["title"], 
                year=data["release_date"].split("-")[0],
                rating = data["popularity"],
                vote_avg = data["vote_average"],
                img_url = data["poster_path"],
                description=data["overview"],)
    if request.user.is_authenticated:
        instance.user = request.user
        instance.save()
   
    return redirect("category", movie_id=movie_id)

def add_cat(request,movie_id):
    if request.method == "POST":
        form = MovieTypeForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            instance = Movie.objects.get(id=movie_id)
            instance.category = category
            instance.save()
            return redirect('home')
    else:
        form = MovieTypeForm()
    return render(request, "add_cat.html", {"form": form})

def create_reviews(request,movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    if request.method=="POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.movie = movie
            new_review.save()
        return redirect('display_home', movie.id)
    else:
        form=ReviewForm()
        return render(request,"createreview.html",{"movie":movie,"form":form})
  




def update_reviews(request, review_id):
    review = get_object_or_404(Review,pk=review_id,user=request.user)
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'update.html', 
                      {'review': review,'form':form})
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('display_home', review.movie.id)
        except ValueError:
            return render(request, 'update.html',
             {'review': review,'form':form,'error':'Bad data in form'})
        
def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('display_home', review.movie.id)