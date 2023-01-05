import dash
import logging
import pathlib

from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from datetime import date
from dateutil import relativedelta
from flask import render_template_string
from flask_login import login_required
from flask.helpers import get_root_path

from app import app
from hubble_reports.hubble_reports import reports
from hubble_reports.utils import get_logger


logger = get_logger(__name__, level=logging.DEBUG)

dash_app = Dash(
    __name__,
    server=app,
    url_base_pathname="/report/",
    use_pages=True,
)

# FYI, you need both an app context and a request context to use url_for() in the Jinja2 templates
with app.app_context(), app.test_request_context():
    layout_dash = (
        pathlib.Path(get_root_path(__name__))
        .parent.joinpath("templates")
        .joinpath("dashboard.html")
    )
    logger.info(f"\n\n\n\n=========>>>layout_dash:\n{layout_dash}\n\n")

    with open(layout_dash, "r") as f:
        html_body = render_template_string(f.read())
        html_body = html_body.replace("HEADER", "Welcome User!!!")

dash_app.index_string = html_body

dash_app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.H1(id="topic-name",children="First"),
        html.Div(
            [
                dcc.DatePickerRange(
                    id="date-range-picker",
                    style={"width": 330},
                    max_date_allowed=date.today()
                ),
            ]
        ),
        html.Div(id="page-content"),
        dcc.Store(id="team_selected", storage_type="session"),
        dcc.Store(id="min_date_range", storage_type="session"),
        dcc.Store(id="max_date_range", storage_type="session"),
        dash.page_container,
    ]
)


@callback(
    Output("min_date_range", "data"),
    Output("max_date_range", "data"),
    Input("date-range-picker", "start_date"),
    Input("date-range-picker", "end_date"),
    )
def update_date_range(st_date, end_date):

    if (not st_date) and (not end_date):
        st_date = date.today()
        end_date = st_date - relativedelta.relativedelta(months=+6, days=+st_date.day-1)
        # raise PreventUpdate
    
    logger.info(f"\n\n\n\n\nUPdate Date range\nStart Date:\n{st_date}\t{type(st_date)}\n\nEnd Date:\n{end_date}\t{type(end_date)}\n\n")
    
    return st_date, end_date

@reports.route("/report")
def dash_entry():
    return dash_app.index()
