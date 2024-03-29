import webbrowser
import os
import re
import requests


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>
    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        .hoverDiv {
            visibility: hidden;
            position: absolute;
            width: 400px;
            z-index: 999;
            border: 1px solid #DBDCDE;
            background: white;
            padding: 5px;
            border-radius: 5px;
        }
        .hoverDiv td:nth-child(2) {
            padding-left: 5px;
        }
        .hover td, .hover span {
            font-size: 8px;
        }
        .shadow{
        	-webkit-box-shadow: 0 10px 6px -6px #777;
        	   -moz-box-shadow: 0 10px 6px -6px #777;
        	        box-shadow: 0 10px 6px -6px #777;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });

          //To Show the Movie details on hover
          $('.movie-tile').hover( function(e) {
            var $hoverDiv = $(this).next();
            var $this = $(this);
            var initTop = e.pageY - $hoverDiv.height()/2;

            // Show the div and put it in the right place
            $hoverDiv.css({
                'visibility' : 'visible',
                'left' : ($this.offset().left + $this.outerWidth()) + 'px',
                'top' : initTop + 'px'
            });

            // Put the hoverDiv on the left if it's going off the page
            if($hoverDiv.width() + $hoverDiv.offset().left > $(window).width()){
                $hoverDiv.css('left', ($this.offset().left - $this.outerWidth()) + 'px')
            }

            // Move the div with mouse
            $this.mousemove(function(e) {
                var topPx = e.pageY - $hoverDiv.height()/2;
                $hoverDiv.css('top', topPx+ 'px');
            });
          }, function() {
            $hoverDiv = $(this).next();

            // When the mouse leaves the element, check if it's going to the hoverDiv or not
            if ($hoverDiv.is(':hover')){
                // Hide the hoverDiv when we leave it and unbind mousemove
                $hoverDiv.mouseleave( function() {
                    $hoverDiv.css('visibility', 'hidden').off('mousemove');
                });
            } else {
                // Hide the hoverDiv and unbind mousemove
                $hoverDiv.css('visibility', 'hidden').off('mousemove');
            }
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h2>{movie_title}</h2>
</div>
<div class="hoverDiv shadow">
    <table>
        <tr>
            <td>Director:</td>
            <td>{director}</td>
        </tr>
        <tr>
            <td>Plot:</td>
            <td>{Plot}</td>
        </tr>
        <tr>
            <td>Runtime:</td>
            <td>{runtime}</td>
        </tr>
        <tr>
            <td>Genre:</td>
            <td>{genre}</td>
        </tr>
        <tr>
            <td>Rated:</td>
            <td>{rated}</td>
        </tr>
        <tr>
            <td>Box Office:</td>
            <td>{box_office}</td>
        </tr>
    </table>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:

        movie = get_movies(movie)
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.movie_trailer_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.movie_trailer_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.movie_title,
            poster_image_url=movie.movie_image_url,
            trailer_youtube_id=trailer_youtube_id,
            director = movie.director,
            Plot = movie.plot,
            runtime = movie.runtime,
            genre = movie.genre,
            rated = movie.rated,
            box_office = movie.box_office


            

        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)


def get_movies(movie):

        p = {'t' : movie.movie_title, 'tomatoes' : 'true'}

        request = requests.get("http://www.omdbapi.com/?i=tt3896198&apikey=371b501c", params=p)
        movie_details = request.json()

        movie.movie_image_url = movie_details['Poster']
        movie.rated = movie_details["Rated"]
        movie.genre = movie_details["Genre"]
        movie.plot = movie_details["Plot"]
        movie.director = movie_details["Director"]
        movie.runtime = movie_details["Runtime"]
        movie.box_office = movie_details["BoxOffice"]

        return movie




