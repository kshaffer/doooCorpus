[# doooCorpus
A corpus study of articles about Domain of One's Own. Includes a Python script for web scraping from a variety of blog/article sources, a Python script for converting manually downloaded content, and an R script for analyzing and visualizing downloaded data. Also contains a pre-loaded collection of scraped and cleaned data.

Blog posts based on the findings in this corpus study can be found at:

- [Domain of One’s Own: A Corpus Study, Part 1 – Words and Voices](http://umwdtlt.com/domain-of-ones-own-a-corpus-study-part-1-words-and-voices/)  
- [Domain of One’s Own: A Corpus Study, Part 2 – Bigrams and Changing Trends](http://umwdtlt.com/domain-of-ones-own-a-corpus-study-part-2-bigrams-and-changing-trends/)  
- [Domain of One’s Own: A Corpus Study, Part 3 – Sentiment Analysis](http://umwdtlt.com/domain-of-ones-own-a-corpus-study-part-3-sentiment-analysis/)  
- [Domain of One’s Own: A Corpus Study, Part 4 – Topic Model](http://umwdtlt.com/domain-of-ones-own-a-corpus-study-part-4-topic-model/)  

## `build_db.py`

This Python script scrapes the URLs in `url_list` and uses Beautiful Soup to parse their content for title, author, date, and main article text. Saves to `dooo_scraped.csv`. The resulting CSV file will need some manual cleanup before mining and analyzing with `dooo_tidy_analysis.R`.

## `dooo.py`

This Python script will take text from `no_scrape.txt` and parse it into the same format as the export of `build_db.py`. Useful for articles that fail during the scraping process. Simply paste the content into `no_scrape.txt` following the provided format, and `dooo.py` will process it. *Be sure to replace typographer's quotes and apostrophes with straight quotes and apostrophes first (find-and-replace) first, or the script will fail.*

## `dooo_tidy_analysis.R`

This R script contains the code necessary to mine and analyze the scraped and cleaned data, and to produce nifty visualizations. Be sure to install all packages included at the beginning of the file with `install.packages('package_name')` first. This script is meant to be run piece-by-piece, rather than all at once.

## `no_scrape.txt`

This text file contains manual copy-and-paste data for a number of articles that failed during the scraping process with `build_db.py`. 

## `dooo_all_data_Jan6_clean.csv`

This file contains the results of the scraping and manual cleaning processes, ready to go if you want to jump right to R and play around with analysis and visualization.

## Other data files

Other CSV files are automatically produced by the Python scripts. You can safely delete them if you like. However, I recommend hanging onto them and appending a date to them before running the scripts again, so you have a record of past scrapes and don't overwrite them.
