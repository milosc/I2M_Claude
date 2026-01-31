---
name: website-crawler-summarizer
description: Crawl domains respectfully, extract readable content, dedupe, and generate structured summaries.
model: sonnet
allowed-tools: Bash, Read, WebFetch, WebSearch, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill website-crawler-summarizer started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill website-crawler-summarizer ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill website-crawler-summarizer instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Website Crawler & Summarizer Skill

## What This Skill Enables

Claude can crawl websites, extract content from web pages, clean HTML to readable text, respect robots.txt, and generate structured summaries or documentation from web content. Perfect for research, competitive analysis, and content aggregation.

## Prerequisites

**Required:**
- Claude Pro subscription
- Code Interpreter feature enabled
- URLs to crawl (or sitemap)

**What Claude handles:**
- Installing scraping libraries (BeautifulSoup, Playwright, Scrapy)
- Fetching web pages
- Parsing HTML
- Extracting readable content
- Respecting robots.txt
- Rate limiting requests
- Content deduplication

## How to Use This Skill

### Single Page Extraction

**Prompt:** "Extract the main content from this webpage: https://example.com/article
Convert to clean Markdown and save as article.md"

Claude will:
1. Fetch the webpage
2. Parse HTML
3. Extract main content (remove ads, nav, footer)
4. Convert to Markdown
5. Save clean output

### Multi-Page Crawl

**Prompt:** "Crawl all pages linked from this site:
Start URL: https://docs.example.com
Only crawl pages under /docs/
Extract content from each page
Save as individual Markdown files
Max 50 pages"

Claude will:
1. Fetch start URL
2. Find all links
3. Filter to matching paths
4. Crawl each page (with rate limiting)
5. Extract and save content
6. Generate index of pages

### Content Summarization

**Prompt:** "Crawl these 10 blog posts and:
1. Extract main content from each
2. Generate 2-sentence summary per post
3. Identify key topics
4. Create master summary document
Format as JSON with metadata."

Claude will:
1. Fetch all URLs
2. Extract content
3. Generate summaries
4. Extract topics/tags
5. Structure as JSON

### Sitemap-Based Crawl

**Prompt:** "Download sitemap from https://example.com/sitemap.xml and:
1. Extract all article URLs
2. Crawl each article
3. Extract: title, date, author, content
4. Save as CSV with metadata"

Claude will:
1. Fetch sitemap XML
2. Parse URL list
3. Crawl each URL (respecting rate limits)
4. Extract structured data
5. Export as CSV

## Common Workflows

### Competitor Analysis
```
"Analyze competitor website:
1. Crawl main site (max 20 pages)
2. Extract: services, pricing mentions, features
3. Identify key messaging themes
4. Create structured comparison report
Focus on product/service pages."
```

### Documentation Mirror
```
"Create local mirror of documentation:
1. Start at https://docs.example.com
2. Crawl all /docs/* pages
3. Download images referenced
4. Convert to Markdown
5. Preserve link structure
6. Generate offline-browseable site"
```

### Research Aggregation
```
"Gather research from these 20 URLs:
1. Extract main content from each
2. Identify key findings and quotes
3. Extract citations and references
4. Group by topic/theme
5. Create annotated bibliography
Output as structured Markdown."
```

### Change Detection
```
"Monitor this webpage for changes:
1. Fetch current version
2. Extract main content
3. Compare with version from last week
4. Highlight what changed
5. Generate change report"
```

## Web Scraping Best Practices

### Respect & Ethics
- **Always check robots.txt**: Claude will respect crawl rules
- **Rate limiting**: Default to 1-2 requests/second
- **User agent**: Identify bot politely
- **Terms of service**: Respect website ToS
- **Copyright**: Content remains property of original creator

