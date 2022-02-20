# Changelog

# [Unreleased]

### Added

- Added a changelog :)
- Some airport utils (`ryanair.airport_utils`), that allow you to compute the haversine distance between two airports (by IATA code), or from a `Flight` object.
  - Airport data in CSV format sourced from [a gist here](https://gist.github.com/chrisgacsal/070379c59d25c235baaa88ec61472b28).

### Fixed

- At _long_ last:
  - Use up-to-date URLs for API endpoints
  - Adapt to current API usage which doesn't require an API key, at least for rate-limited interactions.

### Changed

- `get_flights`, `get_return_flights` now accept a `datetime` type, as well as string date in ISO format.