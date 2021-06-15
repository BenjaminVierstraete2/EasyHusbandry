"use strict";
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);


const listenToSocket = function () {
  
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  })
  socket.on("B2F_client_connected", function() {
    socket.emit("F2B_conditions_connected");
});
  socket.on("B2F_temp_data", function (jsonObject) {
    console.log("dataLoop activated");
    let htmlstring = "";
    const temp = jsonObject.data;
    const metric = jsonObject.metric;
    console.log(temp)
    console.log(metric)
    htmlstring += `<div><p>${Math.round(temp)}${metric}</p></div>`;
    document.querySelector(".js-temp").innerHTML = htmlstring;
    socket.emit('F2B_temp_recieved')

  });
  socket.on("B2F_light_data", function (jsonObject) {
    console.log(jsonObject);
    let htmlstring = "";
    for (const sens of jsonObject.data) {
      console.log(sens);
        htmlstring += `<div><p> ${(Math.round(sens.value))}%</p></div>`;
    }
    document.querySelector(".js-light").innerHTML = htmlstring;
    socket.emit('F2B_light_recieved')

  });
  socket.on("B2F_hum_data", function (jsonObject) {
    console.log(jsonObject);
    let htmlstring = "";
    for (const sens of jsonObject.data) {
      console.log(sens);
        htmlstring += `<div><p> ${(Math.round(sens.value))}%</p></div>`;
    }
    document.querySelector(".js-hum").innerHTML = htmlstring;
    socket.emit('F2B_hum_recieved')
  });

  socket.on("B2F_fan_data", function (jsonObject) {
    console.log(jsonObject);
    let htmlstring = "";
    const state = jsonObject.data;
    console.log(state);
    htmlstring += `${state}`;
    document.querySelector(".js-fan").innerHTML = htmlstring;
    socket.emit('F2B_fan_recieved')
  });

  socket.on("B2F_lamp_data", function (jsonObject) {
    console.log(jsonObject);
    let htmlstring = "";
    const state = jsonObject.data;
    console.log(state);
    htmlstring += `${state}`;
    document.querySelector(".js-lamp").innerHTML = htmlstring;
    socket.emit('F2B_lamp_recieved')
  });
  socket.on("B2F_settimer", function() {
    setTimeout(function(){socket.emit("F2B_conditions_connected")},3000);
  });
};

function toggleNav() {
  let toggleTrigger = document.querySelectorAll(".js-toggle-nav");
  for (let i = 0; i < toggleTrigger.length; i++) {
      toggleTrigger[i].addEventListener("click", function() {
          console.log("clicked");
          document.querySelector("body").classList.toggle("hamburger");
      })
  }
}



document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");
    listenToSocket();
    toggleNav();
  });