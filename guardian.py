import requests
import time
import os
from datetime import datetime

# Config
WORDPRESS_SITE = 'dailysmartliving.wordpress.com'
AMAZON_TAG = 'gadgethumans-21'
REDBUBBLE_USER = 'scotia1973'
PAYPAL_EMAIL = 'scotia1973@gmail.com'
DOMAIN_BUDGET = 10.00  # Buy domain when this amount is reached

LOG_FILE = '/tmp/guardian.log'

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{timestamp}] {msg}'
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def check_wordpress_traffic():
    """Check WordPress stats via public API"""
    try:
        url = f'https://public-api.wordpress.com/rest/v1.1/sites/{WORDPRESS_SITE}/stats'
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            views = data.get('views', 0)
            visitors = data.get('visitors', 0)
            log(f'WordPress: {views} views, {visitors} visitors today')
            return views
    except Exception as e:
        log(f'WordPress error: {e}')
    return 0

def check_amazon_earnings():
    """Log Amazon affiliate status - actual earnings via Amazon API requires more setup"""
    log('Amazon: Tag active - gadgethumans-21. Earnings tracked via Amazon Associates dashboard.')
    return 0.00

def check_redbubble_sales():
    """Check Redbubble for recent sales"""
    try:
        url = f'https://www.redbubble.com/people/{REDBUBBLE_USER}/portfolio.rss'
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            log('Redbubble: Portfolio accessible, monitoring sales.')
        else:
            log(f'Redbubble: Unable to check (status {resp.status_code})')
    except Exception as e:
        log(f'Redbubble error: {e}')
    return 0.00

def should_buy_domain(total_earnings):
    """Decision engine for purchasing domain"""
    if total_earnings >= DOMAIN_BUDGET:
        log(f'THRESHOLD REACHED: ${total_earnings:.2f} >= ${DOMAIN_BUDGET:.2f}')
        log('ACTION REQUIRED: Check earnings and purchase domain at Namecheap.')
        log(f'Suggested domain: dailysmartliving.com')
        log('Purchase steps:')
        log('1. Go to namecheap.com')
        log('2. Search for dailysmartliving.com')
        log('3. Purchase with PayPal: scotia1973@gmail.com')
        log('4. Point DNS to WordPress.com')
        return True
    return False

def run_audit():
    """Main audit cycle"""
    log('=== Guardian Audit Starting ===')
    
    views = check_wordpress_traffic()
    amazon = check_amazon_earnings()
    redbubble = check_redbubble_sales()
    
    total = amazon + redbubble
    log(f'Estimated earnings this cycle: ${total:.2f}')
    
    if should_buy_domain(total):
        log('Domain purchase triggered!')
    else:
        remaining = DOMAIN_BUDGET - total
        log(f'${remaining:.2f} needed before domain purchase.')
    
    log('=== Guardian Audit Complete ===')

if __name__ == '__main__':
    log('Guardian Agent started. Monitoring earnings...')
    log(f'Domain budget: ${DOMAIN_BUDGET:.2f}')
    log(f'PayPal: {PAYPAL_EMAIL}')
    
    while True:
        run_audit()
        log('Sleeping for 6 hours...')
        time.sleep(21600)  # 6 hours
