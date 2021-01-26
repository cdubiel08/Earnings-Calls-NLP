var url_companies = "/api/GetCompanyList";

var urls = [url_companies];

var promises = [];
urls.forEach(function (url) { promises.push(d3.json(url)) });
console.log(promises);
Promise.all(promises).then(data => init(data));
// end JSON Fetch



// function addstocks
function addStocks(response) {
    var stocks = response;
    
    initDropList(stocks);
   // console.log(stocks)
    return stocks;
}//end addstocks() function

function changeCity(city_id) 
{
    updateForecastChart(city_id);
    updateStockCharts(city_id)
     
}

// function init
function init(data) {

    // initialize the data for the elements
    stocksIn = addStocks(data[0]);
     // assign the heading text
    d3.select('#selStock').property('value', 'AAPL');
    updateForecastChart('AAPL');
    updateStockCharts('AAPL');
    

    //d3.select("#heading").text("Apple Inc");
    // update the neighborhoods with city
    //updateStocks("AAPL");

}//end init() function



// function on application startup to initialize dropdown menu options to placeholder text values,
// calls function that populates each filter criteria with tableData values assigned from data.js 
function initDropList(stockData) {
    var select = document.getElementById("selStock")
    console.log(stockData[0])
    for (i = 0; i < stockData.length; i++)
    {
        // create html option tag that will be appended within the select tag
        var option = document.createElement("option");
        // assign option value to each data value iteratively
        option.value = stockData[i]["Ticker"];
        option.text =  stockData[i]["Ticker"] + "- " + stockData[i]["Company"];
        select.appendChild(option);        
    }  
}//initDropList() function


// function to create the droplist for the stocks and earningsDate
function createDropList(menu, selectname, idname)
{ 
    //d3.select("#" + selectname).select("options").remove();
    var select = document.getElementById(selectname)
   
    idtxt = (menu[0]['id']).toString();
    ids = idtxt.split(",");

    nametxt = (menu[0]['name']).toString();
    names = nametxt.split(",");
 
    for (i = 0; i < ids.length; i++)
    {
        // create html option tag that will be appended within the select tag
        var option = document.createElement("option");
        // assign option value to each data value iteratively
        option.value = ids[i];
        option.text = names[i];
        select.appendChild(option);        
    }  
}
