# Stock Acquisition Failure Log — 2026-07-04 OpenMontage WC2026 Teaser

## Verified failures
- Wikimedia Commons `Special:MediaSearch` page fetch: blocked by `robots.txt`; not usable for autonomous bulk download in this environment.
- Pixabay direct CDN URLs like `https://cdn.pixabay.com/photo/...` often returned 21–29 byte stubs instead of full images when fetched via `curl` from this host. Do not assume the file is valid based on HTTP status alone.
- Unsplash `images.unsplash.com` direct URLs returned stubs of 29 bytes in this environment for several photo IDs.
- `image_generate` backend unavailable without `FAL_KEY` and Nous Portal billing; repeated retries are blocked by platform, not transient.

## Verified OK
- Pixabay HTML search page `/images/search/...` can be rendered via `mcp_fetch_fetch` and shows image tiles with URLs; useful for manual URL harvesting.
- `stadium-fans.jpg` from Pixabay direct CDN downloaded successfully at ~287K in this environment; confirms not all Pixabay CDN URLs fail.
- `yt-dlp` metadata fetch succeeded; transcript not available for target video.

## Accepted fallback rule
When stock acquisition yields < 3 usable images:
1) Use the verified local images in `assets/images/`.
2) Switch pipeline to still-led Remotion motion treatment with text cards.
3) Ask the user to manually place additional footage in `assets/video/`.
Do not keep retrying the same blocked providers.
