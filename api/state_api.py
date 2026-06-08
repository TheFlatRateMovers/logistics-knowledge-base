"""
State API
Logistics Event & Graph Protocol v1.0

Repository Path:
/api/state_api.py

Purpose:

Provides access to
current operational state.

State Examples:

- Jobs
- Vehicles
- Crews
- Customers
- Shipments
- Equipment

Architecture:

Event Store
      ↓
State Reducer
      ↓
Current State Store
      ↓
State API
"""

from flask import Flask
from flask import jsonify

app = Flask(__name__)


CURRENT_STATE = {

    "jobs": {},

    "vehicles": {},

    "crews": {},

    "shipments": {},

    "customers": {}
}


@app.route(

    "/state",

    methods=["GET"]

)
def get_state():

    return jsonify(

        CURRENT_STATE

    )


@app.route(

    "/state/jobs",

    methods=["GET"]

)
def get_jobs():

    return jsonify(

        CURRENT_STATE["jobs"]

    )


@app.route(

    "/state/vehicles",

    methods=["GET"]

)
def get_vehicles():

    return jsonify(

        CURRENT_STATE["vehicles"]

    )


@app.route(

    "/state/crews",

    methods=["GET"]

)
def get_crews():

    return jsonify(

        CURRENT_STATE["crews"]

    )


@app.route(

    "/state/customers",

    methods=["GET"]

)
def get_customers():

    return jsonify(

        CURRENT_STATE["customers"]

    )


@app.route(

    "/state/health",

    methods=["GET"]

)
def health():

    return jsonify({

        "status": "healthy",

        "service": "state_api",

        "version": "1.0.0"

    })


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=8001,

        debug=True

    )
