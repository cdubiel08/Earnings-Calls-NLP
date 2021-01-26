function updateStockCharts(ticker)
{
    url = "api/GetRollingAverages/" + ticker;
    Plotly.d3.json(url, function(err, rows){

    function unpack(rows, key) {
    return rows.map(function(row) { return row[key]; });
    }
    console.log(rows)
    
    // only display last 7 days for demo
    x = unpack(rows, 'Date').slice(-7);
    y = unpack(rows, 'MA').slice(-7);
    y1 = unpack(rows, 'EMA').slice(-7);

    yReturn = unpack(rows, 'ER').slice(-7);
    
    xMean = unpack(rows, 'mean').slice(-1);
    yDev = unpack(rows, 'std').slice(-1);
    updateMovingChart(x, y, y1);
    updateReturnChart(x,yReturn );
    updateRiskChart(xMean , yDev);

    
    })
}

function updateMovingChart(x, y, y1)
{
    
    // build EMA and ER charts
    var trace1 = {
        type: "scatter",
        mode: "lines",
        name: 'MA',
        x: x,
        y: y,
        line: {color: '#17BECF'}
        }
    
        var trace2 = {
            type: "scatter",
            mode: "lines",
            name: 'EMA',
            x: x,
            y: y1,
            line: {color: '#7F7F7F'}
        }
    
    
        var data = [trace1, trace2];
    
        var layout = {
        paper_bgcolor: 'black',
        plot_bgcolor : 'black',
        
         
        font: {
           
            color: '#7f7f7f'
          },
        
        yaxis: {
            autorange: true,
           
            type: 'linear'
        },
        autosize: false, width: 550, height: 150,  margin: { l: 60,  r: 30, b: 20,  t: 5 }
        
        };
    
        
        var config = { responsive: true };
    
    
        Plotly.newPlot('todayPrice', data, layout, config);
}


function updateReturnChart(x, yReturn)
{
    
    // build YTD Rate of return
    var trace1 = {
        type: "scatter",
        mode: "lines",
        name: 'Return',
        x: x,
        y: yReturn,
        line: {color: 'brown'}
        }
    
        
    
        var data = [trace1];

        var layout = {
        paper_bgcolor: 'black',
        plot_bgcolor : 'black',
        
         
        font: {
           
            color: '#7f7f7f'
          },
        
        yaxis: {
            autorange: true,
           
            type: 'linear'
        },
        showlegend : true,
        autosize: false, width: 550, height: 150,  margin: { l: 40,  r: 30, b: 20,  t: 5 }
        
        };
    
        
        var config = { responsive: true };
    
    
        Plotly.newPlot('return', data, layout, config);
}

function updateRiskChart(xMean, yDev)
{
    console.log(xMean)
    console.log(yDev)
    
    // build YTD Rate of return
    var trace1 = {
        type: "scatter",       
        name: 'Risk',
        x: xMean,
        y: yDev,
        mode: 'markers',
        marker: {
            color: 'rgb(17, 157, 255)',
            size: 10
        }
      
        };

       
    
    
        
    
        var data = [trace1];

        var layout = {
        paper_bgcolor: 'black',
        plot_bgcolor : 'black',
        
        xaxis: {
            title : "Expected Return"
        },

        yaxis: {
            title : "Risk"
        },
        font: {
           
            color: '#7f7f7f'
          },
        
       
        showlegend : true,
        autosize: false, width: 550, height: 150,  margin: { l: 50,  r: 30, b: 50,  t: 5 }
        
        };
    
        
        var config = { responsive: true };
    
    
        Plotly.newPlot('ratio', data, layout, config);
}
