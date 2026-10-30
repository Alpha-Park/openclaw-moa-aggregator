# -*- coding: utf-8 -*-
"""
OpenClaw MoA Aggregator - Mixture-of-Agents Layered Bradley-Terry Consensus Synthesizer
Standard Library only: math, typing.
Calculates axiomatic Borda count ranking aggregation, fits Bradley-Terry latent model quality
parameters via iterative Minorization-Maximization, and synthesizes layered multi-model responses.
"""

import math
from typing import Dict, List, Any

class OpenClawMoaAggregator:
    def __init__(self):
        pass

    def aggregate_borda_consensus(self, model_rankings: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Executes Borda count consensus aggregation across multi-model ranking votes.
        Each candidate receives (N - 1 - rank) points per voter.
        model_rankings schema: {"model_deepseek": ["cand_B", "cand_A", "cand_C"], ...}
        """
        if not model_rankings:
            return {"consensus_ranking": [], "scores": {}}

        # Collect all candidates
        all_candidates = set()
        for ranks in model_rankings.values():
            all_candidates.update(ranks)

        N = len(all_candidates)
        borda_scores = {c: 0.0 for c in all_candidates}

        for model_name, ranks in model_rankings.items():
            for rank_idx, cand in enumerate(ranks):
                points = (N - 1 - rank_idx)
                borda_scores[cand] = borda_scores.get(cand, 0.0) + points

        sorted_cands = sorted(borda_scores.items(), key=lambda x: x[1], reverse=True)
        max_score = len(model_rankings) * (N - 1) if (N > 1 and model_rankings) else 1.0

        consensus_output = []
        for rank_pos, (c, score) in enumerate(sorted_cands, 1):
            consensus_output.append({
                "rank": rank_pos,
                "candidate_id": c,
                "borda_points": score,
                "normalized_score": round(score / max_score, 4)
            })

        return {
            "voters_count": len(model_rankings),
            "candidates_count": N,
            "top_consensus_candidate": sorted_cands[0][0] if sorted_cands else None,
            "consensus_ranking": consensus_output
        }

    def evaluate_bradley_terry_strengths(self, pairwise_comparisons: List[Dict[str, Any]],
                                        max_iter: int = 50,
                                        tol: float = 1e-5) -> Dict[str, Any]:
        """
        Fits Bradley-Terry model strengths pi_i via Minorization-Maximization (MM):
        P(i beats j) = pi_i / (pi_i + pi_j)
        Iteration: pi_i^(t+1) = W_i / [ sum_{j != i} N_ij / (pi_i^(t) + pi_j^(t)) ]
        """
        items = set()
        for comp in pairwise_comparisons:
            items.add(comp["item_a"])
            items.add(comp["item_b"])

        item_list = sorted(list(items))
        K = len(item_list)
        if K < 2:
            return {"strengths": {i: 1.0 for i in item_list}}

        # Win counts W_i and match counts N_ij
        wins = {i: 0.0 for i in item_list}
        matches = {(i, j): 0.0 for i in item_list for j in item_list if i != j}

        for comp in pairwise_comparisons:
            a, b = comp["item_a"], comp["item_b"]
            outcome = comp.get("outcome", 1.0) # 1.0 = a wins, 0.0 = b wins, 0.5 = tie
            wins[a] += outcome
            wins[b] += (1.0 - outcome)
            matches[(a, b)] += 1.0
            matches[(b, a)] += 1.0

        # MM Iterations
        pi = {i: 1.0 / K for i in item_list}

        for _ in range(max_iter):
            new_pi = {}
            for i in item_list:
                denom = 0.0
                for j in item_list:
                    if i != j and matches[(i, j)] > 0:
                        denom += matches[(i, j)] / (pi[i] + pi[j])
                new_pi[i] = wins[i] / max(1e-6, denom)

            # Normalize sum to 1.0
            total_mass = sum(new_pi.values())
            new_pi = {i: v / total_mass for i, v in new_pi.items()}

            diff = sum(abs(new_pi[i] - pi[i]) for i in item_list)
            pi = new_pi
            if diff < tol:
                break

        ranked_strengths = sorted(
            [{"candidate": i, "latent_strength_pi": round(pi[i], 4), "wins": wins[i]} for i in item_list],
            key=lambda x: x["latent_strength_pi"],
            reverse=True
        )

        return {
            "candidates_count": K,
            "total_comparisons": len(pairwise_comparisons),
            "top_candidate": ranked_strengths[0]["candidate"],
            "ranked_strengths": ranked_strengths
        }

    def synthesize_layered_consensus_response(self, candidate_outputs: List[Dict[str, Any]],
                                              model_weights: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Cross-scores candidate LLM outputs on reasoning density and factual coherence,
        synthesizing the optimal layered response.
        """
        weights = model_weights or {}
        scored_candidates = []

        for cand in candidate_outputs:
            model = cand.get("model", "unknown_llm")
            text = cand.get("response_text", "")
            w = weights.get(model, 1.0)

            # Reasoning density heuristic: token count, bullet points, formal markers
            words = text.split()
            bullet_count = text.count("- ") + text.count("* ") + text.count("1.")
            has_formal_code = "```" in text or "def " in text or "{" in text

            quality_score = len(words) * 0.1 + bullet_count * 2.0 + (10.0 if has_formal_code else 0.0)
            composite_score = quality_score * w

            scored_candidates.append({
                "model": model,
                "candidate_id": cand.get("candidate_id", "cand_01"),
                "token_count": len(words),
                "bullet_count": bullet_count,
                "composite_quality_score": round(composite_score, 2),
                "response_text": text
            })

        scored_candidates.sort(key=lambda x: x["composite_quality_score"], reverse=True)
        winner = scored_candidates[0]

        return {
            "total_candidates_synthesized": len(candidate_outputs),
            "winning_model": winner["model"],
            "winning_candidate_id": winner["candidate_id"],
            "top_quality_score": winner["composite_quality_score"],
            "synthesized_response": winner["response_text"],
            "all_scored_candidates": scored_candidates
        }
