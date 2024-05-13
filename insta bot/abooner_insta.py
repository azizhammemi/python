from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import tkinter as tk


EMAIL = ""
PASSWORD = ""
MENTOR_USERNAME = ""
INSTAGRAM_URL = "https://www.instagram.com/"
MAX_FOLLOWERS_PER_HOUR = 50

class InstaFollower:
    def __init__(self, driver_path=None, text_area=None, num_to_follow=10):
        if driver_path:
            self.driver = webdriver.Chrome(driver_path)
        else:
            self.driver = webdriver.Chrome()
        self.text_area = text_area
        self.num_to_follow = num_to_follow
        self.followed_count = 0
        self.hourly_followed_count = 0
        self.start_time = datetime.now()
        self.last_follow_time = datetime.now()

    def login(self, url, email, password):
        # open Instagram
        self.driver.get(url=url)
        sleep(5)
        
        # login
        email_input = self.driver.find_element(By.NAME, "username")
        email_input.send_keys(email)

        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        sleep(2)
        password_input.send_keys(Keys.ENTER)
        sleep(5)

    def find_followers(self, url, account):
        # get profile
        sleep(5)
        self.driver.get(url=f"{url}{account}/?hl=en")
        sleep(7)
        
        followers = self.driver.find_element(By.XPATH, "//a[contains(@href,'/followers/')]")
        followers.click()



    def follow(self, num_to_follow=10):
        self.update_text("Follow start. Number of followers to follow: {0}".format(num_to_follow))
        sleep(5)
        
        buttons = self.driver.find_elements(By.CSS_SELECTOR, "._aano div div button")

        for button in buttons:
            if self.followed_count >= num_to_follow or self.hourly_followed_count >= MAX_FOLLOWERS_PER_HOUR:
                break
                
            if button.text.lower() == 'follow':
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
                
                button.click()
                self.update_text(button.text)
                self.last_follow_time = datetime.now()
                sleep(2)

        self.update_text("Follow end")

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
        master.mainloop()

    def create_widgets(self):
        tk.Label(self.master, text="Enter your Instagram username:",fg="red",bg="black", font=("Helvetica", 12, "bold")).pack()
        self.email_entry = tk.Entry(self.master,bg="gray",width=20)
        self.email_entry.pack()

        tk.Label(self.master, text="Enter your Instagram password:", fg="red",bg="black", font=("Helvetica", 12, "bold")).pack()  # Set the text color to red
        self.password_entry = tk.Entry(self.master, show="*",bg="gray",width=20)
        self.password_entry.pack()

        tk.Label(self.master, text="Enter mentor's Instagram username:",fg="red",bg="black", font=("Helvetica", 12, "bold")).pack()
        self.username_entry = tk.Entry(self.master,bg="gray",width=20)
        self.username_entry.pack()

        tk.Label(self.master, text="Enter number how follewer do you want max50:",fg="red",bg="black", font=("Helvetica", 12, "bold")).pack()
        self.num_to_follow_entry = tk.Entry(self.master,bg="gray",width=20)
        self.num_to_follow_entry.pack()

        self.text_area = tk.Text(self.master, height=20, width=50,bg="gray")
        self.text_area.pack()

        self.start_button = tk.Button(self.master, text="Start Bot",fg="red",bg="black", font=("Helvetica", 12, "bold"), command=self.start_bot)
        self.start_button.pack()

    def start_bot(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        username = self.username_entry.get()
        num_to_follow = int(self.num_to_follow_entry.get())

        bot = InstaFollower(text_area=self.text_area, num_to_follow=num_to_follow)
        bot.login(url=INSTAGRAM_URL, email=email, password=password)
        bot.find_followers(url=INSTAGRAM_URL, account=username)

        bot.follow(num_to_follow=num_to_follow)


if __name__ == "__main__":
    root = tk.Tk()
    app = InstaBotGUI(root)
    root.mainloop()
