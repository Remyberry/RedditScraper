import nltk
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
from tqdm import tqdm

# Download Nltk resources (if not already downloaded)
##nltk.download('vader_lexicon')
##nltk.download('punkt')

# Sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Define list of shoe brands to count
shoe_brands = ["Nike", "Adidas", "Reebok", "Puma", "New Balance", "Asics", "Converse", "Vans", "Timberland", "Fila", "Skechers"]  # Add more as needed

# Initialize brand sentiment scores and mention counters
brand_sentiments = {brand: {"positive": 0, "negative": 0, "neutral": 0} for brand in shoe_brands}
brand_mentions = Counter()

text_file_path = "BrandCommentAnalysis/TXTResults/scrapedText.txt"
csv_file_path = "BrandCommentAnalysis/brand_sentiment_analysis.csv" 


def analyze_text_file(file_path, csv_file_path):
  """Analyzes sentiment for each comment in a text file, categorizes by brand, and accumulates scores. Saves results to a CSV file."""

  print("Analyzing...")

  try:
    with open(file_path, 'r', encoding="utf-8") as f:
      comments = f.readlines()

      for comment in tqdm(comments, desc = "Reading comments", unit = "comments"):
        comment = comment.strip()  # Remove extra whitespaces
        # Sentiment analysis
        scores = sid.polarity_scores(comment)
        # Lowercase the comment for case-insensitive brand counting
        lower_comment = comment.lower()
        # Identify brand mentions (avoiding potential ellipsis error)
        mentioned_brands = []
        for brand in shoe_brands:
          if isinstance(brand, str):
            lower_brand = brand.lower()
            if lower_brand in lower_comment:
              mentioned_brands.append(brand)
              brand_mentions[brand] += 1  # Increment brand mention count

        # Categorize sentiment by mentioned brands
        for brand in mentioned_brands:
          if scores['compound'] > 0.05:
            brand_sentiments[brand]["positive"] += 1
          elif scores['compound'] < -0.05:
            brand_sentiments[brand]["negative"] += 1
          else:
            brand_sentiments[brand]["neutral"] += 1

      # Write results to CSV file
      with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Brand", "Positive", "Negative", "Neutral", "Total Sentiment Score", "Average Sentiment Score per Comment"])
        for brand, scores in tqdm(brand_sentiments.items(), desc = "Writing csv file", unit = "rows"):
          total_score = scores['positive'] - scores['negative']  # Adjust calculation as needed
          average_sentiment_per_comment = total_score / (brand_mentions[brand] if brand_mentions[brand] > 0 else 1)
          writer.writerow([brand, scores['positive'], scores['negative'], scores['neutral'], total_score, average_sentiment_per_comment])

  except FileNotFoundError:
    print("Error: File not found at", file_path)



def visualize_results(brand_sentiments, brand_mentions):
  """Creates two Matplotlib visualizations:
  1. Horizontal bar graph showing sentiment distribution per brand
  2. Scatter plot showing average sentiment vs brand mention count
  """

  print("Visualizing...")
  # Double-check brand list consistency (assuming 'shoe_brands' is used)
  if len(shoe_brands) != len(brand_sentiments.keys()):
    print("Warning: Brand list inconsistency detected!")

  brand_colors = {
    'Nike': 'royalblue',
    'Adidas': 'orange',
    'Reebok': 'red',
    'Puma': 'black',
    'New Balance': 'gray',
    'Asics': 'teal',
    'Converse': 'darkred',
    'Vans': 'darkblue',
    'Timberland': 'tan',
    'Fila': 'lightblue',
    'Skechers': 'indigo'
  }

  # Extract data for the first graph (sentiment distribution)
  brands = list(brand_sentiments.keys())
  sentiment_data = {'brand': brands}
  sentiment_data['positive'] = [scores['positive'] for scores in brand_sentiments.values()]
  sentiment_data['negative'] = [scores['negative'] for scores in brand_sentiments.values()]
  neutral_counts = [scores['neutral'] for scores in brand_sentiments.values()]
  if neutral_counts:  # Include neutral data if available
      sentiment_data['neutral'] = neutral_counts

  df = pd.DataFrame(sentiment_data)
  width = 0.25  # Adjust bar width as needed

  # Create the first Matplotlib figure (stacked bar graph)
  fig, ax = plt.subplots(figsize=(10, 6))
  ind = np.arange(len(df))

  # Create stacked bars for positive, negative, and neutral (if applicable)
  ax.barh(ind - width, df['positive'], width, color='green', label='Positive')
  ax.barh(ind , df['neutral'], width, color='gold', label='Neutral')
  ax.barh(ind + width, df['negative'], width, color='red', label='Negative')


  # Set y-axis labels and limits
  ax.set(yticks=ind + (width / 4) /2, yticklabels=df['brand'], ylim=[2 * width - 1, len(df)])
  ax.legend()
  plt.xlabel('Mentions Count')
  plt.title('Sentiment Distribution per Brand')
  plt.tight_layout()

  # Extract data for the second graph (average sentiment vs mention count)
  average_sentiments = []
  for brand, scores in brand_sentiments.items():
    total_score = scores['positive'] - scores['negative']
    mention_count = brand_mentions[brand]
    average_sentiment = total_score / (mention_count if mention_count > 0 else 1)
    average_sentiments.append(average_sentiment)

  # Create the second Matplotlib figure (scatter plot)
  plt.figure(figsize=(8, 6))
  for brand, sentiment_score in zip(brands, average_sentiments):
    mention_count = brand_mentions[brand]
    color = brand_colors.get(brand, 'gray')  # Use gray for unmapped brands
    plt.scatter(mention_count, sentiment_score, color=color, label=brand)

  plt.xlabel('Brand Mention Count')
  plt.ylabel('Average Sentiment Score')
  plt.title('Average Sentiment vs Brand Mention Count')
  plt.grid(True)
  plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust position as needed
  plt.tight_layout()

  # Display both Matplotlib figures
  plt.show()


def print_results(csv_file_path):
  """Prints a message indicating that the results are saved in the CSV file."""

  print(f"Brand sentiment analysis results are saved to '{csv_file_path}'.")


# Analyze the comments from the text file and save to CSV
analyze_text_file(text_file_path, csv_file_path)
# Print completion message
print_results(csv_file_path)
# Call visualization of results
visualize_results(brand_sentiments, brand_mentions)
input("Press Enter to continue...")
