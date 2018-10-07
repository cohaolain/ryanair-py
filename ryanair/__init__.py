"""
This module allows you to retrieve the cheapest flights, with/out return flights, within a fixed set of dates.
This is done directly through Ryanair's API and requires an API Key supplied by Ryanair.
"""

import requests
from collections import namedtuple

class Ryanair:
    def __init__(self, apiKey, currency):
        def getFlights(sourceAirport, dateFrom, dateTo):
            params={
                "departureAirportIataCode":sourceAirport,
                "outboundDepartureDateFrom":dateFrom,
                "outboundDepartureDateTo":dateTo,
                "currency":self.currency,
                "apikey":self.apiKey}
            response = requests.get("http://apigateway.ryanair.com/"+"pub/v1/farefinder/3/oneWayFares", params=params).json()['fares']
            flights = []
            for flight in response:
                try:
                    flight=flight['outbound']
                except Exception as e:
                    print(response)
                flights.append(Flight(
                    origin=flight['departureAirport']['iataCode'],
                    originFull=flight['departureAirport']['name']+", "+flight['departureAirport']['countryName'],
                    destination=flight['arrivalAirport']['iataCode'],
                    destinationFull=flight['arrivalAirport']['name']+", "+flight['arrivalAirport']['countryName'],
                    departureTime=flight['departureDate'],
                    price=flight['price']['value']
                ))
            return flights

        def getReturnFlights(sourceAirport, dateFrom, dateTo, returnDateFrom, returnDateTo):
            params={
                "departureAirportIataCode":sourceAirport,
                "outboundDepartureDateFrom":dateFrom,
                "outboundDepartureDateTo":dateTo,
                "inboundDepartureDateFrom":returnDateFrom,
                "inboundDepartureDateTo":returnDateTo,
                "currency":self.currency,
                "apikey":self.apiKey}
            response = requests.get("http://apigateway.ryanair.com/"+"pub/v1/farefinder/3/roundTripFares", params=params).json()['fares']
            trips = []
            for trip in response:
                flight=trip['outbound']
                outbound = (Flight(
                    origin=flight['departureAirport']['iataCode'],
                    originFull=flight['departureAirport']['name']+", "+flight['departureAirport']['countryName'],
                    destination=flight['arrivalAirport']['iataCode'],
                    destinationFull=flight['arrivalAirport']['name']+", "+flight['arrivalAirport']['countryName'],
                    departureTime=flight['departureDate'],
                    price=flight['price']['value']
                ))
                flight=trip['inbound']
                inbound = (Flight(
                    origin=flight['departureAirport']['iataCode'],
                    originFull=flight['departureAirport']['name']+", "+flight['departureAirport']['countryName'],
                    destination=flight['arrivalAirport']['iataCode'],
                    destinationFull=flight['arrivalAirport']['name']+", "+flight['arrivalAirport']['countryName'],
                    departureTime=flight['departureDate'],
                    price=flight['price']['value']
                ))
                trips.append(Trip(outbound=outbound, inbound=inbound, totalPrice=round(outbound.price+inbound.price,2)))
            return trips

        Flight = namedtuple("Flight", ("origin", "originFull", "destination", "destinationFull", "departureTime", "price"))
        Trip = namedtuple("Trip", ("outbound", "inbound", "totalPrice"))
        self.apiKey = apiKey
        self.currency = currency

        self.getFlights = getFlights
        self.getReturnFlights = getReturnFlights
