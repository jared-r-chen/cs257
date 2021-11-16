/*
 * index.js
 * Jared Chen & Aaron Scondorf, 1 November 2021
 */

 // Returns the base URL of the API, onto which endpoint
 // components can be appended.
 function getAPIBaseURL() {
     let baseURL = window.location.protocol
                     + '//' + window.location.hostname
                     + ':' + window.location.port
                     + '/api';
     return baseURL;
 }


 function search_song(){
   // event.preventDefault();
   // let url = getAPIBaseURL() + '/results/';
   let search_string = document.getElementById('search_item').value;
   //console.log(search_string);
   let url = getAPIBaseURL() + '/results/' + search_string;

   document.getElementById('content').innerHTML = '';
   document.getElementById('sort-block').style.display = 'block';

   fetch(url, {method: 'get'})

   .then((response) => response.json())

   .then(function(songs) {
    //console.log(songs);

     let tableBody = '';
     for (let i = 0; i < songs.length; i++) {
         //let song = songs[i];
         tableBody += '<tr>'
                         + '<td>' + songs[i].id + '</td>'
                         + '<td>' + songs[i].name + '</td>'
                         + '<td>' + songs[i].artist + '</td>'
                         + '<td>' + songs[i].highest_pos + '</td>'
                         + '<td>' + songs[i].streams + '</td>'
                         + '</tr>\n';
     }
     //document.getElementById("content").innerHTML = tableBody;
    let songsTable = document.getElementById('songs_table');
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