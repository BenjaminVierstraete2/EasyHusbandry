"use strict";
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

const addSettings = function(data){
    console.log("added")
}

function listenToSubmit(){
    const button = document.querySelector(".js-button")
    button.addEventListener('click', function(){
        let jsonObject ={
            tempMet: document.querySelector("#tempMet").value,
            tempMax: document.querySelector("#tempMax").value,
            tempMin: document.querySelector("#tempMin").value,
            humMax: document.querySelector("#humMax").value,
            humMin: document.querySelector("#humMin").value,
            brightMin: document.querySelector("#brightMin").value,
            from: document.querySelector("#from").value,
            to: document.querySelector("#to").value,
            fan: document.querySelector("#fan").value,
            lamp: document.querySelector("#lamp").value,
        };
    handleData(`http://${lanIP}/api/v1/settings`,addSettings,null,"POST",JSON.stringify(jsonObject));
    });  
}

function toggleNav() {
    let toggleTrigger = document.querySelectorAll(".js-toggle-nav");
    for (let i = 0; i < toggleTrigger.length; i++) {
        toggleTrigger[i].addEventListener("click", function() {
            console.log("clicked");
            document.querySelector("body").classList.toggle("hamburger");
        })
    }
  }

const listenToSocket = function () {
  
    socket.on("connected", function () {
      console.log("verbonden met socket webserver");
    });
  
    socket.on("B2F_client_connected", function() {
      socket.emit("F2B_settings_connected")
    });
    socket.on("B2F_settings", function(jsonObject) {
        document.getElementById("tempMax").placeholder = jsonObject.settings[1];
        document.getElementById("tempMin").placeholder = jsonObject.settings[2];
        document.getElementById("humMax").placeholder = jsonObject.settings[3];
        document.getElementById("humMin").placeholder = jsonObject.settings[4];
        document.getElementById("brightMin").placeholder = jsonObject.settings[5];
        document.getElementById("from").placeholder = jsonObject.settings[6];
        document.getElementById("to").placeholder = jsonObject.settings[7];
        socket.emit("F2B_settings_recieved")
    });
    socket.on("B2F_settimer", function() {
        setTimeout(function(){socket.emit("F2B_settings_connected")},10000);
      });
}

document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");
    listenToSubmit(); 
    toggleNav(); 
    listenToSocket();
});