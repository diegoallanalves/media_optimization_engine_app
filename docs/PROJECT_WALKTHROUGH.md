# Project Walkthrough

## Business problem
A national media campaign has a finite budget and multiple markets competing for investment. Each market has different strategic priority and audience potential. Within a selected market, inventory differs by channel, publisher, price, availability, and minimum purchase size.

## Why two tiers?
Solving every strategic and inventory decision in one huge model can become harder to explain and scale. Tier 1 rapidly prioritizes the market search space and allocates budget. Tier 2 performs exact integer optimization inside each selected market.

## Tier 1
Normalized priority and normalized potential impressions are combined as:

`HeuristicScore = 0.60 × NormalizedPriority + 0.40 × NormalizedImpressions`

Selected markets receive at least their minimum budget and never exceed their maximum budget.

## Tier 2
For each inventory row, `x_i` is the integer number of 1,000-impression units purchased and `y_i` is a binary activation variable.

Objective: maximize total purchased impression units.

Constraints include available inventory, minimum purchase when activated, total market budget, and minimum/maximum channel budget shares.

## Clustering
The dashboard applies K-Means after optimization for exploratory segmentation only. It uses priority, market opportunity, allocated budget, delivered impressions, effective CPM and budget utilization. Clusters help explain different market profiles; they do not alter the optimization result.

## Interview demo
Start with the campaign KPIs, explain Tier 1, rotate the 3D chart, show the cluster profiles, then open Rules & validation to prove that the mathematical solution is also operationally feasible. Finish with Run history to demonstrate persistence and auditability.
