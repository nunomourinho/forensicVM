from guibot.guibot import GuiBot


# Connect to the GUI

bot = GuiBot(vnc_host='127.0.0.1', vnc_port=5900)


# Locate the login form on the website

username_field = bot.locate_element(search_method='xpath', search_query='//input[@name="username"]')

password_field = bot.locate_element(search_method='xpath', search_query='//input[@name="password"]')

submit_button = bot.locate_element(search_method='xpath', search_query='//button[@type="submit"]')


# Fill in the form

username_field.send_keys('my_username')

password_field.send_keys('my_password')


# Submit the form

submit_button.click()
