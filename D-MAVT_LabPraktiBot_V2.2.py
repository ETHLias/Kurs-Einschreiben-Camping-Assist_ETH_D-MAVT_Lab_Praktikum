# For publish


#.\pyinstaller D-MAVT_LabPraktiBot_V2.2.py --onefile --icon=.\icon.ico --window --paths=.\venv\Lib --additional-hooks-dir .\venv

#python.exe -m pip install --upgrade pip

import usernamecheck

with open('Password.txt') as f:
    line = f.readline()

#print(line)

import os
import re
import tkinter.messagebox
from time import sleep
from datetime import datetime

import threading
import tkinter

import playsound as playsound
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


# Refresh Time in Second -----------------------------------------------------------------------------------------------
#Refresh_Time = simpledialog.askinteger(title='D-MAVT', prompt='Refresh Time in second')
Refresh_Time = 300

#simpledialog.askstring(title='D-MAVT', prompt='Username:  ' + Username + '\nPassword: ')
PassWord = line

# Old Eintrag Number
# Num = simpledialog.askinteger(title='D-MAVT', prompt='User: ' + Username + '\nOld Eintrag Numebr: ')
Num = simpledialog.askinteger(title='D-MAVT', prompt='\nOld Eintrag Numebr: ')

Num_old = str(Num)


def log_in_func_fill(dri, username):
    # Get the title of the header
    current_title = dri.title

    log_in_found = False

    if 'Web Login' in current_title:
        log_in_found = True

    if 'Web Anmel' in current_title:
        log_in_found = True

    if log_in_found:

        # Locate the fill and insert login data
        username_fill_1 = dri.find_element(By.ID, 'username')
        password_fill_1 = dri.find_element(By.ID, 'password')
        username_fill_1.send_keys(username)
        password_fill_1.send_keys(PassWord)

        # Locate Login button and lick it. UwU
        login = dri.find_element(By.NAME, '_eventId_proceed')
        login.click()

        current_title = dri.title
        if 'Mandant' in current_title:
            return True
    return False
# Ture for Login successful and now at the Mandant Page
# False for not at the Mandant Page


def log_in_func_1(dri, username):

    # Request of the Webpage
    dri.get('https://www.lehrbetrieb.ethz.ch/laborpraktika/mandantAuswahl.view')



    i = 0
    while True:
        # Get the title of the header
        current_title = dri.title

        if 'Login' in current_title:

            # Lick the Start
            next_move = dri.find_element(By.CLASS_NAME, 'submit')
            next_move.click()

            if log_in_func_fill(dri, username):
                # Login successful
                return True

            # When login failed

        if 'Mandant' in current_title:
            return True

        # Try again for 6 times
        dri.close()
        dri = webdriver.Chrome()
        dri.get('https://www.lehrbetrieb.ethz.ch/laborpraktika/mandantAuswahl.view')
        i = i + 1
        sleep(1)

        # If 3 times is reach, return False
        if i > 3:
            return False
# Ture for Login successful and now at the Mandant Page
# False for 6 attempts fails


def select_mavt_prakti(dri):
    # Should be at the Mandant Auswahl Page

    # Create class for the list of Mandant
    select_element = dri.find_element(By.ID, 'mandantId')
    select = Select(select_element)

    # List Options
    #option_list = select.options

    # Select the D-MAVT Prakti
    select.select_by_value('1')

    # Lick the next
    next_move = dri.find_element(By.ID, 'uebernehmen')
    next_move.click()

    current_title = dri.title

    if 'bersicht' in current_title:
        # In the Status List
        return True
    # Not at the Status List
    return False
# True for now at Status List
# False for not


