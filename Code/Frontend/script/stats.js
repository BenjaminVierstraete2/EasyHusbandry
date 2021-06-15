const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);


const listenToSocket = function () {
  
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });
  
  socket.on("B2F_client_connected", function() {
    socket.emit("F2B_stats_connected");

  });
  socket.on("B2F_tempchart", function (jsonObject) {
    timestamps = jsonObject.time
    data = jsonObject.data
    drawChart(timestamps,data,".js-tempChart","tempChart");
    socket.emit('F2B_tempchart_recieved')
  });
  socket.on("B2F_humchart", function (jsonObject) {
    timestamps = jsonObject.time
    data = jsonObject.data
    drawChart(timestamps,data,".js-humChart","humChart");
    socket.emit('F2B_humchart_recieved')
  });
  socket.on("B2F_lightchart", function (jsonObject) {
    timestamps = jsonObject.time
    data = jsonObject.data
    drawChart(timestamps,data,".js-lightChart","lightChart");
    socket.emit('F2B_lightchart_recieved')
  });
  socket.on("B2F_settimer", function() {
    setTimeout(function(){socket.emit("F2B_stats_connected")},60000);
  });
}



const drawChart = function (timestamps,data,htmllink,chartId){
  document.querySelector(htmllink).innerHTML = `<canvas id="${chartId}"></canvas>`;
  let myChartId = document.getElementById(chartId).getContext('2d');
    let config = {
      type: 'line',
      data: {
        labels: timestamps,
        datasets: [
          {
            backgroundColor: "black", 
            borderColor: "orange",
            data: data,
            fill: false
          }
        ]
      },
      options: {
        scales: {
          y: {
              ticks: {
                  color: 'white'
              },
          },
        x:{
              ticks: {
                  color: 'white'
              },
          }
        },
        responsive: true,
        plugins: {
          title: {
            display: false,
          },
          legend: {
            display: false,
          },
        }
      }
    };
  let myChart = new Chart(myChartId, config);
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