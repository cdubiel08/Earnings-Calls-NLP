function updateForecastChart(ticker)
{
    url = "api/GetLSTMData/" + ticker
    url2 ="api/GetGRUData/" + ticker

   
    
        Plotly.d3.json(url, function(err, rows){

        function unpack(rows, key) {
        return rows.map(function(row) { return row[key]; });
        }
        Plotly.d3.json(url2, function(err, rows2){

            function unpack(rows2, key) {
            return rows2.map(function(row2) { return row2[key]; });
            }
      
        var trace1 = {
        type: "scatter",
        mode: "lines",
        name: 'Actual',
        x: unpack(rows, 'Date'),
        y: unpack(rows, 'Actual'),
        line: {color: '#17BECF'}
        }

        var trace2 = {
        type: "scatter",
        mode: "lines",
        name: 'LSTM Pred',
        x: unpack(rows, 'Date'),
        y: unpack(rows, 'PredLag'),
        line: {color: '#7F7F7F'}
        }

        var trace3 = {
            type: "scatter",
            mode: "lines",
            name: 'GRU Pred',
            x: unpack(rows2, 'Date'),
            y: unpack(rows2, 'PredLag'),
            line: {color: 'brown'}
            }

        var data = [trace1,trace2, trace3];

        var layout = {
        paper_bgcolor: 'black',
        plot_bgcolor : 'black',
        
        title:  'Price Forecast With LSTM and GRU for ' + ticker,
        font: {
           
            color: '#7f7f7f'
          },
        xaxis: {
            autorange: true,
            title : "Date",
            range: ['2020-04-20', '01-01-2021'],
            rangeselector: {buttons: [
                
                {
                    count: 15,
                    label: '15d',
                    step: 'day',
                    stepmode: 'forward'
                },
                {
                count: 1,
                label: '1m',
                step: 'month',
                stepmode: 'forward'
                },
                {
                    count: 3,
                    label: '3m',
                    step: 'month',
                    stepmode: 'forward'
                },
                {
                count: 6,
                label: '6m',
                step: 'month',
                stepmode: 'forward'
                },
                
                {step: 'all'}
            ]},
            rangeslider: {range: ['2020-04-20', '01-01-2021']},
            type: 'date'
        },
        yaxis: {
            autorange: true,
            title : "Stock Price",
           
            type: 'linear'
        },
        height: '800px'

        
        };

        Plotly.newPlot('myDiv', data, layout);
        })
    })
}