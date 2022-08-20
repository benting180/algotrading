# How to use
```bash
python controller.py
```

# Environment
see `requirements.txt`
I am using python3.9 with anaconda


---

# Explaination
Cross-exchange market making
Also referred to as liquidity mirroring or exchange remarketing, this strategy allows you to make a market (creates buy and sell orders) on the maker exchange, while hedging any filled trades on a second, taker exchange. The strategy attempts places maker orders at spreads that are wider than taker orders by a spread equal to min_profitability. (copied from hummingbot)

# Potential improvement

## Software Engineering

### Scalibility

### Exception hanlding


## Strategy


# Reference
- https://youtu.be/jVIagFbQnmo
- https://hummingbot.org/strategies/cross-exchange-market-making/
- https://hummingbot.io/en/blog/2020-09-what-is-market-making/