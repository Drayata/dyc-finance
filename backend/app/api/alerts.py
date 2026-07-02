"""
MarketPulse AI — Alert API Routes
GET /alerts, POST /alerts, PATCH /alerts/{id}, DELETE /alerts/{id}
"""
from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.auth import User
from app.models.user_features import AlertRule, AlertType, AlertPriority
from app.schemas import AlertCreate, AlertUpdate, AlertResponse
from app.security import get_current_user

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


@router.get("")
async def list_alerts(
    is_active: bool = Query(True),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all alerts for current user."""
    query = select(AlertRule).where(
        AlertRule.user_id == current_user.id,
    )
    if is_active is not None:
        query = query.where(AlertRule.is_active == is_active)

    result = await db.execute(query.order_by(AlertRule.created_at.desc()))
    alerts = result.scalars().all()

    return {
        "items": [
            {
                "id": str(a.id),
                "asset_id": str(a.asset_id),
                "alert_type": a.alert_type.value if a.alert_type else None,
                "condition": a.condition,
                "priority": a.priority.value if a.priority else None,
                "channels": a.channels,
                "is_active": a.is_active,
                "trigger_count": a.trigger_count,
                "last_triggered_at": a.last_triggered_at.isoformat() if a.last_triggered_at else None,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in alerts
        ],
        "total": len(alerts),
    }


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_alert(
    data: AlertCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new alert rule."""
    # Check limit
    result = await db.execute(
        select(AlertRule).where(
            AlertRule.user_id == current_user.id,
            AlertRule.is_active == True,
        )
    )
    active_alerts = result.scalars().all()
    if len(active_alerts) >= 50:
        raise HTTPException(status_code=400, detail="Maximum active alert limit reached")

    alert = AlertRule(
        id=uuid4(),
        user_id=current_user.id,
        asset_id=data.asset_id,
        alert_type=AlertType(data.alert_type),
        condition=data.condition,
        priority=AlertPriority(data.priority),
        channels=data.channels,
        cooldown_minutes=data.cooldown_minutes,
        is_one_time=data.is_one_time,
    )
    db.add(alert)
    await db.flush()

    return {"id": str(alert.id), "message": "Alert created"}


@router.patch("/{alert_id}")
async def update_alert(
    alert_id: UUID,
    data: AlertUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an alert rule."""
    result = await db.execute(
        select(AlertRule).where(
            AlertRule.id == alert_id,
            AlertRule.user_id == current_user.id,
        )
    )
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(alert, field, value)
    alert.updated_at = datetime.now(timezone.utc)
    await db.flush()

    return {"message": "Alert updated"}


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an alert rule."""
    result = await db.execute(
        select(AlertRule).where(
            AlertRule.id == alert_id,
            AlertRule.user_id == current_user.id,
        )
    )
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    await db.delete(alert)
    return {"message": "Alert deleted"}
