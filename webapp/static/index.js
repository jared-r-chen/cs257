/*
 * index.js
 * Jared Chen & Aaron Scondorf, 1 November 2021
 */

//global variables
 let global_search_string = '';
 let global_artist_string = '';
 let global_genre_string = '';

window.onload = initialize;

/*
 * This function get the base url thats used for other functions
 */
 function getAPIBaseURL() {
     let baseURL = window.location.protocol
                     + '//' + window.location.hostname
                     + ':' + window.location.port
                     + '/api';
     return baseURL;
 }

/*
 * This function loads genres into drop down menu
 */
 function initialize(){
   let url = getAPIBaseURL() + '/load-genres';

   fetch(url, {method: 'get'})

   .then((response) => response.json())
   .then(function(genres) {

    let genre_HTML_string = "";
    console.log(genres);
    //This for loop adds all genres to a string that can be injected into the HTML
     for (let i = 0; i < genres.length; i++) {
       current_genre = genres[i].genre;
        genre_HTML_string += '<option value="' + current_genre + '">' + current_genre +'</option>'

     }
     //inject HTML
    let genre_drop_down = document.getElementById('search_genre');
      genre_drop_down.innerHTML = genre_HTML_string;
      }
    )
    .catch(function(error) {
        console.log(error);
    });
 }

 /*
  * This function runs when a new genre is added. This function injects a text box
  * into the html so the user knows what genres will be searched for. Additionally,
  * the global_genre_string will have the genre added to it so it can be passed into
  * the api as a single variable.
  */
 function add_genre(){

   let genre = document.getElementById('search_genre').value;
   //This if statement prevents the same genre from being added twice
   if(!global_genre_string.includes(genre)){
     genre_label = '<p class = "genre-item">' + genre + '</p>'
     let genre_block = document.getElementById('genre-block');
     genre_block.innerHTML += genre_label;
   }
   //base case if global_genre_string is empty
   if(global_genre_string === ""){
     global_genre_string += genre;
   }
   else if(!global_genre_string.includes(genre)){
     global_genre_string += "," + genre;
   }
 }

/*
 * Clears genre list
 */
 function clear_genre(){
     document.getElementById('genre-block').innerHTML = '';
     global_genre_string = '';
 }

 /*
  * Very similar to search_song function. This function takes in sort variables
  * in addition to search varibles in order to call the api and the same list but sorted
  * in a different manner.
  */
 function sort_results(){
   let search_song = global_search_string
   //checking sort variables to see what to sort by
   let sort_tag = document.getElementById('sort-tag').value;
   let sort_order = 'ASC'
   if (document.getElementById('order-check').checked){
     sort_order = 'DESC'
   }

   let url = getAPIBaseURL() + '/results' + '?song=' + search_song + '&artist='
   + global_artist_string + '&genres=' + global_genre_string + '&key=' + sort_tag + '&order=' + sort_order;


   fetch(url, {method: 'get'})
   .then((response) => response.json())
   .then(function(songs) {

     let tableBody = '';
     tableBody += '<tr>'
                     + '<td>' + 'Name' + '</td>'
                     + '<td>' + 'Artist' + '</td>'
                     + '<td>' + 'Highest Position' + '</td>'
                     + '<td>' + 'Streams' + '</td>'
                     + '<td>' + 'Genre(s)' + '</td>'
                     + '</tr>\n';
     for (let i = 0; i < songs.length; i++) {
         tableBody += '<tr>'
                         + '<td>' + songs[i].name + '</td>'
                         + '<td>' + songs[i].artist + '</td>'
                         + '<td>' + songs[i].highest_pos + '</td>'
                         + '<td>' + songs[i].streams + '</td>'
                         + '<td>' + songs[i].genres_list + '</td>'
                         + '</tr>\n';
     }
    let songsTable = document.getElementById('songs-table');
    songsTable.innerHTML = '';
     if (songsTable) {
         songsTable.style.visibility = 'visible';
         songsTable.innerHTML = tableBody;
         document.getElementById("content").style = "";
       }
      }
    )
    .catch(function(error) {
        console.log(error);
    });
 }


 /*
  * This function takes in user inputted parameters and puts a results list
  * onto the screen.
  */
 function search_song(){
   /*these two lines will reset the sorting tools if the submit search button is
   pressed when no new values have been inputted.
   */
   document.getElementById('sort-tag').value = "name";
   document.getElementById('order-check').checked = false;

   let search_song = document.getElementById('search_song').value;
   let search_artist = document.getElementById('search_artist').value;

   global_search_string = search_song;
   global_artist_string = search_artist;

   let url = getAPIBaseURL() + '/results' + '?song=' + search_song + '&artist='
   + search_artist + '&genres=' + global_genre_string;

   document.getElementById('sort-block').style.display = 'block';

   fetch(url, {method: 'get'})
   .then((response) => response.json())
   .then(function(songs) {

     let tableBody = '';
     tableBody += '<tr>'
                     + '<td>' + 'Name' + '</td>'
                     + '<td>' + 'Artist' + '</td>'
                     + '<td>' + 'Highest Position' + '</td>'
                     + '<td>' + 'Streams' + '</td>'
                     + '<td>' + 'Genre(s)' + '</td>'
                     + '</tr>\n';
     for (let i = 0; i < songs.length; i++) {
         tableBody += '<tr>'
                         + '<td>' + songs[i].name + '</td>'
                         + '<td>' + songs[i].artist + '</td>'
                         + '<td>' + songs[i].highest_pos + '</td>'
                         + '<td>' + songs[i].streams + '</td>'
                         + '<td>' + songs[i].genres_list + '</td>'
                         + '</tr>\n';
     }
    let songsTable = document.getElementById('songs-table');
     if (songsTable) {
         songsTable.style.visibility = 'visible';
         songsTable.innerHTML = tableBody;
         document.getElementById("content").style = "";
       }
      }
    )
    .catch(function(error) {
        console.log(error);
    });
 }
