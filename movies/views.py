from django.shortcuts import render, redirect
import requests, json
from movies.models import Movie, Configuration, Genre, Movie_Genre, Keyword, Movie_Keyword, Director, Actor, Movie_Director, Movie_Actor, Likes, Querylist
from django.shortcuts import get_object_or_404

from .forms import UserForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

# pip i pandas
# pip i sklearn
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from django.conf import settings

KEY = settings.TMDB_KEY

# Create your views here.
def main(request):
    select = "now_playing" #now_playing, popular, top_rated
    url = "https://api.themoviedb.org/3/movie/{select}?api_key={key}&language=ko&region=KR&page=1".format(select=select, key=KEY)

    response = requests.get(url)
    send_list_len = 30
    np_movies = response.json()['results'][:send_list_len]

    # try:
    movie_list = []
    
    try:
        for row in np_movies:
            video_url = "https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={key}&language=ko".format(movie_id=row['id'], key=KEY)
            video_response = requests.get(video_url).json()
            try: video_path = video_response['results'][-1]['key']
            except: pass

            bulk_list = []
            bulk_list.append(Movie(
            id = row['id'],
            title = row['title'],
            original_title = row['original_title'],
            popularity = row['popularity'],
            vote_average = row['vote_average'],
            release_date = row['release_date'],
            overview = row['overview'],
            backdrop_path = row['backdrop_path'],
            poster_path = row['poster_path'],
            video_path = video_path,
            ))
            try:
                Movie.objects.bulk_create(bulk_list)
            except: 
                Movie.objects.bulk_update(bulk_list, ['popularity'])
                pass

            movie_list.extend(bulk_list)
            bulk_list.clear()
    except:
        movie_list = Movie.objects.order_by('-popularity')[:send_list_len]
    
    # bulk_list.extend(best_movie_list)
    # popular_movie_list = bulk_list
    context = {
        # 'index_list': range(0, len(popular_movie_list))
        'popular_movie_list': movie_list,
        'config': Configuration.objects.get(pk=1),
    }
    return render(request, 'movies/main.html', context)


def detail(request, movie_id):
    # ?????? ????????? movie id??? ??????. id??? ???????????? movie_genre????????? ??????
    # ????????? ??? ??????????
    # m = Movie.objects.get(id=movie_id)
    # mg = m.movie_genre_set.all()  #_set??? ?????????.
    # g = mg.genre.name
    
    # Movie_Genre??? id??? ?????? ???, genre??? ????????????.
        # ??? ??? ???????????? ??? ????????? ???????????? ?????? ?????? ????????? ???????????? ????????? ???. genre_id???.
    # movie_genres = Movie_Genre.objects.filter(movie_id=movie_id)[0]
    # genre = movie_genres.genre_id.name

    detail_url = "https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=ko&append_to_response=keywords,credits,similar".format(movie_id=movie_id, key=KEY)
    detail_response = requests.get(detail_url).json()
    
    selected_movie = Movie.objects.get(pk=movie_id)

    genres = detail_response['genres']
    for genre in genres:
        try:
            Movie_Genre.objects.create(id=movie_id+genre['id'], movie_id=Movie.objects.get(id=movie_id), genre_id=Genre.objects.get(id=genre['id']))
        except: pass

    genre_list = []
    movie_genres = Movie_Genre.objects.filter(movie_id=movie_id)
    for movie_genre in movie_genres:
        genre = movie_genre.genre_id.name
        genre_list.append(genre)

    keywords = detail_response['keywords']['keywords']
    for keyword in keywords:
        try:
            Movie_Keyword.objects.create(id=10000*movie_id+keyword['id'], movie_id=Movie.objects.get(id=movie_id), keyword_id=Keyword.objects.get(id=keyword['id']))
        except: pass

    keyword_list = []
    movie_keywords = Movie_Keyword.objects.filter(movie_id=movie_id)
    for movie_keyword in movie_keywords:
        keyword = movie_keyword.keyword_id.name
        keyword_list.append(keyword)
 
    # director_list = []
    # oDirector_list = []
    # movie_directors = Movie_Director.objects.filter(movie_id=movie_id)
    # for movie_director in movie_directors:
    #     director = movie_director.director_id.name
    #     original_name = movie_director.director_id.original_name
    #     director_list.append(director)
    #     oDirector_list.append(original_name)

    credit = detail_response['credits']['cast'] 
    keyValList = ['known_for_department', "Acting"]
    actor = list(filter(lambda d: d['known_for_department'] in keyValList, credit))
    for a in actor:
        if (Actor.objects.filter(id=a['id'])):
            Actor.objects.filter(id=a['id']).update(name=a['name'], character=a['character'])
        else:
            Actor.objects.create(id=a['id'], name=a['name'], character=a['character'])

        try:
            Movie_Actor.objects.create(id=movie_id+a['id'], movie_id=Movie.objects.get(id=movie_id), actor_id=Actor.objects.get(id=a['id']))
        except:
            pass
    
    actor_list = []
    movie_actors = Movie_Actor.objects.filter(movie_id=movie_id)[:4]
    for movie_actor in movie_actors:
        actor = movie_actor.actor_id.name
        actor_list.append(actor)

    similars_list = []
    similar = detail_response['similar']['results']
    for row in similar:
        if not (Movie.objects.filter(id=row['id'])):
            similar_list = []
            similar_list.append(Movie(
            id = row['id'],
            title = row['title'],
            original_title = row['original_title'],
            popularity = row['popularity'],
            vote_average = row['vote_average'],
            release_date = row['release_date'],
            overview = row['overview'],
            backdrop_path = row['backdrop_path'],
            poster_path = row['poster_path'],
            # video_path = video_path,
            ))
            try:
                Movie.objects.bulk_create(similar_list)
            except:
                pass

            video_url = "https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={key}&language=KR".format(movie_id=row['id'], key=KEY)
            video_response = requests.get(video_url).json()
            try: video_path = video_response['results'][-1]['key']
            except: pass
            try:
                if (Movie.objects.get(id=row['id'])):
                    up = Movie.objects.get(id=row['id'])
                    up.video_path = video_path
                    up.save()
            except: pass

        try:
            similars_list.append(Movie.objects.get(id=row['id']))
        except: pass

    on_like='gray'
    try:
        Likes.objects.get(user_id=request.user, movie_id=movie_id)
        on_like='red'
    except:
        on_like='gray'

    context = {
        'selected_movie': selected_movie,
        'config': Configuration.objects.get(pk=1),
        'genres' : genre_list,
        'keywords' : " / ".join(keyword_list),
        # 'directors' : ", ".join(director_list),
        'actors' : ", ".join(actor_list),
        'similar_list' : similars_list[:60],
        'on_like' : on_like,
    }
    return render(request, 'movies/detail.html', context)

