import time
import tkinter as tk
from tkinter import messagebox

def run_myhours_part(m, tools):
    m.connectToMyTimeTrack()

    def show_popup():
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showinfo("Information", "Please connect for the first time and install the Chrome extension to remember the users and passwords.")
        root.destroy()

    print("Test if we need to wait the page of the user / password")
    if tools.waitLoadingPageByID2(5, 'email-label'):
        # show_popup()
        # print("Need to wait the page of the password")
        # tools.waitLoadingPageByID2(10, 'email-label')
        # time.sleep(30)
        m.enterCredentials2()

    time.sleep(1)
    # Force refresh the page
    tools.driver.refresh()
    # Start tracking time
    m.startTrack2()
    time.sleep(1)
