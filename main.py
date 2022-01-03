
from functions import *
from frame import *
import sys
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = sys.argv[1]
charName = sys.argv[2]


# sleeps are present to avoid making too many requests too quickly (http 429)
sleepTime = 3

# open a browser and navigate to the provided log
driver = webdriver.Firefox()
driver.get(url)

# dismiss the cookies consent banner so that it doesn't block other elements
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, loc_cookieConsentBannerDismissBtn))).click()

fightDate = get_fight_date(driver)

# get number of kills
numKills = len(driver.find_elements(By.XPATH, loc_kill))
print("found " + str(numKills) + " kills")

overallFightStats = []

# collect stats for each kill
# skip the first two sections on the main page because they're not kills
for num in range(1, numKills+1):
    
    fightStats = []
    
    # navigate to the fight
    driver.find_element(By.XPATH, "(" + loc_kill + ")[" + str(num) + "]").click()
    bossName = get_boss_name(driver)
    fightDur = get_fight_duration(driver)
    time.sleep(sleepTime)
    
    # navigate to the Damage Done tab and collect stats
    driver.find_element(By.XPATH, loc_dmgDoneTab).click()
    wait_until_table_exists(driver)
    parse = get_parse(driver, charName)
    activeTime = get_active_time(driver, charName)
    dps = get_dps(driver, charName)
    time.sleep(sleepTime)
    
    # navigate to the Deaths tab and determine if the character died
    driver.find_element(By.XPATH, loc_deathsTab).click()
    didCharDie = did_character_die(driver, charName)
    time.sleep(sleepTime)
    
    # navigate to the Casts tab and collect stats
    driver.find_element(By.XPATH, loc_castsTab).click()
    wait_until_table_exists(driver)
    time.sleep(sleepTime)
    click_cell_by_contents(driver, charName)
    wait_until_table_exists(driver)
    wasBrezUsed = was_ability_used(driver, "Rebirth")
    wasMfUsed = was_ability_used(driver, "Moonfire")
    if wasMfUsed:
        mfUptime = get_ability_uptime(driver, "Moonfire")
    wasFfUsed = was_ability_used(driver, "Faerie Fire")
    if wasFfUsed:
        ffUptime = get_ability_uptime(driver, "Faerie Fire")
    time.sleep(sleepTime)
    
    # add all stats to the stats list
    # note: if you're going to copy and past the stats into a spreadsheet, make sure the order of these appends matches the
    # order of the corresponding columns in the sheet
    fightStats.append(bossName)
    fightStats.append(fightDate)
    fightStats.append(fightDur)
    fightStats.append(parse)
    fightStats.append(activeTime)
    fightStats.append(dps)
    fightStats.append(str(didCharDie))
    fightStats.append(str(wasBrezUsed))
    fightStats.append("")
    fightStats.append("")
    if wasMfUsed:
        fightStats.append(mfUptime)
    else:
        fightStats.append("")
    if wasFfUsed:
        fightStats.append(ffUptime)
    else:
        fightStats.append("")
    
    print("stats collected:")
    print(fightStats)
    overallFightStats.append(fightStats)
    
    # return to the main page
    driver.get(url)
    time.sleep(sleepTime)
    
driver.close()

# write overall fight stats out to a text file
print("overall fight stats collected:")
print(overallFightStats)

fightStatsFile = open(fightDate + "_" + charName + "_fight_stats.txt", "w")

for fightStats in overallFightStats:
    for stat in fightStats:
        fightStatsFile.write(stat + "\t")
    fightStatsFile.write("\n")

fightStatsFile.close()
