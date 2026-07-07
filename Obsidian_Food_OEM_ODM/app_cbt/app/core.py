from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, Response, abort, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
from pydantic import BaseModel, Field
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    func,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker
import requests


BASE_DIR = Path(__file__).resolve().parents[1]
VAULT_DIR = BASE_DIR.parent
DB_PATH = BASE_DIR / "data" / "cbt_app.db"
FACTORY_SEED = VAULT_DIR / "database" / "korea_oem_odm_seed.csv"
RULE_SEED = VAULT_DIR / "database" / "regulatory_screening_rules_seed.csv"
GENERATED_DIR = BASE_DIR / "generated"
SAM_BASE_URL = os.getenv("SAM_BASE_URL", "https://sam.soonsoon.ai")
SAM_API_KEY = os.getenv("SAM_API_KEY", "")
SAM_DEFAULT_MODEL = os.getenv("SAM_MODEL", "az-deepseek-v4-flash")
DEEPSEEK_MODELS = ["az-deepseek-v4-flash", "az-deepseek-v4-pro"]

PRODUCT_CASES = {
    "health_snack": {
        "label": "건강간식",
        "aliases": ["건강간식", "그래놀라", "쿠키", "바", "스낵", "프로틴바", "곡물"],
        "process": ["배합", "성형", "굽기/건조", "냉각", "개별포장"],
        "packages": ["개별포장", "파우치"],
        "ingredients": [
            ("주원료", "귀리/현미/곡물 베이스", "제한 가능", "밀"),
            ("단백질원", "분리대두단백 또는 유청단백", "가능", "대두/우유"),
            ("감미료", "알룰로스 또는 에리스리톨", "가능", ""),
            ("식감 보완", "견과류 또는 식이섬유", "가능", "견과류"),
        ],
        "questions": ["당류/단백질 분석 지원이 가능한가", "알레르기 교차오염 관리 기준이 있는가"],
    },
    "powder_stick": {
        "label": "분말스틱",
        "aliases": ["분말", "스틱", "파우더", "쉐이크", "식이섬유", "건강식품"],
        "process": ["원료계량", "혼합", "체질", "스틱충진", "금속검출"],
        "packages": ["스틱", "파우치"],
        "ingredients": [
            ("주원료", "식이섬유/단백질/곡물 분말", "제한 가능", ""),
            ("향미", "코코아/라떼/과일 향미", "가능", "우유"),
            ("감미료", "알룰로스 또는 스테비아", "가능", ""),
            ("기능성 후보", "프로바이오틱스 또는 비타민", "제한 가능", ""),
        ],
        "questions": ["일반식품과 건강기능식품 중 어느 범위가 가능한가", "스틱포 단위 표시 검수가 가능한가"],
    },
    "sauce": {
        "label": "소스",
        "aliases": ["소스", "드레싱", "양념", "육수", "시즈닝", "매운"],
        "process": ["배합", "가열/살균", "충진", "냉각", "포장"],
        "packages": ["파우치", "병"],
        "ingredients": [
            ("베이스", "고추/간장/채소 추출 베이스", "가능", "대두/밀"),
            ("향미", "마늘/양파/향신료", "가능", ""),
            ("감미/염도", "대체당 또는 저염 설계", "가능", ""),
            ("안정화", "산도조절제 또는 점도 조절 원료", "제한 가능", ""),
        ],
        "questions": ["살균 조건과 보존 기준을 제안할 수 있는가", "파우치/병 포장재 식품용 증빙 제공이 가능한가"],
    },
}

SALES_TYPES = {"D2C", "공동구매", "프랜차이즈", "PB", "B2B", "B2C"}

VIBE_TARGETS = {
    "solo": "1인 가구 온라인 테스트 고객",
    "family": "가족 단위 건강 간편식 구매자",
    "office": "오피스 간식/식사 대체 수요",
    "senior": "고령친화/케어푸드 수요",
    "franchise": "프랜차이즈 반복 발주 담당자",
}

VIBE_SCENES = {
    "breakfast": "아침 대용",
    "snack": "오후 간식",
    "meal": "간편 식사",
    "workout": "운동 전후 보충",
    "gift": "시즌 한정 선물/프로모션",
}

VIBE_TEXTURES = {
    "crispy": "바삭한 식감",
    "chewy": "쫀득한 식감",
    "soft": "부드러운 식감",
    "creamy": "크리미한 질감",
    "clean": "깔끔한 목넘김",
}

VIBE_PROCESS_MODES = {
    "low_sugar": "저당 설계",
    "high_protein": "고단백 설계",
    "hmr": "HMR/RMR 제조",
    "powder": "분말/스틱 충진",
    "sauce": "가열 살균 소스",
    "care": "케어푸드 물성 관리",
}


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    company_type: Mapped[str] = mapped_column(String(40), default="brand")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(80))
    role: Mapped[str] = mapped_column(String(30), default="operator")
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))


class Factory(Base):
    __tablename__ = "factories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    factory_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    company_name: Mapped[str] = mapped_column(String(200), index=True)
    primary_category: Mapped[str] = mapped_column(String(160), index=True)
    product_keywords: Mapped[str] = mapped_column(Text)
    oem_signal: Mapped[bool] = mapped_column(Boolean, default=False)
    odm_signal: Mapped[bool] = mapped_column(Boolean, default=False)
    certification_signal: Mapped[str] = mapped_column(String(220), default="")
    location_signal: Mapped[str] = mapped_column(String(160), default="")
    mvp_fit: Mapped[str] = mapped_column(String(5), index=True, default="C")
    source_url: Mapped[str] = mapped_column(Text, default="")
    verification_status: Mapped[str] = mapped_column(String(40), index=True, default="미확인")
    next_action: Mapped[str] = mapped_column(Text, default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())


class RegulatoryRule(Base):
    __tablename__ = "regulatory_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rule_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    scope: Mapped[str] = mapped_column(String(80), index=True)
    trigger_field: Mapped[str] = mapped_column(String(80), index=True)
    trigger_value: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(20), index=True)
    check_item: Mapped[str] = mapped_column(Text)
    required_evidence: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str] = mapped_column(Text)
    system_action: Mapped[str] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class ProductRequest(Base):
    __tablename__ = "product_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_uid: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    product_case: Mapped[str] = mapped_column(String(40), index=True)
    product_case_label: Mapped[str] = mapped_column(String(40))
    raw_prompt: Mapped[str] = mapped_column(Text)
    sales_type: Mapped[str] = mapped_column(String(40), index=True)
    target_qty: Mapped[int] = mapped_column(Integer, index=True)
    qty_unit: Mapped[str] = mapped_column(String(20), default="개")
    package_type: Mapped[str] = mapped_column(String(60), default="")
    llm_model: Mapped[str] = mapped_column(String(80), default=SAM_DEFAULT_MODEL)
    claim_list: Mapped[str] = mapped_column(Text, default="[]")
    taste_tags: Mapped[str] = mapped_column(Text, default="[]")
    target_price: Mapped[str] = mapped_column(String(80), default="")
    status: Mapped[str] = mapped_column(String(40), index=True, default="draft")
    is_dummy: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())

    spec: Mapped["ProductSpec"] = relationship(back_populates="request", cascade="all, delete-orphan")
    recipe: Mapped["RecipeDraft"] = relationship(back_populates="request", cascade="all, delete-orphan")


class ProductSpec(Base):
    __tablename__ = "product_specs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), unique=True, index=True)
    concept: Mapped[str] = mapped_column(Text)
    process_list: Mapped[str] = mapped_column(Text)
    package_condition: Mapped[str] = mapped_column(Text)
    storage_condition: Mapped[str] = mapped_column(String(80))
    cost_assumption: Mapped[str] = mapped_column(Text)
    validation_questions: Mapped[str] = mapped_column(Text)
    request: Mapped[ProductRequest] = relationship(back_populates="spec")


class RecipeDraft(Base):
    __tablename__ = "recipe_drafts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), unique=True, index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    batch_size: Mapped[str] = mapped_column(String(80))
    unit_weight: Mapped[str] = mapped_column(String(80))
    yield_rate: Mapped[float] = mapped_column(Float, default=0.92)
    quality_targets: Mapped[str] = mapped_column(Text)
    request: Mapped[ProductRequest] = relationship(back_populates="recipe")


class IngredientLine(Base):
    __tablename__ = "ingredient_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), index=True)
    ingredient_role: Mapped[str] = mapped_column(String(80))
    ingredient_name: Mapped[str] = mapped_column(String(180))
    ratio_range: Mapped[str] = mapped_column(String(60))
    allergen_flag: Mapped[str] = mapped_column(String(120), default="")
    substitute_allowed: Mapped[str] = mapped_column(String(40), default="가능")


class ScreeningRun(Base):
    __tablename__ = "screening_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), index=True)
    overall_status: Mapped[str] = mapped_column(String(20), index=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())


class ScreeningFinding(Base):
    __tablename__ = "screening_findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    screening_run_id: Mapped[int] = mapped_column(ForeignKey("screening_runs.id"), index=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), index=True)
    rule_id: Mapped[str] = mapped_column(String(20), index=True)
    severity: Mapped[str] = mapped_column(String(20), index=True)
    message: Mapped[str] = mapped_column(Text)
    required_evidence: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str] = mapped_column(Text)


class MatchResult(Base):
    __tablename__ = "match_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), index=True)
    factory_id: Mapped[int] = mapped_column(ForeignKey("factories.id"), index=True)
    score: Mapped[float] = mapped_column(Float, index=True)
    reason: Mapped[str] = mapped_column(Text)
    confirm_questions: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="candidate", index=True)


class ProductPlan(Base):
    __tablename__ = "product_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), unique=True, index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(40), index=True, default="plan_ready")
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())


class SampleBrief(Base):
    __tablename__ = "sample_briefs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), unique=True, index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(40), index=True, default="draft")
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())


class PurchaseOrderRequest(Base):
    __tablename__ = "purchase_order_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    po_uid: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), index=True)
    status: Mapped[str] = mapped_column(String(40), index=True, default="draft")
    order_type: Mapped[str] = mapped_column(String(40), default="sample_po")
    buyer_company: Mapped[str] = mapped_column(String(160), default="")
    buyer_contact: Mapped[str] = mapped_column(String(120), default="")
    supplier_company: Mapped[str] = mapped_column(String(160), default="")
    supplier_contact: Mapped[str] = mapped_column(String(120), default="")
    order_date: Mapped[str] = mapped_column(String(20), default="")
    due_date: Mapped[str] = mapped_column(String(20), default="")
    delivery_place: Mapped[str] = mapped_column(Text, default="")
    payment_terms: Mapped[str] = mapped_column(Text, default="")
    delivery_terms: Mapped[str] = mapped_column(Text, default="")
    inspection_terms: Mapped[str] = mapped_column(Text, default="")
    vat_type: Mapped[str] = mapped_column(String(40), default="VAT 별도")
    currency: Mapped[str] = mapped_column(String(10), default="KRW")
    raw_order_form: Mapped[str] = mapped_column(Text, default="")
    line_items: Mapped[str] = mapped_column(Text, default="[]")
    subtotal: Mapped[float] = mapped_column(Float, default=0)
    vat_amount: Mapped[float] = mapped_column(Float, default=0)
    total_amount: Mapped[float] = mapped_column(Float, default=0)
    quality_terms: Mapped[str] = mapped_column(Text, default="[]")
    required_documents: Mapped[str] = mapped_column(Text, default="[]")
    risk_flags: Mapped[str] = mapped_column(Text, default="[]")
    is_dummy: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())


