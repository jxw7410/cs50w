document.addEventListener("DOMContentLoaded", function()
{
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
