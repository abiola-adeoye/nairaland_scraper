"""sometimes there are empty tr tags which have no data, in such situations len(tr) doesn't exceed 1 item
with find all, so we skip the rest of code if less than or equal to 1 item"""

import requests
from typing import Dict, List
from itertools import cycle
from bs4 import BeautifulSoup


class NairalandSoup:
    start_page = 0

    def __init__(self, search_word: str) -> None:
        self.search_word: str = search_word.replace(" ", "+")
        self.soup: str = ""
        self.url_structure: str = f"https://www.nairaland.com/search/{self.search_word}/0/0/0/"
        self.current_page = self.start_page
        self.last_page = 20

    def get_response(self):
        try:
            response = requests.get(self.url_structure + str(self.current_page))
            return response.content
        except Exception as err:
            print(err)

    def make_soup_object(self) -> None:
        page_content = self.get_response()
        self.soup = BeautifulSoup(page_content, 'lxml')

        self.get_num_search_results()

    def get_num_search_results(self) -> None:
        pagination_links = self.soup.p
        last_page_result_num = pagination_links.find_all('b')[-1].text
        self.last_page = last_page_result_num


class NairalandScrapper(NairalandSoup):

    def __init__(self, search_word):
        super().__init__(search_word)

    # gets number of search pages that turn up as result, soup object needs to be made to get this
    def get_num_search_results(self) -> str:
        next_page_links = self.soup.p
        num_search_page_results = next_page_links.find_all('b')[-1].text
        return num_search_page_results

    # this extracts the posts tags on result page (headline and actual post)
    def get_page_posts_tags(self):
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