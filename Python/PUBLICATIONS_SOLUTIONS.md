# Publications Update Guide

## Problem: Google Scholar Blocking

Google Scholar aggressively blocks automated scraping, which causes the `scholarly` library to fail. This is a known limitation.

## Solutions (in order of recommendation)

### Solution 1: Manual JSON Update (RECOMMENDED)

This is the most reliable method:

1. **Edit the manual JSON file:**
   ```
   Python/publications_manual.json
   ```

2. **Add your publications** in this format:
   ```json
   {
     "title": "Your Paper Title",
     "authors": "Author 1, Author 2, Author 3",
     "venue": "Conference/Journal Name",
     "year": "2025",
     "abstract": "Full abstract here...",
     "url": "https://doi.org/...",
     "citations": 0
   }
   ```

3. **Run the manual update script:**
   ```bash
   python Python/update_publications_manual.py
   ```

This will update `publications.html` with your manually entered data.

### Solution 2: Use Selenium (More Reliable)

Install Selenium for browser automation:

```bash
pip install selenium scholarly
```

Then use this code in `fetch_publications.py`:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scholarly import scholarly, ProxyGenerator

# Set up Selenium
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

pg = ProxyGenerator()
pg.Selenium_Driver(driver)
scholarly.use_proxy(pg, driver)
```

### Solution 3: Wait and Retry

Google Scholar may temporarily block your IP. Wait 10-15 minutes and try again:

```bash
python Python/fetch_publications.py
```

### Solution 4: Use a VPN

1. Connect to a VPN
2. Run the script:
   ```bash
   python Python/fetch_publications.py
   ```

### Solution 5: Export from Google Scholar Manually

1. Go to your Google Scholar profile
2. Click "Export" → "BibTeX"
3. Save the `.bib` file
4. Use a BibTeX parser to convert to JSON
5. Copy to `publications_manual.json`

## GitHub Actions

The GitHub Actions workflow will also face this issue. To handle it:

1. **Use the manual JSON as fallback:**
   - Keep `publications_manual.json` updated
   - The workflow will use it if Scholar fails

2. **Or disable Scholar fetching:**
   - Comment out the "Fetch Publications" step in `.github/workflows/update_site.yml`

## Recommended Workflow

**For now, use the manual method:**

1. Maintain your publications in `Python/publications_manual.json`
2. Run `python Python/update_publications_manual.py` when you add new papers
3. Commit and push the changes

**Benefits:**
- ✅ Always works
- ✅ Full control over content
- ✅ No rate limiting issues
- ✅ Can add custom formatting

**Drawbacks:**
- ⚠ Manual updates required
- ⚠ Need to remember to update

## Future: API Alternative

Consider using:
- **ORCID API** - More reliable, has official API
- **Semantic Scholar API** - Free, well-documented
- **CrossRef API** - For DOI-based lookups

I can help implement any of these if you prefer!
