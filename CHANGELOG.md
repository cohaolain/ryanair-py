# Changelog

# [v2.1.0] - 2023.03.12
### Added
- Added flight departure time filter keyword arguments to `get_cheapest_flights` and `get_cheapest_return_flights`.

# [v2.0.1] - 2023.03.11
### Fixed
- Module description to account for new functionality.

# [v2.0.0] - 2023.03.11

### Added
- Ability to use the _availability_ endpoint. Now we aren't confined to getting the _cheapest_ flight each day - we can just get them all.
  - This is useful if you want to do your own filtering on those flights, e.g. that fit your travel criteria.
    - e.g. Depart after 19:00 on Fridays, or before 10:00 on Saturdays.
  - Interestingly, I think the "cheapest" flights API now supports some nice new filtering types e.g. day of week, time of day and flight duration. 
    - I think I'll try to add support for these as keyword args in the next version.
- Ability to pass/override arbitrary `custom_params` in api methods.
- _Flight number_ to the `Flight` tuple.
- Added `destination_country` keyword arg to `get_cheapest_return_flights`.
- Improved logging and error handling
  - Request exception now retry with expo backoff
- Much improved README covering existing and new methods

### Changed
- With the addition of the _availability_ endpoint, I've decided to rename the existing methods
  - This is to make it more clear what they're actually intended to do.

| Deprecated name    | New name                    |
|--------------------|-----------------------------|
| get_flights        | get_cheapest_flights        |
| get_return_flights | get_cheapest_return_flights |

- Usage of the old methods will continue to work for now, but may be removed in a future release.
  - For now, a warning will be shown once if you call the methods by their old names.


# [v1.0.2] - 2022.02.26

### Added
- Allow an optional argument to `get_flights` specifying a specific destination country code.

### Fixed
- Update repo URL so packages managers have a working source reference.

# [v1.0.1] - 2022.02.20

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