/**
 * MarketPulse AI — TypeScript Type Definitions
 * Shared types for the entire frontend application.
 */

// Signal types
export type SignalDirection = 'strong_bullish' | 'bullish' | 'neutral' | 'bearish' | 'strong_bearish';
export type RiskLevel = 'very_low' | 'low' | 'medium' | 'high' | 'very_high' | 'extreme';
export type TimeHorizon = 'immediate' | 'short_term' | 'swing' | 'medium_term' | 'structural';
export type ImpactDirection = 'bullish' | 'bearish' | 'neutral' | 'mixed' | 'uncertain';
export type AssetType = 'stock' | 'crypto' | 'index' | 'etf';

export interface Asset {
  symbol: string;
  name: string;
  asset_type: AssetType;
  sector?: string;
  industry?: string;
  country?: string;
  currency?: string;
  price?: number;
  market_cap?: number;
  change_pct?: number;
  data_quality_score?: number;
  liquidity_tier?: string;
  manipulation_risk?: boolean;
  low_liquidity_warning?: boolean;
  unverified_contract?: boolean;
  has_sufficient_history?: boolean;
}

export interface MarketPrice {
  price: number;
  price_change_24h?: number;
  price_change_pct_24h?: number;
  volume_24h?: number;
  market_cap?: number;
  high_24h?: number;
  low_24h?: number;
  open_24h?: number;
  currency: string;
  provider: string;
  data_timestamp: string;
  data_freshness: string;
  data_status: string;
}

export interface Candle {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number;
}

export interface TechnicalIndicators {
  timestamp: string;
  interval: string;
  rsi_14?: number;
  macd?: number;
  macd_signal?: number;
  macd_histogram?: number;
  sma_20?: number;
  sma_50?: number;
  sma_200?: number;
  ema_12?: number;
  ema_26?: number;
  bb_upper?: number;
  bb_middle?: number;
  bb_lower?: number;
  atr_14?: number;
  adx?: number;
  support_1?: number;
  resistance_1?: number;
}

export interface Signal {
  symbol: string;
  asset_name?: string;
  asset_type: string;
  direction: SignalDirection;
  final_score: number;
  confidence_score: number;
  risk_level: RiskLevel;
  time_horizon: TimeHorizon;
  price_at_signal: number;
  expected_move_low?: number;
  expected_move_high?: number;
  technical_score?: number;
  fundamental_score?: number;
  news_score?: number;
  market_context_score?: number;
  onchain_score?: number;
  data_quality_score?: number;
  risk_penalty?: number;
  bull_factors?: Array<{ factor: string; type: string; source: string }>;
  bear_factors?: Array<{ factor: string; type: string; source: string }>;
  key_risks?: Array<{ risk: string; severity: string }>;
  invalidation_conditions?: Array<{ condition: string; type: string }>;
  conflicting_signals?: any[];
  weights_used?: Record<string, number>;
  data_sources?: string[];
  feature_contributions?: Record<string, number>;
  calculation_timestamp: string;
  expires_at?: string;
  disclaimer: string;
  indicators?: TechnicalIndicators;
}

export interface NewsArticle {
  id: string;
  title: string;
  summary?: string;
  source_name?: string;
  published_at: string;
  relevance_score?: number;
  overall_sentiment?: number;
  impact_score?: number;
  impact_direction?: ImpactDirection;
  impact_time_horizon?: TimeHorizon;
  impact_pathway?: string;
  event_category?: string;
  is_verified: boolean;
  source_credibility_score?: number;
  related_assets?: string[];
}

export interface MarketOverview {
  timestamp: string;
  demo_mode: boolean;
  global_market: {
    indices: Array<{
      symbol: string;
      name: string;
      price: number;
      change_pct: number;
      country: string;
    }>;
    market_regime: string;
    risk_condition: string;
  };
  us_market: { indices: any[]; last_updated: string };
  id_market: { indices: any[]; last_updated: string };
  crypto_market: {
    total_market_cap?: number;
    btc_dominance?: number;
    eth_dominance?: number;
    fear_greed_index?: number;
    fear_greed_label?: string;
    last_updated: string;
  };
  top_gainers: any[];
  top_losers: any[];
  most_active: any[];
  market_regime: string;
  risk_condition: string;
  disclaimer: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