class CostCalculation(Base):
    __tablename__ = "cost_calculations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    target_qty: Mapped[int] = mapped_column(Integer)
    serving_unit: Mapped[str] = mapped_column(String(30))
    total_cost: Mapped[float] = mapped_column(Float)
    unit_cost: Mapped[float] = mapped_column(Float)
    supply_price: Mapped[float] = mapped_column(Float)
    vat_included_total: Mapped[float] = mapped_column(Float)
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())


class ToolRun(Base):
    __tablename__ = "tool_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), index=True)
    tool_name: Mapped[str] = mapped_column(String(80), index=True)
    input_hash: Mapped[str] = mapped_column(String(64), index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(30), index=True)
    summary: Mapped[str] = mapped_column(Text)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    error_code: Mapped[str] = mapped_column(String(80), default="")


class GeneratedFile(Base):
    __tablename__ = "generated_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_uid: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("product_requests.id"), index=True)
    doc_type: Mapped[str] = mapped_column(String(40), index=True)
    storage_path: Mapped[str] = mapped_column(Text)
    checksum: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: now_utc())


engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def db_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def as_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def from_json(value: str, default: Any) -> Any:
    try:
        return json.loads(value) if value else default
    except json.JSONDecodeError:
        return default


def make_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def api_error(status_code: int, detail: str) -> None:
    response = jsonify({"detail": detail})
    response.status_code = status_code
    abort(response)


def query_int(name: str, default: int, min_value: int | None = None, max_value: int | None = None) -> int:
    try:
        value = int(request.args.get(name, default))
    except (TypeError, ValueError):
        value = default
    if min_value is not None:
        value = max(value, min_value)
    if max_value is not None:
        value = min(value, max_value)
    return value


def query_bool(name: str) -> bool | None:
    value = request.args.get(name)
    if value is None:
        return None
    return value.lower() in {"1", "true", "yes", "y"}


def json_payload(model: type[BaseModel]) -> BaseModel:
    try:
        return model.model_validate(request.get_json(silent=True) or {})
    except Exception as exc:
        api_error(422, str(exc))


class ProductRequestCreate(BaseModel):
    raw_prompt: str = Field(..., min_length=2)
    product_case: str | None = None
    sales_type: str = "D2C"
    target_qty_text: str | None = None
    target_qty: int | None = Field(None, ge=1)
    qty_unit: str | None = None
    package_type: str | None = None
    claim_list: list[str] = Field(default_factory=list)
    taste_tags: list[str] = Field(default_factory=list)
    target_price: str | None = None
    llm_model: str = SAM_DEFAULT_MODEL
    use_llm: bool = True
    user_id: int = 1
    is_dummy: bool = False
    run_full: bool = True


class VibeCookingCompose(BaseModel):
    product_case: str = "health_snack"
    base_idea: str = Field(..., min_length=2)
    target_customer: str = "solo"
    eating_scene: str = "snack"
    texture: str = "crispy"
    process_mode: str = "low_sugar"
    key_ingredients: list[str] = Field(default_factory=list)
    avoid_ingredients: list[str] = Field(default_factory=list)
    claim_list: list[str] = Field(default_factory=list)
    sales_type: str = "D2C"
    package_type: str = "개별포장"
    target_qty_text: str = "1,000개"
    target_price: str | None = None


class VibeAgentRun(BaseModel):
    planning_goal: str = "샘플 발주 가능한 제품 기획으로 정리"
    include_revision_prompt: bool = True


class FactoryCreate(BaseModel):
    company_name: str
    primary_category: str
    product_keywords: str
    certification_signal: str = ""
    location_signal: str = ""
    mvp_fit: str = "B"
    source_url: str = ""
    verification_status: str = "수동등록"
    notes: str = ""


class FactoryPatch(BaseModel):
    verification_status: str | None = None
    active: bool | None = None
    notes: str | None = None
    next_action: str | None = None


class CostCalculationCreate(BaseModel):
    ingredient_cost: float = Field(450, ge=0)
    packaging_cost: float = Field(120, ge=0)
    manufacturing_fee: float = Field(250, ge=0)
    sample_fee: float = Field(300000, ge=0)
    test_fee: float = Field(250000, ge=0)
    logistics_fee: float = Field(100000, ge=0)
    platform_fee: float = Field(0, ge=0)
    vat_rate: float = Field(0.1, ge=0)
    margin_target: float = Field(0.35, ge=0, lt=0.95)
    serving_unit: str = "1개"


class PurchaseOrderLineCreate(BaseModel):
    item_name: str = Field(..., min_length=1)
    specification: str = ""
    unit: str = "개"
    quantity: float = Field(..., gt=0)
    unit_price: float = Field(0, ge=0)
    requested_delivery_date: str = ""
    notes: str = ""


class PurchaseOrderCreate(BaseModel):
    order_type: str = "sample_po"
    buyer_company: str = "CBT 운영사"
    buyer_contact: str = "브랜드 담당자"
    supplier_company: str = ""
    supplier_contact: str = ""
    order_date: str = ""
    due_date: str = ""
    delivery_place: str = ""
    payment_terms: str = "세금계산서 발행 후 30일 이내 지급"
    delivery_terms: str = "납품 전 일정 확정, 운송비 포함 여부 별도 확인"
    inspection_terms: str = "입고 수량, 외관, 표시사항, 시험성적서 확인 후 검수"
    vat_type: str = "VAT 별도"
    currency: str = "KRW"
    raw_order_form: str = ""
    line_items: list[PurchaseOrderLineCreate] = Field(default_factory=list)
    quality_terms: list[str] = Field(default_factory=list)
    required_documents: list[str] = Field(default_factory=list)
    is_dummy: bool = False


class PurchaseOrderFormParse(BaseModel):
    raw_order_form: str = Field(..., min_length=2)


def detect_case(raw_prompt: str, selected_case: str | None) -> str:
    if selected_case in PRODUCT_CASES:
        return selected_case
    text = raw_prompt.lower()
    for case_key, meta in PRODUCT_CASES.items():
        if any(alias.lower() in text for alias in meta["aliases"]):
            return case_key
    return "health_snack"


def normalize_qty(target_qty: int | None, target_qty_text: str | None) -> tuple[int, str]:
    if target_qty:
        return target_qty, "개"
    text = target_qty_text or ""
    compact = text.replace(",", "")
    match = re.search(r"(\d+(?:\.\d+)?)\s*(만|천|톤|kg|KG|포|개|병|팩)?", compact)
    if not match:
        return 1000, "개"
    number = float(match.group(1))
    unit = match.group(2) or "개"
    if unit == "만":
        return int(number * 10000), "개"
    if unit == "천":
        return int(number * 1000), "개"
    if unit == "톤":
        return int(number * 1000), "kg"
    return int(number), unit.lower() if unit.upper() == "KG" else unit


def normalize_claims(raw_prompt: str, claim_list: list[str]) -> list[str]:
    candidates = ["저당", "무당", "무가당", "제로슈가", "고단백", "프로틴", "식이섬유", "비건", "혈당", "장건강", "면역", "다이어트", "저염", "나트륨 감소"]
    merged = list(dict.fromkeys([*claim_list, *[word for word in candidates if word in raw_prompt]]))
    return merged


def guess_package(case_key: str, raw_prompt: str, package_type: str | None) -> str:
    if package_type:
        return package_type
    for package in ["개별포장", "스틱", "파우치", "병", "팩"]:
        if package in raw_prompt:
            return package
    return PRODUCT_CASES[case_key]["packages"][0]


def clean_text_items(items: list[str]) -> list[str]:
    cleaned = []
    for item in items:
        value = str(item).strip()
        if value:
            cleaned.append(value)
    return list(dict.fromkeys(cleaned))


def vibe_options() -> dict[str, Any]:
    return {
        "product_cases": [{"value": key, "label": value["label"], "packages": value["packages"]} for key, value in PRODUCT_CASES.items()],
        "targets": [{"value": key, "label": value} for key, value in VIBE_TARGETS.items()],
        "scenes": [{"value": key, "label": value} for key, value in VIBE_SCENES.items()],
        "textures": [{"value": key, "label": value} for key, value in VIBE_TEXTURES.items()],
        "process_modes": [{"value": key, "label": value} for key, value in VIBE_PROCESS_MODES.items()],
        "sales_types": sorted(SALES_TYPES),
    }


def compose_vibe_cooking(payload: VibeCookingCompose) -> dict[str, Any]:
    case_key = payload.product_case if payload.product_case in PRODUCT_CASES else detect_case(payload.base_idea, None)
    meta = PRODUCT_CASES[case_key]
    target = VIBE_TARGETS.get(payload.target_customer, payload.target_customer)
    scene = VIBE_SCENES.get(payload.eating_scene, payload.eating_scene)
    texture = VIBE_TEXTURES.get(payload.texture, payload.texture)
    process_mode = VIBE_PROCESS_MODES.get(payload.process_mode, payload.process_mode)
    key_ingredients = clean_text_items(payload.key_ingredients)
    avoid_ingredients = clean_text_items(payload.avoid_ingredients)
    claims = clean_text_items(payload.claim_list)
    if payload.process_mode == "low_sugar":
        claims.append("저당")
    if payload.process_mode == "high_protein":
        claims.append("고단백")
    if payload.process_mode == "care":
        claims.append("섭취편의")
    claims = list(dict.fromkeys(claims))

    prompt_parts = [
        payload.base_idea.strip(),
        f"제품군은 {meta['label']}이고 {target}을 주요 고객으로 본다.",
        f"사용 장면은 {scene}, 목표 식감은 {texture}, 제조 방향은 {process_mode}이다.",
    ]
    if key_ingredients:
        prompt_parts.append(f"핵심 원료 후보는 {', '.join(key_ingredients)}이다.")
    if avoid_ingredients:
        prompt_parts.append(f"제외하거나 줄일 원료는 {', '.join(avoid_ingredients)}이다.")
    if claims:
        prompt_parts.append(f"강조 문구 후보는 {', '.join(claims)}이다.")
    if payload.target_price:
        prompt_parts.append(f"목표 가격/원가는 {payload.target_price} 기준으로 검토한다.")
    prompt_parts.append(f"{payload.sales_type} 판매를 전제로 {payload.target_qty_text} 테스트 생산과 {payload.package_type} 포장을 검토한다.")

    raw_prompt = " ".join(prompt_parts)
    request_payload = {
        "raw_prompt": raw_prompt,
        "product_case": case_key,
        "sales_type": payload.sales_type if payload.sales_type in SALES_TYPES else "D2C",
        "target_qty_text": payload.target_qty_text,
        "package_type": payload.package_type or meta["packages"][0],
        "claim_list": claims,
        "taste_tags": clean_text_items([target, scene, texture, process_mode, *key_ingredients[:3]]),
        "target_price": payload.target_price or "",
        "run_full": True,
    }
    return {
        "vibe_card": {
            "product_case": meta["label"],
            "target_customer": target,
            "eating_scene": scene,
            "texture": texture,
            "process_mode": process_mode,
            "key_ingredients": key_ingredients,
            "avoid_ingredients": avoid_ingredients,
            "claims": claims,
        },
        "request_payload": request_payload,
        "preview_prompt": raw_prompt,
    }


