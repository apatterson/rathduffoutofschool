import stripe
import json
import os

from flask import Flask, render_template, jsonify, request, response, send_from_directory, session
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret')

stripe_pub_key = os.environ['STRIPE_PUB_KEY']
stripe.api_key = os.environ['STRIPE_SECRET_KEY']

def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return int(float(items[0]) * 100)

@app.route("/")
def hello():
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    message = request.args.get('message', '')
    
    return render_template(
        'hello.html',
        key=stripe_pub_key,
        message=message
    )

@app.route("/intent")
def intent():    
    amount = request.args.get('amount', 0)   
    session['email'] = request.args.get('email', 0) 
    session['notes'] = request.args.get('notes', 0)
    return render_template(
        'pay.html',
        amount=amount
    )

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    data = json.loads(request.data)
    # Create a PaymentIntent with the order amount and currency
    intent = stripe.PaymentIntent.create(
        amount=calculate_order_amount(data['items']),
        currency=data['currency'],
        receipt_email=session['email'],
        description=session['notes']
    )

    try:
        # Send publishable key and PaymentIntent details to client
        return jsonify({
            'publishableKey': stripe_pub_key, 
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        return jsonify(error=str(e)), 403
    
    
@app.route('/charge', methods=['GET', 'POST'])
def charge():
    if request.method == 'GET':
        return redirect('/')
    email = request.form['stripeEmail']
    token = request.form['stripeToken']
    reason = session.get('reason') or 'A Charge'
    amount = session['amount']
    message = "Thank you, payment accepted"
    try :
        stripe.Charge.create(
            receipt_email=email,
            source=token,
            amount=amount,
            currency='eur',
            description=reason,
        )
    except Exception as e:
        message = e.error.message
    
    return render_template(
        'hello.html',
        message=message
    )


@app.route('/robots.txt')
def robots():
    text = 'User-Agent: *\nDisallow: /\n'
    return Response(text, mimetype='text/plain')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        app.root_path, 'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
