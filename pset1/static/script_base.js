var user;

//Main function
document.addEventListener("DOMContentLoaded", function()
{

              if (window.location.pathname == "/login")
              {
                     setNavActive("Login");
                     Login();
              }

              if (window.location.pathname == "/register")
              {
                     setNavActive("Register");
                     Register();
              }

              if (window.location.pathname == "/")
              {
                     var temporary_search_storage = {};
                     var book_search_res = "";
                     setNavActive("Search");
                     SearchBar(book_search_res, temporary_search_storage);

              }

              if(window.location.href.indexOf("bookinfo") > -1)
              {
                     setReviewButtons();
                     GetOtherReviews();
                     mReview('#review-button');
                     mReview('#edit-button');
                     DeleteReview();
                     CancelReview();
                     WordCount();
              }

              if (window.location.pathname == "/about")
              {
                     setNavActive("About");
              }

});


function Login()
{
       document.querySelector("#login").onsubmit = function()
       {
              let params =
              {
                     "username" : document.querySelector("#username").value,
                     "password" : document.querySelector("#password").value
              }
              RequestAjax("/login", params, function(response)
              {
                     if (response.request)
                     {
                            user = response.user;
                            window.location.href = "/"
                     }
                     else
                            alert("Username or Password is incorrect or does not exist.");
              });
              return false;
       }
}

function Register()
{
       document.querySelector("#register").onsubmit = function()
       {
              let params =
              {
                     "username" :  document.querySelector("#username").value,
                     "password" : document.querySelector("#password").value,
                     "passwordAgain" : document.querySelector("#password_again").value
              }
              RequestAjax("/register", params, function(response)
              {
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
              });
              return false;
       };
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function SearchBar(book_search_res, temporary_search_storage)
{
       document.querySelector("#search_bar").onsubmit = function()
       {

              book_search_res = document.querySelector("#book").value;
              let params =
              {
                     "book" : book_search_res
              };
              RequestAjax('/search', params, function(response)
              {
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
                            Pagination(book_search_res, temporary_search_storage);
                     }
                     else
                            alert("Item in search not found");
              });
              return false;
       };
}


function Pagination(book_search_res, temporary_search_storage)
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
                            let params =
                            {
                                   "book" : book_search_res,
                                   "page" : pageNum
                            };
                            RequestAjax('/selectpage', params, function(response)
                            {
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
                            });
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
       html = "<thead><tr><th>ISBN</th><th>TITLE</th><th>AUTHOR</th><th>YEAR</th></tr><tbody>";
       for (let index = 0; index < data.length; index++)
       {
              html += "<tr><td><a class='booklink' href='/bookinfo?book="  + data[index].isbn + "'>" + data[index].isbn + "</a></td>"
                     +"<td><a class='booklink' href='/bookinfo?book="  + data[index].isbn + "'>" + data[index].title + "</a></td>"
                     + "<td><a class='booklink' href='/bookinfo?book="  + data[index].isbn + "'>" + data[index].author + "</a></td>"
                     + "<td><a  class='booklink'href='/bookinfo?book="  + data[index].isbn + "'>" + data[index].year + "</a></td></tr>";
       }
       table.innerHTML += html + "</tbody>";
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
                     SubmitReview(bookInfoState.REVIEW);
              else if (htmlID == '#edit-button')
                     SubmitReview(bookInfoState.EDIT);
              else
                     SubmitReview(bookInfoState.ERROR);
       }
}

function SubmitReview(book_info_state)
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

              let params =
              {
                     "review" : document.querySelector('#review').value,
                     "stars" : parseFloat(document.querySelector('#stars').value),
                     "book" : ExtractUrl(),
                     "date" : new Date().toLocaleString().replace(",","").replace(/:.. /," ")
              }
              console.log(params["date"]);

              if (!params["stars"] || (params["stars"] > 5 || params["stars"] < 0))
              {
                     alert("Please submit a valid stars rating");
                     return false;
              }
              else if (params["review"].split(" ") == "")
              {
                     alert("Please fill in the review text field");
                     return false;
              }

              RequestAjax(url, params, function(response)
              {
                     if (response.request)
                     {
                                   DefaultState();
                                   DisplayReview(params["review"], params["stars"].toFixed(1), params["date"]);
                     }
                     else
                     {
                            alert("Oh? Something went wrong. Please submit an error report.");
                     }
              });
              return false;
       }
}

