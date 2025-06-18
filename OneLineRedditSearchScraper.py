import praw
import csv
from tqdm import tqdm

csv_file_path = "BrandCommentAnalysis/CSVResults/RedditScraperResults.csv"
text_file_path = "BrandCommentAnalysis/TXTResults/scrapedText.txt"
reddit = praw.Reddit(user_agent=True, client_id="CLIENT ID", client_secret="API KEY", username='USERNAME',
                    password='PASSWORD', ratelimit_seconds=300)

scrapedData = []

def print_results(csv_file_path, text_file_path):
  """Prints a message indicating that the results are saved in the CSV file."""

  print(f"Brand sentiment analysis results are saved to '{csv_file_path}'.")


def scrapeSearch(subredditName, searchQuery, searchLimit = 25):
    submissionCount = 0
    
    for submission in tqdm(reddit.subreddit(subredditName).search(query=searchQuery, sort="relevance", limit=searchLimit),
                           desc="Scraping Submissions",
                           unit="submissions"):
        submissionCount +=1
        submission_data = {
          "PostID": submission.id,
          "Permalink": submission.permalink,
          "Title": submission.title,
          "SelfText": submission.selftext
          }
        commentsCount = 0
        submission.comments.replace_more(limit=None)
        print(f"Scraping Post {submissionCount} from {subredditName} | ID:{submission.id}")
        for comment in tqdm(submission.comments.list(),desc="Scraping Comments", unit="comments"):  #list() Returns a flattened list of all comments     
            commentsCount += 1
##            print(f"scraping comment {commentsCount}")
            comment_data = {
            "Comment": comment.body
            }
            rowData = {**submission_data, **comment_data}
            scrapedData.append(rowData)
    return scrapedData


def writeFiles(data, csv_file_path, text_file_path):
    with open(csv_file_path, 'w', newline='', encoding="utf-8") as csvfile:                 #Writing a csv file with UTF-8 encoding
        print("writing csv...")
        writer = csv.writer(csvfile)                                                        #New Instance of csv.writer
        writer.writerow(["PostID", "Permalink", "Title", "SelfText", "Comment"])            #Assigning columns
        for item in data:
            writer.writerow([item['PostID'],item['Permalink'],item['Title'],item['SelfText'],item['Comment']])
    print("finished writing csv")
                
    # Open the file for writing in append mode (adds content without overwriting)
    with open(text_file_path, "w", encoding="utf-8") as output_file:
        print("writing txt...")
        for item in data:
          if item['SelfText']:
            output_file.write(f"Self Text: {item['SelfText']}\n")
          for comment in item['Comment']:
            output_file.write(f"{comment}")  # Assuming 'Comment' is a list of comments      
    print("finished writing txt")


scrapeSearch("AskReddit+femalefashionadvice+RunningShoeGeeks+minimalism+onebag", "shoe brand", 5)
writeFiles(scrapedData, csv_file_path, text_file_path)
