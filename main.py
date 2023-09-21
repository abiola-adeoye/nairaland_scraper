from datetime import datetime
from helper.nairaland import NairalandScrapper
from helper.save_to_excel import save_data_to_excel

word = input("What word do you want to search for: ")
yes = NairalandScrapper(word)
print("Started scraping")
aba = yes.scrape_nairaland()
time_of_scrape = datetime.now().strftime("%d/%m/%Y").replace("/","-")

file_name = word +" "+ time_of_scrape

for key in aba:
    print("saving page "+ str(key)+" to excel:")
    h = aba[key]['heading']
    p = aba[key]['post']
    save_data_to_excel(h, p, file_name=file_name)   # doesn't save properly when filename is too long
