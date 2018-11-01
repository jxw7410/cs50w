//Main function
(function(){
       document.addEventListener("DOMContentLoaded", function()
       {
              if (window.location.pathname == "/login")
              {
                     setNavActive("Login");
                     LoginAjax();
              }

              if (window.location.pathname == "/register")
              {
                     setNavActive("Register");
                     RegisterAjax();
              }

              if (window.location.pathname == "/")
              {

                     var temporary_search_storage = {};
                     var book_search_res = "";
                     setNavActive("Search");
                     SearchBarAjax(book_search_res, temporary_search_storage);
                     PaginationAjax(book_search_res, temporary_search_storage);
                     Help();

              }

              if(/bookinfo/.test(window.location.href))
              {
                     setReviewButtons();
                     GetOtherReviewsAjax();
                     mReview('#review-button');
                     mReview('#edit-button');
                     DeleteReviewAjax();
                     CancelReview();
                     WordCount();
              }

              if (window.location.pathname == "/about")
              {
                     setNavActive("About");
              }


       });
})();


function LoginAjax()
{
       document.querySelector("#login").onsubmit = function(){
              const request = new XMLHttpRequest();
              const username = document.querySelector("#username").value;
              const password = document.querySelector("#password").value;
              request.open('POST', '/login');
              request.onload = function ()
              {
                     const response = JSON.parse(request.responseText)
                     if (response.request)
                            window.location.href = "/"
                     else
                            alert("Username or Password is incorrect or does not exist.");
                     };
                     const data = new FormData();
                     data.append("username", username);
                     data.append("password", password);
                     request.send(data);
                     return false;
              };
}


function RegisterAjax()
{
       document.querySelector("#register").onsubmit = function()
       {
              const request = new XMLHttpRequest();
              const username = document.querySelector("#username").value;
              const password = document.querySelector("#password").value;
              const passwordAgain = document.querySelector("#password_again").value;
              request.open('POST', '/register');
              request.onload = function ()
              {
                     const response = JSON.parse(request.responseText)
                     console.log(response);
                     if (response.request)
                            window.location.href = "/"
                     else
                     {
                            if (response.errorcode == 101)
                                   alert("Passwords Do not match");
                            else if (response.errorcode == 102)
                                   alert("Username already exists");
                            else
                                   alert("Unknown Error");
                     }
              };
              const data = new FormData();
              data.append("username", username);
              data.append("password", password);
              data.append("passwordAgain", passwordAgain)
              request.send(data);
              return false;
       };
}


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function SearchBarAjax(book_search_res, temporary_search_storage)
{
       document.querySelector("#search_bar").onsubmit = function()
       {
              const request = new XMLHttpRequest();
              book_search_res = document.querySelector("#book").value;
              request.open('POST', '/search');
              request.onload = function ()
              {
                     const response = JSON.parse(request.responseText)
                     if (response.data)
                     {
                            if (!isEmpty(temporary_search_storage))
                                   temporary_search_storage = {}
                            PrintSearchTable(response.data);
                            PrintPageList(response.page_list)
                            temporary_search_storage[response.page_list.current_page] =
                            {
                                   "data" : response.data,
                                   "page_list" : response.page_list
                            }
                     }
                     else
                            alert("Item in search not found");
              };
              const data = new FormData();
              data.append("book", book_search_res);
              request.send(data);
              return false;
       };
}



function PaginationAjax(book_search_res, temporary_search_storage)
{
       document.querySelector('#search_table_pagination').addEventListener('click', function(event)
       {
              if(event.target.className == "paginate")
              {
                     var pageNum = event.target.getAttribute("tag");
                     if (pageNum in temporary_search_storage)
                     {
                            PrintSearchTable(temporary_search_storage[pageNum].data);
                            PrintPageList(temporary_search_storage[pageNum].page_list);
                     }
                     else
                     {
                            const request = new XMLHttpRequest();
                            request.open('POST', '/selectpage');
                            request.onload = function()
                            {
                                   const response = JSON.parse(request.responseText)
                                   if(response.data)
                                   {
                                          PrintSearchTable(response.data);
                                          PrintPageList(response.page_list)
                                          temporary_search_storage[response.page_list.current_page] =
                                          {
                                                 "data" : response.data,
                                                 "page_list" : response.page_list
                                          };
                                   }
                                   else
                                          alert("error")
                            };
                            const data = new FormData();
                            data.append("book", book_search_res);
                            data.append("page", pageNum);
                            request.send(data);
                            return false;
                     }
              }
       });
}

