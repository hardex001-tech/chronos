import re
from urllib.parse import urlparse
import httpx

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

async def scrape_url_metadata(url: str) -> dict:
    """
    Given a URL, extract the page title, company/platform name, favicon, and root domain.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    parsed = urlparse(url)
    root_domain = parsed.netloc.lower()
    # Remove www.
    if root_domain.startswith("www."):
        root_domain = root_domain[4:]

    # Derive sensible company name from domain (e.g. "goldmansachs.com" -> "Goldman Sachs")
    parts = root_domain.split(".")
    company_name = parts[0].capitalize() if parts else "Unknown"

    default_favicon = f"https://www.google.com/s2/favicons?domain={root_domain}&sz=64"
    result = {
        "url": url,
        "title": company_name,
        "company": company_name,
        "sender_domain": root_domain,
        "logo_url": default_favicon,
        "description": ""
    }

    try:
        async with httpx.AsyncClient(timeout=4.0, follow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chronos/1.0"
        }) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                html = resp.text
                if BS4_AVAILABLE:
                    soup = BeautifulSoup(html, "html.parser")
                    # Title
                    og_title = soup.find("meta", property="og:title")
                    if og_title and og_title.get("content"):
                        result["title"] = og_title["content"].strip()
                    elif soup.title and soup.title.string:
                        result["title"] = soup.title.string.strip()

                    # Company / Site Name
                    og_site_name = soup.find("meta", property="og:site_name")
                    if og_site_name and og_site_name.get("content"):
                        result["company"] = og_site_name["content"].strip()

                    # Description
                    og_desc = soup.find("meta", property="og:description")
                    meta_desc = soup.find("meta", attrs={"name": "description"})
                    if og_desc and og_desc.get("content"):
                        result["description"] = og_desc["content"].strip()[:180]
                    elif meta_desc and meta_desc.get("content"):
                        result["description"] = meta_desc["content"].strip()[:180]

                    # Favicon
                    icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
                    if icon_link and icon_link.get("href"):
                        href = icon_link["href"]
                        if href.startswith("//"):
                            result["logo_url"] = "https:" + href
                        elif href.startswith("/"):
                            result["logo_url"] = f"https://{parsed.netloc}{href}"
                        elif href.startswith("http"):
                            result["logo_url"] = href
                else:
                    # Regex fallback
                    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
                    if title_match:
                        result["title"] = title_match.group(1).strip()
    except Exception:
        # Fallback to domain-derived title
        pass

    return result
