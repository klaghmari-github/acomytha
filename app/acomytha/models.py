"""Modèles métier SQLAlchemy (une classe = une table)."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str | None] = mapped_column(String(180), unique=True)
    display_name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(16))  # admin | parent | child
    password_hash: Mapped[str | None] = mapped_column(String(255))
    pin_hash: Mapped[str | None] = mapped_column(String(255))
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    parent: Mapped[User | None] = relationship(remote_side=[id])
    devices: Mapped[list[DeviceBinding]] = relationship(back_populates="user")


class DeviceBinding(Base):
    __tablename__ = "device_bindings"
    __table_args__ = (UniqueConstraint("user_id", name="uq_one_device_per_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    device_id: Mapped[str] = mapped_column(String(64), nullable=False)
    label: Mapped[str] = mapped_column(String(160), default="")
    user_agent: Mapped[str] = mapped_column(String(300), default="")
    bound_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    user: Mapped[User] = relationship(back_populates="devices")


class DeviceAlert(Base):
    __tablename__ = "device_alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    attempted_device_id: Mapped[str] = mapped_column(String(64), nullable=False)
    bound_device_id: Mapped[str] = mapped_column(String(64), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(300), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)


class SessionToken(Base):
    __tablename__ = "sessions"

    token: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    device_id: Mapped[str] = mapped_column(String(64), nullable=False)
    acting_role: Mapped[str] = mapped_column(String(16), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class Lesson(Base):
    __tablename__ = "lessons"

    lesson_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    domain_id: Mapped[str] = mapped_column(String(8))
    domain: Mapped[str] = mapped_column(String(80))
    subdomain_id: Mapped[str] = mapped_column(String(16), default="")
    subdomain: Mapped[str] = mapped_column(String(80), default="")
    framing: Mapped[str] = mapped_column(String(40), default="standard")
    objective: Mapped[str] = mapped_column(Text, default="")


class Story(Base):
    __tablename__ = "stories"

    story_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    editorial_id: Mapped[str] = mapped_column(String(64), unique=True)
    title: Mapped[str] = mapped_column(String(240))
    kind: Mapped[str] = mapped_column(String(16))
    age_band: Mapped[str] = mapped_column(String(8))
    age_range: Mapped[str] = mapped_column(String(16), default="")
    lesson_id: Mapped[str] = mapped_column(String(32), default="")
    secondary_lessons: Mapped[str] = mapped_column(String(200), default="")
    domain: Mapped[str] = mapped_column(String(8), default="")
    subdomain: Mapped[str] = mapped_column(String(16), default="")
    framing: Mapped[str] = mapped_column(String(40), default="standard")
    setting: Mapped[str] = mapped_column(String(120), default="")
    characters: Mapped[str] = mapped_column(String(200), default="")
    wait_default_ms: Mapped[int] = mapped_column(Integer, default=3000)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    duration_s: Mapped[int] = mapped_column(Integer, default=0)
    has_interaction: Mapped[bool] = mapped_column(Boolean, default=False)
    has_audio: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(32), default="APPROVED_TEXT")


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chunk_id: Mapped[str] = mapped_column(String(160), nullable=False)
    story_id: Mapped[str] = mapped_column(ForeignKey("stories.story_id"), nullable=False)
    kind: Mapped[str] = mapped_column(String(32))
    lesson_id: Mapped[str] = mapped_column(String(32), default="")
    text: Mapped[str] = mapped_column(Text, default="")
    option_1_label: Mapped[str] = mapped_column(String(80), default="")
    option_1_next: Mapped[str] = mapped_column(String(160), default="")
    option_2_label: Mapped[str] = mapped_column(String(80), default="")
    option_2_next: Mapped[str] = mapped_column(String(160), default="")
    option_3_label: Mapped[str] = mapped_column(String(80), default="")
    option_3_next: Mapped[str] = mapped_column(String(160), default="")
    default_next: Mapped[str] = mapped_column(String(160), default="")
    wait_ms: Mapped[int] = mapped_column(Integer, default=0)
    night_policy: Mapped[str] = mapped_column(String(24), default="play")

    __table_args__ = (UniqueConstraint("story_id", "chunk_id", name="uq_story_chunk"),)


class ForestEntry(Base):
    __tablename__ = "forest"
    __table_args__ = (UniqueConstraint("parent_id", "story_id", name="uq_forest"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    story_id: Mapped[str] = mapped_column(ForeignKey("stories.story_id"), nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class AppSetting(Base):
    __tablename__ = "app_settings"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[str] = mapped_column(String(400), default="")
    label: Mapped[str] = mapped_column(String(200), default="")


class Wallet(Base):
    __tablename__ = "wallets"

    parent_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    balance_a: Mapped[float] = mapped_column(Float, default=0.0)
    lifetime_eur: Mapped[float] = mapped_column(Float, default=0.0)


class LedgerEntry(Base):
    __tablename__ = "ledger"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    kind: Mapped[str] = mapped_column(String(32))
    amount_a: Mapped[float] = mapped_column(Float, default=0.0)
    amount_eur: Mapped[float] = mapped_column(Float, default=0.0)
    ref: Mapped[str] = mapped_column(String(80), default="")
    note: Mapped[str] = mapped_column(String(240), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class Purchase(Base):
    __tablename__ = "purchases"
    __table_args__ = (UniqueConstraint("parent_id", "item_type", "item_id", name="uq_purchase"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    item_type: Mapped[str] = mapped_column(String(16))  # story | tree
    item_id: Mapped[str] = mapped_column(String(64))
    price_a: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class StoryOrder(Base):
    __tablename__ = "story_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    context: Mapped[str] = mapped_column(Text, default="")
    ramifications: Mapped[int] = mapped_column(Integer, default=0)
    price_a: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(16), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class VoiceProfile(Base):
    __tablename__ = "voices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(32), default="narrateur")
    path: Mapped[str] = mapped_column(String(400), default="")
    applied_all: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class StoryIdea(Base):
    __tablename__ = "story_ideas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(180), default="")
    text: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class StripeSession(Base):
    __tablename__ = "stripe_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    ref: Mapped[str] = mapped_column(String(80), unique=True)
    provider_id: Mapped[str] = mapped_column(String(120), default="")
    eur: Mapped[float] = mapped_column(Float, default=0.0)
    amount_a: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(16), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