function PrintSearchTable(data)
{
       table = document.getElementById('search_table_result');
       while(table.firstChild)
              table.removeChild(table.firstChild)
       html = "<thead><tr><th>ISBN</th><th>TITLE</th><th>AUTHOR</th><th>YEAR</th></tr><tbody></tbody>";
       tableRef = document.getElementById('search_table_result').getElementsByTagName('tbody')[0];
       for (let index = 0; index < data.length; index++)
       {
              html += "<tr><td><a href='/bookinfo?book="  + data[index].isbn + "'>" + data[index].isbn + "</a></td>"
                     +"<td>" + data[index].title + "</td>"
                     + "<td>" + data[index].author + "</td>"
                     + "<td>" + data[index].year + "</td></tr>";
       }
       table.innerHTML += html;
}

function PrintPageList(data)
{
       paginationElement = document.getElementById('search_table_pagination');
       while(paginationElement.firstChild)
              paginationElement.removeChild(paginationElement.firstChild);
       var html = "";
       for(let index = 0; index < data.pages.length; index++)
       {
              if (data.pages[index])
              {
                     if (data.pages[index] != data.current_page)
                            html += "<button class='paginate' type='button' tag='"+ data.pages[index] +"'>" + data.pages[index] + "</button>";
                     else
                            html += "<strong class='text_paginate'>" + data.pages[index] + "</strong>";
              }
              else
                     html+= "<span class=ellipsis></span>";
       }
       paginationElement.innerHTML += html;
}



function isEmpty(obj)
{
       for(var key in obj)
              if(obj.hasOwnProperty(key))
                     return false;
       return true;
}


function Help()
{
       document.querySelector('#help-btn').onclick = function()
       {
              alert("Please put in part of (or the entire) an isbn, author, or book name");
       }
}


/////////////////////////////////////////////////////////////////////////////////////////////////
function mReview(htmlID)
{
       document.querySelector(htmlID).onclick = function()
       {
              document.getElementById("submit_review_text").style.display = "block";
              document.getElementById("review-button").style.display = "None";
              document.getElementById("edit-button").style.display = "None";
              document.getElementById("delete-button").style.display = "None";

              if (htmlID == '#review-button')
                     SubmitReviewAjax(bookInfoState.REVIEW);
              else if (htmlID == '#edit-button')
                     SubmitReviewAjax(bookInfoState.EDIT);
              else
                     SubmitReviewAjax(bookInfoState.ERROR);
       }
}

function SubmitReviewAjax(book_info_state)
{
       document.querySelector('#reviewform').onsubmit = function()
       {
              var url;
              switch(book_info_state)
              {
                     case bookInfoState.REVIEW:
                            url = '/SubmitReview';
                            break;
                     case bookInfoState.EDIT:
                            url = '/EditReview';
                            break;
                     default:
                            url = '/Error';
                            break;
              }

              const review = document.querySelector('#review').value;
              const stars = parseFloat(document.querySelector('#stars').value);
              var isbn = ExtractUrl();
              if (!stars || (stars > 5 || stars < 0))
              {
                     alert("Please submit a valid stars rating");
                     return false;
              }
              else if(review.split(" ") == "")
              {
                     alert("Please fill in the review text field");
                     return false;
              }
              else
              {
                     const request = new XMLHttpRequest();
                     request.open('POST', url);
                     request.onload = function()
                     {
                            const response = JSON.parse(request.responseText);
                            if (response.request)
                            {
                                   DefaultState();
                                   DisplayReview(review, stars.toFixed(2));
                            }
                            else
                            {
                                   alert("Oh? Something went wrong. Please submit an error report.");
                            }
                     }
                     const data = new FormData();
                     data.append("review", review);
                     data.append("stars", stars);
                     data.append("book", isbn["book"]);
                     request.send(data);
                     return false;
              }
       }
}

