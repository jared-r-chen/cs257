/*
 * mockup3.js
 * Jared Chen & Aaron Scondorf, 14 November 2021
 */

 // Returns the base URL of the API, onto which endpoint
 // components can be appended.

 let global_search_string = '';

 function getAPIBaseURL() {
     let baseURL = window.location.protocol
                     + '//' + window.location.hostname
                     + ':' + window.location.port
                     + '/api';
     return baseURL;
 }

 function sort_results(){
   let search_string = global_search_string
   let sort_tag = document.getElementById('sort-tag').value;
   let sort_order = 'ASC'
   if (document.getElementById('order-check').checked){
     sort_order = 'DESC'
   }

   let url = getAPIBaseURL() + '/songs-like/' + search_string + '?key=' + sort_tag + '&order=' + sort_order;

   fetch(url, {method: 'get'})
   .then((response) => response.json())
   .then(function(songs) {
    //console.log(songs);

     let tableBody = '';
     tableBody += '<tr>'
                         + '<td>' + 'ID' + '</td>'
                         + '<td>' + 'Name' + '</td>'
                         + '<td>' + 'Artist' + '</td>'
                         + '<td>' + 'Genre(s)' + '</td>'
                         + '<td>' + 'Likeness Score' + '</td>'
                         + '</tr>\n';
     for (let i = 1; i < songs.length; i++) {
         //let song = songs[i];
         tableBody += '<tr>'
                         + '<td>' + songs[i].id + '</td>'
                         + '<td>' + songs[i].name + '</td>'
                         + '<td>' + songs[i].artist + '</td>'
                         + '<td>' + songs[i].genres_list + '</td>'
                         + '<td>' + songs[i].likeness + '</td>'
                         + '</tr>\n';
     }

     //document.getElementById("content").innerHTML = tableBody;
    let songsTable = document.getElementById('songs-table');
     if (songsTable) {
         songsTable.style.visibility = 'visible';
         songsTable.innerHTML = tableBody;
         //document.getElementById("content").style = "";
     }
      }
    )
    .catch(function(error) {
        console.log(error);
    });
 }


 function find_songs_like(){
   // event.preventDefault();
   // let url = getAPIBaseURL() + '/results/';
   let search_string = document.getElementById('search_item').value;
   global_search_string = search_string;

   //console.log(search_string);
   let url = getAPIBaseURL() + '/songs-like/' + search_string;

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
                         + '<td>' + 'Genre(s)' + '</td>'
                         + '<td>' + 'Likeness Score' + '</td>'
                         + '</tr>\n';
     for (let i = 1; i < songs.length; i++) {
         //let song = songs[i];
         tableBody += '<tr>'
                         + '<td>' + songs[i].id + '</td>'
                         + '<td>' + songs[i].name + '</td>'
                         + '<td>' + songs[i].artist + '</td>'
                         + '<td>' + songs[i].genres_list + '</td>'
                         + '<td>' + songs[i].likeness + '</td>'
                         + '</tr>\n';
     }
    let searchSongLable = document.getElementById('search-song-name');
    searchSongLable.innerHTML = "Song Used For Search: " + songs[0].name;
     // document.getElementById("content").innerHTML = tableBody;
    let songsTable = document.getElementById('songs-table');
    songsTable.innerHTML = '';
     if (songsTable) {
         songsTable.style.visibility = 'visible';
         songsTable.innerHTML = tableBody;
         //document.getElementById("content").style = "";
     }
      }
    )
    .catch(function(error) {
        console.log(error);
    });
 }
