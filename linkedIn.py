from typing import Any
import httpx
import json
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv

load_dotenv()

# Read the RAPIDAPI_KEY from the environment variables
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("RAPIDAPI_KEY is not set in the environment variables")

mcp = FastMCP("linkedin_profile_scraper")

LINKEDIN_API_BASE = "https://fresh-linkedin-profile-data.p.rapidapi.com"
RAPIDAPI_HOST = "fresh-linkedin-profile-data.p.rapidapi.com"

async def get_linkedin_data(linkedin_url: str) -> dict[str, Any] | None:
    """Fetch LinkedIn profile data using the Fresh LinkedIn Profile Data API."""
    params = {
        "linkedin_url": linkedin_url,
        "include_skills": "true",
        "include_certifications": "true",
        "include_publications": "false",
        "include_honors": "false",
        "include_volunteers": "false",
        "include_projects": "true",
        "include_patents": "false",
        "include_courses": "true",
        "include_organizations": "true",
        "include_profile_status": "false",
        "include_company_public_url": "true"
    }
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{LINKEDIN_API_BASE}/get-linkedin-profile",
                headers=headers,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@mcp.tool()
async def get_profile(linkedin_url: str) -> str:
    """Get LinkedIn profile data for a given profile URL.

    Args:
        linkedin_url: The LinkedIn profile URL.
    """
    data = await get_linkedin_data(linkedin_url)
    if not data:
        return "Unable to fetch LinkedIn profile data."
    return json.dumps(data, indent=2)


