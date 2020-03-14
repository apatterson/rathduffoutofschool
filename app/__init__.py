import os
import stripe
from flask import Flask, request, session
from flask import render_template, Response, redirect, send_from_directory

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret')

stripe_pub_key = os.environ['STRIPE_PUB_KEY']
stripe.api_key = os.environ['STRIPE_SECRET_KEY']


@app.route("/")
def hello():
    amount = request.args.get('amount', 0)
    reason = request.args.get('reason', '')
    try:
        amount = int(float(amount) * 100)
    except:
        amount = 0

    session['reason'] = reason
    session['amount'] = amount
    
    return render_template(
        'hello.html',
        key=stripe_pub_key,
        amount=amount,
        reason=reason
    )

@app.route("/intent")
def intent():
    # Set your secret key. Remember to switch to your live secret key in production!
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    stripe.api_key = 'sk_test_TMBFQTvbZvdFhYhkm5rPKONL007EIsPo5H'

    intent = stripe.PaymentIntent.create(
        amount=1000,
        currency='eur',
        payment_method_types=['card'],
        receipt_email='anthony.patterson2.0@gmail.com',
    )
    
    return render_template(
        'hello.html',
        message=intent.status
    )

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
