from flask import Flask, jsonify, request

app = Flask(__name__)

def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.after_request
def after_request(response):
    return add_cors(response)

# --- 1. HALAMAN UTAMA (HTML) ---
@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YieldFlow AI Agent</title>
        <style>
            body {
                background-color: #0d1117; color: #c9d1d9;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                display: flex; justify-content: center; align-items: center;
                height: 100vh; margin: 0;
            }
            .container {
                text-align: center; padding: 50px; border: 1px solid #30363d;
                border-radius: 15px; background-color: #161b22;
                box-shadow: 0 8px 24px rgba(0,0,0,0.5); max-width: 500px;
            }
            h1 { color: #58a6ff; margin-bottom: 10px; }
            p { font-size: 16px; line-height: 1.5; color: #8b949e; margin-bottom: 30px; }
            .status-badge {
                padding: 8px 16px; background-color: #238636; color: #ffffff;
                border-radius: 20px; font-size: 14px; font-weight: bold;
                display: inline-block; border: 1px solid #2ea043;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>YieldFlow AI</h1>
            <p>Advanced DeFi yield aggregation and liquidity optimization agent. Scans for the highest APY opportunities, calculates impermanent loss risks, and provides auto-compounding strategies on the Base network.</p>
            <div class="status-badge">🟢 System Online & Healthy</div>
        </div>
    </body>
    </html>
    """
    return html_content

# --- 2. ENDPOINT MCP ---
@app.route('/mcp', methods=['GET', 'POST', 'OPTIONS'])
def mcp_endpoint():
    server_info = {
        "name": "YieldFlow Agent Server",
        "version": "1.0.0",
        "website": "https://yieldflow-api.vercel.app",
        "description": "DeFi yield optimization and liquidity agent"
    }
    tools = [
        {"name": "scan_high_yield_pools", "description": "Scan decentralized exchanges for the highest APY liquidity pools", "inputSchema": {"type": "object","properties": {}}},
        {"name": "calculate_impermanent_loss", "description": "Simulate and calculate potential impermanent loss for specific token pairs", "inputSchema": {"type": "object","properties": {}}},
        {"name": "auto_compound_rewards", "description": "Generate optimal auto-compounding routes for farmed tokens", "inputSchema": {"type": "object","properties": {}}}
    ]
    prompts = [
        {"name": "yield_farming_strategy", "description": "Generate a custom yield farming strategy based on risk tolerance", "arguments": []},
        {"name": "risk_adjusted_apy_report", "description": "Create a report comparing APY vs Smart Contract risks across protocols", "arguments": []}
    ]
    
    if request.method == 'GET':
        return jsonify({
            "protocolVersion": "2024-11-05",
            "serverInfo": server_info,
            "tools": tools,
            "prompts": prompts,
            "resources": [] 
        })

    req_data = request.get_json(silent=True) or {}
    req_id = req_data.get("id", 1)
    method = req_data.get("method", "")

    if method == "tools/list":
        result = {"tools": tools}
    elif method == "prompts/list":
        result = {"prompts": prompts}
    else:
        result = {
            "protocolVersion": "2024-11-05",
            "serverInfo": server_info,
            "capabilities": {"tools": {},"prompts": {},"resources": {}}
        }

    return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

# --- 3. ENDPOINT A2A (ID AKUN 16: 22389) ---
@app.route('/.well-known/agent-card.json', methods=['GET','OPTIONS'])
def a2a_endpoint():
    return jsonify({
        "id": "yieldflow",
        "name": "yieldflow",
        "version": "1.0.0",
        "description": "Advanced DeFi yield aggregation and liquidity optimization agent. Scans for the highest APY opportunities, calculates impermanent loss risks, and provides auto-compounding strategies on the Base network.",
        "website": "https://yieldflow-api.vercel.app",
        "url": "https://yieldflow-api.vercel.app",
        "documentation_url": "https://yieldflow-api.vercel.app",
        "provider": {
            "organization": "YieldFlow Finance",
            "url": "https://yieldflow-api.vercel.app"
        },
        "registrations": [
            {
                "agentId": 22389,
                "agentRegistry": "eip155:8453:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
            }
        ],
        "supportedTrust": ["reputation", "tee-attestation"],
        "skills": [
            {"name": "Yield Optimization", "description": "Maximize APY returns", "category": "defi/yield_optimization"},
            {"name": "Liquidity Provision", "description": "Find best liquidity pools", "category": "finance/liquidity_provision"},
            {"name": "Risk Assessment", "description": "Calculate impermanent loss", "category": "analytics/risk_assessment"}
        ]
    })

# --- 4. ENDPOINT OASF ---
@app.route('/oasf', methods=['GET','OPTIONS'])
def oasf_endpoint():
    return jsonify({
        "id": "yieldflow",
        "name": "yieldflow",
        "version": "v0.8.0",
        "description": "Main endpoint for YieldFlow AI",
        "website": "https://yieldflow-api.vercel.app",
        "protocols": ["mcp","a2a"],
        "capabilities": ["scan_high_yield_pools", "calculate_impermanent_loss", "auto_compound_rewards"],
        "skills": [
            {"name": "defi/yield_optimization","type": "operational"},
            {"name": "finance/liquidity_provision","type": "analytical"},
            {"name": "analytics/risk_assessment","type": "analytical"}
        ],
        "domains": [
            "web3/defi",
            "finance/yield_farming",
            "analytics/risk"
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
