# Import external libraries.
from flask import Blueprint, flash, g, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import DecimalField, DecimalRangeField, IntegerField, SelectField, StringField
from wtforms.validators import InputRequired, NumberRange, Regexp

# Import local modules.
from .authenticate import login_required
from .database import get_db
from .option_pricing.black_scholes import BlackScholes
from .option_pricing.binomial import BinomialCRR
from .option_pricing.monte_carlo import MonteCarlo
from .stock_services import filter_closing_prices, filter_info, filter_latest_quote, get_info, get_time_series

# Define the blueprint.
bp = Blueprint("options", __name__)


class StockForm(FlaskForm):
    """ Represents the stock form. """

    ticker = StringField("Stock Ticker", [InputRequired(), Regexp(r"^[A-Z0-9.]{1,6}$", message="Invalid Ticker")])


class OptionForm(FlaskForm):
    """ Represents the option form. """

    model = SelectField("Pricing Model",
                        choices=["Binomial-CRR", "Black-Scholes", "Monte-Carlo"],
                        validators=[InputRequired("Missing Pricing Model")])

    type = SelectField("Option Type",
                       choices=["Call", "Put"],
                       validators=[InputRequired("Missing Option Type")])

    spot = DecimalField("Spot Price",
                        validators=[InputRequired("Missing Spot Price"),
                                    NumberRange(1, 10000, message="Invalid Spot Price")],
                        places=2)

    strike = DecimalField("Strike Price",
                          validators=[InputRequired("Missing Strike Price"),
                                      NumberRange(1, 10000, message="Invalid Strike Price")],
                          places=2)

    time = IntegerField("Days Till Expiration",
                        validators=[InputRequired("Missing Days Till Expiration"),
                                    NumberRange(1, 1825, message="Invalid Days Till Expiration")])

    rfr = DecimalRangeField("Risk Free Rate",
                            validators=[InputRequired("Missing Risk Free Rate"),
                                        NumberRange(0, 1, message="Invalid Risk Free Rate")],
                            render_kw={"min":"0", "max":"1", "step":"0.01"},
                            default=0.2)

    sigma = DecimalRangeField("Volatility",
                              validators=[InputRequired("Missing Volatility"),
                                          NumberRange(0, 1, message="Invalid Volatility")],
                              render_kw={"min":"0", "max":"1", "step":"0.01"},
                              default=0.2)


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    """
    The route for the index page. Operates the stock form to retrieve
    info about a stock.

    Renders
    -------
    options/index.html ( without stock information )
        If the route was requested through the GET method.

    options/index.hmtl ( with stock information )
        If the stock form was submitted and information about a stock
        was retrieved.

    Redirects
    ---------
    options.index
        If the stock form was submitted and information about a stock
        was not retrieved. An error message is also flashed.
    """

    form = StockForm()

    if form.validate_on_submit():
        ticker = form.ticker.data

        stock_info = get_info(ticker)
        stock_prices = get_time_series(ticker)

        if "error" in stock_info:
            flash(stock_info["error"], "error")
            return redirect(url_for("options.index"))

        elif "error" in stock_prices:
            flash(stock_prices["error"], "error")
            return redirect(url_for("options.index"))

        info = filter_info(stock_info)
        quote = filter_latest_quote(stock_prices)
        prices = filter_closing_prices(stock_prices)

        return render_template("options/index.html", form=form, info=info, quote=quote, prices=prices)

    return render_template("options/index.html", form=form)


@bp.route("/pricing", methods=("GET", "POST"))
@login_required
def pricing():
    """
    The route for the pricing page. Operates the option-pricing form.

    Renders
    -------
    options/pricing.html ( without option price )
        If the route was requested through the GET method.

    options/pricing.html ( with option price )
        If the option-pricing form was submitted and the option price
        was calculated.
    """

    form = OptionForm()

    if form.validate_on_submit():
        spot = float(form.spot.data)
        strike = float(form.strike.data)
        time = float(form.time.data / 365)
        rfr = float(form.rfr.data)
        sigma = float(form.sigma.data)

        match form.model.data:
            case "Binomial-CRR":
                option = BinomialCRR(spot, strike, time, rfr, sigma)
            case "Black-Scholes":
                option = BlackScholes(spot, strike, time, rfr, sigma)
            case "Monte-Carlo":
                option = MonteCarlo(spot, strike, time, rfr, sigma)

        price = [form.type.data, round(option.price((form.type.data).lower()), 8)]

        con = get_db()
        cur = con.cursor()

        cur.execute(""" INSERT INTO options (pricing_model, option_type, spot_price, strike_price, time_till_exp, risk_free_rate, sigma, option_price)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?) """, (form.model.data, price[0], spot, strike, form.time.data, rfr, sigma, price[1]))
        cur.execute(""" INSERT INTO users_options (user_id, option_id) VALUES (?, ?) """, (g.user, cur.lastrowid))
        con.commit()

        return render_template("options/pricing.html", form=form, price=price)

    return render_template("options/pricing.html", form=form)


@bp.route("/calculations")
@login_required
def calculations():
    """
    The route for the calculations page. Shows the user's ten most
    recent option-pricing calculations.

    Renders
    -------
    options/calculations.html ( without previous calculations )
        If the user has no previous calculations.

    options/calculations.html ( with previous calculations )
        If the user has previous calculations.
    """

    con = get_db()
    cur = con.cursor()

    data = con.execute(""" SELECT pricing_model, option_type, spot_price, strike_price, time_till_exp, risk_free_rate, sigma, option_price
                             FROM options
                            WHERE id IN (SELECT option_id
                                           FROM users_options
                                          WHERE user_id = ?)
                            ORDER BY id DESC
                            LIMIT 10 """, (g.user,)).fetchall()

    if data:
        calcs = []

        for row in data:
            calcs.append({k: row[k] for k in row.keys()})

        return render_template("options/calculations.html", calcs=calcs)

    return render_template("options/calculations.html")
