"""Liaison une clé ↔ un appareil + alertes admin."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from sentier.models import DeviceAlert, DeviceBinding, User


class DeviceGuard:
    """Premier device_id gagne. Tout autre déclenche une alerte et refuse."""

    def assert_or_bind(
        self,
        db: Session,
        user: User,
        device_id: str,
        user_agent: str = "",
        label: str = "",
    ) -> DeviceBinding:
        holder = self._license_holder(user)
        row = db.query(DeviceBinding).filter(DeviceBinding.user_id == holder.id).one_or_none()
        if row is None:
            row = DeviceBinding(
                user_id=holder.id,
                device_id=device_id,
                label=label or "appareil",
                user_agent=user_agent[:300],
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return row
        if row.device_id == device_id:
            row.last_seen_at = datetime.now(timezone.utc)
            row.user_agent = user_agent[:300] or row.user_agent
            db.commit()
            return row
        alert = DeviceAlert(
            user_id=holder.id,
            attempted_device_id=device_id,
            bound_device_id=row.device_id,
            user_agent=user_agent[:300],
        )
        db.add(alert)
        db.commit()
        raise DeviceConflict(holder, row, alert)

    def reset(self, db: Session, user_id: int) -> None:
        db.query(DeviceBinding).filter(DeviceBinding.user_id == user_id).delete()
        db.commit()

    def _license_holder(self, user: User) -> User:
        if user.role == "child" and user.parent is not None:
            return user.parent
        return user


class DeviceConflict(Exception):
    def __init__(self, user: User, binding: DeviceBinding, alert: DeviceAlert) -> None:
        super().__init__("appareil non autorisé")
        self.user = user
        self.binding = binding
        self.alert = alert