def register_font() -> str:
    candidates = [
        Path("C:/Windows/Fonts/malgun.ttf"),
        Path("C:/Windows/Fonts/NotoSansKR-Regular.ttf"),
        Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
    ]
    for font_path in candidates:
        if font_path.exists():
            try:
                pdfmetrics.registerFont(TTFont("Korean", str(font_path)))
                return "Korean"
            except Exception:
                continue
    return "Helvetica"


def seed_database(db: Session) -> None:
    if not db.scalar(select(func.count(User.id))):
        company = Company(name="CBT 운영사", company_type="operator")
        db.add(company)
        db.flush()
        db.add_all(
            [
                User(email="operator@example.com", name="운영자", role="admin", company_id=company.id),
                User(email="brand@example.com", name="브랜드 담당자", role="brand", company_id=company.id),
            ]
        )

    if not db.scalar(select(func.count(Factory.id))) and FACTORY_SEED.exists():
        with FACTORY_SEED.open("r", encoding="utf-8", newline="") as fp:
            for row in csv.DictReader(fp):
                db.add(
                    Factory(
                        factory_code=row["factory_id"],
                        company_name=row["company_name"],
                        primary_category=row["primary_category"],
                        product_keywords=row["product_keywords"],
                        oem_signal=row["oem_signal"] == "Y",
                        odm_signal=row["odm_signal"] == "Y",
                        certification_signal=row["certification_signal"],
                        location_signal=row["location_signal"],
                        mvp_fit=row["mvp_fit"],
                        source_url=row["source_url"],
                        verification_status=row["verification_status"],
                        next_action=row["next_action"],
                        notes=row["notes"],
                    )
                )

    if not db.scalar(select(func.count(RegulatoryRule.id))) and RULE_SEED.exists():
        with RULE_SEED.open("r", encoding="utf-8", newline="") as fp:
            for row in csv.DictReader(fp):
                db.add(RegulatoryRule(**row))


def ensure_schema_columns() -> None:
    with engine.connect() as conn:
        rows = conn.exec_driver_sql("PRAGMA table_info(product_requests)").fetchall()
        columns = {row[1] for row in rows}
        if rows and "llm_model" not in columns:
            conn.exec_driver_sql(f"ALTER TABLE product_requests ADD COLUMN llm_model VARCHAR(80) DEFAULT '{SAM_DEFAULT_MODEL}'")
            conn.commit()
        if rows and "target_price" not in columns:
            conn.exec_driver_sql("ALTER TABLE product_requests ADD COLUMN target_price VARCHAR(80) DEFAULT ''")
            conn.commit()


def record_tool_run(db: Session, request_id: int, tool_name: str, input_data: Any, summary: str, status: str = "succeeded") -> None:
    db.add(
        ToolRun(
            request_id=request_id,
            tool_name=tool_name,
            input_hash=make_hash(input_data),
            version=1,
            status=status,
            summary=summary,
            finished_at=now_utc(),
        )
    )


def sam_headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if SAM_API_KEY:
        if SAM_API_KEY.startswith("sam_"):
            headers["X-API-Key"] = SAM_API_KEY
        else:
            headers["Authorization"] = f"Bearer {SAM_API_KEY}"
    return headers


def call_sam_structured(req: ProductRequest, model: str) -> tuple[dict[str, Any] | None, str]:
    if not SAM_API_KEY:
        return None, "SAM_API_KEY 없음: 규칙 기반 폴백"
    if model not in DEEPSEEK_MODELS:
        model = SAM_DEFAULT_MODEL

    schema_hint = {
        "concept": {
            "target_customer": "string",
            "eating_scene": "string",
            "selling_point": "string",
            "draft_warning": "string",
        },
        "process_list": ["string"],
        "ingredients": [
            {
                "role": "string",
                "name": "string",
                "ratio_range": "string",
                "allergen": "string",
                "substitute_allowed": "string",
            }
        ],
        "quality_targets": ["string"],
        "validation_questions": ["string"],
        "cost_assumption": {
            "test_qty": "string",
            "expected_cogs_range": "string",
            "moq_note": "string",
        },
    }
    prompt = f"""
한국 식품 OEM/ODM CBT 앱의 바이브 쿠킹 사양화 결과를 JSON으로 작성해라.
제품군: {req.product_case_label}
사용자 입력: {req.raw_prompt}
판매 방식: {req.sales_type}
목표 수량: {req.target_qty}{req.qty_unit}
포장: {req.package_type}
강조 문구: {', '.join(from_json(req.claim_list, []))}

제약:
- 실제 배합비, 소비기한, 인허가, 효능을 확정하지 말고 검토용 초안으로 둔다.
- 공장 견적에 필요한 BOM 역할, 공정, 검증 질문을 구체화한다.
- 출력은 설명 없이 JSON 객체만 반환한다.
- JSON 구조 예시는 다음 키를 따른다: {json.dumps(schema_hint, ensure_ascii=False)}
"""
    payload = {
        "model": model,
        "stream": False,
        "temperature": 0.2,
        "max_tokens": 1800,
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": "너는 한국 식품 OEM/ODM 제조 발주 사양화 전문가다. 법률 판단을 확정하지 않고 확인 질문과 검토용 초안을 만든다.",
            },
            {"role": "user", "content": prompt},
        ],
    }
    try:
        response = requests.post(
            f"{SAM_BASE_URL.rstrip('/')}/openai/v1/chat/completions",
            headers=sam_headers(),
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            timeout=45,
        )
        response.raise_for_status()
        data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        parsed = json.loads(content) if isinstance(content, str) else content
        if not isinstance(parsed, dict):
            return None, "SAM 응답 JSON 객체 아님: 규칙 기반 폴백"
        return parsed, f"SAM {model} 사양화 성공"
    except Exception as exc:
        return None, f"SAM 호출 실패: {type(exc).__name__}: {exc}"


def build_spec_and_recipe(db: Session, req: ProductRequest) -> None:
    meta = PRODUCT_CASES[req.product_case]
    claims = from_json(req.claim_list, [])
    llm_data, llm_summary = call_sam_structured(req, req.llm_model)
    target = "예비 창업자/D2C 테스트 고객" if req.sales_type in {"D2C", "B2C", "공동구매"} else "B2B 반복 발주 담당자"
    concept = llm_data.get("concept") if llm_data else None
    if not isinstance(concept, dict):
        concept = {
        "target_customer": target,
        "eating_scene": "온라인 테스트 판매와 샘플 피드백 수집",
        "selling_point": ", ".join(claims) if claims else f"{meta['label']} 제조 가능성 검토",
        "draft_warning": "검토용 초안이며 표시/인허가 확정 판단이 아닙니다.",
        }
    process_list = llm_data.get("process_list") if llm_data else None
    if not isinstance(process_list, list) or not process_list:
        process_list = meta["process"]
    cost = llm_data.get("cost_assumption") if llm_data else None
    if not isinstance(cost, dict):
        cost = {
        "test_qty": req.target_qty,
        "expected_cogs_range": "공장 상담 전 참고: 직접원가 700~1,200원/판매단위",
        "moq_note": "공장별 MOQ, 샘플비, 리드타임 확인 필요",
        }
    questions = llm_data.get("validation_questions") if llm_data else None
    if not isinstance(questions, list) or not questions:
        questions = [*meta["questions"], "MOQ, 샘플비, 초도 생산 리드타임은 어떻게 되는가"]

    db.query(ProductSpec).filter(ProductSpec.request_id == req.id).delete()
    db.add(
        ProductSpec(
            request_id=req.id,
            concept=as_json(concept),
            process_list=as_json(process_list),
            package_condition=as_json({"package_type": req.package_type, "material_check": "식품용 포장재 증빙 필요"}),
            storage_condition="상온 가정, 제품별 수분활성/살균조건 확인",
            cost_assumption=as_json(cost),
            validation_questions=as_json(questions),
        )
    )

    db.query(RecipeDraft).filter(RecipeDraft.request_id == req.id).delete()
    unit = "40g" if req.product_case == "health_snack" else "20g" if req.product_case == "powder_stick" else "200g"
    db.add(
        RecipeDraft(
            request_id=req.id,
            batch_size="테스트 배치 1kg 기준",
            unit_weight=unit,
            yield_rate=0.92,
            quality_targets=as_json(["맛/식감 샘플 3종 비교", "영양성분 분석", "보관 안정성 확인"]),
        )
    )
    db.query(IngredientLine).filter(IngredientLine.request_id == req.id).delete()
    llm_ingredients = llm_data.get("ingredients") if llm_data else None
    if isinstance(llm_ingredients, list) and llm_ingredients:
        ingredient_rows = [
            (
                str(item.get("role", "원료")),
                str(item.get("name", "")),
                str(item.get("substitute_allowed", "가능")),
                str(item.get("allergen", "")),
                str(item.get("ratio_range", "")),
            )
            for item in llm_ingredients
            if isinstance(item, dict)
        ]
    else:
        ingredient_rows = [(role, name, substitute, allergen, f"{idx * 5}~{idx * 8 + 10}%") for idx, (role, name, substitute, allergen) in enumerate(meta["ingredients"], start=1)]
    for role, name, substitute, allergen, ratio in ingredient_rows:
        db.add(
            IngredientLine(
                request_id=req.id,
                ingredient_role=role,
                ingredient_name=name,
                ratio_range=ratio or "공장 확인",
                allergen_flag=allergen,
                substitute_allowed=substitute,
            )
        )
    record_tool_run(db, req.id, "sam_deepseek_vibe_cooking", {"request": req.raw_prompt, "model": req.llm_model}, llm_summary, "succeeded" if llm_data else "skipped")
    record_tool_run(db, req.id, "vibe_cooking_spec", {"request": req.raw_prompt}, f"{meta['label']} 사양과 레시피 초안 생성")


