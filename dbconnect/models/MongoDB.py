# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from datetime import datetime


class Feedback(BaseModel):
    session_id: str = Field(default=None)
    trace_id: str = Field(default=None)
    response_id: str = Field(default=None)
    feedback: dict = Field(default_factory=dict)

    class Config:
        collection = "feedback_logs"

class STM(BaseModel):
    upn: str
    channel_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_interaction_time: datetime = Field(default=None)
    last_intent: str = Field(default=None)
    num_questions_last_24hr: int = Field(default=0)
    short_term_memory: list = Field(default_factory=list)
    total_tokens: int = Field(default=0)
    metadata: dict = Field(default_factory=dict)

    class Config:
        collection = "short_term_memory"

class LTM(BaseModel):
    upn: str
    channel_name: str
    session_id: str = Field(default=None)
    trace_id: str = Field(default=None)
    response_id: str = Field(default=None)
    timestamp: datetime = Field(default_factory=None)
    role: str = Field(default=None)
    content: str = Field(default=None)
    intent: str = Field(default=None)
    step_name: str = Field(default=None)
    start_time: str = Field(default=None)
    end_time: str = Field(default=None)
    elapsed_time_ms: int = Field(default=0)
    input_tokens: int = Field(default=0)
    output_tokens: int = Field(default=0)
    embedding_tokens: int = Field(default=0)
    model_used: str = Field(default=None)
    prompt_template: str = Field(default=None)
    completion: str = Field(default=None)
    iteration_number: int = Field(default=0)
    max_tokens: int = Field(default=None)
    temperature: float = Field(default=None)
    total_elapsed_time_ms: int = Field(default=None)
    total_tokens: int = Field(default=None)
    total_embedding_tokens: int = Field(default=None)
    tags: list = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)

    class Config:
        collection = "long_term_memory"

class ChargeAndKeepPartners(BaseModel):
    Code: str
    Name: str

    class Config:
        collection = "charge_and_keep_partners"

class Metadata(BaseModel):
    file_id: str
    file_name: str
    last_modified_time: str
    file_type: str
    domain: str
    url: str
    form_indicator: bool
    status: str

    class Config:
        collection = "file_metadata"


class YamlContent(BaseModel):
    file_id: str = Field(default=None)
    file_name: str = Field(default=None)
    last_modified_time: str = Field(default=None)
    file_type: str = Field(default=None)
    status: str = Field(default=None)
    yaml_content: str = Field(default=None)
    html_content: str = Field(default=None)

    class Config:
        collection = "yaml_content"
