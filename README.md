# ProductReviewAnalyzerChromeExtension

This project develops a Chrome extension aimed at providing immediate sentiment analysis of product reviews on Amazon. By using web scraping techniques with Beautiful Soup and rendering dynamic content through Splash within a Docker environment, the extension captures and processes reviews directly from product pages. These reviews are then analyzed using a deep learning model, specifically an LSTM network, to assess the sentiment as positive or negative. The analysis results, expressed as percentages of positive and negative sentiments, are seamlessly displayed to users through a popup on their Chrome browser. 

Below are the steps to Deploy the project 
1. Train the sentiment analysis model and save it (`sentiment_analysis_newonelstm100.keras`) and the accuracy of the model is 86%
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

Output of the above project :

![Screenshot 2024-04-10 203901](https://github.com/h4rik/ProductReviewAnalyzerChromeExtension/assets/108120747/975c71a2-d984-43b2-a946-9be35be5102c)


![Screenshot 2024-03-30 115249](https://github.com/h4rik/ProductReviewAnalyzerChromeExtension/assets/108120747/19ce0acf-8b73-49ab-b8df-31fb6b533e3c)
![Screenshot 2024-03-30 120508](https://github.com/h4rik/ProductReviewAnalyzerChromeExtension/assets/108120747/ec3e0dce-3b10-4ead-b0db-a0b048b5005b)
