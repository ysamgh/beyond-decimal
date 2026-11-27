# arXiv Research Platform — MVP Architecture

## Purpose

Provide a reusable, read-only integration with arXiv for discovery and literature management, plus a local, human-gated manuscript release workflow. This is an independent research tool and is not endorsed by or affiliated with arXiv.

## Architecture

- **Provider adapter:** `ArxivClient` calls only the official legacy Atom query endpoint over HTTPS.
- **Rate policy:** one serialized connection and at least 3.1 seconds between requests, following the published arXiv API terms.
- **Metadata parser:** strict Atom parsing, bounded response size, rejects DTD/entity declarations, validates arXiv IDs, and constructs abstract/PDF links only from validated IDs.
- **Local store:** SQLite stores descriptive metadata, query history, and user-authored notes. It does not mirror or redistribute paper PDFs.
- **Research workflow:** literature inventory includes metadata and notes and explicitly requires human synthesis/source verification.
- **MCP adapter:** optional stdio server exposes read-only discovery, metadata retrieval, notes, library listing, literature inventory, and release preflight.
- **Release gate:** preflight only. No endpoint, token, credential, browser automation, or code path submits to arXiv. The author must verify authorship, affiliation, category, license, source/PDF, endorsement, and submit through the official interface.

## Security controls

1. No arXiv account credentials or tokens are stored or requested.
2. No arbitrary URL fetch tool is exposed; API host is constant.
3. User input is length/type validated; paper IDs are regex validated.
4. SQLite uses parameterized statements.
5. XML response size is capped and DTD/entity declarations are rejected.
6. Network calls have a timeout and are serialized/throttled.
7. PDFs are linked at arXiv, not cached or served by this application. Users must respect each paper's license and copyright.
8. The release preflight reports readiness only and cannot trigger a submission.
9. Local database path can be overridden with `BEYOND_DECIMAL_DB`; do not place the database in a public web directory.

## Install and run

Core CLI (no runtime dependencies):

```bash
python -m pip install -e .
python -m beyond_decimal.arxiv.cli search 'all:minimum description length' --limit 20
python -m beyond_decimal.arxiv.cli review
```

Optional MCP server:

```bash
python -m pip install -e '.[mcp]'
BEYOND_DECIMAL_DB=data/arxiv/research.sqlite3 python -m beyond_decimal.arxiv.mcp_server
```

The MCP server uses stdio. Configure it in the MCP host that launches the process; do not expose stdio through an unauthenticated network bridge.

## MVP scope and non-goals

Included: search, fetch metadata, local library, research notes, literature inventory, and human release preflight.

Not included: automated PDF mirroring, full-text extraction, citation graph crawling, ORCID identity verification, account login, endorsement requests, or arXiv submission. These require separate legal, product, or security review.

## API compliance

The adapter uses arXiv's public Atom API. Identical searches are cached locally for 24 hours (including query, offset, and page size) to avoid unnecessary repeated requests. Respect the current API terms and rate limits. The service should acknowledge arXiv's interoperability statement where appropriate: “Thank you to arXiv for use of its open access interoperability.”

## Validation

CI tests exercise XML parsing, ID validation, rate-limit configuration, SQL persistence, notes, and the release gate. Network tests are mocked; a live smoke test should be run manually at low frequency before production use.
