/*
 * mockup3.js
 * Jared Chen & Aaron Scondorf, 14 November 2021
 */



 let global_search_string = '';

 // Returns the base URL of the API, onto which endpoint
 // components can be appended.
 function getAPIBaseURL() {
     let baseURL = window.location.protocol
                     + '//' + window.location.hostname
                     + ':' + window.location.port
                     + '/api';
     return baseURL;
 }

/*
 * Sorts the results of the find-songs-like function
 */
 function sort_results(){
   let search_string = global_search_string
   //sets values for sorting parameters
   let sort_tag = document.getElementById('sort-tag').value;
   let sort_order = 'ASC'
   if (document.getElementById('order-check').checked){
     sort_order = 'DESC'
   }

   let url = getAPIBaseURL() + '/songs-like/' + search_string + '?key=' + sort_tag + '&order=' + sort_order;

   fetch(url, {method: 'get'})
   .then((response) => response.json())
   .then(function(songs) {

     //generate table
     let tableBody = '';
     tableBody += '<tr>'
                         + '<td>' + 'Name' + '</td>'
                         + '<td>' + 'Artist' + '</td>'
                         + '<td>' + 'Genre(s)' + '</td>'
                         + '<td>' + 'Likeness Score' + '</td>'
                         + '</tr>\n';
     for (let i = 1; i < songs.length; i++) {
         tableBody += '<tr>'
                         + '<td>' + songs[i].name + '</td>'
                         + '<td>' + songs[i].artist + '</td>'
                         + '<td>' + songs[i].genres_list + '</td>'
                         + '<td>' + songs[i].likeness + '</td>'
                         + '</tr>\n';
     }

     //display table
    let songsTable = document.getElementById('songs-table');
     if (songsTable) {
         songsTable.style.visibility = 'visible';
         songsTable.innerHTML = tableBody;
     }
      }
    )
    .catch(function(error) {
        console.log(error);
    });
 }

/*
 *This function finds songs like a given search phrase parameter.
 */
 function find_songs_like(){
   //generate url for api
   let search_string = document.getElementById('search_item').value;
   let sort_tag = document.getElementById('sort-tag').value = 'likeness';
   global_search_string = search_string;

   let url = getAPIBaseURL() + '/songs-like/' + search_string;

   document.getElementById('sort-block').style.display = 'block';

   fetch(url, {method: 'get'})
   .then((response) => response.json())
   .then(function(songs) {

     //generate table
     let tableBody = '';
     tableBody += '<tr>'
                         + '<td>' + 'Name' + '</td>'
                         + '<td>' + 'Artist' + '</td>'
                         + '<td>' + 'Genre(s)' + '</td>'
                         + '<td>' + 'Likeness Score' + '</td>'
                         + '</tr>\n';
     for (let i = 1; i < songs.length; i++) {
         tableBody += '<tr>'
                         + '<td>' + songs[i].name + '</td>'
                         + '<td>' + songs[i].artist + '</td>'
                         + '<td>' + songs[i].genres_list + '</td>'
                         + '<td>' + songs[i].likeness + '</td>'
                         + '</tr>\n';
     }

     //Create lable to display song used for search
    let searchSongLable = document.getElementById('search-song-name');
    searchSongLable.innerHTML = "Song Used For Search: " + songs[0].name + " by " + songs[0].artist;

    //display table
    let songsTable = document.getElementById('songs-table');
    songsTable.innerHTML = '';
     if (songsTable) {
         songsTable.style.visibility = 'visible';
         songsTable.innerHTML = tableBody;
     }
      }
    )
    .catch(function(error) {
        console.log(error);
    });
 }