def run_screening(db: Session, req: ProductRequest) -> ScreeningRun:
    db.query(ScreeningFinding).filter(ScreeningFinding.request_id == req.id).delete()
    db.query(ScreeningRun).filter(ScreeningRun.request_id == req.id).delete()
    run = ScreeningRun(request_id=req.id, overall_status="GREEN")
    db.add(run)
    db.flush()

    ingredient_text = " ".join(line.ingredient_name + " " + line.allergen_flag for line in db.scalars(select(IngredientLine).where(IngredientLine.request_id == req.id)))
    context = {
        "claim_list": " ".join(from_json(req.claim_list, [])) + " " + req.raw_prompt,
        "ingredient_list": ingredient_text,
        "product_case": req.product_case_label,
        "package_type": req.package_type,
        "package_material": req.package_type,
        "factory_candidate": "공장",
    }
    severities: list[str] = []
    for rule in db.scalars(select(RegulatoryRule).where(RegulatoryRule.active.is_(True))):
        target = context.get(rule.trigger_field, "")
        if not target:
            continue
        if re.search(rule.trigger_value, target):
            db.add(
                ScreeningFinding(
                    screening_run_id=run.id,
                    request_id=req.id,
                    rule_id=rule.rule_id,
                    severity=rule.severity,
                    message=rule.check_item,
                    required_evidence=rule.required_evidence,
                    source_url=rule.source_url,
                )
            )
            severities.append(rule.severity)
    run.overall_status = "RED" if "RED" in severities else "YELLOW" if "YELLOW" in severities else "GREEN"
    record_tool_run(db, req.id, "regulatory_screening", context, f"규제 스크리닝 {run.overall_status}")
    return run


def score_factory(req: ProductRequest, factory: Factory, findings: list[ScreeningFinding]) -> tuple[float, list[str]]:
    meta = PRODUCT_CASES[req.product_case]
    haystack = f"{factory.primary_category} {factory.product_keywords} {factory.certification_signal} {factory.notes}".lower()
    score = 0.0
    reasons: list[str] = []
    if any(alias.lower() in haystack for alias in meta["aliases"]):
        score += 30
        reasons.append("제품군 키워드 일치")
    if any(proc.lower().replace("/", "") in haystack.replace("/", "") for proc in meta["process"]):
        score += 15
        reasons.append("필요 공정 신호 보유")
    if req.package_type and req.package_type.lower() in haystack:
        score += 12
        reasons.append("포장 방식 신호 일치")
    if factory.mvp_fit == "A":
        score += 15
        reasons.append("초기 검증 적합도 A")
    elif factory.mvp_fit == "B":
        score += 8
    if factory.oem_signal:
        score += 6
    if factory.odm_signal:
        score += 6
    cert = factory.certification_signal.upper()
    if "HACCP" in cert:
        score += 8
        reasons.append("HACCP 신호")
    if "GMP" in cert and req.product_case == "powder_stick":
        score += 8
        reasons.append("GMP 신호")
    if factory.verification_status in {"공개정보확인", "공공DB상세확인", "공식페이지확인"}:
        score += 5
    if req.target_qty <= 5000 and any(word in haystack for word in ["소량", "샘플", "스타트업"]):
        score += 10
        reasons.append("소량/샘플 대응 신호")
    if any(f.severity == "RED" and "알레르기" in f.message for f in findings) and "HACCP" in cert:
        score += 4
    return min(score, 100), reasons


def run_matching(db: Session, req: ProductRequest) -> list[MatchResult]:
    db.query(MatchResult).filter(MatchResult.request_id == req.id).delete()
    findings = list(db.scalars(select(ScreeningFinding).where(ScreeningFinding.request_id == req.id)))
    ranked: list[tuple[float, Factory, list[str]]] = []
    meta = PRODUCT_CASES[req.product_case]
    terms = [*meta["aliases"], req.product_case_label]
    filters = [Factory.active.is_(True), Factory.mvp_fit.in_(["A", "B"])]
    candidates = db.scalars(select(Factory).where(*filters).limit(180)).all()
    for factory in candidates:
        text = f"{factory.primary_category} {factory.product_keywords} {factory.notes}"
        if not any(term in text for term in terms):
            continue
        score, reasons = score_factory(req, factory, findings)
        if score >= 28:
            ranked.append((score, factory, reasons))
    ranked.sort(key=lambda item: item[0], reverse=True)
    results: list[MatchResult] = []
    for score, factory, reasons in ranked[:5]:
        questions = [
            "현재 입력 기준 MOQ와 샘플비를 확인해 주세요.",
            "라벨 검수와 시험성적서 대응 가능 범위를 알려 주세요.",
            *PRODUCT_CASES[req.product_case]["questions"],
        ]
        result = MatchResult(
            request_id=req.id,
            factory_id=factory.id,
            score=round(score, 1),
            reason=f"{factory.company_name}: {', '.join(reasons[:4])}",
            confirm_questions=as_json(list(dict.fromkeys(questions))),
        )
        db.add(result)
        results.append(result)
    record_tool_run(db, req.id, "factory_matcher", {"request_id": req.id}, f"공장 후보 {len(results)}개 생성")
    return results


def build_documents(db: Session, req: ProductRequest, screening: ScreeningRun | None = None) -> None:
    if not screening:
        screening = db.scalar(select(ScreeningRun).where(ScreeningRun.request_id == req.id).order_by(ScreeningRun.id.desc()))
    spec = db.scalar(select(ProductSpec).where(ProductSpec.request_id == req.id))
    findings = list(db.scalars(select(ScreeningFinding).where(ScreeningFinding.request_id == req.id).order_by(ScreeningFinding.severity)))
    matches = list(db.scalars(select(MatchResult).where(MatchResult.request_id == req.id).order_by(MatchResult.score.desc()).limit(5)))
    ingredients = list(db.scalars(select(IngredientLine).where(IngredientLine.request_id == req.id)))
    factories = {f.id: f for f in db.scalars(select(Factory).where(Factory.id.in_([m.factory_id for m in matches])))} if matches else {}
    concept = from_json(spec.concept if spec else "", {})

    plan_body = {
        "title": f"{req.product_case_label} 제품 기획안",
        "request_uid": req.request_uid,
        "concept": concept,
        "product_spec": {
            "process": from_json(spec.process_list if spec else "", []),
            "package": req.package_type,
            "storage": spec.storage_condition if spec else "",
        },
        "recipe_direction": [
            {
                "role": line.ingredient_role,
                "name": line.ingredient_name,
                "ratio": line.ratio_range,
                "allergen": line.allergen_flag,
            }
            for line in ingredients
        ],
        "screening": [{"severity": f.severity, "message": f.message, "evidence": f.required_evidence} for f in findings],
        "factory_summary": [
            {"factory": factories[m.factory_id].company_name, "score": m.score, "reason": m.reason}
            for m in matches
            if m.factory_id in factories
        ],
        "next_actions": ["RED/YELLOW 항목 확인", "상위 후보 3곳 MOQ/샘플비 확인", "원가계산 결과로 목표 판매가 재검토"],
    }

    brief_status = "needs_review" if screening and screening.overall_status == "RED" else "ready_to_send"
    brief_body = {
        "title": f"{req.product_case_label} 샘플 개발 요청서",
        "disclaimer": "견적 및 샘플 가능 여부 확인용 검토 초안입니다. 정식 발주서나 계약서가 아닙니다.",
        "request_overview": {
            "product_case": req.product_case_label,
            "sales_type": req.sales_type,
            "target_qty": f"{req.target_qty:,}{req.qty_unit}",
            "package_type": req.package_type,
        },
        "manufacturing_spec": from_json(spec.process_list if spec else "", []),
        "bom_draft": plan_body["recipe_direction"],
        "regulatory_questions": [{"severity": f.severity, "question": f"{f.message} - {f.required_evidence}"} for f in findings],
        "factory_questions": [
            {
                "factory": factories[m.factory_id].company_name,
                "questions": from_json(m.confirm_questions, []),
            }
            for m in matches
            if m.factory_id in factories
        ],
        "reply_fields": ["가능/불가", "수정 제안", "MOQ", "샘플비", "예상 리드타임", "필요 자료"],
    }

    db.query(ProductPlan).filter(ProductPlan.request_id == req.id).delete()
    db.query(SampleBrief).filter(SampleBrief.request_id == req.id).delete()
    db.add(ProductPlan(request_id=req.id, status="plan_ready", body=as_json(plan_body)))
    db.add(SampleBrief(request_id=req.id, status=brief_status, body=as_json(brief_body)))
    record_tool_run(db, req.id, "procurement_brief_writer", {"request_id": req.id}, f"기획안/발주안 생성: {brief_status}")


def calculate_cost(db: Session, req: ProductRequest, payload: CostCalculationCreate) -> CostCalculation:
    direct_unit = payload.ingredient_cost + payload.packaging_cost + payload.manufacturing_fee
    incidental_total = payload.sample_fee + payload.test_fee + payload.logistics_fee + payload.platform_fee
    total_cost = direct_unit * req.target_qty + incidental_total
    unit_cost = total_cost / req.target_qty
    supply_price = unit_cost / (1 - payload.margin_target)
    vat_included_total = supply_price * req.target_qty * (1 + payload.vat_rate)
    body = {
        "line_items": [
            {"category": "원재료비", "unit_amount": payload.ingredient_cost},
            {"category": "포장비", "unit_amount": payload.packaging_cost},
            {"category": "제조비", "unit_amount": payload.manufacturing_fee},
            {"category": "샘플비", "total_amount": payload.sample_fee},
            {"category": "시험비", "total_amount": payload.test_fee},
            {"category": "물류비", "total_amount": payload.logistics_fee},
        ],
        "moq_scenarios": [
            {"qty": qty, "unit_cost": round((direct_unit * qty + incidental_total) / qty, 1)}
            for qty in [1000, 5000, 10000]
        ],
        "warning": "공공 가격이나 수동 입력 기반 참고 원가이며 공장 견적 확정값이 아닙니다.",
    }
    calc = CostCalculation(
        request_id=req.id,
        version=1,
        target_qty=req.target_qty,
        serving_unit=payload.serving_unit,
        total_cost=round(total_cost, 1),
        unit_cost=round(unit_cost, 1),
        supply_price=round(supply_price, 1),
        vat_included_total=round(vat_included_total, 1),
        body=as_json(body),
    )
    db.add(calc)
    record_tool_run(db, req.id, "cost_calculator", payload.model_dump(), f"1식당 원가 {calc.unit_cost:,.0f}원")
    return calc


def run_full_pipeline(db: Session, req: ProductRequest) -> None:
    build_spec_and_recipe(db, req)
    screening = run_screening(db, req)
    matches = run_matching(db, req)
    build_documents(db, req, screening)
    calculate_cost(db, req, CostCalculationCreate(serving_unit="1포" if req.product_case == "powder_stick" else "1병" if req.product_case == "sauce" else "1개"))
    if not matches:
        req.status = "on_hold"
    elif screening.overall_status == "RED":
        req.status = "needs_review"
    else:
        req.status = "brief_ready"
    req.updated_at = now_utc()


