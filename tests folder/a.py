# Sentiment Analysis Library (replace with your preferred library)
from textblob import TextBlob
import csv


# Function to Analyze Review Characteristics (modify based on your criteria)
def review_characteristics(review):
  score = 0
  if len(review) < 50:
    score -= 1  # Short reviews penalized
  if "amazing" in review or "terrible" in review and len(review) < 100:
    score -= 2  # Strong sentiment words in short reviews penalized more
  return score

# Replace 'your_file.csv' with the actual path to your CSV file
with open('final_dataset.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)

  # Skip the header row (optional, if your file has a header row)
  next(reader, None)  # Skip header row

  for row in reader:
      # Access the review comment (assuming it's in the 4th column)
      reviews = row[3]
      for review in reviews:
          sentiment = TextBlob(review).sentiment.polarity  # Sentiment analysis (positive: > 0, negative: < 0)
          characteristic_score = review_characteristics(review)
          total_score = sentiment + characteristic_score
          
          # Flag for Potential Fakeness (adjust thresholds as needed)
          is_potentially_fake = total_score > 0.5 and characteristic_score < -1 or total_score < -0.5

          print(f"Review: {review}")
          print(f"Sentiment: {sentiment:.2f} (Positive) or {sentiment:.2f} (Negative)".format(sentiment, -sentiment))
          print(f"Characteristic Score: {characteristic_score}")
          print(f"Total Score: {total_score:.2f}")
          if is_potentially_fake:
            print("** This review is flagged as potentially fake based on sentiment and characteristics. **")
          print("-"*50)


# Analyze Each Review
##for review in reviews:
##  sentiment = TextBlob(review).sentiment.polarity  # Sentiment analysis (positive: > 0, negative: < 0)
##  characteristic_score = review_characteristics(review)
##  total_score = sentiment + characteristic_score
##
##  # Flag for Potential Fakeness (adjust thresholds as needed)
##  is_potentially_fake = total_score > 0.5 and characteristic_score < -1 or total_score < -0.5
##
##  print(f"Review: {review}")
##  print(f"Sentiment: {sentiment:.2f} (Positive) or {sentiment:.2f} (Negative)".format(sentiment, -sentiment))
##  print(f"Characteristic Score: {characteristic_score}")
##  print(f"Total Score: {total_score:.2f}")
##  if is_potentially_fake:
##    print("** This review is flagged as potentially fake based on sentiment and characteristics. **")
##  print("-"*50)
