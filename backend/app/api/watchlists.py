"""
MarketPulse AI — Watchlist API Routes
GET /watchlists, POST /watchlists, POST /watchlists/{id}/items, DELETE /watchlists/{id}/items/{assetId}
"""
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.auth import User
from app.models.user_features import Watchlist, WatchlistItem
from app.schemas import WatchlistCreate, WatchlistResponse, WatchlistItemAdd
from app.security import get_current_user

router = APIRouter(prefix="/api/watchlists", tags=["Watchlists"])


@router.get("")
async def list_watchlists(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all watchlists for current user."""
    result = await db.execute(
        select(Watchlist)
        .options(selectinload(Watchlist.items))
        .where(Watchlist.user_id == current_user.id)
        .order_by(Watchlist.sort_order)
    )
    watchlists = result.scalars().all()

    return {
        "items": [
            {
                "id": str(w.id),
                "name": w.name,
                "description": w.description,
                "is_default": w.is_default,
                "item_count": len(w.items) if w.items else 0,
                "created_at": w.created_at.isoformat() if w.created_at else None,
            }
            for w in watchlists
        ],
        "total": len(watchlists),
    }


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_watchlist(
    data: WatchlistCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new watchlist."""
    # Check limit (free tier: 3 watchlists)
    result = await db.execute(
        select(Watchlist).where(Watchlist.user_id == current_user.id)
    )
    existing = result.scalars().all()
    if len(existing) >= 10:
        raise HTTPException(status_code=400, detail="Maximum watchlist limit reached")

    watchlist = Watchlist(
        id=uuid4(),
        user_id=current_user.id,
        name=data.name,
        description=data.description,
        sort_order=len(existing),
    )
    db.add(watchlist)
    await db.flush()

    return {
        "id": str(watchlist.id),
        "name": watchlist.name,
        "description": watchlist.description,
        "created_at": watchlist.created_at.isoformat() if watchlist.created_at else None,
    }


@router.post("/{watchlist_id}/items", status_code=status.HTTP_201_CREATED)
async def add_watchlist_item(
    watchlist_id: UUID,
    data: WatchlistItemAdd,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add an asset to a watchlist."""
    result = await db.execute(
        select(Watchlist).where(
            Watchlist.id == watchlist_id,
            Watchlist.user_id == current_user.id,
        )
    )
    watchlist = result.scalar_one_or_none()
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")

    item = WatchlistItem(
        id=uuid4(),
        watchlist_id=watchlist_id,
        asset_id=data.asset_id,
        target_price_high=data.target_price_high,
        target_price_low=data.target_price_low,
        notes=data.notes,
    )
    db.add(item)
    await db.flush()

    return {"id": str(item.id), "message": "Asset added to watchlist"}


@router.delete("/{watchlist_id}/items/{item_id}")
async def remove_watchlist_item(
    watchlist_id: UUID,
    item_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Remove an asset from a watchlist."""
    result = await db.execute(
        select(WatchlistItem)
        .join(Watchlist)
        .where(
            WatchlistItem.id == item_id,
            Watchlist.id == watchlist_id,
            Watchlist.user_id == current_user.id,
        )
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(item)
    return {"message": "Item removed from watchlist"}


@router.delete("/{watchlist_id}")
async def delete_watchlist(
    watchlist_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a watchlist."""
    result = await db.execute(
        select(Watchlist).where(
            Watchlist.id == watchlist_id,
            Watchlist.user_id == current_user.id,
        )
    )
    watchlist = result.scalar_one_or_none()
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")

    await db.delete(watchlist)
    return {"message": "Watchlist deleted"}
