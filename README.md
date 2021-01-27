# Stock Price Predictions from Earnings Calls

Rice Data Analytics Program
Team Members: Radhika Balasubramaniam, Chad Dubiel, Katy Fuentes, Pankaj Tahiliani

## Background 
Every quarter, public companies report earnings and company updates. Companies host a conference call in order to provide additional commentary and answer questions from participants. 

## Data 
The dataset used consists of earnings call transcripts for S&P 500 companies.
The team webscraped Seeking Alpha earning transcripts. The transcripts include a prepared remarks section, a question-and-answer section, and instructions from the call operator. 

## Key Considerations 
Is there a change in stock price after an earnings call?
Does an earnings call influence the stock price?
Was is the call’s sentiment? What are common words/topics used across company earnings calls?
What is the price change for the stock before and after the call? Is there a trend or can you predict the change in price?

## Process 
1. Download S&P100 and then S&P500 list from Wikipedia
2. Scrape Seeking Alpha webpages for each company transcript with date, title, URL
3. Narrow list to only earning call transcript URLs 
4. Scrape each Seeking Alpha webpage for the earnings call transcript and save to text file
5. Scrape Yahoo finance webpage by Stock symbol and download 2015 through 2020 stock price history
6. Read text files and preprocess text


### TF-IDF and Count vectorization 
Documents were split 80%/20% into training and test subsets. Term Frequency * Inverse Document Frequency is a method in which to quanitify a terms importance to a document in a corpus. CountVectorizer() and TfidfVectorizer() methods of the scikit-learn library were fit with the training subset and then the vectorizer was used to transform both the training and test subset into matrices of term frequency for each earnings call transcript. 

### Classification
Returns were considered for 1 day, 7 days and 28 days after the closing price the trading day prior to the earnings call transcript release. Each return was classified as 'buy', 'hold', or 'sell' based on a >3%, <3% & >-3%, or <-3% return over the period, respectively. 

### Logistic Regression Model
These features were fit onto a logistic regression machine learning model, LogisticRegression(), also a part of the scikit-learn librabry. The model was most effective when considering returns 1 day after the prior close. After using grid search for hyperparameter tuning and 5 fold cross validation, the most effective solver was the 'liblinear' parameter with L1 lasss regularization. The model had a mean accuracy score of 74%. 

### Model Performance
The model was backtested from the period of 2015 - 2020. The theoretical return of the model over that period was measured as 321%. The S & P 500 (SPX) had a return of 83% for the same period, equating to the model providing a market adjusted of 238%

### Text and Sentiment Analysis
For the purpose of this analysis, only the prepared remarks for 2020 earnings calls for S&P100 companies compared to the full transcript text to compare the difference.
The transcripts were modified by the following processing steps: 

1. Removed numbers and punctuation
2. Preprocessed text by cleaning up contractions, removing html, tokenizing words, lemmatized words, removed stop words, and minimum character words
3. Removed infrequent words

Sentiment analysis is used to measure the attitude, sentiments, evaluations, or emotions of a speaker based on the algorithmic treatment of subjectivity in a text.


#### Latent Dirichlet Allocation (LDA)
Latent Dirichlet Allocation (LDA) models can be used to reveal a hidden structure in a collection of texts representing the weight of text in a topic space. The process involves loading data, cleaning, exploring general output in form of a word cloud, preparing the data for LDA analysis, training the LDA model, and analyzing the results with a visual. The earning call transcripts were uploaded in the raw format and cleaned with the various steps detailed above.  The wordcloud for the full transcript and prepared remarks are different but mostly contain the same common words. Next, the text was tokenized into a corpus and dictionary for each. The model was trained on 25 topics which was a combination of keywords based on a weight to the topic. To visual the topics pyLDAvis was used to better understand and interpret individual topics and their relationships.  For the most part the terms overlapped in the full transcript and prepared remarks, but the topic distribution varied significantly between the two.
	
