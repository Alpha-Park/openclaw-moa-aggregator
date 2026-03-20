# openclaw-moa-aggregator (Mixture-of-Agents Intelligence)

An advanced OpenClaw skill implementing the **Mixture-of-Agents (MoA)** architecture. It coordinates multiple specialized sub-agents to generate a single, high-fidelity synthesis of information, optimized for competitive intelligence and complex decision-making.

## Architecture: The MoA Loop
1.  **Proposal Phase (Layer 1)**: Parallel sub-agents (e.g., Search Agent, Finance Agent, Social Sentiment Agent) generate independent perspectives.
2.  **Aggregation Phase (Layer 2)**: A Critic/Synthesizer agent reviews all proposals, identifies hallucinations, and merges them into a cohesive "Final Truth."

## Tools

### `moa_intel_synthesis`
Runs a multi-agent loop to analyze a market or competitor.
- `topic`: The target for analysis (e.g., "Genspark's Series B move vs GenPark").
- `agents`: List of personas to involve (e.g., ["skeptic", "visionary", "analyst"]).

### `moa_execute_complex`
Breaks down a complex business goal into agent-specific sub-tasks.

## Usage
"Genius, run an MoA analysis on Genspark's $300M funding. I want a skeptic and a financial analyst's view merged."

## GitHub Integration
Part of the Alpha-Park Intelligence Suite.
