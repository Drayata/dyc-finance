# Data Sources

MarketPulse AI aggregates data from several external providers to generate its market intelligence.

## 1. Stock Market Data
- **Provider**: Alpha Vantage
- **Usage**: Historical EOD (End of Day) candle data, fundamental data (P/E, Market Cap, EPS), and technical indicators.
- **Compliance Notes**: Data is delayed or processed based on API tier constraints. 

## 2. Cryptocurrency Data
- **Provider**: CoinGecko
- **Usage**: Live prices, historical candles, market cap, volume, and basic on-chain metrics.
- **Compliance Notes**: CoinGecko free tier is used for the mock/development environment; a Pro API key is required for production volume.

## 3. Financial News Data
- **Provider**: NewsAPI (and integrated specific scrapers)
- **Usage**: Real-time article scraping for sentiment analysis.
- **Compliance Notes**: Full article texts are only used for transient processing and NLP scoring. Only titles and summaries are stored persistently.

## 4. Indonesian Stock Data
- **Provider**: IDX (Indonesia Stock Exchange) compliant providers (e.g., Yahoo Finance via yfinance, or specific licensed vendors).
- **Compliance Notes**: Adheres strictly to legal regulations regarding Indonesian market data distribution.