async def search_jobs(keywords: str, geo_code: int = 92000000, date_posted: str = "Any time", 
                      experience_levels: list = None, company_ids: list = None, 
                      title_ids: list = None, onsite_remotes: list = None, 
                      functions: list = None, industries: list = None, 
                      job_types: list = None, sort_by: str = "Most relevant", 
                      easy_apply: str = "false", under_10_applicants: str = "false", 
                      start: int = 0) -> dict[str, Any] | None:
    """Search for jobs using the Fresh LinkedIn Profile Data API."""
    # Initialize empty lists for optional parameters
    experience_levels = experience_levels or []
    company_ids = company_ids or []
    title_ids = title_ids or []
    onsite_remotes = onsite_remotes or []
    functions = functions or []
    industries = industries or []
    job_types = job_types or []
    
    payload = {
        "keywords": keywords,
        "geo_code": geo_code,
        "date_posted": date_posted,
        "experience_levels": experience_levels,
        "company_ids": company_ids,
        "title_ids": title_ids,
        "onsite_remotes": onsite_remotes,
        "functions": functions,
        "industries": industries,
        "job_types": job_types,
        "sort_by": sort_by,
        "easy_apply": easy_apply,
        "under_10_applicants": under_10_applicants,
        "start": start
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{LINKEDIN_API_BASE}/search-jobs",
                headers=headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error during job search: {e}")
            return None

@mcp.tool()
async def get_jobs(keywords: str, geo_code: int = 92000000, date_posted: str = "Any time", 
                   company_id: int = None) -> str:
    """Search for jobs on LinkedIn based on keywords and other filters.
    
    Args:
        keywords: Job keywords to search for (e.g., "marketing", "software engineer")
        geo_code: Geographic location code (default: 92000000 for worldwide)
        date_posted: Time filter for job postings (e.g., "Any time", "Past month", "Past week", "24hr")
        company_id: Optional company ID to filter jobs by specific company
    """
    company_ids = [company_id] if company_id is not None else []
    
    data = await search_jobs(
        keywords=keywords,
        geo_code=geo_code,
        date_posted=date_posted,
        company_ids=company_ids
    )
    
    if not data:
        return "Unable to fetch LinkedIn job search results."
    return json.dumps(data, indent=2)




async def get_linkedin_pdf_cv(linkedin_url: str) -> bytes | None:
    """Fetch LinkedIn profile as PDF CV using the Fresh LinkedIn Profile Data API."""
    params = {
        "linkedin_url": linkedin_url
    }
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{LINKEDIN_API_BASE}/get-profile-pdf-cv",
                headers=headers,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.content  # Return the binary PDF content
        except Exception as e:
            print(f"Error fetching PDF CV: {e}")
            return None

@mcp.tool()
async def get_pdf_cv(linkedin_url: str, output_path: str = None) -> str:
    """Get LinkedIn profile as a PDF CV for a given profile URL.
    
    This function retrieves a PDF version of the LinkedIn profile and can either
    save it to a file or return a message confirming the PDF was generated.
    
    Args:
        linkedin_url: The LinkedIn profile URL.
        output_path: Optional path to save the PDF file. If not provided, 
                     the PDF won't be saved to disk.
    """
    pdf_data = await get_linkedin_pdf_cv(linkedin_url)
    if not pdf_data:
        return "Unable to fetch LinkedIn profile PDF CV."
    
    if output_path:
        try:
            with open(output_path, "wb") as file:
                file.write(pdf_data)
            return f"PDF CV saved successfully to: {output_path}"
        except Exception as e:
            return f"Error saving PDF CV: {e}"
    else:
        return f"PDF CV generated successfully for {linkedin_url} (size: {len(pdf_data)} bytes). No file was saved as no output path was provided."


# Constants for Job Posting Feed API
JOB_POSTING_API_BASE = "https://job-posting-feed-api.p.rapidapi.com"
JOB_POSTING_API_HOST = "job-posting-feed-api.p.rapidapi.com"

async def get_job_postings(
    search: str = None,
    title_search: bool = None,
    description_type: str = "html",
    location_filter: str = None,
    organization_filter: str = None,
    remote: bool = None,
    include_ai: bool = None,
    ai_employment_type_filter: str = None,
    ai_work_arrangement_filter: str = None,
    ai_experience_level_filter: str = None,
    ai_visa_sponsorship_filter: bool = None
) -> dict[str, Any] | None:
    """Fetch job postings using the Job Posting Feed API."""
    # Build params dict, excluding None values
    params = {}
    if search is not None:
        params["search"] = search
    if title_search is not None:
        params["title_search"] = str(title_search).lower()
    if description_type:
        params["description_type"] = description_type
    if location_filter:
        params["location_filter"] = location_filter
    if organization_filter:
        params["organization_filter"] = organization_filter
    if remote is not None:
        params["remote"] = str(remote).lower()
    if include_ai is not None:
        params["include_ai"] = str(include_ai).lower()
    if ai_employment_type_filter:
        params["ai_employment_type_filter"] = ai_employment_type_filter
    if ai_work_arrangement_filter:
        params["ai_work_arrangement_filter"] = ai_work_arrangement_filter
    if ai_experience_level_filter:
        params["ai_experience_level_filter"] = ai_experience_level_filter
    if ai_visa_sponsorship_filter is not None:
        params["ai_visa_sponsorship_filter"] = str(ai_visa_sponsorship_filter).lower()
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": JOB_POSTING_API_HOST
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{JOB_POSTING_API_BASE}/active-ats-meili",
                headers=headers,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching job postings: {e}")
            return None

@mcp.tool()
async def search_active_jobs(
    search: str = None,
    title_search: bool = False,
    remote: bool = None,
    location: str = None,
    company: str = None,
    experience_level: str = None
) -> str:
    """Search for active job postings with various filters.
    
    Args:
        search: Keywords to search for in job listings (e.g., "Flutter Developer")
        title_search: Set to True to search keywords in job titles only
        remote: Set to True for remote jobs only, False for non-remote only
        location: Filter by location(s), use semicolons for multiple (e.g., "United States;London")
        company: Filter by company/organization, use semicolons for multiple (e.g., "Google;Microsoft")
        experience_level: Filter by experience level: "0-2", "2-5", "5-10", "10+", or combinations with semicolons
    """
    data = await get_job_postings(
        search=search,
        title_search=title_search,
        description_type="html",
        location_filter=location,
        organization_filter=company,
        remote=remote,
        ai_experience_level_filter=experience_level,
        include_ai=True  # Enable AI features since we're using experience_level
    )
    
    if not data:
        return "Unable to fetch job postings."
    return json.dumps(data, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")