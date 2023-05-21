
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
const myPromise = new Promise(async (resolve, reject) => {
    try{
        const response = await fetch('http://localhost:8003/list-forecast');
        if (!response.ok){
            throw new Error('Request failed with status ' + response.status);
        }
        const data = await response.json();
        resolve(data);
    }catch (error){
        reject(error);
    }
});
let copy;
myPromise
    .then(result => {
        console.log(result);
        copy = JSON.parse(JSON.stringify(result));
    })
    .catch(error => {
        console.error(error);
    })
console.log(copy);

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
  
function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Year', 'Sales', 'Expenses'],
        ['2004',  1000,      400],
        ['2005',  1170,      460],
        ['2006',  660,       1120],
        ['2007',  1030,      540],
        ['2008',  500,       400]
    ]);
  
    var options = {
        title: 'Company Performance',
        curveType: 'function',
        legend: { position: 'bottom' }
    };
  
    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
  
    chart.draw(data, options);
}