def serialize_request(req: ProductRequest, detail: bool = False) -> dict[str, Any]:
    data = {
        "id": req.id,
        "request_uid": req.request_uid,
        "product_case": req.product_case,
        "product_case_label": req.product_case_label,
        "raw_prompt": req.raw_prompt if detail else req.raw_prompt[:90],
        "sales_type": req.sales_type,
        "target_qty": req.target_qty,
        "qty_unit": req.qty_unit,
        "package_type": req.package_type,
        "llm_model": req.llm_model,
        "claim_list": from_json(req.claim_list, []),
        "taste_tags": from_json(req.taste_tags, []),
        "target_price": req.target_price,
        "status": req.status,
        "is_dummy": req.is_dummy,
        "created_at": req.created_at.isoformat(),
        "updated_at": req.updated_at.isoformat(),
    }
    return data


def serialize_factory(factory: Factory) -> dict[str, Any]:
    return {
        "id": factory.id,
        "factory_code": factory.factory_code,
        "company_name": factory.company_name,
        "primary_category": factory.primary_category,
        "product_keywords": factory.product_keywords,
        "certification_signal": factory.certification_signal,
        "location_signal": factory.location_signal,
        "mvp_fit": factory.mvp_fit,
        "verification_status": factory.verification_status,
        "source_url": factory.source_url,
        "notes": factory.notes,
        "active": factory.active,
    }


def default_purchase_order_lines(db: Session, req: ProductRequest) -> list[dict[str, Any]]:
    cost = db.scalar(select(CostCalculation).where(CostCalculation.request_id == req.id).order_by(CostCalculation.id.desc()))
    unit_price = cost.supply_price if cost else 0
    return [
        {
            "item_name": f"{req.product_case_label} {req.package_type} 생산",
            "specification": f"{req.raw_prompt[:80]}",
            "unit": req.qty_unit,
            "quantity": req.target_qty,
            "unit_price": unit_price,
            "requested_delivery_date": "",
            "notes": "초도/샘플 발주 기준, 최종 단가는 공급사 견적서로 확정",
        }
    ]


def parse_float_text(value: str) -> float:
    match = re.search(r"[-+]?\d[\d,]*(?:\.\d+)?", value or "")
    return float(match.group(0).replace(",", "")) if match else 0


def parse_date_text(value: str) -> str:
    match = re.search(r"(\d{4})[.\-/년\s]+(\d{1,2})[.\-/월\s]+(\d{1,2})", value or "")
    if not match:
        return ""
    year, month, day = (int(part) for part in match.groups())
    try:
        return datetime(year, month, day).date().isoformat()
    except ValueError:
        return ""


