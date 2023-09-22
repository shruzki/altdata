from flask import Flask, render_template, request, send_file
from news_sentiment import news_sentiment_function  # Import your news sentiment function
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        if ticker:
            # Call your news sentiment function to get the CSV and date range
            sentiment_csv, earliest_date, latest_date = news_sentiment_function(ticker)

            # Call Yahoo Finance API to get stock price data for the same date range
            stock_data = yf.download(ticker, start=earliest_date, end=latest_date)

            # Plot sentiment score and stock price
            fig, ax1 = plt.subplots()

            ax1.set_xlabel('Date')
            ax1.set_ylabel('Sentiment Score', color='tab:blue')
            ax1.plot(sentiment_csv['timestamp'], sentiment_csv['sentiment_score'], color='tab:blue')
            ax1.tick_params(axis='y', labelcolor='tab:blue')

            ax2 = ax1.twinx()
            ax2.set_ylabel('Stock Price', color='tab:red')
            ax2.plot(stock_data.index, stock_data['Close'], color='tab:red')
            ax2.tick_params(axis='y', labelcolor='tab:red')

            plt.title(f'Sentiment Score vs. Stock Price for {ticker}')
            plt.tight_layout()

            # Save the plot to a BytesIO buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()

            # Provide a download link for the sentiment CSV
            sentiment_csv_download = sentiment_csv.to_csv(index=False)
            sentiment_csv_buffer = BytesIO()
            sentiment_csv_buffer.write(sentiment_csv_download.encode())
            sentiment_csv_buffer.seek(0)

            return render_template('index.html', plot_img=buffer, sentiment_csv=sentiment_csv_buffer, ticker=ticker)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
