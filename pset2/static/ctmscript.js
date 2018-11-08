document.addEventListener("DOMContentLoaded", function()
{

       if (!localStorage.getItem("username"))
       {
              document.getElementById('main-container').setAttribute('class', 'blur');
              document.getElementById('overlay').style.display = "block";
              document.querySelector('#setusername').onsubmit = () =>
              {
                     document.getElementById('usernamepopup').style.display = "none";
                     let username = document.querySelector('#usernameinput').value;
                     localStorage.setItem("username", username);
                     document.querySelector("#username").innerHTML = username;
                     document.getElementById('main-container').setAttribute('class', null);
              }
       }
       else
              document.querySelector("#username").innerHTML = " " + localStorage.getItem("username");

       //genertic protocol to set up a socket
       var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

        //function
       socket.on('connect', () => {
       //Do something booaaah
       });
});



//Ajax
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
