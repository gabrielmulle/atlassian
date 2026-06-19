"""
Autoselect (pyautogui)

This first script, mouse-pos.py, is to discover the mouse coordinates in the screen
"""

import pyautogui

while True:
        x, y = pyautogui.position()
        positionStr = 'x: ' + str(x).rjust(4) + ' y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\\b' * len(positionStr), end='', flush=True)


"""
Run the script in the second screen, and in the main screen, move the cursor to the place where you want to see the coordinate. Take note of the coordinates, we will need it to set up the second script.
The second script, autoselect.py, will autonomously select the projects and spaces in the CMA tools based on the names or keys from a CSV file.
"""

import pandas
import time
import pyautogui
pyautogui.FAILSAFE = True

# 1. You'll need a csv file named 'projects.csv', with the header 'name', and all the names or keys you want the script to select
# 2. Prepare the CMA in the main monitor, and put it in the projects selection phase, sort by name asc
# 3. Start the script in the second monitor, and move the mouse to the main monitor
# PS: The 'pyautogui.FAILSAFE = True' is a failsafe feature that will stop the script from executing if you move the mouse to the 0 position (top left corner)

# In this case, I'm use an absolute location/folder, but you can just use the csf file name (e.g projects.csv), and put the csv in the same location as the script
source = pandas.read_csv('/Users/gabrielmuller/Documents/Clients/NCR/autoselect/projects.csv')

# 5 seconds to prepare
time.sleep(5) 

for _, row in source.iterrows():
    
    # output the current item
    print("Selecting project ", row["name"]) 

    # move mouse to search box
    pyautogui.moveTo(515, 600, duration=0.3) 
    pyautogui.click()
    
    # select all text
    pyautogui.hotkey('ctrl', 'a') 
    
    # search for the current item
    pyautogui.write(row['name'], interval=0.1) 
    
    # 3 seconds to allow the application to load the items
    time.sleep(3)
    
    # check the box to add the item to the selection
    pyautogui.moveTo(575, 695, duration=0.3, tween=pyautogui.easeInOutQuad) 
    pyautogui.click()
    time.sleep(1)

