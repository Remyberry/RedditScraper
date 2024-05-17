import praw
import csv
import time
import tkinter as tk
from tkinter import ttk
from tqdm import tqdm


csv_file_path = "C:/Users/DICT/Desktop/BrandCommentAnalysis/CSVResults/RedditScraperResults.csv"
text_file_path = "C:/Users/DICT/Desktop/BrandCommentAnalysis/TXTResults/scrapedText.txt"

reddit = praw.Reddit(user_agent=True,
                     client_id="mJQZkgxNUcvHsYwVDr23dQ",
                     client_secret="zzUYSxZEcoo19vQqDE5-nO2CzDkO2g",
                     username='Remyrraj',
                     password='Santos016',
                     ratelimit_seconds=300)

print(f"Logged in as {reddit.user.me()}")

scrapedData = []      #Initialize storage of data

def startScrape(subreddit_entry, query_entry, limit_entry):
    subredditName = subreddit_entry #.get()
    searchQuery = query_entry #.get()
    searchLimit = int(limit_entry) #.get()
    
    submissionCount = 0
    
    for submission in reddit.subreddit(subredditName).search(query=searchQuery, sort="relevance", limit=searchLimit):
        submissionCount +=1
        submission_data = {
          "PostID": submission.id,
          "Permalink": submission.permalink,
          "Title": submission.title,
          "SelfText": submission.selftext
          }
        
        commentsCount = 0
        # submission.comment_limit = 1000
        submission.comments.replace_more(limit=None)
        print(f"Scraping Post {submissionCount} from {subredditName} | ID:{submission.id}")
        # i = submission.num_comments
        for comment in tqdm(submission.comments.list(), desc = "Scraping Comments", unit = "comments"):  #list() Returns a flattened list of all comments     
            commentsCount += 1
            comment_data = {
            "Comment": comment.body
            }
            rowData = {**submission_data, **comment_data}
            scrapedData.append(rowData)
            time.sleep(0.01)
    return scrapedData


def writeFiles(data, csv_file_path, text_file_path):
    with open(csv_file_path, 'w', newline='', encoding="utf-8") as csvfile:                 #Writing a csv file with UTF-8 encoding
        writer = csv.writer(csvfile)                                                        #New Instance of csv.writer
        writer.writerow(["PostID", "Permalink", "Title", "SelfText", "Comment"])            #Assigning columns
        for item in tqdm(data, desc = "Writing csv file", unit = "rows"):
            writer.writerow([item['PostID'],item['Permalink'],item['Title'],item['SelfText'],item['Comment']])
                
    # Open the file for writing in append mode (adds content without overwriting)
    with open(text_file_path, "w", encoding="utf-8") as output_file:
        for item in tqdm(data, desc = "Writing txt file", unit = "rows"):
          if item['SelfText']:
            output_file.write(f"Self Text: {item['SelfText']}\n")
          for comment in item['Comment']:
            output_file.write(f"{comment}")  # Assuming 'Comment' is a list of comments

def appendFiles(data, csv_file_path, text_file_path):
    with open(csv_file_path, 'a', newline='', encoding="utf-8") as csvfile:                 #Writing a csv file with UTF-8 encoding
        writer = csv.writer(csvfile)                                                        #New Instance of csv.writer
        writer.writerow(["PostID", "Permalink", "Title", "SelfText", "Comment"])            #Assigning columns
        for item in tqdm(data, desc = "Writing csv file", unit = "rows"):
            writer.writerow([item['PostID'],item['Permalink'],item['Title'],item['SelfText'],item['Comment']])
                
    # Open the file for writing in append mode (adds content without overwriting)
    with open(text_file_path, "a", encoding="utf-8") as output_file:
        for item in tqdm(data, desc = "Writing txt file", unit = "rows"):
          if item['SelfText']:
            output_file.write(f"Self Text: {item['SelfText']}\n")
          for comment in item['Comment']:
            output_file.write(f"{comment}")  # Assuming 'Comment' is a list of comments


def build_gui():
    root = tk.Tk()
    root.geometry("600x400")
    root.title("Reddit Scraper")

    # Labels and Entry widgets
    label_subreddit = tk.Label(root, text="Subreddit:")
    label_subreddit.pack()
    subreddit_entry = tk.Entry(root)
    subreddit_entry.pack()

    label_query = tk.Label(root, text="Search Query:")
    label_query.pack()
    query_entry = tk.Entry(root)
    query_entry.pack()

    limit_label = tk.Label(root, text="Limit:")
    limit_label.pack()
    limit_entry = tk.Entry(root)
    limit_entry.pack()

    progress_bar = ttk.Progressbar(root, orient='horizontal', mode='indeterminate', length=200)
    progress_bar.pack(padx=20, pady=20)

    # Button to trigger scraping (pass entry widgets as arguments)
    button_scrape = tk.Button(root, text="Scrape", command=lambda: [progress_bar.start,
                                                                    startScrape(subreddit_entry, query_entry, limit_entry),
                                                                    appendFiles(scrapedData, csv_file_path, text_file_path),
                                                                    progress_bar.stop])
    button_scrape.pack(padx=10, pady=10)

    # button_write = tk.Button(root, text="Write", command=lambda: writeFiles(scrapedData, csv_file_path, text_file_path))
    # button_write.pack()

    # button_append = tk.Button(root, text="Append", command=lambda: appendFiles(scrapedData, csv_file_path, text_file_path))
    # button_append.pack()
    
    return root

# Main function
# def main():
#   root = build_gui()
#   root.mainloop()
  


# if __name__ == "__main__":
#   main()


startScrape("AskReddit", "best shoe brand", 50)
startScrape("femalefashionadvice", "best  brand", 50)
startScrape("RunningShoeGeeks", "best  brand", 50)
startScrape("minimalism", "best  brand", 50)
startScrape("onebag", "best  brand", 50)
startScrape("Sneakers", "best  brand", 50)

startScrape("AskReddit", "worst shoe brand", 50)
startScrape("femalefashionadvice", "worst shoe brand", 50)
startScrape("RunningShoeGeeks", "worst  brand", 50)
startScrape("minimalism", "worst  brand", 50)
startScrape("onebag", "worst  brand", 50)
startScrape("Sneakers", "worst  brand", 50)
writeFiles(scrapedData, csv_file_path, text_file_path)
input("Press Enter to continue...")