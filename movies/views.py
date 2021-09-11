from django.shortcuts import render
import requests, json
from movies.models import Movie, Configuration, Genre, Movie_Genre, Keyword, Movie_Keyword, Director, Actor, Movie_Director, Movie_Actor
from django.shortcuts import get_object_or_404

KEY="689125aca44db2c4475bb17c79fc8ff4"

# Create your views here.
def main(request):
    select = "now_playing" #now_playing, popular, top_rated
    url = "https://api.themoviedb.org/3/movie/{select}?api_key={key}&language=ko&region=KR&page=1".format(select=select, key=KEY)

    response = requests.get(url)
    send_list_len = 20
    np_movies = response.json()['results'][:send_list_len]

    bulk_list = []
    for row in np_movies:
        video_url = "https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={key}&language=ko".format(movie_id=row['id'], key=KEY)
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

    popular_movie_list = Movie.objects.order_by('-popularity')[:send_list_len]
    # popular_movie_list = bulk_list
    context = {
        # 'index_list': range(0, len(popular_movie_list))
        'popular_movie_list': popular_movie_list,
        'config': Configuration.objects.get(pk=1),
    }
    return render(request, 'movies/main.html', context)


def detail(request, movie_id):
    detail_url = "https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=ko&append_to_response=keywords,credits,similar".format(movie_id=movie_id, key=KEY)
    detail_response = requests.get(detail_url).json()
    
    selected_movie = Movie.objects.get(pk=movie_id)
    # 일단 필터로 movie id를 얻고. id가 일치하는 movie_genre값들을 얻고

    #역참조 후 정참조
    # m = Movie.objects.get(id=movie_id)
    # mg = m.movie_genre_set.all()  #_set에 오류남.
    # g = mg.genre.name

    
    # 되는 코드!!!!!!!!!!!!!
    # Movie_Genre에 id를 넣은 후, genre로 정참조함.
        # 그 때 정참조할 땐 참조할 모델명이 아닌 현재 모델의 외래키를 넣어야 함. genre_id로.
    # movie_genres = Movie_Genre.objects.filter(movie_id=movie_id)[0]
    # genre = movie_genres.genre_id.name
    genre_list = []
    movie_genres = Movie_Genre.objects.filter(movie_id=movie_id)
    for movie_genre in movie_genres:
        genre = movie_genre.genre_id.name
        genre_list.append(genre)

    keyword_list = []
    movie_keywords = Movie_Keyword.objects.filter(movie_id=movie_id)
    for movie_keyword in movie_keywords:
        keyword = movie_keyword.keyword_id.name
        keyword_list.append(keyword)
 

    director_list = []
    oDirector_list = []
    movie_directors = Movie_Director.objects.filter(movie_id=movie_id)
    for movie_director in movie_directors:
        director = movie_director.director_id.name
        original_name = movie_director.director_id.original_name
        director_list.append(director)
        oDirector_list.append(original_name)
    
    actor_list = []
    movie_actors = Movie_Actor.objects.filter(movie_id=movie_id)[:4]
    for movie_actor in movie_actors:
        actor = movie_actor.actor_id.name
        actor_list.append(actor)

    context = {
        'selected_movie': selected_movie,
        'config': Configuration.objects.get(pk=1),
        'genres' : genre_list,
        'keywords' : " / ".join(keyword_list),
        'directors' : ", ".join(director_list),
        'actors' : ", ".join(actor_list),
    }
    return render(request, 'movies/detail.html', context)

def learn(request):

    # # Genre 테이블 업데이트
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
                    Similar.objects.create(id=r['id']+row['id'] ,movie_id=Movie.objects.get(id=r['id']), recommand_id=row['id'])
                except:
                    pass

    context = { 'state': 'Done.' }
    return render(request, 'movies/learn.html', context)

def search(request):
    if 'input_movie' in request.GET:
        query = request.GET.get('input_movie')
        try:
            url = "https://api.themoviedb.org/3/search/movie?api_key={key}&language=ko-KR&page={p}&query={query}".format(key=KEY, query=query, p=1)
            response = requests.get(url).json()
            total_pages = response['total_pages']
            for page in range(2,total_pages):
                url = "https://api.themoviedb.org/3/search/movie?api_key={key}&language=ko-KR&page={p}&query={query}".format(key=KEY, query=query, p=page)
        except:
            pass
            
        context = {'what':'no'}
    return render(request, 'movies/main.html', context)