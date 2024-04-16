# ProductReviewAnalyzerChromeExtension

Below are the steps to Deploy the project 
1. Train the sentiment analysis model and save it (`sentiment_analysis_newonelstm100.keras`).
2. Create or load the tokenizer and save it (`tokenizerlstm100.pickle`).
3. Uploading dataset (`data.csv`) for training.
4. Start Django server to handle requests from chrome extension which acts like API. (`python manage.py runserver`).
5. Start Splash in Docker for web scraping.
6.  Add your Chrome extension from Chrome Web Store or manage extensions (by manually adding the file).
7. Open your Chrome extension in an amazon product page and wait for analysis.
8. Display’s sentiment analysis results in the Chrome extension, including the graph.

Softwares Required for the project are :
1.Python: 3.12.1

2.Tensorflow: 2.16.1

3.Keras: 3.0.5

4.BeautifulSoup: 4.12.3

5.Splash: 3.5.0

6.Docker: 24.0.7

7.Django: 5.0.2

8.Numpy: 1.26.4

