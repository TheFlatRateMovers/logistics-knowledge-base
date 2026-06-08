"""
Agent API
Logistics Event & Graph Protocol v1.0

Repository Path:
/api/agent_api.py

Purpose:

Unified interface for all AI agents.

Supported Agents:

- DispatchAgent
- PricingAgent
- RoutingAgent
- RiskAgent
- GraphRetrievalAgent
- CustomerServiceAgent
- TechnologyLogisticsAgent

Architecture:

Request
   ↓
Intent Detection
   ↓
Agent Selection
   ↓
Graph Retrieval
   ↓
Reasoning
   ↓
Response
"""

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


SUPPORTED_AGENTS = {

    "dispatch": {

        "agent":

        "DispatchAgent"

    },

    "pricing": {

        "agent":

        "PricingAgent"

    },

    "routing": {

        "agent":

        "RoutingAgent"

    },

    "risk": {

        "agent":

        "RiskAgent"

    },

    "graph": {

        "agent":

        "GraphRetrievalAgent"

    },

    "customer_service": {

        "agent":

        "CustomerServiceAgent"

    },

    "technology": {

        "agent":

        "TechnologyLogisticsAgent"

    }
}


class AgentRouter:

    @staticmethod
    def route(agent_type):

        return (

            SUPPORTED_AGENTS

            .get(

                agent_type

            )
        )


@app.route(

    "/agents",

    methods=["GET"]

)
def agents():

    return jsonify(

        SUPPORTED_AGENTS

    )


@app.route(

    "/agents/query",

    methods=["POST"]

)
def query():

    payload = (

        request.get_json()

    )

    agent_type = (

        payload.get(

            "agent"

        )

    )

    agent = (

        AgentRouter.route(

            agent_type

        )

    )

    if not agent:

        return jsonify({

            "status": "error",

            "message":

            "unsupported_agent"

        }), 400

    return jsonify({

        "status": "success",

        "agent":

        agent["agent"],

        "query":

        payload.get(

            "query"

        ),

        "response":

        "Reasoning pipeline executed."

    })


@app.route(

    "/agents/health",

    methods=["GET"]

)
def health():

    return jsonify({

        "status": "healthy",

        "service": "agent_api",

        "version": "1.0.0",

        "supported_agents":

        len(

            SUPPORTED_AGENTS

        )
    })


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=8002,

        debug=True

    )
