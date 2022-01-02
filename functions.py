
from frame import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException  


# waits until a page's main table exists. use this method before interacting with a table
def wait_until_table_exists(driver):
    print("entering wait_until_table_exists")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, loc_mainTableHeader)))
    print("exiting wait_until_table_exists")


# assumes a table is present
# todo add exception handling for if a cell with the specified contents doesn't exist
def click_cell_by_contents(driver, cellContents):
    print("entering click_cell_by_contents")
    driver.find_element(By.XPATH, "//table[@id='main-table-0']//*[contains(text(), '" + cellContents + "')]").click()
    print("exiting click_cell_by_contents")


# assumes a table is present
# finds and returns the row number of the cell with the specified contents
# todo add exception handling for if a cell with the specified contents doesn't exist
def get_row_num_by_cell_contents(driver, cellContents):
    print("entering get_row_num_by_cell_contents with " + cellContents)
    
    # get all of the main table's rows
    mainTableRows = driver.find_elements(By.XPATH, loc_mainTableRow)
    
    # search through the rows for the specified cell contents
    i = 1
    for row in mainTableRows:
        if cellContents in row.get_attribute("innerText"):
            break
        else:
            i += 1
    
    print("exiting get_row_num_by_cell_contents with " + str(i))
    return i


# functions for getting fight stats

def get_fight_date(driver):
    print("entering get_fight_date")
    fightDate = driver.find_element(By.XPATH, loc_fightDate).get_attribute("innerText")
    print("exiting get_fight_date with " + fightDate)
    return fightDate


def get_boss_name(driver):
    print("entering get_boss_name")
    bossName = driver.find_element(By.XPATH, loc_bossName).get_attribute("innerText").replace(" Normal\n+","")
    print("exiting get_boss_name with " + bossName)
    return bossName


def get_fight_duration(driver):
    print("entering get_fight_duration")
    fightDur = driver.find_element(By.XPATH, loc_fightDur).get_attribute("innerText").strip("()")
    print("exiting get_fight_duration with " + fightDur)
    return fightDur


# functions for getting character performance stats

# assumes the Damage Done tab is open and not filtered
def get_parse(driver, charName):
    print("entering get_parse")
    rowNum = get_row_num_by_cell_contents(driver, charName)
    parse = driver.find_element(By.XPATH, "//table[@id='main-table-0']/tbody/tr[" + str(rowNum) + "]/td[1]/a").get_attribute("innerText")
    print("exiting get_parse with " + parse)
    return parse


# assumes the Damage Done tab is open and not filtered
def get_active_time(driver, charName):
    print("entering get_active_time")
    rowNum = get_row_num_by_cell_contents(driver, charName)
    activeTime = driver.find_element(By.XPATH, "//table[@id='main-table-0']/tbody/tr[" + str(rowNum) + "]/td[6]").get_attribute("innerText")
    print("exiting get_active_time with " + activeTime)
    return activeTime


# assumes the Damage Done tab is open and not filtered
def get_dps(driver, charName):
    print("entering get_dps")
    rowNum = get_row_num_by_cell_contents(driver, charName)
    dps = driver.find_element(By.XPATH, "//table[@id='main-table-0']/tbody/tr[" + str(rowNum) + "]/td[7]").get_attribute("innerText")
    print("exiting get_dps with " + dps)
    return dps


# assumes the Deaths tab is open and not filtered
def did_character_die(driver, charName):
    print("entering did_character_die")
    
    # the table on the Deaths tab has a different header from the other pages, so
    # wait_until_table_exists() can't be used here
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, loc_deathsTabTableHeader)))
    
    try:
        if driver.find_element(By.XPATH, "//table[@id='deaths-table-0']//span[contains(text(),'" + charName + "')]"):
            charDied = True
    except NoSuchElementException:
        charDied = False
    
    print("exiting did_character_die with " + str(charDied))
    return charDied


# assumes the Casts tab is open and filtered to a specific character
def was_ability_used(driver, abilityName):
    print("entering was_ability_used with " + abilityName)
    
    try:
        if driver.find_element(By.XPATH, "//table[@id='main-table-0']//*[contains(text(), '" + abilityName + "')]"):
            abilityUsed = True
    except NoSuchElementException:
        abilityUsed = False
    
    print("exiting was_ability_used with " + str(abilityUsed))
    return abilityUsed


# assumes the Casts tab is open and filtered to a specific character
def get_ability_uptime(driver, abilityName):
    print("entering get_ability_uptime")
    
    rowNum = get_row_num_by_cell_contents(driver, abilityName)
    abilityUptime = driver.find_element(By.XPATH, "//table[@id='main-table-0']/tbody/tr[" + str(rowNum) + "]/td[3]").get_attribute("innerText")
    
    print("exiting get_ability_uptime with " + abilityUptime)
    return abilityUptime