def extract_order_field(text: str, labels: list[str]) -> str:
    joined = "|".join(re.escape(label) for label in labels)
    patterns = [
        rf"(?:^|\n)\s*(?:{joined})\s*[:：]\s*([^\n\r]+)",
        rf"(?:^|\n)\s*(?:{joined})\s+([^\n\r]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(" \t-|")
    return ""


def split_order_list(value: str) -> list[str]:
    return [item.strip(" -\t") for item in re.split(r"[\n,;/]+", value or "") if item.strip(" -\t")]


def parse_purchase_order_form(raw_order_form: str, req: ProductRequest | None = None) -> dict[str, Any]:
    text = raw_order_form.replace("\r\n", "\n").replace("\r", "\n")
    buyer = extract_order_field(text, ["발주처", "구매자", "매입처", "Buyer", "Purchaser"])
    supplier = extract_order_field(text, ["공급처", "수주처", "납품처", "제조사", "Supplier", "Vendor"])
    order_date = parse_date_text(extract_order_field(text, ["발주일", "주문일", "Order Date", "PO Date"]))
    due_date = parse_date_text(extract_order_field(text, ["납기일", "납품일", "입고일", "Delivery Date", "Due Date"]))
    delivery_place = extract_order_field(text, ["납품장소", "배송지", "입고장소", "Delivery Place", "Ship To"])
    payment_terms = extract_order_field(text, ["결제조건", "지급조건", "Payment Terms"])
    delivery_terms = extract_order_field(text, ["납품조건", "배송조건", "Delivery Terms"])
    inspection_terms = extract_order_field(text, ["검수조건", "검사조건", "Inspection Terms"])
    vat_text = extract_order_field(text, ["VAT", "부가세", "세액"])
    vat_type = "VAT 포함" if re.search(r"포함|included|incl", vat_text, re.IGNORECASE) else "VAT 별도" if vat_text else ""
    item_name = extract_order_field(text, ["품목명", "품명", "제품명", "상품명", "Item", "Product"])
    specification = extract_order_field(text, ["규격", "사양", "Spec", "Specification"])
    quantity_text = extract_order_field(text, ["수량", "Qty", "Quantity"])
    unit_price_text = extract_order_field(text, ["단가", "Unit Price"])
    unit = extract_order_field(text, ["단위", "Unit"])
    if quantity_text and not unit:
        unit_match = re.search(r"\d[\d,]*(?:\.\d+)?\s*([가-힣A-Za-z]+)", quantity_text)
        unit = unit_match.group(1) if unit_match else ""
    quantity = parse_float_text(quantity_text)
    unit_price = parse_float_text(unit_price_text)

    if not item_name:
        for line in text.split("\n"):
            compact = line.strip()
            if not compact or re.search(r"품목|수량|단가|금액", compact) and not re.search(r"\d", compact):
                continue
            if re.search(r"\d[\d,]*\s*(개|포|팩|병|kg|KG|톤)", compact):
                item_name = re.split(r"\s{2,}|\t|,", compact)[0].strip()
                if not quantity:
                    quantity = parse_float_text(compact)
                unit_match = re.search(r"\d[\d,]*(?:\.\d+)?\s*(개|포|팩|병|kg|KG|톤)", compact)
                unit = unit or (unit_match.group(1) if unit_match else "")
                numbers = re.findall(r"\d[\d,]*(?:\.\d+)?", compact)
                if not unit_price and len(numbers) >= 2:
                    unit_price = float(numbers[-1].replace(",", ""))
                break

    fallback_item = f"{req.product_case_label} {req.package_type} 생산" if req else "품목"
    line_items = []
    if item_name or quantity or unit_price:
        line_items.append(
            {
                "item_name": item_name or fallback_item,
                "specification": specification,
                "unit": unit or (req.qty_unit if req else "개"),
                "quantity": quantity or (req.target_qty if req else 1),
                "unit_price": unit_price,
                "requested_delivery_date": due_date,
                "notes": "발주 양식 원문에서 자동 추출",
            }
        )

    return {
        "buyer_company": buyer,
        "supplier_company": supplier,
        "order_date": order_date,
        "due_date": due_date,
        "delivery_place": delivery_place,
        "payment_terms": payment_terms,
        "delivery_terms": delivery_terms,
        "inspection_terms": inspection_terms,
        "vat_type": vat_type,
        "line_items": line_items,
        "quality_terms": split_order_list(extract_order_field(text, ["품질조건", "품질 기준", "Quality Terms"])),
        "required_documents": split_order_list(extract_order_field(text, ["필수서류", "첨부서류", "Required Documents"])),
    }


def normalize_purchase_order_lines(lines: list[PurchaseOrderLineCreate], fallback: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source = [line.model_dump() for line in lines] if lines else fallback
    normalized = []
    for line in source:
        quantity = float(line.get("quantity") or 0)
        unit_price = float(line.get("unit_price") or 0)
        amount = round(quantity * unit_price, 1)
        normalized.append(
            {
                "item_name": str(line.get("item_name") or "품목"),
                "specification": str(line.get("specification") or ""),
                "unit": str(line.get("unit") or "개"),
                "quantity": quantity,
                "unit_price": unit_price,
                "amount": amount,
                "requested_delivery_date": str(line.get("requested_delivery_date") or ""),
                "notes": str(line.get("notes") or ""),
            }
        )
    return normalized


def purchase_order_risk_flags(order: PurchaseOrderCreate, lines: list[dict[str, Any]]) -> list[str]:
    flags = []
    if not order.supplier_company.strip():
        flags.append("공급처 상호가 비어 있습니다.")
    if not order.delivery_place.strip():
        flags.append("납품장소가 비어 있습니다.")
    if not order.due_date.strip() and not any(line.get("requested_delivery_date") for line in lines):
        flags.append("납기일이 비어 있습니다.")
    if not order.payment_terms.strip():
        flags.append("결제조건이 비어 있습니다.")
    if "VAT" not in order.vat_type.upper():
        flags.append("VAT 포함/별도 기준을 명확히 확인하세요.")
    if any(float(line.get("unit_price") or 0) <= 0 for line in lines):
        flags.append("단가 0원 품목이 있어 견적 확정 전 상태입니다.")
    if not order.raw_order_form.strip():
        flags.append("받은 실제 발주 양식 원문/메모가 비어 있습니다.")
    return flags


def create_purchase_order_record(db: Session, req: ProductRequest, payload: PurchaseOrderCreate) -> PurchaseOrderRequest:
    parsed = parse_purchase_order_form(payload.raw_order_form, req) if payload.raw_order_form.strip() else {}
    updates = {}
    for field in ["buyer_company", "supplier_company", "order_date", "due_date", "delivery_place", "payment_terms", "delivery_terms", "inspection_terms", "vat_type"]:
        parsed_value = parsed.get(field)
        if parsed_value and not str(getattr(payload, field, "")).strip():
            updates[field] = parsed_value
    if parsed.get("quality_terms") and not payload.quality_terms:
        updates["quality_terms"] = parsed["quality_terms"]
    if parsed.get("required_documents") and not payload.required_documents:
        updates["required_documents"] = parsed["required_documents"]
    effective = payload.model_copy(update=updates) if updates else payload

    matches = list(db.scalars(select(MatchResult).where(MatchResult.request_id == req.id).order_by(MatchResult.score.desc()).limit(1)))
    supplier_company = effective.supplier_company
    if not supplier_company and matches:
        factory = db.get(Factory, matches[0].factory_id)
        supplier_company = factory.company_name if factory else ""
    parsed_lines = parsed.get("line_items") or []
    fallback_lines = parsed_lines or default_purchase_order_lines(db, req)
    lines = normalize_purchase_order_lines(effective.line_items, fallback_lines)
    subtotal = round(sum(float(line["amount"]) for line in lines), 1)
    vat_amount = round(subtotal * 0.1, 1) if effective.vat_type == "VAT 별도" else 0
    total_amount = round(subtotal + vat_amount, 1)
    quality_terms = effective.quality_terms or ["입고 수량/외관 검수", "표시사항 초안 확인", "알레르기 및 원산지 증빙 확인"]
    required_documents = effective.required_documents or ["견적서", "사업자등록증", "HACCP 등 인증서", "시험성적서 또는 원료 규격서"]
    risk_payload = effective.model_copy(update={"supplier_company": supplier_company})
    risk_flags = purchase_order_risk_flags(risk_payload, lines)
    status = "needs_review" if risk_flags else "ready_to_send"
    order = PurchaseOrderRequest(
        po_uid=str(uuid.uuid4()),
        request_id=req.id,
        status=status,
        order_type=effective.order_type,
        buyer_company=effective.buyer_company,
        buyer_contact=effective.buyer_contact,
        supplier_company=supplier_company,
        supplier_contact=effective.supplier_contact,
        order_date=effective.order_date or now_utc().date().isoformat(),
        due_date=effective.due_date,
        delivery_place=effective.delivery_place,
        payment_terms=effective.payment_terms,
        delivery_terms=effective.delivery_terms,
        inspection_terms=effective.inspection_terms,
        vat_type=effective.vat_type,
        currency=effective.currency,
        raw_order_form=effective.raw_order_form,
        line_items=as_json(lines),
        subtotal=subtotal,
        vat_amount=vat_amount,
        total_amount=total_amount,
        quality_terms=as_json(quality_terms),
        required_documents=as_json(required_documents),
        risk_flags=as_json(risk_flags),
        is_dummy=effective.is_dummy,
    )
    db.add(order)
    record_tool_run(db, req.id, "purchase_order_builder", {"request_id": req.id}, f"발주요청 {status} / {len(lines)}개 품목")
    return order


def serialize_purchase_order(order: PurchaseOrderRequest) -> dict[str, Any]:
    return {
        "id": order.id,
        "po_uid": order.po_uid,
        "request_id": order.request_id,
        "status": order.status,
        "order_type": order.order_type,
        "buyer_company": order.buyer_company,
        "buyer_contact": order.buyer_contact,
        "supplier_company": order.supplier_company,
        "supplier_contact": order.supplier_contact,
        "order_date": order.order_date,
        "due_date": order.due_date,
        "delivery_place": order.delivery_place,
        "payment_terms": order.payment_terms,
        "delivery_terms": order.delivery_terms,
        "inspection_terms": order.inspection_terms,
        "vat_type": order.vat_type,
        "currency": order.currency,
        "raw_order_form": order.raw_order_form,
        "line_items": from_json(order.line_items, []),
        "subtotal": order.subtotal,
        "vat_amount": order.vat_amount,
        "total_amount": order.total_amount,
        "quality_terms": from_json(order.quality_terms, []),
        "required_documents": from_json(order.required_documents, []),
        "risk_flags": from_json(order.risk_flags, []),
        "is_dummy": order.is_dummy,
        "created_at": order.created_at.isoformat(),
        "updated_at": order.updated_at.isoformat(),
    }


def purchase_order_document_body(order: PurchaseOrderRequest) -> dict[str, Any]:
    return {
        "title": f"발주요청서 {order.id}",
        "document_notice": "공급사 확인 및 내부 검토용 발주요청서입니다. 최종 계약 조건은 견적서/계약서/공급사 승낙으로 확정합니다.",
        "order_header": {
            "po_uid": order.po_uid,
            "status": order.status,
            "order_type": order.order_type,
            "order_date": order.order_date,
            "due_date": order.due_date,
        },
        "parties": {
            "buyer_company": order.buyer_company,
            "buyer_contact": order.buyer_contact,
            "supplier_company": order.supplier_company,
            "supplier_contact": order.supplier_contact,
        },
        "line_items": from_json(order.line_items, []),
        "amounts": {
            "currency": order.currency,
            "subtotal": order.subtotal,
            "vat_type": order.vat_type,
            "vat_amount": order.vat_amount,
            "total_amount": order.total_amount,
        },
        "delivery_payment_inspection": {
            "delivery_place": order.delivery_place,
            "delivery_terms": order.delivery_terms,
            "payment_terms": order.payment_terms,
            "inspection_terms": order.inspection_terms,
        },
        "quality_terms": from_json(order.quality_terms, []),
        "required_documents": from_json(order.required_documents, []),
        "risk_flags": from_json(order.risk_flags, []),
        "received_order_form": order.raw_order_form,
    }


def build_vibe_agent_report(db: Session, req: ProductRequest, payload: VibeAgentRun) -> dict[str, Any]:
    spec = db.scalar(select(ProductSpec).where(ProductSpec.request_id == req.id))
    ingredients = list(db.scalars(select(IngredientLine).where(IngredientLine.request_id == req.id)))
    screening = db.scalar(select(ScreeningRun).where(ScreeningRun.request_id == req.id).order_by(ScreeningRun.id.desc()))
    findings = list(db.scalars(select(ScreeningFinding).where(ScreeningFinding.request_id == req.id)))
    matches = list(db.scalars(select(MatchResult).where(MatchResult.request_id == req.id).order_by(MatchResult.score.desc()).limit(5)))
    cost = db.scalar(select(CostCalculation).where(CostCalculation.request_id == req.id).order_by(CostCalculation.id.desc()))

    score = 20
    strengths: list[str] = []
    risks: list[str] = []
    actions: list[str] = []

    if spec:
        score += 15
        strengths.append("제품 컨셉, 공정, 포장 조건이 사양화되어 있습니다.")
    else:
        risks.append("바이브 쿠킹 사양이 아직 없어 공장 검토 언어가 부족합니다.")
        actions.append("전체 실행으로 사양과 레시피 초안을 먼저 생성하세요.")

    if len(ingredients) >= 3:
        score += 15
        strengths.append(f"BOM 초안이 {len(ingredients)}개 원료 역할로 분해되어 있습니다.")
    else:
        risks.append("원재료 역할이 3개 미만이라 견적 비교가 어렵습니다.")
        actions.append("주원료, 감미/향미, 기능성 원료, 포장재를 분리해 입력하세요.")

    if screening and screening.overall_status == "GREEN":
        score += 20
        strengths.append("현재 규제 플래그는 GREEN입니다.")
    elif screening and screening.overall_status == "YELLOW":
        score += 10
        risks.append("YELLOW 규제 플래그가 있어 증빙 확인 후 발주해야 합니다.")
    elif screening and screening.overall_status == "RED":
        risks.append("RED 규제 플래그가 있어 발주안 전송 전 전문가 검토가 필요합니다.")
    else:
        risks.append("규제 스크리닝이 아직 실행되지 않았습니다.")

    if matches:
        best_score = max(match.score for match in matches)
        score += 20 if best_score >= 60 else 12
        strengths.append(f"공장 후보 {len(matches)}개가 있으며 최고 적합도는 {best_score}점입니다.")
    else:
        risks.append("공장 후보가 없어 제품군, 포장, MOQ 조건을 완화해야 합니다.")
        actions.append("공장 DB에서 제품군/포장 키워드를 보강하거나 요청 조건을 단순화하세요.")

    if cost and cost.unit_cost > 0:
        score += 10
        strengths.append(f"참고 원가는 판매단위당 {cost.unit_cost:,.0f}원으로 계산되어 있습니다.")
    else:
        actions.append("원가 재계산으로 목표 판매가와 MOQ 민감도를 확인하세요.")

    red_findings = [finding for finding in findings if finding.severity == "RED"]
    yellow_findings = [finding for finding in findings if finding.severity == "YELLOW"]
    for finding in red_findings[:3]:
        risks.append(f"RED: {finding.message}")
    for finding in yellow_findings[:3]:
        risks.append(f"YELLOW: {finding.message}")

    if req.target_qty < 1000:
        risks.append("목표 수량이 낮아 샘플비와 단가가 크게 올라갈 수 있습니다.")
        actions.append("1,000개/5,000개/10,000개 MOQ 시나리오를 비교하세요.")
    if not from_json(req.claim_list, []):
        actions.append("저당, 고단백, 비건 등 검증할 강조 문구를 명확히 고르세요.")

    concept = from_json(spec.concept if spec else "", {})
    revision_prompt = ""
    if payload.include_revision_prompt:
        revision_prompt = (
            f"{req.raw_prompt} "
            f"기획 목표는 '{payload.planning_goal}'이다. "
            "공장 견적 전 확인이 필요한 원료 증빙, 표시 리스크, MOQ, 샘플비, 대체 원료 질문을 추가해 수정안을 만들어라."
        )

    score = max(0, min(score, 100))
    if red_findings or not matches:
        decision = "hold"
    elif score >= 75:
        decision = "send_brief"
    else:
        decision = "revise"

    report = {
        "planning_goal": payload.planning_goal,
        "decision": decision,
        "readiness_score": score,
        "fit_summary": {
            "concept": concept,
            "sales_type": req.sales_type,
            "target_qty": f"{req.target_qty:,}{req.qty_unit}",
            "package_type": req.package_type,
        },
        "strengths": clean_text_items(strengths),
        "risks": clean_text_items(risks),
        "recommended_actions": clean_text_items(actions or ["상위 공장 후보 3곳에 MOQ, 샘플비, 리드타임을 확인하세요."]),
        "revision_prompt": revision_prompt,
    }
    record_tool_run(db, req.id, "vibe_cooking_agent", {"planning_goal": payload.planning_goal}, f"기획 적합도 {score}점 / {decision}")
    return report


def request_detail(db: Session, req: ProductRequest) -> dict[str, Any]:
    spec = db.scalar(select(ProductSpec).where(ProductSpec.request_id == req.id))
    recipe = db.scalar(select(RecipeDraft).where(RecipeDraft.request_id == req.id))
    ingredients = list(db.scalars(select(IngredientLine).where(IngredientLine.request_id == req.id)))
    screening = db.scalar(select(ScreeningRun).where(ScreeningRun.request_id == req.id).order_by(ScreeningRun.id.desc()))
    findings = list(db.scalars(select(ScreeningFinding).where(ScreeningFinding.request_id == req.id)))
    matches = list(db.scalars(select(MatchResult).where(MatchResult.request_id == req.id).order_by(MatchResult.score.desc())))
    factories = {f.id: f for f in db.scalars(select(Factory).where(Factory.id.in_([m.factory_id for m in matches])))} if matches else {}
    plan = db.scalar(select(ProductPlan).where(ProductPlan.request_id == req.id))
    brief = db.scalar(select(SampleBrief).where(SampleBrief.request_id == req.id))
    cost = db.scalar(select(CostCalculation).where(CostCalculation.request_id == req.id).order_by(CostCalculation.id.desc()))
    purchase_orders = list(db.scalars(select(PurchaseOrderRequest).where(PurchaseOrderRequest.request_id == req.id).order_by(PurchaseOrderRequest.created_at.desc())))
    tool_runs = list(db.scalars(select(ToolRun).where(ToolRun.request_id == req.id).order_by(ToolRun.id)))
    return {
        **serialize_request(req, detail=True),
        "spec": {
            "concept": from_json(spec.concept, {}),
            "process_list": from_json(spec.process_list, []),
            "package_condition": from_json(spec.package_condition, {}),
            "storage_condition": spec.storage_condition,
            "cost_assumption": from_json(spec.cost_assumption, {}),
            "validation_questions": from_json(spec.validation_questions, []),
        }
        if spec
        else None,
        "recipe": {
            "id": recipe.id,
            "batch_size": recipe.batch_size,
            "unit_weight": recipe.unit_weight,
            "yield_rate": recipe.yield_rate,
            "quality_targets": from_json(recipe.quality_targets, []),
            "ingredients": [
                {
                    "role": line.ingredient_role,
                    "name": line.ingredient_name,
                    "ratio_range": line.ratio_range,
                    "allergen_flag": line.allergen_flag,
                    "substitute_allowed": line.substitute_allowed,
                }
                for line in ingredients
            ],
        }
        if recipe
        else None,
        "screening": {
            "overall_status": screening.overall_status if screening else "not_run",
            "findings": [
                {"rule_id": f.rule_id, "severity": f.severity, "message": f.message, "required_evidence": f.required_evidence, "source_url": f.source_url}
                for f in findings
            ],
        },
        "matches": [
            {
                "id": match.id,
                "score": match.score,
                "reason": match.reason,
                "status": match.status,
                "confirm_questions": from_json(match.confirm_questions, []),
                "factory": serialize_factory(factories[match.factory_id]) if match.factory_id in factories else None,
            }
            for match in matches
        ],
        "product_plan": {"id": plan.id, "status": plan.status, "body": from_json(plan.body, {})} if plan else None,
        "sample_brief": {"id": brief.id, "status": brief.status, "body": from_json(brief.body, {})} if brief else None,
        "cost_calculation": {
            "id": cost.id,
            "target_qty": cost.target_qty,
            "serving_unit": cost.serving_unit,
            "total_cost": cost.total_cost,
            "unit_cost": cost.unit_cost,
            "supply_price": cost.supply_price,
            "vat_included_total": cost.vat_included_total,
            "body": from_json(cost.body, {}),
        }
        if cost
        else None,
        "purchase_orders": [serialize_purchase_order(order) for order in purchase_orders],
        "tool_runs": [
            {"tool_name": run.tool_name, "status": run.status, "summary": run.summary, "finished_at": run.finished_at.isoformat() if run.finished_at else None}
            for run in tool_runs
        ],
    }


def render_pdf(db: Session, req: ProductRequest, doc_type: str, purchase_order: PurchaseOrderRequest | None = None) -> GeneratedFile:
    detail = request_detail(db, req)
    if doc_type == "product_plan":
        data = detail["product_plan"]["body"] if detail["product_plan"] else None
    elif doc_type == "sample_brief":
        data = detail["sample_brief"]["body"] if detail["sample_brief"] else None
    elif doc_type == "purchase_order":
        order = purchase_order or db.scalar(select(PurchaseOrderRequest).where(PurchaseOrderRequest.request_id == req.id).order_by(PurchaseOrderRequest.created_at.desc()))
        data = purchase_order_document_body(order) if order else None
    else:
        data = None
    if not data:
        api_error(404, "document_not_ready")

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    file_uid = str(uuid.uuid4())
    output = GENERATED_DIR / f"{file_uid}_{doc_type}.pdf"
    font = register_font()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="KTitle", fontName=font, fontSize=18, leading=24, alignment=TA_CENTER, spaceAfter=8))
    styles.add(ParagraphStyle(name="KHeading", fontName=font, fontSize=12, leading=16, textColor=colors.HexColor("#0f5132"), spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle(name="KBody", fontName=font, fontSize=9, leading=13))
    doc = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=16 * mm, leftMargin=16 * mm, topMargin=15 * mm, bottomMargin=15 * mm)
    story: list[Any] = [Paragraph(str(data.get("title", "문서")), styles["KTitle"])]
    story.append(Paragraph(f"request_id: {req.request_uid} / generated_at: {now_utc().isoformat()} / 검토용 초안", styles["KBody"]))
    story.append(Spacer(1, 5 * mm))

    def add_section(title: str, value: Any) -> None:
        story.append(Paragraph(title, styles["KHeading"]))
        if isinstance(value, list):
            rows = [["항목", "내용"]]
            for idx, item in enumerate(value, start=1):
                rows.append([str(idx), json.dumps(item, ensure_ascii=False) if isinstance(item, dict) else str(item)])
            table = Table(rows, colWidths=[18 * mm, 150 * mm])
            table.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), font), ("FONTSIZE", (0, 0), (-1, -1), 8), ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef6ef"))]))
            story.append(table)
        elif isinstance(value, dict):
            rows = [[str(k), json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)] for k, v in value.items()]
            table = Table(rows, colWidths=[42 * mm, 126 * mm])
            table.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), font), ("FONTSIZE", (0, 0), (-1, -1), 8), ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey)]))
            story.append(table)
        else:
            story.append(Paragraph(str(value), styles["KBody"]))

    for key, value in data.items():
        if key == "title":
            continue
        add_section(key, value)
        story.append(Spacer(1, 3 * mm))

    doc.build(story)
    checksum = hashlib.sha256(output.read_bytes()).hexdigest()
    generated = GeneratedFile(file_uid=file_uid, request_id=req.id, doc_type=doc_type, storage_path=str(output), checksum=checksum)
    db.add(generated)
    record_tool_run(db, req.id, "pdf_renderer", {"doc_type": doc_type}, f"{doc_type} PDF 생성")
    return generated


