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
       var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
       if(window.mobilecheck())
       {
              document.getElementById('send-btn').innerHTML = "+";
              returningUserCheck();
              SendMessage(socket);
              ReceivedMessage(socket);
              SetCurrentChannel(socket);
              JoinChannel(socket);
              popupcancel(socket);
       }
       else
       {
              returningUserCheck();
              WindowResizeEvent();
              SetCurrentChannel(socket);
              JoinChannel(socket)
              SendMessage(socket);
              ReceivedMessage(socket);
              popupcancel();

       }
});


popupcancel = () =>
{
       items = document.getElementsByClassName("popup-cancel-btn");
       for(var i = 0; i < items.length; i++)
       {
              items[i].addEventListener('click', () =>
              {
                     console.log("cancel button pressed");
                     popupcancelfunc();
                     return false;
              });
       }
}

popupcancelfunc = () =>
{
       items = document.getElementsByClassName('overlay');
       for(var i = 0; i < items.length; i++)
       {
              items[i].style.display = "none";
       }
}


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


Init_Config = () =>
{
       windowheight = documentHeight();
       navbarheight= document.getElementById('top-nav').offsetHeight;
       messagebarheight = document.getElementById('bottom-div').offsetHeight;
       height = windowheight - (navbarheight + messagebarheight);
       document.getElementById('chat-display-area').style.marginTop = String(navbarheight)+"px";
       document.getElementById('chat-display-area').style.height = String(height)+"px";
}

WindowResizeEvent = () =>
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

documentHeight = () =>
{
    return Math.max(
        document.documentElement.clientHeight,
        document.body.scrollHeight,
        document.documentElement.scrollHeight,
        document.body.offsetHeight,
        document.documentElement.offsetHeight
    );
}

SetCurrentChannel = (socket) =>
{
       document.getElementById("create_chan_btn").addEventListener('click', function()
       {
              popupcancelfunc();
              document.getElementById('create-ch').style.display = 'block';
              document.querySelector('#create-ch-form').onsubmit = () =>
              {
                     channel = document.getElementById('channel-name-input').value;
                     socket.emit('Create Channel', {"channel" : channel});
                     socket.once('Initializing Channel', data=>
                     {
                            if(data["channel"])
                            {
                                   localStorage.setItem("currentChannel", data["channel"]);
                                   document.getElementById('chat-name').innerHTML = "Chatroom: " + channel;
                            }
                            else
                                   alert("Channel already exist.");
                            document.getElementById('create-ch').style.display = 'none';
                     });

                     return false;
              }
              return false;
       });
}

JoinChannel = (socket) =>
{

       document.getElementById('join_chan_btn').addEventListener('click', () =>
       {
              popupcancelfunc();
              document.getElementById('join-ch').style.display = 'block';
              document.querySelector('#join-ch-form').onsubmit = () =>
              {
                     channel = document.getElementById('join-input').value;
                     socket.emit('Join Channel', {"channel" : channel});
                     socket.once('Joining Channel', data =>
                     {
                            if(data["request"])
                            {
                                   localStorage.setItem("currentChannel", channel);
                                   document.getElementById('chat-name').innerHTML = "Chatroom: " + channel;
                            }
                            else
                                   alert("Channel does not exist.");
                            document.getElementById('join-ch').style.display = 'none';
                     });
                     return false;
              }
              return false;
       });
}

SendMessage = (socket) =>
{
       document.querySelector('#user-input-field').onsubmit = () =>
       {
              channel = localStorage.getItem('currentChannel');
              if (channel)
              {
                     message = document.getElementById('message-input').value;
                     socket.emit("Send Message", {"channel" : channel, "message" : message});

              }
              else
                     alert("Not subscribed to a channel, please create, or join a channel.");

              return false;
       };
}

ReceivedMessage = (socket) =>
{

       socket.on('Message Added', data =>
       {
              console.log(data)
              if(data["confirm"])
              {
                     html = "<div class='chatbubble'>" + data["message"] + "</div>";
                     document.getElementById('chat-display').innerHTML += html;
              }
       });
}