def goto_anmeldung_setup_filter(dri):
    # lick the Bottom to the Prakti List
    button_to_anmelden = dri.find_element(By.LINK_TEXT, 'Praktikum anmelden')
    button_to_anmelden.click()

    current_title = dri.title

    if 'Angebotene' in current_title:
        # Now at the List Page to Anmelden

        # Check the Anmeldbar
        next_move = dri.find_element(By.NAME, 'freePlaces')
        next_move.click()

        # Filter activation
        next_move = dri.find_element(By.ID, 'applyFilters')
        next_move.click()

        current_title = dri.title

        if 'Angebotene' in current_title:
            return True
        return False
    return False
# True for Filter applied and still at the List Page
# False for something went wrong and not at the List Page anymore


def watch_dogs(dri, n_old):
    current_title = dri.title
    while 'Angebotene' in current_title:
        # At the List Page

        # Extract the Eintrag number
        inhalt = dri.find_element(By.CLASS_NAME, 'mTop').text
        # print(inhalt)

        # Isolate the number
        pattern = '[0-9]+.?[0-9]*'
        num_now = re.findall(pattern, inhalt)
        num_now = num_now[0].strip()

        # If number changed break out the loop
        if num_now != n_old:
            return int(num_now)

        # Print out the Log
        time_now = datetime.now()
        print(time_now)
        print('Checked, current Num ', num_now)
        # print('Now sleep for ', Refresh_Time, 's')

        # Sleep and refresh and refresh title
        sleep(Refresh_Time)
        dri.refresh()
        current_title = dri.title
    # Went wrong and not at Page anymore
    return int(-10)
# Return the new number of options
# Return <0 for drop out of page


# Function for Popup notification
# Status 1 for correct otherwise for break
def pop_1(n_old, n_now, status):
    # Pop up a window at the front to notify user
    win = tkinter.Tk()

    win.geometry('300x200')
    win.title('D-MAVT')
    win.resizable(False, False)
    win.attributes('-topmost', True)
    win.attributes('-alpha', 0.5)

    win_text_f = tkinter.Text(win, height=5, width=52)

    win_label = tkinter.Label(win, text='Now')
    win_label.config(font='Courier, 14')

    if status == 1:

        win_text = 'Eintrag Num changed from ' + str(n_old) + ' to ' + str(n_now)
        b1 = tkinter.Button(win, text='Lick after Anmelden', command=win.destroy)

    else:
        win_text = 'Program stop!'
        b1 = tkinter.Button(win, text='OK I guess', command=win.destroy)

    win_label.pack()
    win_text_f.pack()
    b1.pack()

    win_text_f.insert(tkinter.END, win_text)

    win.mainloop()


def play_music():
    tkinter.messagebox.showinfo(title='D-MAVT', message='playing music')
    playsound.playsound('notification.mp3')


# Function to run the notification
# Status 1 for correct otherwise for break
def notification(n_old, n_now, status):
    # Print out the Log
    time_now = datetime.now()
    print(time_now)
    print('Checked, current Num ', n_now, 'old ', n_old)

    thread = threading.Thread(target=pop_1, daemon=True, args=(n_old, n_now, status))

    thread.start()

    #thread_2 = threading.Thread(target=playsound.playsound, args=('notification.mp3', True), daemon=True)
    #thread_2.start()

    #thread_3 = threading.Thread(target=play_music(), daemon=True)
    #thread_3.start()

    #playsound.playsound('path.mp3',)

    os.startfile("notification.mp3")

    thread.join()

    #pop_1(n_old, n_now, 0)




