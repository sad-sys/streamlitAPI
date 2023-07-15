import streamlit as st
import openai
import re
import ast
import requests
import json

def get_flights(query_string):
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchFlights"
    headers = {
        "X-RapidAPI-Key": "051fbe5ae3mshc5e6a0572f5f515p15c4adjsn4922e270d9eb",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params = query_string)
    print ('•••••••••••••••••••••••••••••••')
    print (response)
    data = response.json()
    return data['data']['flights']

def show_flights(flights):
    for i, flight in enumerate(flights, 1):
        st.write(f"Flight {i}")
        
        for j, segment in enumerate(flight['segments'], 1):
            st.write(f"\tSegment {j}")
            
            for k, leg in enumerate(segment['legs'], 1):
                st.write(f"\t\tLeg {k}")
                st.write(f"\t\tOrigin Station: {leg['originStationCode']}")
                st.write(f"\t\tDestination Station: {leg['destinationStationCode']}")
                st.write(f"\t\tDeparture Date and Time: {leg['departureDateTime']}")
                st.write(f"\t\tArrival Date and Time: {leg['arrivalDateTime']}")
                st.write(f"\t\tClass of Service: {leg['classOfService']}")
                st.write(f"\t\tCarrier Code: {leg['marketingCarrierCode']}")

                equipment_id = leg.get('equipmentId', 'N/A') # N/A will be used if 'equipmentId' is not found
                st.write(f"\t\tEquipment: {equipment_id}")

                st.write(f"\t\tFlight Number: {leg['flightNumber']}")
                st.write(f"\t\tNumber of Stops: {leg['numStops']}")
                st.write(f"\t\tDistance (km): {leg['distanceInKM']}")
                st.write(f"\t\tIs International: {leg['isInternational']}")

def generate_advert(flights):
    # Start a conversation for OpenAI API
    conversation = [
        {"role": "system", "content": "You are a creative AI, trained to generate engaging and attractive advertisements for flights."},
        {"role": "user", "content": f"I have the following flights available: {flights}. Can you create an advertisement based on this information?"}
    ]
    
    # Make OpenAI API request
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.6,
        max_tokens=500
    )
    
    # Extract advert text
    advert_text = response['choices'][0]['message']['content']
    
    return advert_text


def main():
    st.title("Flight Search")

    prompt = st.text_input("Enter your trip data", "I want to go on a holiday to france in august from LHR to CDG")

    if st.button("Search Flights"):
        # Set OpenAI key
        openai.api_key = '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'
        
        # Formulate conversation for OpenAI API
        conversation = [
            {"role": "system", "content": "You are a helpful assistant to present data in string format for the tripadvisor API "},
            {"role": "user", "content": f"I have the following trip data({prompt}) Can you make data that can be inputted into the tripadvisor API based off this data, just write the params in the format 'querystring = {{'sourceAirportCode': 'AIRPORT SOURCE CODE E.G. LHR', 'destinationAirportCode': 'Airport Code e.g. CDG', date: 'YYYY-MM-DD', itineraryType: 'ONE_WAY', sortOrder: 'ML_BEST_VALUE', numAdults: '1', numSeniors: '0', classOfService: 'ECONOMY', pageNumber: '1', currencyCode: 'USD'}}'"},
            {"role":"user", "content": "For Example an output for a trip to China would be ''' querystring = {'sourceAirportCode': 'LHR', 'destinationAirportCode': 'PEK', date: '2023-08-01', itineraryType: 'ONE_WAY', sortOrder: 'ML_BEST_VALUE', numAdults: '1', numSeniors: '0', classOfService: 'ECONOMY', pageNumber: '1', currencyCode: 'USD'} '''"}
        ]
        
        # Make OpenAI API request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.6,
            max_tokens=500
        )
        
        # Extract query string
        response_content = response['choices'][0]['message']['content']
        pattern = r'querystring\s*=\s*({[^}]+})'
        matches = re.findall(pattern, response_content)
        query_string = ast.literal_eval(matches[0]) if matches else None
        print (query_string)
        # If query string found, get and show flights
        if query_string:
            flights = get_flights(query_string)
            
            show_flights(flights)
        else:
            st.write("Sorry, could not formulate the trip data.")


if __name__ == "__main__":
    main()
