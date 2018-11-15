window.mobilecheck = function() {
  var check = false;
  if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) )
  {
     check = true;
  }
  return check;
};

Init_Config = () =>
{
       windowheight = documentHeight();
       navbarheight= document.getElementById('top-nav').offsetHeight;
       messagebarheight = document.getElementById('bottom-div').offsetHeight;
       height = windowheight - (navbarheight + messagebarheight);
       document.getElementById('chat-display-area').style.marginTop = String(navbarheight)+"px";
       document.getElementById('chat-display-area').style.height = String(height)+"px";
}



document.addEventListener("DOMContentLoaded", function()
{

       Init_Config();
       var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
       socket.on('connection', data =>
       {
              console.log(data);
       });

       socket.on('my_response', data=>
       {
              console.log(data);
       });

       if(window.mobilecheck())
       {
              document.getElementById('send-btn').innerHTML = "+";
              returningUserCheck(socket);
              SendMessage(socket);
              ReceivedMessage(socket);
              SetCurrentChannel(socket);
              JoinChannel(socket);
              popupcancel(socket);
       }
       else
       {
              returningUserCheck(socket);
              WindowResizeEvent();
              SetCurrentChannel(socket);
              JoinChannel(socket)
              SendMessage(socket);
              ReceivedMessage(socket);
              popupcancel();
              KeySendMessage(socket);
       }

});


popupcancel = () =>
{
       items = document.getElementsByClassName("popup-cancel-btn");
       for(var i = 0; i < items.length; i++)
       {
              items[i].addEventListener('click', () =>
              {
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


returningUserCheck = (socket) =>
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
              {
                     document.querySelector("#username").innerHTML = " " + localStorage.getItem("username");
                     channel = localStorage.getItem("currentChannel");
                     if(channel)
                     {
                            socket.emit('join_channel', {"user": localStorage.getItem("username"), "channel" : channel});
                            socket.once('joined_channel', data =>
                            {
                                   if(data["request"])
                                          document.getElementById('chat-name').innerHTML = "Chatroom: " + channel;
                            });
                     }

              }

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
                     user = localStorage.getItem("username");
                     socket.emit('create_channel', {"user" : user, "channel" : channel });
                     socket.once('init_channel', data=>
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
                     user = localStorage.getItem("username");
                     socket.emit('join_channel', {"user" : user, "channel" : channel});
                     socket.once('joined_channel', data =>
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
              console.log("sending message");
              channel = localStorage.getItem('currentChannel');
              if (channel)
              {

                     message = document.getElementById('message-input').value;
                     document.getElementById('message-input').value = "";
                     socket.emit("send_message", {"channel" : channel, "message" : message});

              }
              else
                     alert("Not subscribed to a channel, please create, or join a channel.");

              return false;
       };
}

KeySendMessage = (socket) =>
{

       document.getElementById("message-input").addEventListener("keypress", function(event)
       {
          console.log("sending message");
          var key = event.keyCode
          if (key === 13)
          {
                     channel = localStorage.getItem('currentChannel');
                     if (channel)
                     {
                            message = document.getElementById('message-input').value;
                            document.getElementById('message-input').value = "";
                            socket.emit("send_message", {"channel" : channel, "message" : message});
                            event.preventDefault();

                     }
                     else
                            alert("Not subscribed to a channel, please create, or join a channel.");
          }
          return false;
       });


}

ReceivedMessage = (socket) =>
{

       socket.on('receive_message', data =>
       {
              console.log(data)
              if(data["confirm"])
              {

                     html = "<div class='chatbubble-padding'><div class='namebubble'>"+ data["user"]+"</div><div class='chatbubble'>"
                            + data["message"] + "</div><div class='time-stamp'>11:11:11</div></div>";
                     document.getElementById('current-chat').innerHTML += html;
                     $('#current-chat').scrollTop($('#current-chat')[0].scrollHeight);
              }
       });
}