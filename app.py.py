from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# Provided credentials
access_token = 'ixw6N5Xv4hJ7R41nEJKOjCtJV3Rs'
initiator_name = 'testapi'
security_credential = 'El9b5Fg3idGdkzFyHmKOPOweTW6wpkXB38Uyk9oClfagPSP6VPvx+pANJ2Z5fcFJ+qNCVN3X9QDf1nhO1y+QK1oiXtaElEObjfb3DEnruXP3BpAxEXSlWAEHrJXyFtkF5hcjSJ3dFwFOn0v1fyvFn5j0DNumeQR/Wig0NK/SQ+ViM2w3DqEOuUjH0jHthHBRdyiiDwrggDCCyx0PHQnaOTh7Bw8zq8exkVmBmr+a01+m794olbjUDN/+HyYEpi6WP9LmzA6Lm7LtifIJcfaSJpIYfHiRfmnAI4zGiejy/9aUHSMI+1Ssyj0icYxUW0dILur8bzduvOWXfJmqk0AYTw=='
business_short_code = 600989

@app.route('/')
def home():
    return render_template_string('''
        <!doctype html>
        <title>Check Transaction Status</title>
        <h1>Check Transaction Status</h1>
        <form action="/check_status" method="post">
            Transaction ID: <input type="text" name="transaction_id"><br>
            <input type="submit" value="Check Status">
        </form>
    ''')

@app.route('/check_status', methods=['POST'])
def check_status():
    transaction_id = request.form['transaction_id']
    try:
        api_url = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        payload = {
            "Initiator": initiator_name,
            "SecurityCredential": security_credential,
            "CommandID": "TransactionStatusQuery",
            "TransactionID": transaction_id,
            "PartyA": business_short_code,
            "IdentifierType": "4",
            "ResultURL": "https://mydomain.com/TransactionStatus/result/",
            "QueueTimeOutURL": "https://mydomain.com/TransactionStatus/queue/",
            "Remarks": "Checking transaction status",
            "Occasion": "Payment verification"
        }

        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
