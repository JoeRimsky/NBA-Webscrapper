# Author: Joe Rimsky, Tyler Leake, Michael Grimm
# CSC 308 Final Project
# 4/9/19

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from tkinter import *

def main():
	sRTemp = 0
	sLTemp = 0
	url = input_GUI()
	driver = connect_to_website(url)
	while driver.find_element_by_xpath('//*[@id="block-league-content"]/game-detail/div[1]/game-marquee/div[2]/div/div[2]/div[2]/div[4]').text == "LIVE":
		sRTemp, sLTemp = retrieve_data(driver, sRTemp, sLTemp)
	driver.quit()

# Function that creates the GUI to retrieve a URL
def input_GUI():
	def getURL():
		global url
		url = E1.get()
		master.destroy()
	master = Tk()
	L1 = Label(master, text="Please input the URL you wish to pull scores from")
	E1 = Entry(master, bd=5)
	B1 = Button(master, text="Enter",command=getURL)
	L1.pack(side=LEFT)
	E1.pack(side=RIGHT)
	B1.pack(side=BOTTOM)
	master.mainloop()
	return url

# Function to establish the connection to the given URL
def connect_to_website(url):
	timeout = 10 # seconds
	driver = webdriver.Chrome()
	driver.get(url)
	try:
		elements = EC.presence_of_element_located((By.XPATH, '//*[@id="block-league-content"]/game-detail/div[1]/game-marquee/div[2]/div/div[2]'))
		WebDriverWait(driver, timeout).until(elements)
		print("Loaded")
	except TimeoutException:
		print("Timed out")
	return driver

def retrieve_data(driver, sRTemp, sLTemp):
	teamLeft = driver.find_element_by_xpath('//*[@id="block-league-content"]/game-detail/div[1]/game-marquee/div[2]/div/div[2]/div[1]/div/div/span[1]')
	teamRight = driver.find_element_by_xpath('//*[@id="block-league-content"]/game-detail/div[1]/game-marquee/div[2]/div/div[2]/div[3]/div/div/span[1]')
	scoreLeft = driver.find_element_by_xpath('//*[@id="block-league-content"]/game-detail/div[1]/game-marquee/div[2]/div/div[2]/div[1]/div/div/span[2]')
	if int(scoreLeft.text) > sLTemp:
		print("Left team scored.")
	sLTemp = int(scoreLeft.text)
	scoreRight = driver.find_element_by_xpath('//*[@id="block-league-content"]/game-detail/div[1]/game-marquee/div[2]/div/div[2]/div[3]/div/div/span[2]')
	if int(scoreRight.text) > sRTemp:
		print("Right team scored.")
	sRTemp = int(scoreRight.text)
	print_to_file(teamLeft, teamRight, scoreLeft, scoreRight)
	return sRTemp, sLTemp

def print_to_file(teamLeft, teamRight, scoreLeft, scoreRight):
	with open('score.txt', 'w', encoding='utf-8') as f_out:
		f_out.write(teamLeft.text + ": " + scoreLeft.text + " " + teamRight.text + ": " + scoreRight.text)

main()