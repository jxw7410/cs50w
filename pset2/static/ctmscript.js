window.mobilecheck = function() {
  var check = false;
  if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) )
  {
     check = true;
  }
  return check;
};




document.addEventListener("DOMContentLoaded", function()
{
       console.log("begin");
       Init_Config();

       if(window.mobilecheck())
       {
              document.getElementById('send-btn').innerHTML = "+";
              returningUserCheck();
              SendMessage();
       }
       else
       {
              returningUserCheck();
              WindowResizeEvent();
              var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
              SetCurrentChannel(socket);
              SendMessage();

       }
});


returningUserCheck = () =>
{
        if (!localStorage.getItem("username"))
              {
                     document.getElementById('main-container').setAttribute('class', 'blur');
                     document.getElementById('signup').style.display = "block";
                     document.querySelector('#setusername').onsubmit = () =>
                     {
                            document.getElementById('signup').style.display = "none";
                            let username = document.querySelector('#usernameinput').value;
                            localStorage.setItem("username", username);
                            document.querySelector("#username").innerHTML = username;
                            document.getElementById('main-container').setAttribute('class', null);
                            return false;
                     }
              }
              else
                     document.querySelector("#username").innerHTML = " " + localStorage.getItem("username");
}


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
              return false;
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

function SetCurrentChannel(socket)
{
       document.getElementById("create_chan_btn").addEventListener('click', function()
       {
              document.getElementById('create-ch').style.display = 'block';
              document.querySelector('#create-ch-form').onsubmit = () =>
              {
                     channel = document.getElementById('channel-name-input').value;
                     console.log(channel);
                     socket.emit('Create Channel', {"name" : channel});
                     socket.once('Initializing Channel', data=>
                     {
                            if(data["channel"])
                            {
                                   localStorage.setItem("currentChannel", data["channel"]);
                            }
                            else
                                   alert("Channel already exists");
                            document.getElementById('create-ch').style.display = 'none';
                     });

                     return false;
              }
              return false;
       });
}

function SendMessage()
{
       document.querySelector('#user-input-field').onsubmit = () =>
       {
              if (localStorage.getItem('currentChannel'))
              {
                     message = document.getElementById('message-input').value;
                     if (message)
                            alert(message);

                           document.getElementById('message-input').value = "";
              }
              else
                     alert("Not subscribed to a channel, please create, or join a channel.");

              return false;
       };
}

