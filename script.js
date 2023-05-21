
/*
fetch('http://localhost:8003/list-forecast')
    .then(response => {
        if (!response.ok){
            throw new Error('Request failed with status ' + response.status);
        }
        console.log(response.json());
    })
    .then(data => {
    
    })
    .catch(error => {
        console.error('Error:', error);
    });*/
let array = [['Time', 'Humidity', 'Temperature']];
const myPromise = new Promise(async (resolve, reject) => {
    try{
        const response = await fetch('http://cse191.ucsd.edu/api03/list-forecast');
        if (!response.ok){
            throw new Error('Request failed with status ' + response.status);
        }
        const data = await response.json();
        resolve(data);
    }catch (error){
        reject(error);
    }
});

myPromise
    .then(result => {
        console.log(result);
        copy = JSON.parse(JSON.stringify(result));
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(drawChart);
        for (let entry of copy){
            let temp = entry['temperature'];
            let time = new Date(entry['forecast_ts']);
            let hours = time.getHours();
            let minute = time.getMinutes();
            time = `${hours}:${minute}`;
            let humidity = entry['humidity'];
            inputChart(time, humidity, temp);
        }
        drawChart();
    })
    .catch(error => {
        console.error(error);
    })

  
function inputChart(time, humidity, temperature){
    array.push([time, humidity, temperature]);
}    
function drawChart() {
    var data = google.visualization.arrayToDataTable(array);
  
    var options = {
        title: 'Weather of Seoul, Korea',
        curveType: 'function',
        legend: { position: 'bottom' }
    };
  
    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
  
    chart.draw(data, options);
}