def search(request): 
    query = None

    if 'input_movie' in request.GET:
        # return render(request, 'movies/error.html', {
        #     'error_message': request.GET.get('input_movie')
        # })
        query = request.GET.get('input_movie')
        if not Querylist.objects.filter(query_name=query):
            url = "https://api.themoviedb.org/3/search/movie?api_key={key}&language=ko-KR&page={p}&query={query}".format(key=KEY, query=query, p=1)
            response = requests.get(url).json()
            total_pages = response['total_pages']

            movies = response['results']
            for movie in movies:
                try:
                    bulk_list = []  
                    bulk_list.append(Movie(
                    id = movie['id'],
                    title = movie['title'],
                    original_title = movie['original_title'],
                    popularity = movie['popularity'],
                    vote_average = movie['vote_average'],
                    release_date = movie['release_date'],
                    overview = movie['overview'],
                    backdrop_path = movie['backdrop_path'],
                    poster_path = movie['poster_path'],
                    # video_path = video_path,
                    ))
                    try:
                        Movie.objects.bulk_create(bulk_list)
                    except:
                        pass

                    video_url = "https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={key}&language=KR".format(movie_id=movie['id'], key=KEY)
                    video_response = requests.get(video_url).json()
                    try: video_path = video_response['results'][-1]['key']
                    except: pass

                    try:
                        if (Movie.objects.get(id=movie['id'])):
                            up = Movie.objects.get(id=movie['id'])
                            up.video_path = video_path
                            up.save()
                    except: pass
                except:pass


            for page in range(2,total_pages):
                #????????? ??????
                if page > 10: break

                url = "https://api.themoviedb.org/3/search/movie?api_key={key}&language=ko-KR&page={p}&query={query}".format(key=KEY, query=query, p=page)
                response = requests.get(url).json()
                movies = response['results']

                for movie in movies:
                    try:
                        bulk_list = []  
                        bulk_list.append(Movie(
                        id = movie['id'],
                        title = movie['title'],
                        original_title = movie['original_title'],
                        popularity = movie['popularity'],
                        vote_average = movie['vote_average'],
                        release_date = movie['release_date'],
                        overview = movie['overview'],
                        backdrop_path = movie['backdrop_path'],
                        poster_path = movie['poster_path'],
                        # video_path = video_path,
                        ))
                        try:
                            Movie.objects.bulk_create(bulk_list)
                        except:
                            pass
                            
                        video_url = "https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={key}&language=KR".format(movie_id=movie['id'], key=KEY)
                        video_response = requests.get(video_url).json()
                        try: video_path = video_response['results'][-1]['key']
                        except: pass

                        try:
                            if (Movie.objects.get(id=movie['id'])):
                                up = Movie.objects.get(id=movie['id'])
                                up.video_path = video_path
                                up.save()
                        except: pass
                    except: pass
            Querylist.objects.create(query_name=query)

    # popular_movie_list = Movie.objects.order_by('-popularity')[:send_list_len]
        popular_movie_list = Movie.objects.all().filter(title__icontains=query).order_by('-popularity')
        # popular_movie_list = bulk_list[:20]
        context = {
            # 'index_list': range(0, len(popular_movie_list))
            'popular_movie_list': popular_movie_list[:60],
            'config': Configuration.objects.get(pk=1),
        }
        return render(request, 'movies/main.html', context)

    else:
        return render(request, 'movies/error.html', {
            'error_message': "You didn't get a request"
        })
    
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('movies:signin')
        if not form.is_valid():
            form = UserForm()
            context = {'form':form, 'error':"?????? ?????? ???????????????."}
            return render(request, 'movies/signup.html', context)
    else:
        form = UserForm()
        return render(request, 'movies/signup.html', {'form':form})

