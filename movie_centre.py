import media 
import fresh_tomatoes



dark_knight = media.Movie("The Dark Knight","https://www.youtube.com/watch?v=yrz8TakoaMo")

dunkirk = media.Movie("Dunkirk","https://www.youtube.com/watch?v=F-eMt3SrfFU")

skyfall = media.Movie("Skyfall","https://www.youtube.com/watch?v=sE7_WdlYGJI")

taken = media.Movie("Taken","https://www.youtube.com/watch?v=pbA-tBrHNfI")

joker = media.Movie("Joker","https://www.youtube.com/watch?v=zAGVQLHvwOY")

john_wick = media.Movie("John Wick","https://www.youtube.com/watch?v=2AUmvWm5ZDQ")

inception = media.Movie("Inception", "https://www.youtube.com/watch?v=d3A3-zSOBT4")

sicario = media.Movie("Sicario","https://www.youtube.com/watch?v=sR0SDT2GeFg")

taken = media.Movie("Taken","https://www.youtube.com/watch?v=pbA-tBrHNfI")

mission_impossible = media.Movie("Mission Impossible: Ghost Protocol","https://www.youtube.com/watch?v=YMOx_2kD_RY")


movies = [dark_knight,dunkirk,skyfall,taken,joker,john_wick,inception,sicario,mission_impossible]


fresh_tomatoes.open_movies_page(movies)