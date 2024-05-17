import praw
import csv
from tqdm import tqdm

csv_file_path = "C:/Users/DICT/Desktop/BrandCommentAnalysis/CSVResults/RedditScraperResults.csv"
text_file_path = "C:/Users/DICT/Desktop/BrandCommentAnalysis/TXTResults/scrapedText.txt"

reddit = praw.Reddit(user_agent=True, client_id="mJQZkgxNUcvHsYwVDr23dQ", client_secret="zzUYSxZEcoo19vQqDE5-nO2CzDkO2g", username='Remyrraj',
                    password='Santos016', ratelimit_seconds=300)

url="https://www.reddit.com/r/AskReddit/comments/vt6nn/reddit_most_of_us_are_cheap_and_willing_to_go/"
submission = reddit.submission("vt6nn")
print(submission.title)
print(submission.selftext)
print("Reading all commetns...")
submission.comments.replace_more(limit=None)
##for comments in post.comments:
##    print(comments.body)
submissionCount =0
commentsCount = 0
with open(csv_file_path, 'a', newline='', encoding="utf-8") as csvfile:                 #Writing a csv file with UTF-8 encoding
        writer = csv.writer(csvfile)                                                        #New Instance of csv.writer
        print(f"scraping post {submissionCount}")
        for comment in tqdm(submission.comments.list(), desc = "Writing csv", unit = "comments"):  #list() Returns a flattened list of all comments     
            commentsCount += 1
            writer.writerow([submission.id,submission.permalink,submission.title,submission.selftext,comment.body])

commentsCount = 0    
# Open the file for writing in append mode (adds content without overwriting)
with open(text_file_path, "a", encoding="utf-8") as output_file:
    submission = reddit.submission(url=url)
    # Write post title
    output_file.write(f"Title: {submission.title}\n")
    # Write self-text (if it exists)
    if submission.selftext:
        output_file.write(f"Self Text: {submission.selftext}\n")
    # Write comments
    output_file.write("Comments:\n")
    for comment in tqdm(submission.comments.list(), desc = "Writing TXT", unit = "comments"):
        commentsCount += 1
        output_file.write(f"{comment.body}\n")


print("finished")
