from datetime import datetime
import tkinter as tk
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

EMAIL = ""
PASSWORD = ""
MENTOR_USERNAME = ""
INSTAGRAM_URL = "https://www.instagram.com/"
MAX_FOLLOWERS_PER_HOUR = 50

class InstaFollower:
    def __init__(self, text_area=None, num_to_follow=10, driver_path=None):
        if driver_path:
            self.driver = webdriver.Chrome(driver_path)
        else:
            self.driver = webdriver.Chrome()
        
        self.text_area = text_area
        self.num_to_follow = num_to_follow
        self.followed_count = 0
        self.hourly_followed_count = 0
        self.last_follow_time = datetime.now()

    def login(self, url, email, password):
        self.update_text("Logging in to Instagram...")
        self.driver.get(url=url)
        sleep(5)
        
        email_input = self.driver.find_element(By.NAME, "username")
        email_input.send_keys(email)

        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        sleep(2)
        password_input.send_keys(Keys.ENTER)
        sleep(5)
        self.update_text("Successfully logged in!")

    def find_followers(self, url, account):
        self.update_text("Finding followers...")
        self.driver.get(url=f"{url}{account}")
        sleep(7)

        element = self.driver.find_element(By.CLASS_NAME, "x78zum5")
        followers_list = element.find_elements(By.TAG_NAME, "li")

        if len(followers_list) >= 3:
            followers_list[2].click()
        else:
            self.update_text("Insufficient followers to click on the 3rd element")
        
        sleep(3)

    def unfollow_target_users(self):
        self.update_text("Unfollow start")

        elements = self.driver.find_elements(By.XPATH, "//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x6s0dn4 xozqiw3 x1q0g3np']/div[3]")

        for i in range(min(len(elements), self.num_to_follow)):
            if self.followed_count >= self.num_to_follow or self.hourly_followed_count >= MAX_FOLLOWERS_PER_HOUR:
                break
            self.followed_count += 1
            self.hourly_followed_count += 1
            current_time = datetime.now()
            time_diff = (current_time - self.last_follow_time).seconds
            if time_diff < 3600 and self.hourly_followed_count >= MAX_FOLLOWERS_PER_HOUR:
                remaining_time = 3600 - time_diff
                self.update_text("Maximum number of followers followed per hour reached. Sleeping for {0} seconds.".format(remaining_time))
                break
                
            if self.hourly_followed_count > MAX_FOLLOWERS_PER_HOUR:
                self.update_text("Maximum number of followers followed per hour exceeded.")
                break

            sleep(1)
            element = elements[i]
            element.click()
            sleep(1)
            unfollow_button = self.driver.find_element(By.XPATH, "//button[@class='_a9-- _ap36 _a9-_']")
            unfollow_button.click()
            self.update_text(f"Unfollow successful for element {i+1}")
            self.last_follow_time = datetime.now()

        self.update_text("Finished unfollowing elements")

    def update_text(self, message):
        if self.text_area:
            self.text_area.insert(tk.END, message + "\n")
            self.text_area.see(tk.END)

class InstaBotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Instagram Bot")
        self.master.config(bg="black")  # Définir la couleur de fond en noir
   
         
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Enter your Instagram username:",fg="red",bg="black", font=("Helvetica", 12, "bold")).pack()
        self.email_entry = tk.Entry(self.master,bg="gray")
        self.email_entry.pack()

        tk.Label(self.master, text="Enter your Instagram password:",fg="red",bg="black", font=("Helvetica", 12, "bold")).pack()
        self.password_entry = tk.Entry(self.master, show="*",bg="gray")
        self.password_entry.pack()

        tk.Label(self.master, text="Enter your Instagram username:",fg="red",bg="black", font=("Helvetica", 12, "bold")).pack()
        self.username_entry = tk.Entry(self.master,bg="gray")
        self.username_entry.pack()

        tk.Label(self.master, text="Enter number to unfollow max50:",fg="red",bg="black", font=("Helvetica", 12, "bold")).pack()
        self.num_to_unfollow_entry = tk.Entry(self.master,bg="gray")
        self.num_to_unfollow_entry.pack()

        self.text_area = tk.Text(self.master,bg="gray",height=20, width=50)
        self.text_area.pack()

        self.start_button = tk.Button(self.master, text="Start Bot",fg="red",bg="black", font=("Helvetica", 12, "bold"), command=self.start_bot)
        self.start_button.pack()

    def start_bot(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        username = self.username_entry.get()
        num_to_unfollow = int(self.num_to_unfollow_entry.get())

        bot = InstaFollower(text_area=self.text_area, num_to_follow=num_to_unfollow)
        bot.login(url=INSTAGRAM_URL, email=email, password=password)
        bot.find_followers(url=INSTAGRAM_URL, account=username)
        bot.unfollow_target_users()

if __name__ == "__main__":
    root = tk.Tk()
    app = InstaBotGUI(root)
    root.mainloop()