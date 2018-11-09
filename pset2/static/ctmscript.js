
document.addEventListener("DOMContentLoaded", function()
{
       Init_Config();

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

       WindowResizeEvent();
       SendMessage()

       //genertic protocol to set up a socket
       var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

        //function
       socket.on('connect', () => {
       //Do something booaaah
       });
});

function Init_Config()
{
       windowheight = documentHeight();
       navbarheight= document.getElementById('top-nav').offsetHeight;
       messagebarheight = document.getElementById('bottom-div').offsetHeight;
       height = windowheight - (navbarheight + messagebarheight);
       document.getElementById('chat-display-area').style.marginTop = String(navbarheight)+"px";
       document.getElementById('chat-display-area').style.height = String(height)+"px";
}

function WindowResizeEvent()
{
       window.addEventListener('resize', ()=>
       {
              windowheight = documentHeight();
              navbarheight= document.getElementById('top-nav').offsetHeight;
              messagebarheight = document.getElementById('bottom-div').offsetHeight;
              height = windowheight - (navbarheight + messagebarheight);
              document.getElementById('chat-display-area').style.marginTop = String(navbarheight)+"px";
              document.getElementById('chat-display-area').style.height = String(height)+"px";
       });
}

function documentHeight() {
    return Math.max(
        document.documentElement.clientHeight,
        document.body.scrollHeight,
        document.documentElement.scrollHeight,
        document.body.offsetHeight,
        document.documentElement.offsetHeight
    );
}

function SendMessage()
{
       document.querySelector('#user-input-field').onsubmit = () =>
       {
              message = document.getElementById('message-input').value;
              if (message)
                     alert(message);
                     document.getElementById('message-input').value = "";
              return false;
       };
}

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
