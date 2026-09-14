# Interview Guide

## 30-second explanation
I built a two-tier media optimization engine in Python and SQL Server. Tier 1 uses
an explainable heuristic to prioritize markets and allocate the campaign budget.
Tier 2 uses Mixed-Integer Programming to maximize impressions inside each selected
market while respecting inventory, CPM pricing, minimum purchases, and channel-mix
business rules. The rules are configuration-driven from SQL Server, and the results
are persisted and visualized in Streamlit.

## Why two tiers?
The heuristic quickly reduces the combinatorial search space; MIP then performs
rigorous constrained optimization on the smaller downstream problem.

## Biggest challenge
A pure impressions objective naturally concentrates spend in the cheapest channel.
I handled that by expressing media-mix policy as explicit minimum and maximum
channel-spend constraints stored in SQL Server.

## Production scaling
Independent market MIPs can run in parallel. For enterprise deployment I would
containerize the service, use Gurobi/CPLEX where scale requires it, add automated
tests and monitoring, and deploy parallel workers on AWS or Azure.
