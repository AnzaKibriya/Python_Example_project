from src.features.pages.common.basepage import BASEPAGE
from src.features.pages.common.commonlocators import COMMONLOCATORS
from selenium.webdriver.common.by import By
from src.features.util import configuration
import time, random



class WYRPAGE(BASEPAGE):

    locator_dictionary_wyr_page = {
        "wyr_page_heading": (By.XPATH, './/h3'),
        "questionnaire_container": (By.XPATH, './/div[contains(@class, "Questionnaire-container")]'),
        "progress_bar": (By.XPATH, './/div[contains(@class, "progressBar")]'),
        "left_survey_card": (By.XPATH, './/div[@role = "button" and contains(@class, "Activity-optionLeft")]'),
        "right_survey_card": (By.XPATH, './/div[@role = "button" and contains(@class, "Activity-optionRight")]'),
        "start_wyr_assessment": (By.XPATH, './/div[text() = "Would You Rather"]/../button'),
        "wyr_result_page_top_line": (By.XPATH, './/p[contains(@class,"Results")]'),
        "interests_headings": (By.XPATH, './/span[contains(@class,"ProgramCard-topRowContainer")]/div[1]'),
        "interest_choose_buttons": (By.XPATH, './/button[contains(@class,"ProgramCard-chooseButton")]')
    }

    constants = {
        "wyr_page_heading": 'Would You Rather...',
        "progress_bar_attr": 'value',
        "wyr_result_page_top_line": 'Here are the results of the survey based on the choices you made.'
    }

    def __init__(self, context):
        self.common_locators = COMMONLOCATORS.common_locators(self)
        self.browser = context.browser

    def navigate_to(self):
        self.browser.get(configuration.get_url("url") + "/wyr")
        return self.is_at()

    def is_at(self):
        heading = self.get_element_text(
            self.find_element(
                self.locator_dictionary_wyr_page['wyr_page_heading']
            )
        )
        return heading == self.constants["wyr_page_heading"]

    def get_percentage(self):
        return self.get_attribute(
            self.find_element(self.locator_dictionary_wyr_page["progress_bar"])
            , self.constants["progress_bar_attr"]
        )

    def get_card_text(self, side):
        if side == "right":
            return self.get_element_text(self.find_element(self.locator_dictionary_wyr_page["right_survey_card"]))
        else:
            return self.get_element_text(self.find_element(self.locator_dictionary_wyr_page["left_survey_card"]))

    def click_left_right(self, option):
        prev_card_text = self.get_card_text("right")

        if option.lower() == "right":
            self.click_element(
                self.find_element(self.locator_dictionary_wyr_page["right_survey_card"])
            )
        elif option.lower() == "left":
            self.click_element(
                self.find_element(self.locator_dictionary_wyr_page["left_survey_card"])
            )

        try:
            current_card_text = self.get_card_text("right")
        except:
            return 1

        while(prev_card_text == current_card_text):
            try:
                current_card_text = self.get_card_text("right")
            except:
                if (prev_card_text == current_card_text):
                    break

    def complete_survey(self):
        options = ["left", "right"]
        while (self.is_element_displayed(self.locator_dictionary_wyr_page["questionnaire_container"])):
            self.click_left_right(random.choice(options))

    def click_on_start_assessment(self):
        self.click_element(
            self.find_element(
                self.locator_dictionary_wyr_page["start_wyr_assessment"]
            )
        )

    def is_at_result_page(self):
        return self.get_element_text(
            self.find_element(
                self.locator_dictionary_wyr_page["wyr_result_page_top_line"]
            )
        ) == self.constants["wyr_result_page_top_line"]

    def select_interest(self, interest):
        interest_elems = self.find_elements(self.locator_dictionary_wyr_page["interests_headings"])
        choose_buttons = self.find_elements(self.locator_dictionary_wyr_page["interest_choose_buttons"])

        for i in range(0, len(interest_elems)-1):
            if self.get_element_text(interest_elems[i]) == interest:
                self.click_element(choose_buttons[i])
                break
