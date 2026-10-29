# Rural Outfitters home-page Best Sellers feed

This repository publishes the six product IDs shown in each home-page Best Sellers tab. A daily GitHub Action reads the public Shopify collection order and writes `best-sellers.json`. The Cloudflare Best Sellers worker uses that feed to maintain the `custom-badge-1` product tag.

The feed contains public product IDs only. If the storefront request fails or returns an incomplete list, the action fails without replacing the last valid feed.
