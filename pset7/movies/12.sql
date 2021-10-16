select title from movies where id in (
select movie_id from stars join people on stars.person_id=people.id where people.name='Helena Bonham Carter')
and id in (
select movie_id from stars join people on stars.person_id=people.id where people.name='Johnny Depp');