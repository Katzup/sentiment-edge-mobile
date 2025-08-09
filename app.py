#!/usr/bin/env python3
"""
Railway Two-Tier Trading App - URGENT DEPLOYMENT
Deploys the new two-tier trading strategy to Railway for automated sessions
"""

import os
import sys
import json
import logging
import schedule
import time
import threading
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from typing import Dict, Any

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("⚠️  Using system environment variables.")

# Import our two-tier trading strategy
from two_tier_trading_strategy import TwoTierTradingStrategy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)
start_time = time.time()

# Global system status
system_status = {
    'healthy': True,
    'last_session': None,
    'next_session': None,
    'sessions_today': 0,
    'error_count': 0,
    'strategy_type': 'two_tier'
}

# Initialize two-tier trading strategy
trading_strategy = TwoTierTradingStrategy(
    max_position_size=0.10,
    confidence_threshold=0.75
)

def execute_trading_session(session_name: str):
    """Execute a Tier 2 trading session"""
    try:
        logger.info(f"🚀 Executing {session_name} trading session...")
        
        # Execute Tier 2 focused session
        tier2_session = trading_strategy.execute_tier2_session(session_name)
        
        # Update system status
        system_status.update({
            'last_session': {
                'timestamp': datetime.now().isoformat(),
                'session_name': session_name,
                'execution_time': tier2_session.execution_time_seconds,
                'focused_stocks': len(tier2_session.focused_stocks),
                'recommendations': len(tier2_session.trading_session.recommendations),
                'orders_executed': len(tier2_session.trading_session.orders_submitted),
                'session_pnl': tier2_session.trading_session.session_pnl,
                'portfolio_value': tier2_session.trading_session.portfolio_value_after
            },
            'sessions_today': system_status['sessions_today'] + 1,
            'healthy': True
        })
        
        logger.info(f"✅ {session_name} session completed:")
        logger.info(f"   Execution time: {tier2_session.execution_time_seconds:.1f}s")
        logger.info(f"   Orders executed: {len(tier2_session.trading_session.orders_submitted)}")
        logger.info(f"   Session P&L: ${tier2_session.trading_session.session_pnl:+,.2f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ {session_name} session failed: {e}")
        system_status['error_count'] += 1
        system_status['healthy'] = False
        return False

def execute_tier1_analysis():
    """Execute Tier 1 comprehensive analysis (5pm daily)"""
    try:
        logger.info("🔍 Starting Tier 1 comprehensive analysis...")
        
        # Execute Tier 1 comprehensive analysis  
        tier1_analysis = trading_strategy.execute_tier1_analysis()
        
        logger.info(f"✅ Tier 1 analysis completed:")
        logger.info(f"   Duration: {tier1_analysis.analysis_duration_minutes:.1f} minutes")
        logger.info(f"   Stocks analyzed: {tier1_analysis.total_stocks_analyzed}")
        logger.info(f"   Top prospects: {len(tier1_analysis.top_prospects)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Tier 1 analysis failed: {e}")
        system_status['error_count'] += 1
        return False

# Schedule trading sessions (Eastern Time)
schedule.every().day.at("10:00").do(lambda: execute_trading_session("10am_session"))
schedule.every().day.at("13:00").do(lambda: execute_trading_session("1pm_session"))  
schedule.every().day.at("15:30").do(lambda: execute_trading_session("3:30pm_session"))

# Schedule Tier 1 analysis (5pm daily)
schedule.every().day.at("17:00").do(execute_tier1_analysis)

def run_scheduler():
    """Run the trading scheduler in background thread"""
    logger.info("📅 Starting trading scheduler...")
    logger.info("   10:00 AM - Morning trading session")
    logger.info("   1:00 PM - Lunch trading session") 
    logger.info("   3:30 PM - Afternoon trading session")
    logger.info("   5:00 PM - Tier 1 comprehensive analysis")
    
    while True:
        schedule.run_pending()
        time.sleep(30)  # Check every 30 seconds

# Flask routes
@app.route('/')
def home():
    """Home page with system status"""
    return jsonify({
        'service': 'SentientEdge Two-Tier Trading System',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.1',
        'strategy': 'two_tier',
        'next_session': get_next_session_time()
    })

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy' if system_status['healthy'] else 'unhealthy',
        'service': 'SentientEdge Two-Tier Trading',
        'timestamp': datetime.now().isoformat(),
        'uptime_seconds': time.time() - start_time,
        'sessions_today': system_status['sessions_today'],
        'error_count': system_status['error_count'],
        'last_session': system_status['last_session']
    })

@app.route('/status')
def status():
    """Detailed system status"""
    return jsonify(system_status)

@app.route('/manual_session')
def manual_session():
    """Manual trigger for trading session (emergency use)"""
    session_name = request.args.get('name', 'manual')
    success = execute_trading_session(f"manual_{session_name}")
    
    return jsonify({
        'success': success,
        'session_name': session_name,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/manual_tier1')  
def manual_tier1():
    """Manual trigger for Tier 1 analysis"""
    success = execute_tier1_analysis()
    
    return jsonify({
        'success': success,
        'analysis_type': 'tier1_comprehensive',
        'timestamp': datetime.now().isoformat()
    })

def get_next_session_time():
    """Get the next scheduled session time"""
    now = datetime.now()
    today_sessions = [
        datetime.combine(now.date(), datetime.strptime("10:00", "%H:%M").time()),
        datetime.combine(now.date(), datetime.strptime("13:00", "%H:%M").time()),
        datetime.combine(now.date(), datetime.strptime("15:30", "%H:%M").time()),
        datetime.combine(now.date(), datetime.strptime("17:00", "%H:%M").time())
    ]
    
    # Find next session today
    for session_time in today_sessions:
        if session_time > now:
            return session_time.isoformat()
    
    # If no more sessions today, return tomorrow's first session
    tomorrow_10am = datetime.combine(now.date() + timedelta(days=1), datetime.strptime("10:00", "%H:%M").time())
    return tomorrow_10am.isoformat()

if __name__ == '__main__':
    logger.info("🚀 Starting SentientEdge Two-Tier Trading System on Railway")
    
    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Get port from Railway environment
    port = int(os.environ.get('PORT', 8080))
    
    # Run Flask app
    app.run(host='0.0.0.0', port=port)
