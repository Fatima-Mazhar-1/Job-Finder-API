from pydantic import BaseModel, Field
from typing import List, Optional

class JobSearchRequest(BaseModel):
    """Model for job search request parameters"""
    position: str = Field(..., description="Job title or position")
    experience: str = Field(..., description="Required years of experience")
    salary: Optional[str] = Field(None, description="Expected salary range")
    jobNature: Optional[str] = Field(None, description="Job nature (remote, onsite, hybrid)")
    location: Optional[str] = Field(None, description="Job location")
    skills: str = Field(..., description="Required skills for the job")

class JobListing(BaseModel):
    """Model for individual job listing"""
    job_title: str
    company: str
    experience: Optional[str] = None
    jobNature: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    apply_link: str
    source: str = Field(..., description="Source platform (LinkedIn, Indeed, etc.)")
    
class JobSearchResponse(BaseModel):
    """Model for job search response"""
    relevant_jobs: List[JobListing] 