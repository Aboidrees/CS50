select avg(ratings.rating) from movies join ratings on movies.id=ratings.movie_id where year=2012;