app = Flask(__name__, static_folder=str(BASE_DIR / "static"), static_url_path="/static")
CORS(app)


def startup() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(engine)
    ensure_schema_columns()
    with db_session() as db:
        seed_database(db)


startup()


@app.get("/")
def index():
    return send_from_directory(BASE_DIR / "static", "index.html")


@app.get("/api/health")
def health() -> dict[str, Any]:
    with db_session() as db:
        return {
            "status": "ok",
            "db": str(DB_PATH),
            "sam_configured": bool(SAM_API_KEY),
            "default_llm_model": SAM_DEFAULT_MODEL,
            "deepseek_models": DEEPSEEK_MODELS,
            "factories": db.scalar(select(func.count(Factory.id))),
            "rules": db.scalar(select(func.count(RegulatoryRule.id))),
            "requests": db.scalar(select(func.count(ProductRequest.id))),
        }


@app.get("/api/llm/models")
def list_llm_models() -> dict[str, Any]:
    models = [{"alias": alias, "provider": "microsoft_foundry", "selected": alias == SAM_DEFAULT_MODEL} for alias in DEEPSEEK_MODELS]
    try:
        response = requests.get(f"{SAM_BASE_URL.rstrip('/')}/v1/models?task=chat", headers=sam_headers(), timeout=15)
        response.raise_for_status()
        catalog = response.json().get("models", [])
        deepseek = [model for model in catalog if "deepseek" in str(model.get("alias", "")).lower()]
        if deepseek:
            models = [
                {
                    "alias": model.get("alias"),
                    "provider": model.get("provider"),
                    "capabilities": model.get("capabilities", {}),
                    "selected": model.get("alias") == SAM_DEFAULT_MODEL,
                }
                for model in deepseek
            ]
    except Exception:
        pass
    return {"default": SAM_DEFAULT_MODEL, "sam_configured": bool(SAM_API_KEY), "models": models}


@app.get("/api/vibe-cooking/options")
def get_vibe_cooking_options() -> dict[str, Any]:
    return vibe_options()


@app.post("/api/vibe-cooking/compose")
def compose_vibe_cooking_request() -> dict[str, Any]:
    payload = json_payload(VibeCookingCompose)
    return compose_vibe_cooking(payload)


@app.get("/api/summary")
def summary() -> dict[str, Any]:
    with db_session() as db:
        status_rows = db.execute(select(ProductRequest.status, func.count(ProductRequest.id)).group_by(ProductRequest.status)).all()
        case_rows = db.execute(select(ProductRequest.product_case_label, func.count(ProductRequest.id)).group_by(ProductRequest.product_case_label)).all()
        return {
            "status_counts": dict(status_rows),
            "case_counts": dict(case_rows),
            "factory_count": db.scalar(select(func.count(Factory.id)).where(Factory.active.is_(True))),
            "red_findings": db.scalar(select(func.count(ScreeningFinding.id)).where(ScreeningFinding.severity == "RED")),
        }


@app.post("/api/product-requests")
def create_product_request() -> dict[str, Any]:
    payload = json_payload(ProductRequestCreate)
    with db_session() as db:
        user = db.get(User, payload.user_id)
        if not user:
            api_error(404, "user_not_found")
        case_key = detect_case(payload.raw_prompt, payload.product_case)
        qty, qty_unit = normalize_qty(payload.target_qty, payload.target_qty_text)
        if payload.qty_unit:
            qty_unit = payload.qty_unit
        claims = normalize_claims(payload.raw_prompt, payload.claim_list)
        llm_model = payload.llm_model if payload.llm_model in DEEPSEEK_MODELS else SAM_DEFAULT_MODEL
        req = ProductRequest(
            request_uid=str(uuid.uuid4()),
            user_id=user.id,
            product_case=case_key,
            product_case_label=PRODUCT_CASES[case_key]["label"],
            raw_prompt=payload.raw_prompt,
            sales_type=payload.sales_type if payload.sales_type in SALES_TYPES else "D2C",
            target_qty=qty,
            qty_unit=qty_unit,
            package_type=guess_package(case_key, payload.raw_prompt, payload.package_type),
            llm_model=llm_model,
            claim_list=as_json(claims),
            taste_tags=as_json(payload.taste_tags),
            target_price=payload.target_price or "",
            is_dummy=payload.is_dummy,
        )
        db.add(req)
        db.flush()
        if payload.run_full:
            run_full_pipeline(db, req)
        return request_detail(db, req)


@app.get("/api/product-requests")
def list_product_requests() -> dict[str, Any]:
    status = request.args.get("status")
    product_case = request.args.get("product_case")
    include_dummy = query_bool("include_dummy") or False
    limit = query_int("limit", 20, 1, 100)
    offset = query_int("offset", 0, 0)
    with db_session() as db:
        filters = []
        if status:
            filters.append(ProductRequest.status == status)
        if product_case:
            filters.append(ProductRequest.product_case == product_case)
        if not include_dummy:
            filters.append(ProductRequest.is_dummy.is_(False))
        total = db.scalar(select(func.count(ProductRequest.id)).where(*filters))
        rows = db.scalars(select(ProductRequest).where(*filters).order_by(ProductRequest.created_at.desc()).limit(limit).offset(offset)).all()
        return {"total": total, "limit": limit, "offset": offset, "items": [serialize_request(row) for row in rows]}


