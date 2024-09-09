// var xValues = ['Mar23', 'Mar28', 'Apr2', 'Apr7', 'Apr12', 'Apr17'];
// var yValues = [0.1,0.1,0.1,0.1,0.1,0.1];

// new Chart("lineChart", {
//   type: "line",
//   data: {
//     labels: xValues,
//     datasets: [{
//       fill: false,
//       lineTension: 0,
//       backgroundColor: "rgba(0,0,255,1.0)",
//       borderColor: "#ffc107",
//       borderWidth: 8,
//       data: yValues
//     }]
//   },
//   options: {
//     legend: {display: false},
//     scales: {
//       yAxes: [{display: true, ticks: {
//             min: 0.1,
//             max: 10000,
//             stepSize: 1000
//         }}],
//       responsive: true
//     }
//   }
// });

// const day = [
//     { x: Date.parse('2022-04-23 00:00:00 GMT+0800'), y: 10000 },
//     { x: Date.parse('2022-04-24 00:00:00 GMT+0800'), y: 12 },
//     { x: Date.parse('2022-04-25 00:00:00 GMT+0800'), y: 600 },
//     { x: Date.parse('2022-04-26 00:00:00 GMT+0800'), y: 9 },
//     { x: Date.parse('2022-04-27 00:00:00 GMT+0800'), y: 12 },
//     { x: Date.parse('2022-04-28 00:00:00 GMT+0800'), y: 3 },
//     { x: Date.parse('2022-04-29 00:00:00 GMT+0800'), y: 9 },
// ];

// const week = [
//     { x: Date.parse('2022-10-31 00:00:00 GMT+0800'), y: 50 },
//     { x: Date.parse('2022-11-07 00:00:00 GMT+0800'), y: 30 },
//     { x: Date.parse('2022-11-14 00:00:00 GMT+0800'), y: 60 },
//     { x: Date.parse('2022-11-21 00:00:00 GMT+0800'), y: 700 },
//     { x: Date.parse('2022-11-28 00:00:00 GMT+0800'), y: 10000 },
// ];

// const month = [
//     { x: Date.parse('2022-01-19 00:00:00 GMT+0800'), y: 900 },
//     { x: Date.parse('2022-02-26 00:00:00 GMT+0800'), y: 500 },
//     { x: Date.parse('2022-03-03 00:00:00 GMT+0800'), y: 800 },
//     { x: Date.parse('2022-04-07 00:00:00 GMT+0800'), y: 500 },
//     { x: Date.parse('2022-05-10 00:00:00 GMT+0800'), y: 950 },
//     { x: Date.parse('2022-06-17 00:00:00 GMT+0800'), y: 500 },
//     { x: Date.parse('2022-07-24 00:00:00 GMT+0800'), y: 300 },
//     { x: Date.parse('2022-08-31 00:00:00 GMT+0800'), y: 500 },
//     { x: Date.parse('2022-09-07 00:00:00 GMT+0800'), y: 300 },
//     { x: Date.parse('2022-10-14 00:00:00 GMT+0800'), y: 600 },
//     { x: Date.parse('2022-11-21 00:00:00 GMT+0800'), y: 7000 },
//     { x: Date.parse('2022-12-28 00:00:00 GMT+0800'), y: 10000 },
// ];

// // setup 
// const data = {
// //labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
// datasets: [{
// label: 'Daily Sales',
// data: day,
// borderColor: [
//   'rgba(255, 193, 7, 1)',
// ],
// borderWidth: 2
// }]
// };

// // config 
// const config = {
// type: 'line',
// data,
// options: {
// scales: {
//   x: {
//       type: 'time',
//       time: {
//           unit: 'day'
//       }
//   },
//   y: {
//     ticks: {
//     min: 0.1,
//     max: 10000,
//     stepSize: 1000
// }},
// responsive: true
  
// }
// }
// };

// // render init block
// const myChart = new Chart(
// document.getElementById('myChart'),
// config
// );
// function timeFrame(period){
// //console.log(period)
// console.log(period.value);
// if(period.value == 'day') {
//     myChart.config.options.scales.x.time.unit = period.value;
//     myChart.config.data.datasets[0].data = day;
//     myChart.config.data.datasets[0].label = 'Daily Sales';
// }
// if(period.value == 'week') {
//     myChart.config.options.scales.x.time.unit = period.value;
//     myChart.config.data.datasets[0].data = week;
//     myChart.config.data.datasets[0].label = 'Weekly Sales';

