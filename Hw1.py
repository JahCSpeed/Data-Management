import math
from collections import defaultdict
from collections import Counter
# You may not add any other imports
# For each function, replace "pass" with your code
# --- TASK 1: READING DATA ---
# 1.1
def printDict(dictionary):
    i = 0
    for key in dictionary:
        print(str(key) + ": "+ str(dictionary[key]))
    print("\n")
def returnGreatestAvg(d):
    list_t =[]
    top_genre = str()
    value = float()
    for genres in d:
        if float(d[genres]) > value:
            value = float(d[genres])
            top_genre = genres
    return top_genre
def convert_to_list(lst):
    temp = {}
    for i in range(0,len(lst)):
        temp += {lst[i][0]: lst[i][1]}
    return temp
def parseString(string):
    return string.split('|')
def read_ratings_data(f):
    rating_direct = defaultdict(list)
    with open(f) as file:
        for line in file.readlines():
            parsed_string = parseString(line.strip())
            for values in parsed_string[1:len(parsed_string)-1]:
                rating_direct[parsed_string[0]].append(float(values))
    file.close()
    return rating_direct
# 1.2
def read_movie_genre(f):
    movie_genere_direct = {}
    with open(f) as file:
        for line in file.readlines():
            parsed_string = parseString(line.strip())
            movie_genere_direct[parsed_string[2]] = (str(parsed_string[0]).strip())
    file.close()
    return movie_genere_direct
# --- TASK 2: PROCESSING DATA ---
# 2.1
def create_genre_dict(d):
    genere_direct = defaultdict(list)
    for k, v in sorted(d.items()):
            genere_direct[v].append(k)
    return genere_direct
# 2.2
def calculate_average_rating(d):
    rating_avg_direct = {}
    for k, v in sorted(d.items()):
        temp = 0
        for content in v:
            temp+= float(content)
        if len(v) == 0:
            rating_avg_direct[k] = (0)
        else:
            rating_avg_direct[k] = (float(temp/len(v)))
    return rating_avg_direct


# --- TASK 3: RECOMMENDATION ---
# 3.1
def get_popular_movies(d, n=10):
    temp = dict(sorted(d.items(), key=lambda item: item[1], reverse = True)[0:n])
    return (temp)
# 3.2
def filter_movies(d, thres_rating=3):
    filter_movies_direct = {}
    for key in d:
        if float(d[key]) >= thres_rating:
            filter_movies_direct[key] = (float(d[key]))
    return dict(sorted(filter_movies_direct.items(), key=lambda item: item[1], reverse = True))

# 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    temp_sub_genre_dict = genre_to_movies[str(genre)]
    unsorted_popular_movie_genre_direct = {}
    for entry in temp_sub_genre_dict:
        unsorted_popular_movie_genre_direct[entry] = (float(movie_to_average_rating[entry]))
    popular_movie_genre_direct = dict(sorted(unsorted_popular_movie_genre_direct.items(), key = lambda item: item[1], reverse = True)[0:n])
    return popular_movie_genre_direct
    
# 3.4
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    temp_genre_list = genre_to_movies[genre]
    final_genre_sum = 0
    for key in temp_genre_list:
        final_genre_sum += float(movie_to_average_rating[key])
    return final_genre_sum/len(temp_genre_list)
# 3.5
def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
    genre_rating_direct = {}
    for genre in genre_to_movies:
        genre_rating_direct[genre] = get_genre_rating(genre,genre_to_movies,movie_to_average_rating)
    genre_rating_direct = dict(sorted(genre_rating_direct.items(), key = lambda item: item[1], reverse = True)[0:n])
    return genre_rating_direct
# --- TASK 4: USER FOCUSED ---
# 4.1
def read_user_ratings(f):
    user_ratings_direct = defaultdict(list)
    with open(f) as file:
        for line in file.readlines():
            parsed_string = parseString(line.strip())
            if parsed_string:
                try:
                    user_ratings_direct[str(parsed_string[2])].append((parsed_string[0],float(parsed_string[1])))
                except:
                    continue
    file.close()
    return user_ratings_direct
# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    temp_user_movies_dict = defaultdict(list)
    genre_avg = {}
    for movie in user_to_movies[str(user_id)]:
            temp_user_movies_dict[movie_to_genre[movie[0]]].append((movie[0],float(movie[1])))
    for genre in temp_user_movies_dict:
        temp_sum = 0
        temp_len = 0
        for movie in temp_user_movies_dict[genre]:
            temp_sum += float(movie[1])
            temp_len += 1
        genre_avg[genre] = float((temp_sum/temp_len))
    return returnGreatestAvg(genre_avg)
# 4.3
def recommend_movies(user_id, user_to_movies, movie_to_genre, 
movie_to_average_rating):
    top_genre = get_user_genre(user_id,user_to_movies,movie_to_genre)
    movies_in_genre =  create_genre_dict(movie_to_genre)[str(top_genre)]
    movies_rated = {}
    final_recomended = {}
    for movie in movies_in_genre:
        for rated_movies in user_to_movies[str(user_id)]:
            if rated_movies[0] == movie:
                movies_rated[str(movie)] = float(rated_movies[1])
                break
    for movie in movies_in_genre:
        if movies_rated.get(movie) is None:
            final_recomended[movie]  = float(movie_to_average_rating[movie])        
    final_recomended = dict(sorted(final_recomended.items(), key = lambda item: item[1], reverse = True)[0:3])
    return final_recomended

    
# --- main function for your testing ---
def main():
    rating_direct = read_ratings_data('movieRatingSample.txt')
    #print(rating_direct)
    genre_direct = read_movie_genre('genreMovieSample.txt')
    #print(genre_direct)
    genre_to_movie = create_genre_dict(genre_direct)
    #print(genre_to_movie)
    rating_avg_direct = calculate_average_rating(rating_direct)
    #print(rating_avg_direct)
    user_rating = read_user_ratings('movieRatingSample.txt')
    #print(get_popular_movies(rating_avg_direct,3))
    #print(filter_movies(rating_avg_direct,3.5))
    #print(get_popular_in_genre("Comedy",genre_to_movie,rating_avg_direct,3))
    #print(get_genre_rating("Action",genre_to_movie,rating_avg_direct))
    #print(genre_popularity(genre_to_movie,rating_avg_direct))
    #print(user_rating)
    #print(get_user_genre(6,user_rating,genre_direct))
    #print(recommend_movies(6,user_rating,genre_direct,rating_avg_direct))
main()