#### VADER Sentiment Intensity Analyzer (SIA) polarity scoring 
VADER (Valence Aware Dictionary for Sentiment Reasoning) is a model used for text sentiment analysis that is sensitive to both polarity (positive/negative) and intensity. VADER sentimental analysis relies on a prepackaged dictionary that maps lexical features into scores, which categorize text into positive, neutral, and negative. These texts are aggregated by document to arrive at overall opinion. VADER uses a combination of sentiment lexicon and list of lexical features which are generally labelled according to their semantic orientation as either positive or negative .
VADER was applied across the processed text of the full and prepared remarks section of the earnings call transcripts. The prepacked VADER Sentiment Intensity Analyzer (SIA) polarity scoring and lexicon was used and compared to Hu Liu  (HL) and Loughran McDonald   (LM) word lists to compare tone and impact of classifying a call’s sentiment correctly.    The Hu-Liu lexicon was developed from a feature space of online movie reviews that were assigned negativity/positivity scores by the reviewers themselves. The HL lexicon consists of 6,786 words labeled positive or negative. The LM lexicon was constructed from words that are prevalent in 10-K reports of publicly-traded companies. The positive and negative labels assigned to these words are specific to the finance domain. The LM lexicon consists of 2,707 positive or negative words. Depending on the dictionary used, there is a significant difference between what is categorized as “Positive”. In addition, the sentiment scores change between the full transcript and prepared remarks which are likely influenced by the questions asked.

Sentiment Totals	Using HL Dictionary	Using LM Dictionary
Positive 		255			374
Negative		88			16
Neutral			58			11


#### Linear Discriminant Analysis on sentiment scores and price
Linear Discriminant Analysis is the linear classification technique for multi-classes of data. LDA consists of statistical properties of the data calculated for each class. LDA was applied across the processed text of the full and prepared remarks section of the earnings call transcripts. For purposes of this model, the “X” input consists of the adjusted close, close, high, low, open stock price and the SIA polarity which consists computations of subjectivity, polarity, negative, positive, and neutral scores. The “y” input consists of an imputed “label” value that measured the positivity score and assigned 1 for positive scores over 0.15 in the full transcript, based on the average of 0.150631, and 0.10 in the prepared remarks, based on the average of 0.143419. Based on the f1 score and classification report numbers, the model performed better with the condensed text in the prepared remarks which makes sense due to the variety of questions and answers included in the full transcript of the calls.


### Time Series Forecating
Traditionally  machine learning (ML) models used different features and corelate the data to prices but there is no time dimension in the data.
Time-series forecasting models are the models that are capable to predict future values based on previously observed values. Time-series forecasting is widely used for non-stationary data. Non-stationary data are called the data whose statistical properties e.g. the mean and standard deviation are not constant over time but instead, these metrics vary over time. We used Keras LSTM and GRU model to do time series forecasting. 

Stock prices are very volatile and lot of factors that contribute to the stock prices. Its important to identify the stocks that should be included in the the model evaluation while building a new LSTM/GRU model. For this, we did sma/ema comparison, created risk matrix with expected returns , plotting sns grid to identify overlays/clusters to identify similar patterns in stock movement. Also created a heatmap to identify the stock movement relative to other stocks. This process will help to remove stocks with high fluctations and no fluctations to prevent the model from overfitting or underfitting. For evaluation purposes, we restricted the stocks to 25. 

We used stock data from the past 15 years. We used data shifting and rolling window concepts to prepare the dataset. Nueral network with four layers and one dense layer was used. Since the data needs to be in timeseries we trained on the data prior to 2018 and used the data from 2018 for testing purposes. After the evaluation we identified that both the models were able to identify the trend patterns. On furthur analysis, we noticed LSTM performed better than GRU. Here is the attached results of the model for the apple stock.

![LSTM vs GRU](Earnings-Calls-NLP/static/images/lstm.jpg)


##### Data Sources

1. [S&P 100/500 List](https://en.wikipedia.org/wiki/List_of_stock_exchanges) 
2. [Earnings Calls Transcripts](https://seekingalpha.com/earnings/earnings-call-transcripts) 
The transcripts from Seeking Alpha are protected by copyright and cannot be used for commercial purposes. This is an educational project for the Data Visualization Program at Rice University and the use of the information should be permitted on the Copyright Fair Use principal.
3. [Yahoo Finance Historical stock price](https://sg.finance.yahoo.com/)

##### Further Reading
[Natural Language Processing – Part III: Feature Engineering: Applying NLP Using Domain Knowledge to Capture Alpha from Transcripts](https://www.spglobal.com/marketintelligence/en/documents/nlp-iii-final-013020-10a.pdf)


###### Next applications
Backtrack results
Predict trends
Predict price
Embed sentiment in model



