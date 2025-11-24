# Automatic Publications Updater

This script automatically fetches your publications from Google Scholar and updates `publications.html`.

## Features

- ✅ Fetches all publications from your Google Scholar profile
- ✅ Includes author names, venues, years, and abstracts
- ✅ Automatically sorts by year (newest first)
- ✅ Shows citation counts
- ✅ Maintains the modern card-based design
- ✅ Saves backup to JSON file

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Update your Scholar ID** (if needed):
   - Open `fetch_publications.py`
   - Change `SCHOLAR_ID = 'ELEdK98AAAAJ'` to your ID
   - (Your current ID is already set correctly)

## Usage

### Manual Update

Run the script from the repository root:

```bash
python Python/fetch_publications.py
```

This will:
1. Fetch all publications from Google Scholar
2. Save them to `Python/publications_data.json`
3. Update `publications.html` with the new data

### Automatic Update (GitHub Actions)

The script can be integrated into your GitHub Actions workflow to automatically update publications daily or on push.

Add this to `.github/workflows/update_site.yml`:

```yaml
- name: Update Publications
  run: |
    cd Python
    python fetch_publications.py
```

## Output Format

Each publication will be displayed as a card with:
- **Title** (linked to the publication URL)
- **Authors** (all co-authors listed)
- **Venue** (journal/conference name)
- **Year**
- **Abstract** (if available)
- **Citation count** (if > 0)

## Troubleshooting

### Rate Limiting

If you get rate-limited by Google Scholar, uncomment these lines in `fetch_publications.py`:

```python
pg = ProxyGenerator()
pg.FreeProxies()
scholarly.use_proxy(pg)
```

### Missing Publications

- Check your Google Scholar profile is public
- Verify your Scholar ID is correct
- Some publications may take time to appear on Scholar

## Notes

- The script preserves the HTML structure and styling
- Publications are automatically sorted by year (newest first)
- A backup JSON file is created in `Python/publications_data.json`
- The script is safe to run multiple times