function CancelReview()
{
       document.querySelector('#review-cancel-btn').onclick = function()
       {
              DefaultState();
       }
}


function DeleteReview()
{
       document.querySelector('#delete-button').onclick = function()
       {
              if(confirm("Do you want to delete your review?"))
              {
                     let params =
                     {
                            "book" : ExtractUrl()
                     };
                     RequestAjax("/DeleteReview", params, function(response)
                     {
                            if(response.request)
                            {
                                   alert("Your review has been deleted");
                                   document.getElementById('user-rating').innerHTML =  "0.00 / 5.0";
                                   document.getElementById('user-date-post').innerHTML = "";
                                   document.getElementById("my_review_text").innerHTML = "";
                                   setReviewButtons();
                            }
                            else
                            {
                                   alert("Oh? Something went wrong. Please submit an error report.");
                            }
                     });
                     return false;
              }
       }
}

function GetOtherReviews()
{
       let param=
       {
              "book" : ExtractUrl()
       }
       RequestAjax('/GetFewReviews', param, function(response)
       {
          if(response.data)
          {
              renderUserReviews(response.data);
              jqueryinfscrollreviews(param);
          }
       });
}

function jqueryinfscrollreviews(param)
{
       $(window).scroll(function () {
            if ($(window).scrollTop() == $(document).height() - $(window).height())
            {
                     RequestAjax('/nextreview', param, function(response)
                     {
                            if(response.data)
                            {
                                   var html =    "<div class='review-box-padding'>"
                                                 +"<div class='user-review-ctn drop-shadow-style1'>"
                                                 +"<div class='review-span'><span><strong>" + response.data.user + "</strong>"
                                                 +"<span id='user-rating' class='review-star'>:  " + parseFloat(response.data.rating).toFixed(1)+ " / 5.0" + "</span>"
                                                 +"<span id='user-date-post'>" + response.data.date+ "</span> </span></div>"
                                                 +"<div> <p id='review-container' rows='4' cols='50'>"
                                                 +"<span id ='my_review_text' class='review-span'>" + response.data.review + "</span></p></div></div></div>";
                                   document.getElementById('other-user-reviews-ctn').innerHTML += html;
                            }

                     });
            }
       });
}

function renderUserReviews(data)
{
       var html =""
       for(let i = 0; i < data.length; i++)
       {
              html += "<div class='review-box-padding'>"
                     +"<div class='user-review-ctn drop-shadow-style1'>"
                     +"<div class='review-span'><span><strong>" + data[i].user + "</strong>"
                     +"<span id='user-rating' class='review-star'>:  " + parseFloat(data[i].rating).toFixed(1)+ " / 5.0" + "</span>"
                     +"<span id='user-date-post'>" + data[i].date+ "</span> </span></div>"
                     +"<div> <p id='review-container' rows='4' cols='50'>"
                     +"<span id ='my_review_text' class='review-span'>" + data[i].review + "</span></p></div></div></div>";
       }
       document.getElementById('other-user-reviews-ctn').innerHTML = html;
}


function DisplayReview(review, stars, date)
{
       document.getElementById('user-rating').innerHTML = stars + " / 5.0";
       document.getElementById('user-date-post').innerHTML = date;
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
       return false;
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
    return params[parse[0]];
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


function RequestAjax(link, params, callbackfunction, method='POST')
{
       const request = new XMLHttpRequest();
       request.open(method, link);
       request.onload = function()
       {
              const response = JSON.parse(request.responseText);
              callbackfunction(response);
       };
       const data = new FormData();
       keys = Object.keys(params)
       for (let i = 0; i < keys.length; i++)
       {
              data.append(keys[i], params[keys[i]]);
       }
       request.send(data);
}
