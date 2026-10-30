# -*- coding: utf-8 -*-
from client import OpenClawMoaAggregator

moa = OpenClawMoaAggregator()

# 1. Borda Count Consensus
rankings = {
    "deepseek_r1": ["cand_B", "cand_A", "cand_C"],
    "claude_35_sonnet": ["cand_A", "cand_B", "cand_C"],
    "gpt_4o": ["cand_B", "cand_C", "cand_A"]
}
borda = moa.aggregate_borda_consensus(rankings)
print(f"Borda Winner: {borda['top_consensus_candidate']}")
for r in borda['consensus_ranking']:
    print(f"  Rank {r['rank']}: {r['candidate_id']} ({r['borda_points']} pts)")

# 2. Bradley-Terry Latent Strengths
comparisons = [
    {"item_a": "model_r1", "item_b": "model_gpt", "outcome": 1.0},
    {"item_a": "model_r1", "item_b": "model_claude", "outcome": 0.5},
    {"item_a": "model_claude", "item_b": "model_gpt", "outcome": 1.0}
]
bt = moa.evaluate_bradley_terry_strengths(comparisons)
print(f"\nBradley-Terry Top Model: {bt['top_candidate']}")
for s in bt['ranked_strengths']:
    print(f"  {s['candidate']}: Pi={s['latent_strength_pi']}")

# 3. Layered Output Synthesis
outputs = [
    {"candidate_id": "c1", "model": "model_r1", "response_text": "Solution:\n1. Compute eigenvalues\n2. Verify proof\n```python\nreturn True\n```"},
    {"candidate_id": "c2", "model": "model_gpt", "response_text": "Here is the short answer: Yes, it is true."}
]
synth = moa.synthesize_layered_consensus_response(outputs, model_weights={"model_r1": 1.2, "model_gpt": 1.0})
print(f"\nSynthesized Winner: {synth['winning_candidate_id']} by {synth['winning_model']} (Score: {synth['top_quality_score']})")
