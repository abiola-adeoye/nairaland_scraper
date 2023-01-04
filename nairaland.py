"""sometimes there are empty table row tags which have no data, in such situations len(tr) doesn't exceed 1 item
with find all, so we skip the rest of code if less than or equal to 1 item"""
import requests
from typing import Dict, List, Union, Optional, Any
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

    def _get_response(self) -> Union[str, bytes]:
        """ Gets the response content of page we want to scrape"""
        try:
            response = requests.get(self.url_structure + str(self.current_page))
            return response.content
        except Exception as err:
            print(err)

    def make_soup_object(self) -> None:
        """Make beautifulsoup object of page we want to scrape"""
        page_content = self._get_response()
        self.soup = BeautifulSoup(page_content, 'lxml')

    def _get_num_search_results(self) -> None:
        """Gets the total number of result pages for the searched word"""
        pagination_links = self.soup.p
        last_page_result_num = pagination_links.find_all('b')[-1].text
        self.last_page = int(last_page_result_num)


class NairalandScrapper(NairalandSoup):

    def __init__(self, search_word):
        super().__init__(search_word)
        super().make_soup_object()
        super()._get_num_search_results()

        self.headline_mod_cycle = cycle([0, 1])
        self.headline_mod_num = next(self.headline_mod_cycle)

        self.post_mod_cycle = cycle([1, 0])
        self.post_mod_num = next(self.post_mod_cycle)

    # function to call
    def scrape_nairaland(self) -> dict[int, dict[Any, Any]]:
        data = {}
        while True:
            heading = []
            post = []
            data[self.current_page] = {}
            page_tags = self._get_page_tr()
            for index in range(len(page_tags)):
                if index % 2 == self.headline_mod_num:
                    details = self._get_headline_details(post_headline=page_tags[index])
                    heading.append(details)
                elif index % 2 == self.post_mod_num:
                    details = self._get_post_details(post_content=page_tags[index])
                    post.append(details)
            data[self.current_page]['heading'] = heading
            data[self.current_page]['post'] = post
            self.current_page += 1

            if self.current_page == self.last_page:
                break
            self.make_soup_object()

            # reset the itertool cycle so the empty tag check is reset for next page
            self.headline_mod_cycle = cycle([0, 1])
            self.headline_mod_num = next(self.headline_mod_cycle)

            self.post_mod_cycle = cycle([1, 0])
            self.post_mod_num = next(self.post_mod_cycle)
        return data

    # extracts table row tags on result page (headline and actual post)
    def _get_page_tr(self) -> List[str]:
        nairaland_stats_for_day = self.soup.table   # I want to extract data here to use
        post_block = nairaland_stats_for_day.find_next_sibling("table")
        page_tr = post_block.find_all("tr")
        return page_tr

    # for get heading
    @staticmethod
    def _get_headline_text(headline_tag_data: List[str]) -> List[str]:
        return [headline.text for headline in headline_tag_data[-3::]]

    @staticmethod
    def _get_time_tag(headline_data):
        return headline_data.find('span', {'class': 's'})

    @staticmethod
    def _get_time_post(time_tag):
        if time_tag:
            return time_tag.text
        return "not available"

    @staticmethod
    def _check_heading_tr_tag_empty(tr_tag_value):
        if len(tr_tag_value) <= 1:      # should be <= 1
            return True

    # for get post
    @staticmethod
    def _extract_post_block(post_table_tr_data):
        return post_table_tr_data.find('div')

    @staticmethod
    def _extract_blockquote(post_block_data):
        """ Extracts the tag where a previous post is quoted, returns the tag or None"""
        return post_block_data.find('blockquote')

    @staticmethod
    def _extract_quote_status(blockquote_data) -> bool:
        """Returns True if there was a quote"""
        if blockquote_data:
            return True
        return False

    @staticmethod
    def _extract_quote_text(blockquote_data) -> str:
        if blockquote_data:
            quoted_post = blockquote_data.extract().text
            return quoted_post
        return blockquote_data

    @staticmethod
    def _extract_post_statistic(post: str) -> str:
        post_statistics = post.find('p')  # likes and shares
        if post_statistics:
            return post_statistics.text
        return ""

    def _get_headline_details(self, post_headline: str) -> Optional[dict[str, Union[str, Any]]]:
        headline_details = {}
        headline_values = post_headline.find_all("a")
        if self._check_heading_tr_tag_empty(headline_values):  # if True post table row tag is empty, i.e. no post
            self.headline_mod_num = next(self.headline_mod_cycle)
            self.post_mod_num = next(self.post_mod_cycle)
            return {'board':"",'post_title':"",'posted_by_user':"",'time_of_post':""}

        time = self._get_time_tag(post_headline)
        headline_text = self._get_headline_text(headline_values)

        headline_details['board'] = headline_text[0]
        headline_details['post_title'] = headline_text[1]
        headline_details['posted_by_user'] = headline_text[2]
        headline_details['time_of_post'] = self._get_time_post(time)
        return headline_details

    def _get_post_details(self, post_content: str) -> Dict[str, str]:
        post_details = {}
        post_block = self._extract_post_block(post_content)

        blockquote = self._extract_blockquote(post_block)
        post_details['quote'] = self._extract_quote_status(blockquote)
        post_details['quoted_post'] = self._extract_quote_text(blockquote)
        post_details['post_text'] = post_block.text
        post_details['statistics'] = self._extract_post_statistic(post_content)

        return post_details
