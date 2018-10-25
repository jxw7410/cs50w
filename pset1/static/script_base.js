//Not using local storage because it's overkill for what is intended
let temporary_search_storage = {};

//Init Function
(function(){
       document.addEventListener("DOMContentLoaded", function(){
              if (window.location.pathname == "/login")
              {
                     setNavActive("Login");
                     LoginAsync();
              }
              if (window.location.pathname == "/")
              {
                     setNavActive("Search");
                     SearchBarAsync();
                     PaginationAsync();

              }
              if (window.location.pathname == "/register")
              {
                     setNavActive("Register");
                     RegisterAsync();
              }

              if (window.location.pathname == "/about")
              {
                     setNavActive("About");
              }

              if(/bookinfo/.test(window.location.href))
              {
                     setReviewButtons();
                     CreateReview();
                     CancelReview();
              }

       });
})();


function CreateReview()
{
       document.querySelector('#review-button').onclick = function()
       {
              document.getElementById("submit_review_text").style.display = "block";
              document.getElementById("review-button").style.display = "None";
              document.getElementById("edit-button").style.display = "None";
              document.getElementById("delete-button").style.display = "None";
       }
       SubmitReviewAsync();
}

function CancelReview()
{
       document.querySelector('#review-cancel-btn').onclick = function()
       {
              document.getElementById("submit_review_text").style.display = "None";
              document.getElementById("review-button").style.display = "inline";
              document.getElementById("edit-button").style.display = "inline";
              document.getElementById("delete-button").style.display = "inline";
       }
}

function SubmitReviewAsync()
{

}

function RegisterAsync()
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
                     if (response.request)
                            window.location.href = "/"
                     else
                     {
                            if (data.errorcode == 101)
                                   alert("Passwords Do not match");
                            else if (data.errorcode == 102)
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

function PaginationAsync()
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
                                   if(response.request)
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
                            data.append("book", book);
                            data.append("page", pageNum);
                            request.send(data);
                            return false;
                     }
              }
       });
}

function SearchBarAsync()
{
       var book = "";
       document.querySelector("#search_bar").onsubmit = function()
       {
              const request = new XMLHttpRequest();
              book = document.querySelector("#book").value;
              request.open('POST', '/search');
              request.onload = function ()
              {
                     const response = JSON.parse(request.responseText)
                     console.log(response)
                     if (response.request)
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
              data.append("book", book);
              request.send(data);
              return false;
       };
}

function LoginAsync()
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

function setReviewButtons()
{
       if(document.querySelector("#my_review_text").value == null)
              {
                     document.querySelector("#edit-button").className += " disabled";
                     document.querySelector("#delete-button").className += " disabled";
              }
              else
              {
                     document.querySelector("#review-button").className += " disabled";
              }

}

//display search table, no pagination
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


function setNavActive(navtag)
{
       res = document.getElementsByClassName("nav-item");
              for(var i = 0; i < res.length ; i++)
              {
                     if (res[i].getAttribute("tag") == navtag)
                            res[i].className += " active";
              }
}


