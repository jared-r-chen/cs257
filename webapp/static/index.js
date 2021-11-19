/*
 * index.js
 * Jared Chen & Aaron Scondorf, 1 November 2021
 */

 // Returns the base URL of the API, onto which endpoint
 // components can be appended.

 // window.onload = initialize;
 //
 // function initialize() {
 //     let element = document.getElementById('sort-tag');
 //     if (element) {
 //         element.onchange = sort_results;
 //     }
 // }
 let global_search_string = '';
 let global_artist_string = '';
 let global_genre_string = '';

window.onload = initialize;



 function getAPIBaseURL() {
     let baseURL = window.location.protocol
                     + '//' + window.location.hostname
                     + ':' + window.location.port
                     + '/api';
     return baseURL;
 }

 function initialize(){
   let url = getAPIBaseURL() + '/load-genres';

   fetch(url, {method: 'get'})

   .then((response) => response.json())
   .then(function(genres) {
    //console.log(songs);
    let genre_HTML_string = "";
    console.log(genres);
     for (let i = 0; i < genres.length; i++) {
       current_genre = genres[i].genre;
        genre_HTML_string += '<option value="' + current_genre + '">' + current_genre +'</option>'

     }
     //document.getElementById("content").innerHTML = tableBody;
    let genre_drop_down = document.getElementById('search_genre');
      genre_drop_down.innerHTML = genre_HTML_string;
      }
    )
    .catch(function(error) {
        console.log(error);
    });
 }


 function add_genre(){
   let genre = document.getElementById('search_genre').value;

   if(!global_genre_string.includes(genre)){
     // console.log('should add item');
     genre_label = '<p class = "genre-item">' + genre + '</p>'
     let genre_block = document.getElementById('genre-block');
     genre_block.innerHTML += genre_label;
   }

   if(global_genre_string === ""){
     global_genre_string += genre;
   }
   else if(!global_genre_string.includes(genre)){
     global_genre_string += "," + genre;
   }
   // console.log(global_genre_string);
 }

 function clear_genre(){
     document.getElementById('genre-block').innerHTML = '';
     global_genre_string = '';
 }

 function sort_results(){
   let search_song = global_search_string
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
    //console.log(songs);

     let tableBody = '';
     tableBody += '<tr>'
                     + '<td>' + 'ID' + '</td>'
                     + '<td>' + 'Name' + '</td>'
                     + '<td>' + 'Artist' + '</td>'
                     + '<td>' + 'Highest Position' + '</td>'
                     + '<td>' + 'Streams' + '</td>'
                     + '<td>' + 'Genre(s)' + '</td>'
                     + '</tr>\n';
     for (let i = 0; i < songs.length; i++) {
         //let song = songs[i];
         tableBody += '<tr>'
                         + '<td>' + songs[i].id + '</td>'
                         + '<td>' + songs[i].name + '</td>'
                         + '<td>' + songs[i].artist + '</td>'
                         + '<td>' + songs[i].highest_pos + '</td>'
                         + '<td>' + songs[i].streams + '</td>'
                         + '<td>' + songs[i].genres_list + '</td>'
                         + '</tr>\n';
     }
     //document.getElementById("content").innerHTML = tableBody;
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



 function search_song(){
   // event.preventDefault();
   // let url = getAPIBaseURL() + '/results/';
   let search_song = document.getElementById('search_song').value;
   let search_artist = document.getElementById('search_artist').value;

   global_search_string = search_song;
   global_artist_string = search_artist;

   let url = getAPIBaseURL() + '/results' + '?song=' + search_song + '&artist='
   + search_artist + '&genres=' + global_genre_string;

   //document.getElementById('content').innerHTML = '';
   document.getElementById('sort-block').style.display = 'block';

   fetch(url, {method: 'get'})

   .then((response) => response.json())

   .then(function(songs) {
    //console.log(songs);

     let tableBody = '';
     tableBody += '<tr>'
                     + '<td>' + 'ID' + '</td>'
                     + '<td>' + 'Name' + '</td>'
                     + '<td>' + 'Artist' + '</td>'
                     + '<td>' + 'Highest Position' + '</td>'
                     + '<td>' + 'Streams' + '</td>'
                     + '<td>' + 'Genre(s)' + '</td>'
                     + '</tr>\n';
     for (let i = 0; i < songs.length; i++) {
         //let song = songs[i];
         tableBody += '<tr>'
                         + '<td>' + songs[i].id + '</td>'
                         + '<td>' + songs[i].name + '</td>'
                         + '<td>' + songs[i].artist + '</td>'
                         + '<td>' + songs[i].highest_pos + '</td>'
                         + '<td>' + songs[i].streams + '</td>'
                         + '<td>' + songs[i].genres_list + '</td>'
                         + '</tr>\n';
     }
     //document.getElementById("content").innerHTML = tableBody;
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