// }
// if(period.value == 'month') {
//     myChart.config.options.scales.x.time.unit = period.value;
//     myChart.config.data.datasets[0].data = month;
//     myChart.config.data.datasets[0].label = 'Monthly Sales';

// }
// myChart.update();
// }

// const dates = ['2022-04-25', '2022-04-26', '2022-04-27', '2022-04-28', '2022-04-29', '2022-04-30', '2022-05-01'];
// const datapoints = [1, 2, 3, 4, 5, 6, 7];

// console.log

// const data = {
//     labels: dates,
//     datasets: [{
//       label: 'Weekly Sales',
//       data: datapoints,
//       backgroundColor: [
//         'rgba(255, 26, 104, 0.2)',
//         'rgba(54, 162, 235, 0.2)',
//         'rgba(255, 206, 86, 0.2)',
//         'rgba(75, 192, 192, 0.2)',
//         'rgba(153, 102, 255, 0.2)',
//         'rgba(255, 159, 64, 0.2)',
//         'rgba(0, 0, 0, 0.2)'
//       ],
//       borderColor: [
//         'rgba(255, 26, 104, 1)',
//         'rgba(54, 162, 235, 1)',
//         'rgba(255, 206, 86, 1)',
//         'rgba(75, 192, 192, 1)',
//         'rgba(153, 102, 255, 1)',
//         'rgba(255, 159, 64, 1)',
//         'rgba(0, 0, 0, 1)'
//       ],
//       borderWidth: 1
//     }]
//   };

//   // config 
//   const config = {
//     type: 'bar',
//     data,
//     options: {
//       scales: {
//         y: {
//           beginAtZero: true
//         }
//       }
//     }
//   };

//   // render init block
//   const myChart = new Chart(
//     document.getElementById('myChart'),
//     config
//   );

//   function filterData(){
//       const dates2 = [...dates];
//       console.log(dates2);
//       const startdate = document.getElementById('startdate');
//       const enddate = document.getElementById('enddate');

//       const indexstartdate = dates2.indexOf(startdate.value);
//       const indexenddate = dates2.indexOf(enddate.value);

//       const filterDate = dates2.slice(indexstartdate, indexenddate + 1);

//       myChart.config.data.labels = filterDate;

//       const datapoints2 = [...datapoints];
//       const filterDatapoints = datapoints2.slice(indexstartdate, indexenddate + 1);

//       myChart.config.data.datasets[0].data = filterDatapoints;


//       myChart.update;
//   }

// setup 



const dates = ['2022-04-25', '2022-04-26', '2022-04-27', '2022-04-28', '2022-04-29', '2022-04-30', '2022-05-01'];
const datapoints = [108, 332, 103, 405, 500, 906, 1000];

console.log(new Date('2022-04-25 00:00:00 GMT+0800'))
const convertedDates = dates.map(date => new Date(date).setHours(0,0,0,0));
console.log(convertedDates)

const data = {
    labels: dates,
    datasets: [{
      label: 'ASINS Found',
      data: datapoints,
    backgroundColor: 'rgba(255, 193, 7, 1)',
    borderColor: 'rgba(201, 152, 4, 1)',
    borderWidth: 1
  }] 
};

// config 
const config = {
  type: 'line',
  data,
  options: {
    scales: {
     
      x: {
        type: 'time',
        time: {
          unit: 'day'
        }
      },
      y: {
        beginAtZero: true
      }
    }
  }
};

// render init block
const myChart = new Chart(
  document.getElementById('myChart'),
  config
);

function filterDate(){
  const start1 = new Date(document.getElementById('start').value);
  const start = start1.setHours(0,0,0,0);
  const end1 = new Date(document.getElementById('end').value);
  const end = end1.setHours(0,0,0,0);

  
  const filterDates = convertedDates.filter(date => date >= start && date <= end) 
  myChart.config.data.labels = filterDates;

  const startArray = convertedDates.indexOf(filterDates[0])
  const endArray = convertedDates.indexOf(filterDates[filterDates.length -1])
  console.log(endArray);
  const copydatapoints = [...datapoints];
  copydatapoints.splice(endArray + 1, filterDates.length);
  copydatapoints.splice(0, startArray);
  console.log(copydatapoints)
  myChart.config.data.datasets[0].data = copydatapoints;
  myChart.update();
}
function resetDate(){
  myChart.config.data.labels = convertedDates;
  myChart.config.data.datasets[0].data = datapoints;
  myChart.update();
}