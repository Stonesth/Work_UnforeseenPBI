from Tools import tools_v000 as tools
from MyHours import myhours as m
from AzureDevOps import azuredevops as a
from ServiceNow import servicenow as sn
import os
from os.path import dirname
import time
import tkinter as tk
from tkinter import messagebox








# -18 for the name of this project Work_UnforeseenPBI
# save_path = dirname(__file__)[ : -18]
save_path = os.path.dirname(os.path.abspath("__file__"))
propertiesFolder_path = save_path + "\\"+ "Properties"

# a.save_path = tools.readProperty(propertiesFolder_path, 'Work_UnforeseenPBI', 'save_path=')
# a.boards = tools.readProperty(propertiesFolder_path, 'Work_UnforeseenPBI', 'boards=')
# a.pbi = tools.readProperty(propertiesFolder_path, 'Work_UnforeseenPBI', 'pbi=')


a.iteration = tools.readProperty(propertiesFolder_path, 'Work_UnforeseenPBI', 'iteration=')
a.sprint = tools.readProperty(propertiesFolder_path, 'Work_UnforeseenPBI', 'sprint=')
a.incidentNumber = tools.readProperty(propertiesFolder_path, 'Work_UnforeseenPBI', 'incidentNumber=')






# Open Browser
tools.openBrowserChrome()

# MyHours part
m.connectToMyTimeTrack()

# afficher une popup expliquant qu'il faut se connecter une première fois
# Et installer l'extension chrome pour retenir les users et password
def show_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Information", "Please connect for the first time and install the Chrome extension to remember the users and passwords.")
    root.destroy()


print ("Test if we need to wait the page of the user / password")
if tools.waitLoadingPageByID2(5, 'email-label') :
    # show_popup()
    # print ("Need to wait the page of the password")
    # tools.waitLoadingPageByID2(10, 'email-label')
    # time.sleep(30)
    m.enterCredentials2()

time.sleep(1)

# Force refresh the page
tools.driver.refresh()

# Start tracking time
m.startTrack2()
time.sleep(1)

# ServiceNow part
sn.connectToServiceNow(sn.user_name)
time.sleep(1)
sn.connectToServiceNowIncidentChange(sn.incident_change_id)
sn.collectData()

print("Caller = ", sn.caller)
print("incidentTitle = ", sn.incidentTitle )
print("description_text = ", sn.description_text )

# Create a new PBI in Azure DevOps
# def createNewPBI(iteration, sprint, caller, incidentTitle, description_text) :
# ex : createNewPBI("2025.4", ".2", "JF30LB", "Test from automation", "This is a test from automation to create a new PBI in Azure DevOps")
a.createNewPBI(a.iteration, a.sprint, sn.user_name, "RUN - " + a.incidentNumber + " - " + sn.incidentTitle, "Caller = " + sn.caller + "\n" + sn.description_text)


time.sleep(20)