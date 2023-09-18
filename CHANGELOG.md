# Changelog

# [v3.0.0] - 2023.09.18
### Added
- Error handling for airport data loading.
- Unit testing for main endpoints parsing, internal retryable queries w/ backoff, error handling and logging. 

### Changed
- Module console logging is now only set up if handlers haven't already been specified.
- `dataclass` usage instead of `namedtuple`.
- Only load airport data as needed.
- Separated out concerns to `SessionManager`.
- Less redundant logging.
- Propagate up exceptions if all retries fail. 

### Removed
- **Removed the availability API.**
  - Unfortunately, grabbing a session cookie is now insufficient to use this API.
Usage of the API now requires a session cookie to be generated within a "real" browser session.
I do not wish to add the capability to specifically work around this, seemingly intentional, limitation.
  - With all this in mind, I've decided to regrettably remove the ability to use this endpoint from the library, 
since it will fail in most cases without such a workaround implemented.
- Methods deprecated in v2.0.0 have now been completely removed.

# [v2.3.1] - 2023.05.03
### Added
- README warning note for availability API
- README non-affiliation disclaimer.

# [v2.3.0] - 2023.05.03
### Added
- Optional `destination_airport` keyword argument to the cheap flights endpoints, 
in case you only care about the cheapest flight to a single airport.
- Improved type hints on the main API methods.
- In regard to the availability API:
  - Ability to grab a session cookie for use by the availability API.
  - Exceptions raised when the availbility API declines to provide results,
  for reasons such as rate limiting or the lack of a session cookie.  
  - Thanks to [@dolohow](https://www.github.com/dolohow).

### Changed
- When the library hits an exception parsing an API response, it will now also log the original query params.
  - Thanks to [@dolohow](https://www.github.com/dolohow).
- Small refactors, additional type hints 

### Fixed
- `currency` is now only added as a parameter on calls to `get_cheapest_return_flights` whenit is configured, identical
to `get_cheapest_flights`.

# [v2.2.0] - 2023.04.18
### Added
- Ability to constrain the max price of retrieved flights/trips from the API when 
using `get_cheapest_flights` or `get_cheapest_return_flights` via the `max_price` kwarg.
- Added `currency` field to the `Flight` object.
  - Availability API method `get_all_flights` does not support specifying currency (it is always the currency of the
  departure country), but this was not documented. `Flight` will now allow the user to see what currency has been
returned.
- Log a warning when returned currency doesn't match the configured value.
  - Primarily to warn users using the `get_all_flights` API that the response isn't as configured.
  - Might also be useful if the `get_cheapest_flights` and `get_cheapest_return_flights` APIs ever stop respecting
requests for results in specific currencies.

### Fixed
- Incorrect date format used for logs.

### Changed
- It is now _optional_ to specify `currency` when creating an instance of the library.
  - If not specified, the API decides the return currency (normally the currency of the departure country).
  - If an API, such as the availability / `get_all_flights` API, doesn't support it anyway, this will be ignored,
except for the purposes of deciding whether a warning should be shown, where the currencies mismatch.

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