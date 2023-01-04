## Nairaland scraper(still under development, mostly refining the code)

Nairaland is a Nigerian English-language internet forum. Founded by Nigerian entrepreneur Seun Osewa on March 8, 2005, it is targeted primarily at Nigerian domestic residents and is the 6th most visited website in Nigeria.

The webscraper built here receives a search term one would want to find out about on the nairaland platform search for post on these search terms, extract the pages of results, extract all post on these pages as well as the details of the post like the board it was posted on and more then save to an excel file. the plan is to save the excel file to a blob storage on azure but this has not been implemented yet.

to use the scraper, pull the code, install the requirements and run the naira.py file, enter the word you want to extract data on from nairaland for now don't enter a length word (not more than 15 chars, issues with saving to excel)

A more detailed Readme file would be added in the future
