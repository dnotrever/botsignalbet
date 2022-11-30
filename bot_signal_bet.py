import time, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from bot_telegram import send_message

os.system('cls')

# - - Parâmetros - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

choice_team = input('\n  Time: ')
c_actived_1 = True if choice_team else False

choice_corners = input('\n  Escanteios: ')
c_actived_2 = True if choice_corners else False

choice_goalshots = input('\n  Chutes ao Gol: ')
c_actived_3 = True if choice_goalshots else False

choice_dangerous = input('\n  Ataques Perigosos: ')
c_actived_4 = True if choice_dangerous else False

choice_possession = input('\n  Posse de Bola: ')
c_actived_5 = True if choice_possession else False

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

os.system('cls')
print(f'\n\tPesquisando por {choice_team}...\n')

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=options)
action = ActionChains(driver)

driver.get('https://www.bet365.com/#/IP/B1')
driver.maximize_window()

team_exists = False

try: WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'iip-IntroductoryPopup_Cross'))).click()
except: pass

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ovm-ClassificationHeader_Text '))).click()

action.send_keys(Keys.END)
action.perform()

time.sleep(3)

names = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ovm-FixtureDetailsTwoWay_TeamName ')))

for name in names:
    
    if choice_team == name.text:
        name.click()
        team_exists = True
        break

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if team_exists:
    
    team_validator = True

    while True:
        
        time.sleep(1.0)
        
        os.system('cls')
        
        ligue = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ipe-EventHeader_BreadcrumbText '))).text
        ligue_format = ligue.replace('Ao-Vivo Futebol - ', '')
        
        teams = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'lsb-ScoreBasedScoreboardAggregate_TeamName-normal')))
        goals = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'lsb-ScoreBasedScoreboardAggregate_TeamScore ')))
        
        gametime = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ml1-SoccerClock_Clock '))).text
        gameinjury = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ml1-SoccerClock_InjuryTime '))).text
        
        all_stats = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ml1-AllStatsAdvanced')))
        stats_team1 = WebDriverWait(all_stats, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ml1-WheelChartAdvanced_Team1Text ')))
        stats_team2 = WebDriverWait(all_stats, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ml1-WheelChartAdvanced_Team2Text ')))
        mid_stats = WebDriverWait(all_stats, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ml1-ProgressBarAdvancedDual_SideLabel ')))
        sub_stats = WebDriverWait(all_stats, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ml1-StatsColumnAdvanced_MiniValue ')))
        
        possession_team1 = '-'
        if len(stats_team1) == 3: possession_team1 = stats_team1[2].text
        
        possession_team2 = '-'
        if len(stats_team2) == 3: possession_team2 = stats_team2[2].text
        
        team_1 = {
            'name': teams[0].text,
            'goals': goals[0].text,
            'attacks': stats_team1[0].text,
            'dangerous': stats_team1[1].text,
            'possession': possession_team1,
            'corners': sub_stats[0].text,
            'redcards': sub_stats[1].text,
            'yellowcards': sub_stats[2].text,
            'shots': mid_stats[0].text,
            'goalshots': mid_stats[1].text
        }
        
        team_2 = {
            'name': teams[1].text,
            'goals': goals[1].text,
            'attacks': stats_team2[0].text,
            'dangerous': stats_team2[1].text,
            'possession': possession_team2,
            'corners': sub_stats[3].text,
            'redcards': sub_stats[4].text,
            'yellowcards': sub_stats[5].text,
            'shots': mid_stats[2].text,
            'goalshots': mid_stats[3].text
        }
        
        if team_validator:
            choice_team = team_1 if choice_team == team_1['name'] else team_2
            team_validator = False
        
        print(f'''
            
            {ligue_format}
            
            Tempo - {gametime}
                
            {team_1['name']} {team_1['goals']} x {team_2['goals']} {team_2['name']}
            
            Estatisticas:
            
                Escanteios ........... {team_1['corners']} x {team_2['corners']}
                Ataques .............. {team_1['attacks']} x {team_2['attacks']}
                Ataques Perigosos .... {team_1['dangerous']} x {team_2['dangerous']}
                Posse de Bola (%) .... {team_1['possession']} x {team_2['possession']}
                Chutes ao Gol ........ {team_1['goalshots']} x {team_2['goalshots']}
                Finalizações ......... {team_1['shots']} x {team_2['shots']}
                Cartões Amarelos ..... {team_1['yellowcards']} x {team_2['yellowcards']}
                Cartões Vermelhos .... {team_1['redcards']} x {team_2['redcards']}
              
        ''')
        
        # - - Condições - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        
        
        
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

else:
    
    os.system('cls')
    print(f'\n\tPesquisa: {choice_team}')
    print('\n\tO time não está em partida ou o nome está incorreto.\n\n')
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -