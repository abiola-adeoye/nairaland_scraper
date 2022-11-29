# any method that is not protected needs to be improved.
# sometimes there are empty table rows in nairaland which don't have any data but the table row tag shows
# in such situations table row data doesn't exceed 1 item with find all, so we skip the rest of code if less
# than or equal to 1 item

import requests
from typing import Dict, List
from bs4 import BeautifulSoup


class NairalandScrapper(object):

    def __init__(self, search_word):
        self.search_word = search_word
        self.url_structure = "https://www.nairaland.com/search/{search_term}/0/0/0/{page}"
        self.soup = ""
        self.page = 0

    def get_nairaland_data(self):
        self.__make_soup()
        pass

    # makes request to nairaland with the inputted search term, can currently take one worded search terms
    # i want to take multiple worded search terms
    def get_request_content(self):
        response = requests.get(self.url_structure.format(search_term=self.search_word, page=self.page))
        return response.content

    # makes the soup object
    def __make_soup(self):
        page_content = self.__get_request_content()
        self.soup = BeautifulSoup(page_content, 'lxml')

    # gets number of search pages that turn up as result, soup object needs to be made to get this
    def __get_num_search_results(self) -> str:
        next_page_links = self.soup.p
        num_search_page_results = next_page_links.find_all('b')[-1].text
        return num_search_page_results

    # this extracts the posts tags on result page (headline and actual post)
    def get_page_posts_tags(self) -> List[str]:
        nairaland_stats_for_day = self.soup.table   # i want to extract data here to use
        post_table = nairaland_stats_for_day.find_next_sibling("table")
        post_table_tr = post_table.find_all("tr")
        return post_table_tr

    # extracts time of post,
    # needs working on
    def extract_post_time(self, post_data_list: List[str]) -> Dict:    # post headline start from 1st tr tag
        post_data = []
        for post_id in range(0, len(post_data_list), 2):
            post_headline_data = {}

            headline = post_data_list[post_id].find_all("a")
            if len(headline) <= 1:  # check if post is empty
                continue
            time = self.extract_time_tag(post_data_list[post_id])
            headline_list = self.extract_post_headline(headline)

            post_headline_data['board'] = headline_list[0]
            post_headline_data['post_title'] = headline_list[1]
            post_headline_data['posted_by_user'] = headline_list[2]
            post_headline_data['time_of_post'] = self.extract_time_post(time)

            post_data.append(post_headline_data)
        return post_data

    @staticmethod
    def extract_post_headline(headline_tag_data):
        return [headline.text for headline in headline_tag_data[-3::]]

    def extract_time_tag(self, post_data):
        return post_data.find('span', {'class':'s'})

    def extract_time_post(self, time_tag_data):
        if time_tag_data:
            return time_tag_data.text
        return "not available"



    # functional, would have to check for variable names later
    def extract_post_text(self, post_data_list):
        post_data = []
        for post_id in range(1, len(post_data_list), 2):    # post start from 2nd tr tag
            nairaland_user_post = {}

            post_block = self.__extract_post_block(post_data_list[post_id])

            blockquote = self.extract_blockquote(post_block)
            nairaland_user_post['quote'] = self.extract_quote_status(blockquote)
            nairaland_user_post['quoted_post'] = self.extract_quote_data(blockquote)

            nairaland_user_post['post_text'] = post_block.text

            nairaland_user_post['statistics'] = self.extract_post_statistic(post_data_list[post_id])

            post_data.append(nairaland_user_post)   # adding dictionaries to a list brings up issues
        return post_data

    def __extract_post_block(self, post_table_tr_data):
        return post_table_tr_data.find('div')

    def __extract_blockquote(self, post_block_data):
        return post_block_data.find('blockquote')

    def __extract_quote_status(self, blockquote_data):
        if blockquote_data:
            return True
        return False

    def __extract_quote_text(self, blockquote_data):
        if blockquote_data:
            quoted_post = blockquote_data.extract().text
            return quoted_post
        return blockquote_data

    def __extract_post_statistic(self, post):
        post_statistics = post.find('p')  # likes and shares
        if post_statistics:
            return post_statistics.text
        return ""