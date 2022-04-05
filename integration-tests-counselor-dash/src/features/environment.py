from src.features.util import session
from src.features.util import driver, screenshot, configuration


def before_step(context, step):
    pass


def after_step(context, step):
    session.clear_cookies_if_required(session.Stage.step, context)
    if step.status == "failed":
        print("step failed")
        screenshot.capture_failure(context, step)


def before_scenario(context, scenario):
    context.browser.get(configuration.get_url("url"))


def after_scenario(context, scenario):
    session.clear_cookies_if_required(session.Stage.scenario, context)
    if scenario.status == "failed":
        screenshot.capture_failure(context, scenario)


def before_feature(context, feature):
    pass


def after_feature(context, feature):
    session.clear_cookies_if_required(session.Stage.feature, context)
    pass


def before_all(context):
    browsertype = configuration.get_browser()
    context.browser = driver.switch_browser(browsertype)
    context.browser.maximize_window()
    context.browser.implicitly_wait(15)
    # context.browser.get(configuration.get_url("url"))


def after_all(context):
    context.browser.close()
    context.browser.quit()