def main(username):
    # Initializing

    # Start up the Browser
    driver = webdriver.Chrome()

    num_now = 0

    i = 1

    for i in range(7):

        # Request login
        if log_in_func_1(driver, username):
            # At the Mandant Page
            if select_mavt_prakti(driver):
                # At the Status list
                if goto_anmeldung_setup_filter(driver):
                    # Filter applied still at the right page
                    # Run Watch loop and get return value
                    num_now = watch_dogs(driver, Num_old)

                    i = 1

                    if num_now > -1:
                        # Eintrag number changed
                        # Send notification status 1

                        notification(Num_old, num_now, 1)



                        # Pop out a final window
                        #message_for_pop = 'Did you done the Anmelden?'
                        #tkinter.messagebox.showinfo(title='D-MAVT', message=message_for_pop)



                        # Code complete
                        return 1

                    # Something went wrong and drop out of the Target page
                    else:
                        print(datetime.now())
                        print('Something went wrong drop out of Target, retry ', i)

                # Not at the Target page, wrong
                else:
                    print(datetime.now())
                    print('Failed at stage set_up filter, retry ', i)

            # Not at the Status list, sth. went wrong
            else:
                print(datetime.now())
                print('Login failed at stage 2, not at the Status list, retry ', i)

        # Login failed at very beginning
        else:
            print(datetime.now())
            print('Login failed at stage 1, retry ', i)

    notification(Num_old, -50, 0)

    # Pop out a final window
    message_for_pop = 'Fix it?'
    tkinter.messagebox.showinfo(title='D-MAVT', message=message_for_pop)



    # Code complete
    return 0


def varification():

    name = simpledialog.askstring(title='D-MAVT', prompt='Please enter username:')
    if usernamecheck.check_user_registration(name):
        return name
    else:
        i = 0
        while True:
            name = simpledialog.askstring(title='D-MAVT', prompt='user not registered!\nPlease enter username:')
            if usernamecheck.check_user_registration(name):
                return name
            else:
                i = i + 1
                if i > 5:
                    return "0"


#while True:
try:

    # Pop out a window for set up the Volume
    tkinter.messagebox.showinfo(title='D-MAVT', message='Turn up the volume for audible notification!')

    # Check if the password is nothing
    if PassWord != '':

        # Check if the user is registered
        username = varification()
        if username == "0":
            notification(0, 0, 0)
            pass
        else:
            main(username)
    else:
        tkinter.messagebox.showinfo(title='D-MAVT', message='Password is empty!')





except Exception:
    notification(0, 0, 0)
    pass




# Locate the input elements
#Username_Fill = driver.find_element(By.ID, 'username')
#Password_Fill = driver.find_element(By.ID, 'password')

# Insert Login Data
#Username_Fill.send_keys()
#Password_Fill.send_keys()

# Locate Login button and lick it. UwU
#Login = driver.find_element(By.NAME, '_eventId_proceed')
#Login.click()

# Should be at the Mandant Auswahl Page

# Create class for the list of Mandant
#select_element = driver.find_element(By.ID, 'mandantId')
#select = Select(select_element)

# List Options
#option_list = select.options

# Select the D-MAVT Prakti
#select.select_by_value('1')

# Lick the next
#Next_Move = driver.find_element(By.ID, 'uebernehmen')
#Next_Move.click()

# lick the Bottom to the Prakti List
#Button_to_Anmelden = driver.find_element(By.LINK_TEXT, 'Praktikum anmelden')
#Button_to_Anmelden.click()

# Check the Anmeldbar
#Next_Move = driver.find_element(By.NAME, 'freePlaces')
#Next_Move.click()

# Filter activation
#Next_Move = driver.find_element(By.ID, 'applyFilters')
#Next_Move.click()


#while True:

    # Extract the Eintrag number
    #Inhalt = driver.find_element(By.CLASS_NAME, 'mTop').text
    #print(Inhalt)

    # Isolate the number
    #Pattern = '[0-9]+.?[0-9]*'
    #Num_now = re.findall(Pattern, Inhalt)
    #Num_now = Num_now[0].strip()

    # If number changed break out the loop
    #if Num_now != Num_old:
        #break

    # Print out the Log
    #Time_Now = datetime.now()
    #print(Time_Now)
    #print('Checked, current Num ', Num_now)
    #print('Now sleep for ', Refresh_Time, 's')

    # Sleep and refresh
    #sleep(Refresh_Time)
    #driver.refresh()