function CancelReview()
{
       document.querySelector('#review-cancel-btn').onclick = function()
       {
              DefaultState();
       }
}


function DeleteReviewAjax()
{
       document.querySelector('#delete-button').onclick = function()
       {
              if(confirm("Do you want to delete your review?"))
              {
                     var isbn = ExtractUrl();
                     const request = new XMLHttpRequest();
                     request.open('POST', '/DeleteReview');
                     request.onload = function()
                     {
                            const response = JSON.parse(request.responseText)
                            if(response.request)
                            {
                                   alert("Your review has been deleted");
                                   document.getElementById('review-star').innerHTML = "";
                                   document.getElementById("my_review_text").innerHTML = "";
                                   setReviewButtons();
                            }
                            else
                            {
                                   alert("Oh? Something went wrong. Please submit an error report.");
                            }
                     }
                     const data= new FormData();
                     data.append("book", isbn["book"]);
                     request.send(data);
                     return false;
              }

       }
}


function GetOtherReviewsAjax()
{
       var isbn = ExtractUrl();
       const request = new XMLHttpRequest();
       request.open('POST', '/GetFewReviews');
       request.onload = function()
       {
              const response = JSON.parse(request.responseText);
              console.log(response);
       }
       const data = new FormData();
       data.append("book", isbn["book"]);
       request.send(data);
       return false;
}

function renderUserReviews(data)
{
       var html =""
       for(let i = 0; i < data.length; i++)
       {

       }
}


function DisplayReview(review, stars)
{
       document.querySelector("#review-star").innerHTML = stars + " / 5.0";
       document.querySelector('#my_review_text').innerHTML = review;
       setReviewButtons();
}


function DefaultState()
{
       document.getElementById("submit_review_text").style.display = "None";
       document.getElementById("review-button").style.display = "inline";
       document.getElementById("edit-button").style.display = "inline";
       document.getElementById("delete-button").style.display = "inline";
}


function setReviewButtons()
{

       if(document.querySelector("#my_review_text").innerHTML.split(' ') == "")
       {
              document.querySelector('#review-button').classList.remove("disabled");
              document.querySelector("#edit-button").className += " disabled";
              document.querySelector("#delete-button").className += " disabled";
       }
       else
       {
              document.querySelector("#review-button").className += " disabled";
              document.querySelector("#edit-button").classList.remove("disabled");
              document.querySelector("#delete-button").classList.remove("disabled");
       }

}


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function setNavActive(navtag)
{
       res = document.getElementsByClassName("nav-item");
              for(var i = 0; i < res.length ; i++)
              {
                     if (res[i].getAttribute("tag") == navtag)
                            res[i].className += " active";
              }
}


//function from stackover flow to extra URL
function ExtractUrl(url = window.location.search.substr(1).split('&'))
{
    if (url == "") return {};
    var params = {};
    for (var i = 0; i < url.length; ++i)
    {
        var parse=url[i].split('=', 2);
        if (parse.length == 1)
            params[parse[0]] = "";
        else
            params[parse[0]] = decodeURIComponent(parse[1].replace(/\+/g, " "));
    }
    return params;
}

function WordCount()
{
       document.querySelector('#review').onkeyup = function()
       {
              const wordLimit = 4000;
              var wordCount = document.querySelector('#review').value;
              if(parseInt(wordLimit))
              {
                     document.querySelector('#word-limit').innerHTML = 4000 - wordCount.length;
              }

       }
}


//Enumerable
const bookInfoState ={
              REVIEW: 'Review',
              EDIT: 'Edit',
              ERROR: 'Error'
};
