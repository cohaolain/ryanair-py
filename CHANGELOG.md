# Changelog

# [Unreleased]

### Added

- Added a changelog :)

### Fixed

- At _long_ last:
  - Use up-to-date URLs for API endpoints
  - Adapt to current API usage which doesn't require an API key, at least for rate-limited interactions.

### Changed

- `get_flights`, `get_return_flights` now accept a `datetime` type, as well as string date in ISO format.