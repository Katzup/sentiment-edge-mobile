#!/usr/bin/env python3
"""
Static Dashboard Generator for GitHub Pages
Generates HTML dashboard that can be served as static content
"""

import os
import json
from datetime import datetime
from alpaca.trading.client import TradingClient
from alpaca_sentientedge_trader import AlpacaSentientEdgeTrader
import yfinance as yf

def generate_static_dashboard():
    """Generate static HTML dashboard for GitHub Pages"""
    
    # Get data (same logic as Flask dashboard)
    client = TradingClient(
        os.getenv('ALPACA_API_KEY'), 
        os.getenv('ALPACA_SECRET_KEY'), 
        paper=True
    )
    
    # Account status
    account = client.get_account()
    equity = float(account.equity)
    cash = float(account.cash)
    margin_used = abs(cash) if cash < 0 else 0
    margin_pct = margin_used / equity * 100 if equity > 0 else 0
    
    # Current positions
    positions = client.get_all_positions()
    position_data = []
    total_value = 0
    total_pnl = 0
    
    for pos in positions:
        value = float(pos.market_value)
        pnl = float(pos.unrealized_pl)
        pnl_pct = float(pos.unrealized_plpc) * 100
        total_value += value
        total_pnl += pnl
        
        position_data.append({
            'symbol': pos.symbol,
            'quantity': int(pos.qty),
            'avg_cost': round(float(pos.avg_entry_price), 2),
            'current_price': round(float(pos.current_price), 2),
            'value': round(value, 2),
            'pnl': round(pnl, 2),
            'pnl_pct': round(pnl_pct, 1)
        })
    
    # Market data
    spy = yf.Ticker('SPY')
    qqq = yf.Ticker('QQQ')
    vix = yf.Ticker('^VIX')
    
    spy_data = spy.history(period='2d')
    qqq_data = qqq.history(period='2d')
    vix_data = vix.history(period='5d')
    
    spy_return = ((spy_data['Close'].iloc[-1] - spy_data['Close'].iloc[-2]) / spy_data['Close'].iloc[-2] * 100) if len(spy_data) >= 2 else 0
    qqq_return = ((qqq_data['Close'].iloc[-1] - qqq_data['Close'].iloc[-2]) / qqq_data['Close'].iloc[-2] * 100) if len(qqq_data) >= 2 else 0
    current_vix = vix_data['Close'].iloc[-1] if len(vix_data) > 0 else 20
    
    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SentientEdge Trading Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="300"> <!-- Auto-refresh every 5 minutes -->
    <style>
        body {{ font-family: -apple-system, system-ui, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: rgba(255,255,255,0.95); padding: 25px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin-bottom: 25px; }}
        .header h1 {{ margin: 0; color: #1a202c; font-size: 32px; }}
        .header p {{ margin: 10px 0 0 0; color: #4a5568; }}
        .card {{ background: rgba(255,255,255,0.95); padding: 25px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin-bottom: 25px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; }}
        .metric {{ display: inline-block; margin-right: 30px; }}
        .metric-label {{ font-size: 14px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; }}
        .metric-value {{ font-size: 28px; font-weight: bold; margin-top: 5px; }}
        .positive {{ color: #22c55e; }}
        .negative {{ color: #ef4444; }}
        .neutral {{ color: #6b7280; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb; }}
        th {{ background: #f9fafb; font-weight: 600; color: #374151; }}
        .symbol {{ font-weight: bold; font-family: 'Monaco', 'Consolas', monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 SentientEdge Trading Dashboard (GitHub Pages)</h1>
            <p>Static Dashboard | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} | Auto-refresh: 5min</p>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>💰 Account Summary</h3>
                <div class="metric">
                    <div class="metric-label">Total Equity</div>
                    <div class="metric-value">${equity:,.2f}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Cash</div>
                    <div class="metric-value {'negative' if cash < 0 else 'positive'}">${cash:,.2f}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Margin</div>
                    <div class="metric-value {'negative' if margin_pct > 50 else 'neutral'}">{margin_pct:.1f}%</div>
                </div>
            </div>
            
            <div class="card">
                <h3>📈 Market Benchmarks</h3>
                <div class="metric">
                    <div class="metric-label">SPY Daily</div>
                    <div class="metric-value {'positive' if spy_return >= 0 else 'negative'}">{spy_return:+.2f}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">QQQ Daily</div>
                    <div class="metric-value {'positive' if qqq_return >= 0 else 'negative'}">{qqq_return:+.2f}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">VIX</div>
                    <div class="metric-value {'negative' if current_vix > 25 else 'positive' if current_vix < 15 else 'neutral'}">{current_vix:.1f}</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>🏆 Current Positions ({len(positions)})</h3>
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Qty</th>
                        <th>Avg Cost</th>
                        <th>Current</th>
                        <th>Value</th>
                        <th>P&L</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Add position rows
    for pos in sorted(position_data, key=lambda x: x['value'], reverse=True):
        pnl_class = 'positive' if pos['pnl'] >= 0 else 'negative'
        html_content += f"""
                    <tr>
                        <td class="symbol">{pos['symbol']}</td>
                        <td>{pos['quantity']}</td>
                        <td>${pos['avg_cost']}</td>
                        <td>${pos['current_price']}</td>
                        <td>${pos['value']:,.0f}</td>
                        <td class="{pnl_class}">${pos['pnl']:,.0f} ({pos['pnl_pct']:+.1f}%)</td>
                    </tr>
"""
    
    html_content += f"""
                </tbody>
            </table>
        </div>
        
        <div class="card" style="text-align: center;">
            <p>🤖 Generated by GitHub Actions | Hosted on GitHub Pages</p>
            <p style="font-size: 12px; color: #666;">Updates automatically every 5 minutes during market hours</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Write to docs/index.html for GitHub Pages
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.html', 'w') as f:
        f.write(html_content)
    
    print(f"✅ Static dashboard generated: docs/index.html")
    print(f"📊 Account: ${equity:,.0f} | Positions: {len(positions)} | SPY: {spy_return:+.1f}% | QQQ: {qqq_return:+.1f}%")

if __name__ == "__main__":
    generate_static_dashboard()