# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawMoaAggregator

client = OpenClawMoaAggregator()

TOOLS = [
    {
        "name": "aggregate_borda_consensus",
        "description": "Calculates Borda count consensus ranking across multi-model ranked votes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "model_rankings": {"type": "object"}
            },
            "required": ["model_rankings"]
        }
    },
    {
        "name": "evaluate_bradley_terry_strengths",
        "description": "Fits Bradley-Terry latent model quality parameters via Minorization-Maximization.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pairwise_comparisons": {"type": "array", "items": {"type": "object"}}
            },
            "required": ["pairwise_comparisons"]
        }
    },
    {
        "name": "synthesize_layered_consensus_response",
        "description": "Cross-scores multi-agent candidate outputs to synthesize optimal layered consensus.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "candidate_outputs": {"type": "array", "items": {"type": "object"}},
                "model_weights": {"type": "object"}
            },
            "required": ["candidate_outputs"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "aggregate_borda_consensus":
            res = client.aggregate_borda_consensus(args["model_rankings"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "evaluate_bradley_terry_strengths":
            res = client.evaluate_bradley_terry_strengths(args["pairwise_comparisons"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "synthesize_layered_consensus_response":
            res = client.synthesize_layered_consensus_response(args["candidate_outputs"], args.get("model_weights"))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
