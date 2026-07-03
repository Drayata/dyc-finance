from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from datetime import datetime, timedelta

from app.security import get_current_user
from app.providers.registry import registry
from app.analytics.backtesting import backtest_engine
from app.analytics.signal_engine import signal_engine

router = APIRouter(prefix="/api/backtests", tags=["backtests"])

@router.post("/")
async def run_backtest(
    request: Dict[str, Any],
    current_user: Any = Depends(get_current_user)
):
    """
    Run a backtest for a specific asset over a historical period.
    """
    symbol = request.get("symbol")
    days = request.get("days", 365)
    tp_pct = request.get("take_profit_pct", 0.05)
    sl_pct = request.get("stop_loss_pct", 0.02)
    
    if not symbol:
        raise HTTPException(status_code=400, detail="Symbol is required")
        
    try:
        # 1. Fetch historical candles
        market_provider = registry.get_market_provider(request.get("asset_type", "stock"))
        candles = await market_provider.get_candles(symbol, interval="1d", limit=days)
        
        if not candles:
            raise HTTPException(status_code=404, detail=f"No historical data found for {symbol}")
            
        # 2. Simulate historical signals (In a real system, we'd query the DB for saved historical signals)
        # For MVP, we will mock historical signals by running a simple moving average crossover on the candles
        mock_signals = []
        for i in range(20, len(candles)):
            # Extremely simple mock signal generation for the backtest demonstration
            short_sma = sum(c["close"] for c in candles[i-10:i]) / 10
            long_sma = sum(c["close"] for c in candles[i-20:i]) / 20
            
            if short_sma > long_sma:
                mock_signals.append({
                    "timestamp": candles[i]["timestamp"],
                    "direction": "bullish"
                })
                
        # 3. Run backtest
        result = backtest_engine.run_backtest(
            symbol=symbol,
            historical_candles=candles,
            signals=mock_signals,
            strategy_config={
                "take_profit_pct": tp_pct,
                "stop_loss_pct": sl_pct
            }
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backtest failed: {str(e)}")

@router.get("/{backtest_id}")
async def get_backtest(
    backtest_id: str,
    current_user: Any = Depends(get_current_user)
):
    """
    Retrieve a previously run backtest result (mocked for MVP).
    """
    return {"status": "ok", "message": "Backtest history retrieval not fully implemented in MVP"}