### Technical Considerations
- **Dynamic content**: Use Playwright for JavaScript-heavy sites
- **Authentication**: Provide cookies/tokens if needed
- **Pagination**: Handle "Load More" and infinite scroll
- **Anti-bot measures**: Respect CAPTCHAs (don't try to bypass)

## Content Extraction Methods

### HTML Parsing
- BeautifulSoup for static HTML
- CSS selectors for targeting elements
- XPath for complex queries

### Readability Algorithms
- Remove boilerplate (nav, ads, footers)
- Extract main article content
- Preserve formatting (headings, lists, links)

### Structured Data
- JSON-LD extraction
- Schema.org metadata
- Open Graph tags
- Twitter Cards

## Tips for Best Results

1. **Start Small**: Test with 1-2 pages before bulk crawling
2. **Specify Scope**: Define which pages to crawl ("only /blog/* paths")
3. **Rate Limits**: Mention if you need slower crawling ("1 page per 5 seconds")
4. **Content Type**: Describe what to extract ("article text only, no comments")
5. **Error Handling**: "Skip pages that error and continue" vs "stop on first error"
6. **Deduplication**: "Skip duplicate content" if crawling related pages
7. **Storage**: Specify output format (Markdown, JSON, CSV, HTML)

## Advanced Features

### JavaScript Rendering
- Use Playwright for SPAs
- Wait for dynamic content to load
- Handle infinite scroll
- Click "Load More" buttons

### Link Discovery
- Find all links on page
- Filter by pattern (regex)
- Depth-limited crawling
- Breadth-first vs depth-first

### Data Extraction
- Tables to CSV
- Lists to arrays
- Forms and inputs
- Metadata extraction

### Content Processing
- HTML to Markdown conversion
- Text cleaning and normalization
- Language detection
- Content summarization

## Troubleshooting

**Issue:** Getting blocked or rate limited
**Solution:** "Slow down to 1 request per 10 seconds" and "Add random delays between requests"

**Issue:** Content not extracting correctly
**Solution:** "Show me the raw HTML first" then identify CSS selectors for main content

**Issue:** JavaScript content not loading
**Solution:** "Use Playwright to render JavaScript" or "Wait 5 seconds for content to load"

**Issue:** Too many pages being crawled
**Solution:** Set limits: "Max 50 pages" or "Only crawl 2 levels deep" or "Stick to /docs/* path"

**Issue:** Images/assets not downloading
**Solution:** "Download all images referenced in articles" or provide specific asset types needed

**Issue:** Different page structures
**Solution:** Provide multiple CSS selectors: "Try article.content, then div.post-body, then main"

## Legal & Ethical Considerations

**Important**: Always respect:
- Copyright and intellectual property
- Website terms of service
- robots.txt directives
- Rate limits and server resources
- Privacy and personal data
- Commercial use restrictions

**Use cases**: Research, archival, accessibility, personal use
**Prohibited**: Spam, unauthorized scraping, data theft, ToS violations

## Learn More

- [robots.txt Guide](https://developers.google.com/search/docs/crawling-indexing/robots/intro) - Crawling etiquette
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - HTML parsing
- [Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html) - Advanced crawling
- [Playwright](https://playwright.dev/) - Browser automation
- [Mozilla Readability](https://github.com/mozilla/readability) - Content extraction


## Key Features

- Robots-aware crawling
- Boilerplate removal
- Language detection
- JSON/MD export

## Use Cases

- Competitive intel packs
- Documentation mirrors
- Research briefs

## Examples

### Example 1: Basic fetch + Readability (Node)

```javascript
import { JSDOM } from 'jsdom';
import { Readability } from '@mozilla/readability';
import fetch from 'node-fetch';

const html = await (await fetch('https://example.com')).text();
const doc = new JSDOM(html, { url: 'https://example.com' });
const article = new Readability(doc.window.document).parse();
console.log(article.title);
```

## Troubleshooting

### Blocked by anti-bot

Reduce concurrency, add polite delays, and avoid sensitive endpoints.

### BeautifulSoup returning None for elements that visibly exist on page

Content may be JavaScript-rendered. Use Playwright or Puppeteer to render DOM. Check if element is in iframe or shadow DOM.

### UnicodeDecodeError or mojibake characters in extracted content

Detect charset from HTTP headers or meta tags. Use response.encoding='utf-8' or chardet library. Specify parser='lxml' explicitly.

### Playwright crawl timing out or consuming excessive memory with multiple pages

Close browser contexts after each page. Use browser.newContext() per session. Set timeout limits and enable headless mode.

### Readability extraction missing article content or extracting wrong sections

Try different parsers (lxml, html.parser, html5lib). Manually specify article CSS selector as fallback if auto-detect fails.

## Learn More

For additional documentation and resources, visit:

https://github.com/mozilla/readability
