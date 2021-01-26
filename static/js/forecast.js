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
            y: unpack(rows, 'Pred'),
            line: {color: '#7F7F7F'}
            }

            var trace3 = {
                type: "scatter",
                mode: "lines",
                name: 'GRU Pred',
                x: unpack(rows2, 'Date'),
                y: unpack(rows2, 'Pred'),
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

    updateStatistics(ticker)
}


function updateStatistics(ticker)
{
    url = "api/GetMetrics/" + ticker
    
    Plotly.d3.json(url, function(err, rows3){

        function unpack(rows3, key) {
            return rows3.map(function(row3) { return row3[key]; });
            }
            
        


        d3.select("#lstm").selectAll("table").remove();
        d3.select("#gru").selectAll("table").remove();

        // build lstm table
        let table = d3.select("#lstm").append('table').attr('class', 'table').style('color', 'grey')
        let header = table.append('thead')

        let headers = ['Type', 'RMSE', 'NRMSE', 'MAE', 'R2']
        headers.forEach(function (d) {
            let colHeader = header.append('th')
            colHeader.text(d)
        })

        var row = table.append('tr')
        var type_row = row.append('td')
        var rmse_row = row.append('td')
        var nrmse_row = row.append('td')
        var mae_row = row.append('td')
        var r2_row = row.append('td')
        
        type_row.text('LSTM')
        rmse_row.text(rows3.lstmRMSE)
        nrmse_row.text(rows3.lstmNRMSE * 100)
        mae_row.text(rows3.lstmMAE)
        r2_row.text(rows3.lstmR2)
        
        row = table.append('tr')
        type_row = row.append('td')
        rmse_row = row.append('td')
        nrmse_row = row.append('td')
        mae_row = row.append('td')
        r2_row = row.append('td')

        type_row.text('LSTM With Lag')
        rmse_row.text(rows3.lstmRMSELag)
        nrmse_row.text(rows3.lstmNRMSELag * 100 )
        mae_row.text(rows3.lstmMAELag)
        r2_row.text(rows3.lstmR2Lag)
        
        // build gru tabl
        table = d3.select("#gru").append('table').attr('class', 'table').style('color', 'grey')
        header = table.append('thead')

        headers = ['Type', 'RMSE', 'NRMSE', 'MAE', 'R2']
        headers.forEach(function (d) {
            let colHeader = header.append('th')
            colHeader.text(d)
        })

        var row = table.append('tr')
        var type_row = row.append('td')
        var rmse_row = row.append('td')
        var nrmse_row = row.append('td')
        var mae_row = row.append('td')
        var r2_row = row.append('td')
        
        type_row.text('GRU')
        rmse_row.text(rows3.gruRMSE)
        nrmse_row.text(rows3.gruNRMSE * 100)
        mae_row.text(rows3.gruMAE)
        r2_row.text(rows3.gruR2)
        
        row = table.append('tr')
        type_row = row.append('td')
        rmse_row = row.append('td')
        nrmse_row = row.append('td')
        mae_row = row.append('td')
        r2_row = row.append('td')

        type_row.text('GRU With Lag')
        rmse_row.text(rows3.gruRMSELag)
        nrmse_row.text(rows3.gruNRMSELag * 100)
        mae_row.text(rows3.gruMAELag)
        r2_row.text(rows3.gruR2Lag)



        // only display last 7 days for demo
        //x = unpack(rows, 'Date').slice(-7);



    })
}