@app.get("/api/product-requests/<int:request_id>")
def get_product_request(request_id: int) -> dict[str, Any]:
    with db_session() as db:
        req = db.get(ProductRequest, request_id)
        if not req:
            api_error(404, "request_not_found")
        return request_detail(db, req)


@app.post("/api/product-requests/<int:request_id>/vibe-agent")
def run_vibe_agent(request_id: int) -> dict[str, Any]:
    payload = json_payload(VibeAgentRun)
    with db_session() as db:
        req = db.get(ProductRequest, request_id)
        if not req:
            api_error(404, "request_not_found")
        return build_vibe_agent_report(db, req, payload)


@app.post("/api/product-requests/<int:request_id>/tool-runs/full")
def rerun_full(request_id: int) -> dict[str, Any]:
    with db_session() as db:
        req = db.get(ProductRequest, request_id)
        if not req:
            api_error(404, "request_not_found")
        run_full_pipeline(db, req)
        return request_detail(db, req)


@app.post("/api/product-requests/<int:request_id>/cost-calculations")
def create_cost_calculation(request_id: int) -> dict[str, Any]:
    payload = json_payload(CostCalculationCreate)
    with db_session() as db:
        req = db.get(ProductRequest, request_id)
        if not req:
            api_error(404, "request_not_found")
        calc = calculate_cost(db, req, payload)
        return {
            "id": calc.id,
            "unit_cost": calc.unit_cost,
            "total_cost": calc.total_cost,
            "supply_price": calc.supply_price,
            "vat_included_total": calc.vat_included_total,
            "body": from_json(calc.body, {}),
        }


@app.post("/api/product-requests/<int:request_id>/purchase-orders")
def create_purchase_order(request_id: int) -> dict[str, Any]:
    payload = json_payload(PurchaseOrderCreate)
    with db_session() as db:
        req = db.get(ProductRequest, request_id)
        if not req:
            api_error(404, "request_not_found")
        order = create_purchase_order_record(db, req, payload)
        db.flush()
        return serialize_purchase_order(order)


@app.post("/api/product-requests/<int:request_id>/purchase-orders/parse-form")
def parse_purchase_order_form_endpoint(request_id: int) -> dict[str, Any]:
    payload = json_payload(PurchaseOrderFormParse)
    with db_session() as db:
        req = db.get(ProductRequest, request_id)
        if not req:
            api_error(404, "request_not_found")
        parsed = parse_purchase_order_form(payload.raw_order_form, req)
        return {"parsed": parsed}


@app.get("/api/product-requests/<int:request_id>/purchase-orders")
def list_purchase_orders(request_id: int) -> dict[str, Any]:
    with db_session() as db:
        req = db.get(ProductRequest, request_id)
        if not req:
            api_error(404, "request_not_found")
        rows = db.scalars(select(PurchaseOrderRequest).where(PurchaseOrderRequest.request_id == request_id).order_by(PurchaseOrderRequest.created_at.desc())).all()
        return {"items": [serialize_purchase_order(row) for row in rows]}


@app.get("/api/purchase-orders/<int:order_id>")
def get_purchase_order(order_id: int) -> dict[str, Any]:
    with db_session() as db:
        order = db.get(PurchaseOrderRequest, order_id)
        if not order:
            api_error(404, "purchase_order_not_found")
        return serialize_purchase_order(order)


@app.post("/api/purchase-orders/<int:order_id>/documents/pdf")
def create_purchase_order_pdf(order_id: int) -> dict[str, Any]:
    with db_session() as db:
        order = db.get(PurchaseOrderRequest, order_id)
        if not order:
            api_error(404, "purchase_order_not_found")
        req = db.get(ProductRequest, order.request_id)
        if not req:
            api_error(404, "request_not_found")
        generated = render_pdf(db, req, "purchase_order", order)
        return {"file_uid": generated.file_uid, "download_url": f"/api/files/{generated.file_uid}/download", "checksum": generated.checksum}


@app.delete("/api/product-requests/<int:request_id>")
def delete_product_request(request_id: int) -> dict[str, Any]:
    with db_session() as db:
        req = db.get(ProductRequest, request_id)
        if not req:
            api_error(404, "request_not_found")
        db.query(PurchaseOrderRequest).filter(PurchaseOrderRequest.request_id == request_id).delete()
        db.delete(req)
        return {"deleted": request_id}


@app.delete("/api/dummy-data")
def delete_dummy_data() -> dict[str, Any]:
    with db_session() as db:
        ids = [row.id for row in db.scalars(select(ProductRequest).where(ProductRequest.is_dummy.is_(True)))]
        order_ids = [row.id for row in db.scalars(select(PurchaseOrderRequest).where(PurchaseOrderRequest.is_dummy.is_(True)))]
        for order_id in order_ids:
            order = db.get(PurchaseOrderRequest, order_id)
            if order:
                db.delete(order)
        for request_id in ids:
            db.query(PurchaseOrderRequest).filter(PurchaseOrderRequest.request_id == request_id).delete()
            req = db.get(ProductRequest, request_id)
            if req:
                db.delete(req)
        return {"deleted": ids, "deleted_purchase_orders": order_ids, "count": len(ids)}


@app.get("/api/admin/factories")
def list_factories() -> dict[str, Any]:
    q = request.args.get("q")
    product_case = request.args.get("product_case")
    cert = request.args.get("cert")
    package_type = request.args.get("package_type")
    mvp_fit = request.args.get("mvp_fit")
    verification_status = request.args.get("verification_status")
    active = query_bool("active")
    limit = query_int("limit", 30, 1, 100)
    offset = query_int("offset", 0, 0)
    with db_session() as db:
        filters = []
        if q:
            like = f"%{q}%"
            filters.append((Factory.company_name.like(like)) | (Factory.product_keywords.like(like)) | (Factory.primary_category.like(like)))
        if verification_status:
            filters.append(Factory.verification_status == verification_status)
        if mvp_fit:
            filters.append(Factory.mvp_fit == mvp_fit.upper())
        if cert:
            filters.append(Factory.certification_signal.like(f"%{cert}%"))
        if package_type:
            filters.append(Factory.product_keywords.like(f"%{package_type}%"))
        if product_case and product_case in PRODUCT_CASES:
            case_terms = PRODUCT_CASES[product_case]["aliases"]
            term_filter = None
            for term in case_terms:
                clause = (Factory.primary_category.like(f"%{term}%")) | (Factory.product_keywords.like(f"%{term}%")) | (Factory.notes.like(f"%{term}%"))
                term_filter = clause if term_filter is None else term_filter | clause
            if term_filter is not None:
                filters.append(term_filter)
        if active is not None:
            filters.append(Factory.active.is_(active))
        total = db.scalar(select(func.count(Factory.id)).where(*filters))
        rows = db.scalars(select(Factory).where(*filters).order_by(Factory.mvp_fit, Factory.company_name).limit(limit).offset(offset)).all()
        return {"total": total, "items": [serialize_factory(row) for row in rows]}


@app.get("/api/admin/factory-filter-options")
def factory_filter_options() -> dict[str, Any]:
    with db_session() as db:
        statuses = [row[0] for row in db.execute(select(Factory.verification_status).distinct().order_by(Factory.verification_status)).all() if row[0]]
        mvp_fits = [row[0] for row in db.execute(select(Factory.mvp_fit).distinct().order_by(Factory.mvp_fit)).all() if row[0]]
        return {
            "product_cases": [{"value": key, "label": value["label"]} for key, value in PRODUCT_CASES.items()],
            "certifications": ["HACCP", "GMP", "ISO", "FSSC22000", "비건", "할랄"],
            "package_types": ["개별포장", "스틱", "파우치", "병"],
            "verification_statuses": statuses,
            "mvp_fits": mvp_fits,
        }


@app.post("/api/admin/factories")
def create_factory() -> dict[str, Any]:
    payload = json_payload(FactoryCreate)
    with db_session() as db:
        next_id = (db.scalar(select(func.max(Factory.id))) or 0) + 1
        factory = Factory(
            factory_code=f"MANUAL-{next_id}",
            company_name=payload.company_name,
            primary_category=payload.primary_category,
            product_keywords=payload.product_keywords,
            certification_signal=payload.certification_signal,
            location_signal=payload.location_signal,
            mvp_fit=payload.mvp_fit,
            source_url=payload.source_url,
            verification_status=payload.verification_status,
            notes=payload.notes,
            oem_signal=True,
            odm_signal=True,
        )
        db.add(factory)
        db.flush()
        return serialize_factory(factory)


@app.patch("/api/admin/factories/<int:factory_id>")
def patch_factory(factory_id: int) -> dict[str, Any]:
    payload = json_payload(FactoryPatch)
    with db_session() as db:
        factory = db.get(Factory, factory_id)
        if not factory:
            api_error(404, "factory_not_found")
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(factory, key, value)
        factory.updated_at = now_utc()
        return serialize_factory(factory)


@app.get("/api/admin/rules")
def list_rules() -> dict[str, Any]:
    limit = query_int("limit", 50, 1, 100)
    offset = query_int("offset", 0, 0)
    with db_session() as db:
        rows = db.scalars(select(RegulatoryRule).order_by(RegulatoryRule.rule_id).limit(limit).offset(offset)).all()
        return {
            "items": [
                {
                    "rule_id": row.rule_id,
                    "scope": row.scope,
                    "trigger_field": row.trigger_field,
                    "trigger_value": row.trigger_value,
                    "severity": row.severity,
                    "check_item": row.check_item,
                    "required_evidence": row.required_evidence,
                    "source_url": row.source_url,
                    "active": row.active,
                }
                for row in rows
            ]
        }


@app.post("/api/product-requests/<int:request_id>/documents/<doc_type>/pdf")
def create_document_pdf(request_id: int, doc_type: str) -> dict[str, Any]:
    if doc_type not in {"product_plan", "sample_brief", "purchase_order"}:
        api_error(400, "invalid_doc_type")
    with db_session() as db:
        req = db.get(ProductRequest, request_id)
        if not req:
            api_error(404, "request_not_found")
        generated = render_pdf(db, req, doc_type)
        return {"file_uid": generated.file_uid, "download_url": f"/api/files/{generated.file_uid}/download", "checksum": generated.checksum}


@app.get("/api/files/<file_uid>/download")
def download_file(file_uid: str):
    with db_session() as db:
        generated = db.scalar(select(GeneratedFile).where(GeneratedFile.file_uid == file_uid))
        if not generated:
            api_error(404, "file_not_found")
        return send_file(generated.storage_path, mimetype="application/pdf", as_attachment=True, download_name=Path(generated.storage_path).name)


@app.get("/api/export/product-requests/<int:request_id>.json")
def export_request_json(request_id: int) -> Response:
    with db_session() as db:
        req = db.get(ProductRequest, request_id)
        if not req:
            api_error(404, "request_not_found")
        body = json.dumps(request_detail(db, req), ensure_ascii=False, indent=2)
        return Response(body.encode("utf-8"), mimetype="application/json; charset=utf-8")
