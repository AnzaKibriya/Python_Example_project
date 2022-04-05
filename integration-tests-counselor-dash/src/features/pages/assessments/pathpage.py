from src.features.pages.common.basepage import BASEPAGE
from src.features.pages.common.commonlocators import COMMONLOCATORS
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from src.features.util import configuration
import time, random



class PATHPAGE(BASEPAGE):

    locator_dictionary_path_page = {
        "path_page_heading": (By.XPATH, './/h3'),
        "progress_bar": (By.XPATH, './/div[@role = "progressbar"]'),
        "yes_button": (By.XPATH, './/div[@role = "button" and contains(@class, "index-yes")]'),
        "no_button": (By.XPATH, './/div[@role = "button" and contains(@class, "index-no")]'),
        "rewind_button": (By.XPATH, './/div[@role = "button" and contains(@class, "index-rewind")]'),
        "maybe_button": (By.XPATH, './/div[@role = "button" and contains(@class, "index-maybe")]'),
        "survey_card": (By.XPATH, './/div[@id = "cards"]/div[contains(@style, "touch-action")]'),
        "personality_subtitle": (By.XPATH, './/div[@id = "app"]//div[contains(@class, "SelectCluster-subtitle")]'),
        "careers_for_you_button": (By.XPATH, './/button[contains(text() , "Careers For You")]'),
        "i_understand_button": (By.XPATH, './/button/span[contains(text() , "I Understand")]'),
        "cluster_cards": (By.XPATH, './/div[contains(@class , "SelectCluster-clusterCard")]'),
        "career_major_cards": (By.XPATH, './/div[contains(@class , "SelectCareer-clusterCard")]'),
        "path_result_title": (By.XPATH, './/div[contains(@class , "index-title")]'),
        "start_path_assessment": (By.XPATH, './/div[text() = "Find Your Path"]/../button')
    }

    constants = {
        "path_page_heading": 'Find Your Path',
        "progress_bar_attr": 'aria-valuenow',
        "personality_subtitle": 'Based on this quiz, you are someone who is...',
        "path_result_title": 'Find Your Path Results'
    }

    def __init__(self, context):
        self.common_locators = COMMONLOCATORS.common_locators(self)
        self.browser = context.browser

    def navigate_to(self):
        self.browser.get(configuration.get_url("url") + "/path")
        return self.is_at()

    def is_at(self):
        heading = self.get_element_text(
            self.find_element(
                self.locator_dictionary_path_page['path_page_heading']
            )
        )
        return heading == self.constants["path_page_heading"]

    def click_on_start_survey(self):
        self.click_element(
            self.find_element(
                self.common_locators['start_survey_button']
            )
        )

    def get_percentage(self):
        return self.get_attribute(
            self.find_element(self.locator_dictionary_path_page["progress_bar"])
            , self.constants["progress_bar_attr"]
        )

    def get_card_text(self):
        return self.get_element_text(self.find_element(self.locator_dictionary_path_page["survey_card"]))

    def click_on_yes_no_maybe_rewind(self, option):
        prev_percentage = int(self.get_percentage())
        prev_card_text = self.get_card_text()

        if option.lower() == "yes":
            self.click_element(
                self.find_element(self.locator_dictionary_path_page["yes_button"])
            )
        elif option.lower() == "no":
            self.click_element(
                self.find_element(self.locator_dictionary_path_page["no_button"])
            )
        elif option.lower() == "maybe":
            self.click_element(
                self.find_element(self.locator_dictionary_path_page["maybe_button"])
            )
        elif option.lower() == "rewind":
            self.click_element(
                self.find_element(self.locator_dictionary_path_page["rewind_button"])
            )

        current_card_text = self.get_card_text()
        while(prev_card_text == current_card_text):
            try:
                current_card_text = self.get_card_text()
            except:
                if (prev_card_text == current_card_text):
                    break


        current_percentage = int(self.get_percentage())
        if (current_percentage > prev_percentage and option.lower() != "rewind"):
            print("Clicked on button " + option +" successfully")
        elif (current_percentage < prev_percentage and option.lower() == "rewind"):
            print("Clicked on button " + option +" successfully")
        else:
            print("Progress bar didn't increased on clicking " + option +" button")

    def swipe_for_yes_no_maybe(self, dir):
        prev_percentage = int(self.get_percentage())
        card = self.find_element(self.locator_dictionary_path_page["survey_card"])
        self.swipe(card, dir)
        current_percentage = int(self.get_percentage())
        if (current_percentage > prev_percentage):
            print("Swiped to " + dir +" successfully")
        else:
            print("Progress bar didn't increased on swiping " + dir)


    def complete_survey_till_personalities(self):
        options = ["yes", "no", "maybe"]
        while (self.is_element_displayed(self.locator_dictionary_path_page["survey_card"])):
            print(self.get_percentage())
            self.click_on_yes_no_maybe_rewind(random.choice(options))


    def get_personailty_subtitles(self):
        elems = self.find_elements(self.locator_dictionary_path_page["personality_subtitle"])
        subtitles = []
        for elem in elems:
            subtitles.append(self.get_element_text(elem))
        return subtitles


    def is_on_personality_result_page(self):
        return len(self.get_personailty_subtitles()) > 0


    def click_on_button(self, button_text):
        if button_text == "Careers for you":
            self.click_element(self.find_element(self.locator_dictionary_path_page["careers_for_you_button"]))
        elif button_text == "I Understand":
            self.click_element(self.find_element(self.locator_dictionary_path_page["i_understand_button"]))


    def select_cards(self, number, card_type):
        if card_type == "cluster":
            cards = self.find_elements(self.locator_dictionary_path_page["cluster_cards"])
        elif card_type == "career" or card_type == "major":
            cards = self.find_elements(self.locator_dictionary_path_page["career_major_cards"])

        if len(cards) > 0:
            if number.lower() == "first":
                self.click_element(cards[0])
            elif number.lower() == "second":
                self.click_element(cards[1])
            elif number.lower() == "third":
                self.click_element(cards[2])
            elif number.lower() == "fourth":
                self.click_element(cards[3])
            self.click_element(self.find_element(self.common_locators["select_button"]))
            if (card_type != "major"):
                self.click_element(self.find_element(self.common_locators["continue_button"]))
            else:
                self.click_element(self.find_element(self.common_locators["see_results_button"]))


    def is_at_result_page(self):
        try:
            path_result_title = self.get_element_text(
                self.find_element(self.locator_dictionary_path_page["path_result_title"]))
        except:
            path_result_title = ""
        return path_result_title == self.constants["path_result_title"]


    def click_on_start_assessment(self):
        self.click_element(
            self.find_element(
                self.locator_dictionary_path_page["start_path_assessment"]
            )
        )
