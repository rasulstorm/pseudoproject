from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    # Base cost
    total_cost = 0

    # University selection
    if data['university'] == 'Kazakhstan':
        total_cost += 100000
    elif data['university'] == 'EU':
        total_cost += 120000
    elif data['university'] == 'America':
        total_cost += 150000

    # Format selection
    if data['format'] == 'LaTeX':
        total_cost += 50000
    elif data['format'] == 'Word':
        total_cost += 0

    # Language selection
    if data['language'] == 'Russian':
        total_cost += 10000
    elif data['language'] == 'Kazakh':
        total_cost += 30000
    elif data['language'] == 'English':
        total_cost += 0

    # Volume selection
    if data['volume'] == '50pages':
        total_cost += 0
    elif data['volume'] == '30-45pages':
        total_cost += 1000
    elif data['volume'] == '50+pages':
        total_cost += 10000

    # Code project
    if data['code'] == 'Yes':
        total_cost += 80000
    elif data['code'] == 'No':
        total_cost += 0

    # Diploma or Dissertation
    if data['type'] == 'Dissertation':
        total_cost += 60000

    return jsonify({'total_cost': total_cost})

@app.route('/contact')
def contact():
    return "<h2>Contact Us</h2><p>Reach us on Telegram: <a href='https://t.me/Itatti' target='_blank'>https://t.me/Itatti</a></p>"

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
