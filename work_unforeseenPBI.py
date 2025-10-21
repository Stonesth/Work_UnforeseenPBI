from Tools import tools_v000 as tools
from MyHours import myhours as m
from AzureDevOps import azuredevops as a
from ServiceNow import servicenow as sn
import os
from os.path import dirname
import time
import tkinter as tk
from tkinter import messagebox

import myhours_part







# -18 for the name of this project Work_UnforeseenPBI
# save_path = dirname(__file__)[ : -18]
save_path = os.path.dirname(os.path.abspath("__file__"))
propertiesFolder_path = save_path + "\\"+ "Properties"

# a.save_path = tools.readProperty(propertiesFolder_path, 'Work_UnforeseenPBI', 'save_path=')
# a.boards = tools.readProperty(propertiesFolder_path, 'Work_UnforeseenPBI', 'boards=')
# a.pbi = tools.readProperty(propertiesFolder_path, 'Work_UnforeseenPBI', 'pbi=')


a.iteration = tools.readProperty(propertiesFolder_path, 'Work_UnforeseenPBI', 'iteration=')
a.sprint = tools.readProperty(propertiesFolder_path, 'Work_UnforeseenPBI', 'sprint=')
# a.incidentNumber = tools.readProperty(propertiesFolder_path, 'Work_UnforeseenPBI', 'incidentNumber=')






# Open Browser
tools.openBrowserChrome()

# Condition to run MyHours part
if True:  # Replace True with your condition
    myhours_part.run_myhours_part(m, tools)

if True:
    # ServiceNow part
    sn.connectToServiceNow(sn.user_name)
    time.sleep(1)
    sn.connectToServiceNowIncidentChange(sn.incident_change_id)
    sn.collectData()

    print("Caller = ", sn.caller)
    print("incidentTitle = ", sn.incidentTitle )
    print("description_text = ", sn.description_text )

if True: 
    # Create a new PBI in Azure DevOps
    # def createNewPBI(iteration, sprint, caller, incidentTitle, description_text) :
    # ex : createNewPBI("2025.4", ".2", "JF30LB", "Test from automation", "This is a test from automation to create a new PBI in Azure DevOps")
    a.createNewPBI(a.iteration, a.sprint, sn.user_name, "RUN - " + sn.incident_change_id + " - " + sn.incidentTitle, "Caller = " + sn.caller + "\n" + sn.description_text)
else :
    # It's to test the findCreatedPBIID function without creating a new PBI
    tools.driver.get("https://dev.azure.com/NNBE/Finance/_backlogs/backlog/Finance%20Boards%20Team/Features?showParents=true&System.AreaPath=IT%20Finance&text=%5B" + a.iteration + "%5D%20IT%20Finance%20RUN&System.IterationPath=Finance%5CPI" + a.iteration)
    # wait until the page is loaded
    tools.waitLoadingPageByXPATH2(5, '//*[@id="__bolt-4"]/td[5]/div/a')


# Need to find in Azure DevOps the created PBI ID and fillin in the MyHours entry
print("Find the created PBI ID in Azure DevOps")
pbi_id = a.findCreatedPBIID("RUN - " + sn.incident_change_id + " - " + sn.incidentTitle)

if pbi_id == "" :
    print("Error : PBI ID not found")
    tools.closeBrowser()
    exit(1)
    
# Need to call the project StartPBI to fillin the MyHours entry with the found PBI ID
# Need to update the Properties/StartPBI.properties file with the found PBI ID
# def updateProperty(propertiesFolder_path, projectName, property_name, property_value) :
# for the propertiesFolder_path we need to have something like :
# C:\\Users\\JF30LB\\Projects\\python\\Projects\\StartPBI\\Properties
startpbi_properties_path = os.path.join(os.path.dirname(save_path), "StartPBI", "Properties")
tools.updateProperty(startpbi_properties_path, 'StartPBI', 'pbi=', pbi_id)

tools.updateProperty(save_path + "\\" + "Properties", 'StartPBI', 'pbi=', pbi_id)

# Need to run the StartPBI.py python script
os.system('python "' + os.path.join(os.path.dirname(save_path), "StartPBI", "start_pbi.py") + '"')


time.sleep(20)