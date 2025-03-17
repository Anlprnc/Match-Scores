from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

team_ids = {
    "Arsenal": "t3",
    "Fulham": "t54",
    "Man City": "t43",
    "Man Utd": "t1",
    "Liverpool": "t14",
    "Chelsea": "t8",
    "Spurs": "t6",
    "Aston Villa": "t7",
    "Newcastle": "t4",
    "Brighton": "t36",
    "West Ham": "t21",
    "Crystal Palace": "t31",
    "Brentford": "t94",
    "Everton": "t11",
    "Nott'm Forest": "t17",
    "Bournemouth": "t91",
    "Wolves": "t39",
    "Leicester": "t13",
    "Ipswich": "t44",
    "Southampton": "t20",
}

def get_team_logo_url(team_name):
    """Takım adına göre logo URL'sini döndürür"""
    team_id = team_ids.get(team_name, "")
    if team_id:
        return f"https://resources.premierleague.com/premierleague/badges/50/{team_id}.png"
    return ""

def fetch_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.premierleague.com/fixtures")
        time.sleep(3)
        
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_button.click()
            time.sleep(1)
        except:
            pass
        
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".matchList")))
        
        match_elements = driver.find_elements(By.CSS_SELECTOR, ".match-fixture")
        
        matches = []
        for match in match_elements:
            try:
                match_status = match.get_attribute('data-comp-match-item-status')
                home_team = match.get_attribute('data-home')
                away_team = match.get_attribute('data-away')
                venue = match.get_attribute('data-venue')
                
                home_logo_url = get_team_logo_url(home_team)
                away_logo_url = get_team_logo_url(away_team)
                
                if match_status == 'L':
                    minute = match.find_element(By.CSS_SELECTOR, '.match-fixture__minutes strong').text
                    score = match.find_element(By.CSS_SELECTOR, '.match-fixture__score').text
                    scores = score.split('-')
                    
                    match_data = {
                        'status': 'LIVE',
                        'minute': minute,
                        'home_team': home_team,
                        'away_team': away_team,
                        'home_score': scores[0].strip(),
                        'away_score': scores[1].strip(),
                        'stadium': venue,
                        'home_logo': home_logo_url,
                        'away_logo': away_logo_url
                    }
                else:
                    kickoff_time = match.find_element(By.CSS_SELECTOR, 'time').text
                    
                    match_data = {
                        'status': 'UPCOMING',
                        'kickoff': kickoff_time,
                        'home_team': home_team,
                        'away_team': away_team,
                        'stadium': venue,
                        'home_logo': home_logo_url,
                        'away_logo': away_logo_url
                    }
                
                matches.append(match_data)
                
            except Exception as e:
                print(f"Error processing match: {str(e)}")
                continue
            
        return matches
            
    finally:
        driver.quit()

@app.route('/matches', methods=['GET'])
def get_matches():
    try:
        matches = fetch_data()
        return jsonify({
            'success': True,
            'data': matches
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)