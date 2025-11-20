"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# --- Business Schemas for STRNADEL engineering site ---

class Inquiry(BaseModel):
    """
    Inquiries from the contact/quote form
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Contact person name")
    company: Optional[str] = Field(None, description="Company name")
    email: str = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone")
    subject: Optional[str] = Field(None, description="Short subject")
    message: str = Field(..., description="Project details or message")
    
class CaseStudy(BaseModel):
    """
    Case studies / portfolio entries
    Collection name: "casestudy"
    """
    title: str = Field(..., description="Project title")
    client: Optional[str] = Field(None, description="Client or industry")
    services: List[str] = Field(default_factory=list, description="Services involved")
    materials: List[str] = Field(default_factory=list, description="Materials used")
    description: Optional[str] = Field(None, description="Summary of the project")
    challenges: Optional[str] = Field(None, description="Challenges faced")
    solutions: Optional[str] = Field(None, description="Solutions applied")
    specs: Optional[str] = Field(None, description="Key specs and tolerances")
    images: List[HttpUrl] = Field(default_factory=list, description="Image URLs")

class JobOpening(BaseModel):
    """
    Careers postings
    Collection name: "jobopening"
    """
    title: str
    location: str = Field("Horka nad Moravou, Czech Republic")
    type: str = Field("Full-time")
    description: Optional[str] = None
    requirements: List[str] = Field(default_factory=list)
    benefits: List[str] = Field(default_factory=list)
    
class TeamMember(BaseModel):
    """
    Team members
    Collection name: "teammember"
    """
    name: str
    role: str
    bio: Optional[str] = None
    photo: Optional[HttpUrl] = None
    email: Optional[str] = None

# Example legacy schemas kept for reference (unused in this project)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
