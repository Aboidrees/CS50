select people.name from stars join movies,people on stars.person_id=people.id and stars.movie_id=movies.id where title='Toy Story';