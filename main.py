
from functions import *
from frame import *
import sys
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = sys.argv[1]
charName = sys.argv[2]

# open a browser and navigate to the provided log
driver = webdriver.Firefox()
driver.get(url)

# dismiss the cookies consent banner so that it doesn't block other elements
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, cookieConsentBannerDismissButton))).click()

fightDate = get_fight_date(driver)

# get number of kills
numKills = len(driver.find_elements(By.XPATH, killRow))
print("found " + str(numKills) + " kills")

overallFightStats = []

# collect stats for each kill
# skip the first two rows on the main page because they're not kills
# the sleeps are present to avoid making too many requests (http 429)
for num in range(3, numKills+3):
    
    fightStats = []
    
    # navigate to the fight
    driver.find_element(By.XPATH, "//div[@class='report-overview-boss-box'][" + str(num) + "]//span[@class='report-overview-boss-kill']").click()    
    bossName = get_boss_name(driver)
    fightDur = get_fight_duration(driver)
    time.sleep(3)
    
    # navigate to the Damage Done tab and collect stats
    driver.find_element(By.XPATH, dmgDoneTab).click()
    wait_until_table_exists(driver)
    parse = get_parse(driver, charName)
    activeTime = get_active_time(driver, charName)
    dps = get_dps(driver, charName)
    time.sleep(3)
    
    # navigate to the Deaths tab and determine if the character died
    driver.find_element(By.XPATH, deathsTab).click()
    wait_until_table_exists(driver)
    didCharDie = did_character_die(driver, charName)
    time.sleep(3)
    
    # navigate to the Casts tab and collect stats
    driver.find_element(By.XPATH, castsTab).click()
    wait_until_table_exists(driver)
    time.sleep(3)
    click_cell_by_contents(driver, charName)
    wait_until_table_exists(driver)
    wasBrezUsed = was_ability_used(driver, "Rebirth")
    ffUptime = get_ability_uptime(driver, "Faerie Fire")
    time.sleep(3)
    
    # add all stats to the stats list
    # note: if you're going to copy and past the stats into a spreadsheet, make sure the order of these appends matches the
    # order of the corresponding columns in the sheet
    fightStats.append(bossName)
    fightStats.append(fightDate)
    fightStats.append(fightDur)
    fightStats.append(parse)
    fightStats.append(activeTime)
    fightStats.append(dps)
    fightStats.append(didCharDie)
    fightStats.append(wasBrezUsed)
    fightStats.append("")
    fightStats.append("")
    fightStats.append(ffUptime)
    
    print("stats collected:")
    print(fightStats)
    overallFightStats.append(fightStats)
    
    # return to the main page
    driver.get(url)
    time.sleep(3)
    
driver.close()

# write overall fight stats out to a text file
print("overall fight stats collected:")
print(overallFightStats)

fightStatsFile = open(fightDate + "_fight_stats.txt", "w")

for fightStats in overallFightStats:
    for stat in fightStats:
        fightStatsFile.write(stat + "\t")
    fightStatsFile.write("\n")

fightStatsFile.close()