def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('movies:main')
        if user is None:
            context = {'form':form, 'error':"???????????? ????????? ????????????."}
            return render(request, 'movies/signin.html', context)
    else:
        form = LoginForm()
        return render(request, 'movies/signin.html', {'form':form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('movies:main')

@login_required
def userinfo(request):
    user = User.objects.get(username=request.user)
    likes = Likes.objects.filter(user_id=user).values('movie_id')

    #????????????
    data = list(Movie_Genre.objects.all().values('movie_id', 'genre_id'))
    df = pd.DataFrame(data)
    df['genre_id'] = df['genre_id'].apply(str)
    df = df.groupby('movie_id')['genre_id'].apply(' '.join).reset_index()

    count_vector = CountVectorizer(ngram_range=(1,3))
    vector_genres = count_vector.fit_transform(df['genre_id'])

    cos_sim = cosine_similarity(vector_genres, vector_genres).argsort()[:, ::-1]

    like_movies = []
    recommand_movies = []
    for like in likes:
        movie = Movie.objects.get(id=like['movie_id'])
        like_movies.append(movie)

        target = df[ df['movie_id']==like['movie_id'] ].index.values
        reco_movies = cos_sim[target, :8].reshape(-1)
        reco_movies = reco_movies[reco_movies != target]
        reco_movies = df.iloc[reco_movies].values
        
        for reco in reco_movies:
            m = Movie.objects.get(id=reco[0])
            if m not in recommand_movies:
                recommand_movies.append(m)
    
    import random
    random.shuffle(recommand_movies)

    content = {'likes':like_movies, 'recos':recommand_movies[:30], 'config': Configuration.objects.get(pk=1)}
    return render(request, 'movies/userinfo.html', content )

# anaconda notebook ?????? ??????
    # def mgdf(request):
    #     data = list(Movie_Genre.objects.all().values('movie_id', 'genre_id'))
    #     df = pd.DataFrame(data)
    #     df['genre_id'] = df['genre_id'].apply(str)
    #     df = df.groupby('movie_id')['genre_id'].apply(' '.join).reset_index()

    #     from sklearn.feature_extraction.text import CountVectorizer
    #     count_vector = CountVectorizer(ngram_range=(1,3))
    #     vector_genres = count_vector.fit_transform(df['genre_id'])

    #     from sklearn.metrics.pairwise import cosine_similarity
    #     cos_sim = cosine_similarity(vector_genres, vector_genres).argsort()[:, ::-1]

    #     context = { 'state': 'Done.', 'df': cos_sim.shape }
    #     return render(request, 'movies/learn.html', context)


@login_required
def change_pw(request):
    context= {}
    if request.method == "POST":
        current_password = request.POST.get("origin_password")
        user = request.user
        if check_password(current_password, user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                login(request,user)
                return redirect("movies:userinfo")
            else:
                context.update({'error':"????????? ??????????????? ?????? ??????????????????."})
        else:
            context.update({'error':"?????? ??????????????? ???????????? ????????????."})
    return render(request, "movies/change_pw.html", context)

@login_required
def like(request, movie_id):
    user = User.objects.get(username=request.user)
    like_this = Likes.objects.filter(user_id=user, movie_id=movie_id)
    if like_this:
        like_this.delete()
    else:
        Likes.objects.create(user_id=user, movie_id=movie_id)
    # return render(request, 'movies/ex.html', {'user':user, 'movie_id':movie_id, 'on':on_like})
    return redirect('movies:detail', movie_id)





def learn(request):

    # # Genre ????????? ????????????
    # url = "https://api.themoviedb.org/3/genre/movie/list?api_key={key}&language=ko".format(key=KEY)
    # response = requests.get(url).json()
    # genres = response['genres']
    # for genre in genres:
    #     if (Genre.objects.filter(id=genre['id'])):
    #         Genre.objects.filter(id=genre['id']).update(name=genre['name'])
    #     else:
    #         Genre.objects.create(id=genre['id'], name=genre['name'])

    selects = ["now_playing", "popular", "top_rated"]
    for select in selects:
        # Movie_Genre Create
        url = "https://api.themoviedb.org/3/movie/{select}?api_key={key}&language=ko&region=KR&page=1".format(select=select, key=KEY)
        response = requests.get(url).json()['results']
        for r in response:
            genre = r['genre_ids']
            for g in genre:
                    try:
                        Movie_Genre.objects.create(id=r['id']+g, movie_id=Movie.objects.get(id=r['id']), genre_id=Genre.objects.get(id=g))
                    except:
                        pass

        # # Keyword create
        # url = "https://api.themoviedb.org/3/movie/{select}?api_key={key}&language=ko&region=KR&page=1".format(select=select, key=KEY)
        # response = requests.get(url).json()['results']
        for r in response:
            detail_url = "https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=ko&append_to_response=videos,images,keywords,credits,similar".format(movie_id=r['id'], key=KEY)
            detail_response = requests.get(detail_url).json()
            keyword = detail_response['keywords']['keywords']
            for k in keyword:
                # Keyword table
                if (Keyword.objects.filter(id=k['id'])):
                    Keyword.objects.filter(id=k['id']).update(name=k['name'])
                else:
                    Keyword.objects.create(id=k['id'], name=k['name'])
            #     # Movie_Keyword table
                    try:
                        Movie_Keyword.objects.create(id=r['id']+k['id'], movie_id=Movie.objects.get(id=r['id']), keyword_id=Keyword.objects.get(id=k['id']))
                    except:
                        pass

        # # Director, Actor
        # url = "https://api.themoviedb.org/3/movie/{select}?api_key={key}&language=ko&region=KR&page=1".format(select=select, key=KEY)
        # response = requests.get(url).json()['results']
        for r in response:
            detail_url = "https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=ko&append_to_response=videos,images,keywords,credits,similar".format(movie_id=r['id'], key=KEY)
            detail_response = requests.get(detail_url).json()
            credit = detail_response['credits']['cast']
            keyValList = ['known_for_department', "Directing"]
            director = list(filter(lambda d: d['known_for_department'] in keyValList, credit))
            for d in director:
                if (Director.objects.filter(id=d['id'])):
                    Director.objects.filter(id=d['id']).update(name=d['name'], original_name=d['original_name'])
                else:
                    Director.objects.create(id=d['id'], name=d['name'], original_name=d['original_name'])
                try:
                    Movie_Director.objects.create(id=r['id']+d['id'], movie_id=Movie.objects.get(id=r['id']), director_id=Director.objects.get(id=d['id']))
                except:
                    pass

            keyValList = ['known_for_department', "Acting"]
            actor = list(filter(lambda d: d['known_for_department'] in keyValList, credit))
            for a in actor:
                if (Actor.objects.filter(id=a['id'])):
                    Actor.objects.filter(id=a['id']).update(name=a['name'], character=a['character'])
                else:
                    Actor.objects.create(id=a['id'], name=a['name'], character=a['character'])

                try:
                    Movie_Actor.objects.create(id=r['id']+a['id'], movie_id=Movie.objects.get(id=r['id']), actor_id=Actor.objects.get(id=a['id']))
                except:
                    pass

        # #similar
        # url = "https://api.themoviedb.org/3/movie/{select}?api_key={key}&language=ko&region=KR&page=1".format(select=select, key=KEY)
        # response = requests.get(url).json()['results']
        for r in response:
            detail_url = "https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=ko&append_to_response=videos,images,keywords,credits,similar".format(movie_id=r['id'], key=KEY)
            detail_response = requests.get(detail_url).json()
            similar = detail_response['similar']['results']
            
            bulk_list = []
            for row in similar:
                video_url = "https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={key}&language=KR".format(movie_id=row['id'], key=KEY)
                video_response = requests.get(video_url).json()
                try: video_path = video_response['results'][-1]['key']
                except: pass

                bulk_list.append(Movie(
                id = row['id'],
                title = row['title'],
                original_title = row['original_title'],
                popularity = row['popularity'],
                vote_average = row['vote_average'],
                release_date = row['release_date'],
                overview = row['overview'],
                backdrop_path = row['backdrop_path'],
                poster_path = row['poster_path'],
                video_path = video_path,
                ))
            try:
                Movie.objects.bulk_create(bulk_list)
            except:
                pass            

            for row in similar:
                try:
                    Similar.objects.create(recommand_id=Movie.objects.get(id=r['id']), search_id=row['id'])
                except:
                    pass

    context = { 'state': 'Done.' }
    return render(request, 'movies/learn.html', context)
