from mcp.server.fastmcp import FastMCP  
from src.job_api import fetch_linkedin_jobs, fetch_xing_jobs
 

mcp = FastMCP("Job Rommender")
@mcp.tool()
async def fetchlinkedin(listofkey):
    return fetch_linkedin_jobs(listofkey)
@mcp.tool()
async def fetchxing(listofkey):
    return fetch_xing_jobs(listofkey)

if __name__ == "__main__":
    mcp.run(transport="stdio")