import googlemaps
import xlsxwriter
import time
import json

def get_nearby_places(api_key, location, radius=30000, place_type='beauty_salon'):
    # Initialize the Google Maps client with your API key
    gmaps = googlemaps.Client(key=api_key)

    places = []
    next_page_token = None

    while True:
        # Search for nearby places of the specified type
        places_result = gmaps.places_nearby(location=location, radius=radius, type=place_type, page_token=next_page_token)

        # Extract relevant information for each place
        for place in places_result['results']:
            place_id = place['place_id']
            place_details = gmaps.place(place_id=place_id)['result']

            name = place_details.get('name')
            address = place_details.get('formatted_address')
            phone_number = place_details.get('formatted_phone_number', 'N/A')
            rating = place_details.get('rating', 'N/A')
            user_ratings_total = place_details.get('user_ratings_total', 'N/A')
            website = place_details.get('website', 'N/A')

            place_info = {
                'name': name,
                'address': address,
                'phone_number': phone_number,
                'rating': rating,
                'user_ratings_total': user_ratings_total,
                'website': website
            }

            places.append(place_info)

        # Check if there is a next page token
        next_page_token = places_result.get('next_page_token')
        if not next_page_token:
            break

        # Google API requires a short delay before requesting the next page
        time.sleep(2)

    return places

def write_to_excel(data, filename='places.xlsx'):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Define the headers
    headers = ['Name', 'Address', 'Phone Number', 'Rating', 'User Ratings Total', 'Website']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Write the data
    for row_num, place in enumerate(data, start=1):
        worksheet.write(row_num, 0, place['name'])
        worksheet.write(row_num, 1, place['address'])
        worksheet.write(row_num, 2, place['phone_number'])
        worksheet.write(row_num, 3, place['rating'])
        worksheet.write(row_num, 4, place['user_ratings_total'])
        worksheet.write(row_num, 5, place['website'])

    workbook.close()

def write_to_json(data, filename='places.json'):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    API_KEY = ''  # Add your Google Maps API key here

    # Define the location (latitude, longitude) for the given coordinates of Lahore
    LOCATION = (31.582045, 74.329376)

    # Specify the place type for beauty salons
    PLACE_TYPE = 'beauty_salon'
    # accounting, airport, amusement_park, aquarium, art_gallery, atm, bakery, bank, bar,
    # beauty_salon, bicycle_store, book_store, bowling_alley, bus_station, cafe, campground,
    # car_dealer, car_rental, car_repair, car_wash, casino, cemetery, church, city_hall,
    # clothing_store, convenience_store, courthouse, dentist, department_store, doctor, drugstore,
    # electrician, electronics_store, embassy, fire_station, florist, funeral_home, furniture_store,
    # gas_station, gym, hair_care, hardware_store, hindu_temple, home_goods_store, hospital,
    # insurance_agency, jewelry_store, laundry, lawyer, library, light_rail_station, liquor_store,
    # local_government_office, locksmith, lodging, meal_delivery, meal_takeaway, mosque, movie_rental,
    # movie_theater, moving_company, museum, night_club, painter, park, parking, pet_store,
    # pharmacy, physiotherapist, plumber, police, post_office, primary_school, real_estate_agency,
    # restaurant, roofing_contractor, rv_park, school, secondary_school, shoe_store, shopping_mall,
    # spa, stadium, storage, store, subway_station, supermarket, synagogue, taxi_stand,
    # tourist_attraction, train_station, transit_station, travel_agency, university, veterinary_care, zoo

    # Define a larger radius to cover the city
    RADIUS = 30000  # 30000 meters (30 kilometers)

    # Get the nearby places of the specified type within the defined radius
    nearby_places = get_nearby_places(api_key=API_KEY, location=LOCATION, radius=RADIUS, place_type=PLACE_TYPE)

    # Print the results
    for place in nearby_places:
        print(f"Name: {place['name']}")
        print(f"Address: {place['address']}")
        print(f"Phone Number: {place['phone_number']}")
        print(f"Rating: {place['rating']}")
        print(f"User Ratings Total: {place['user_ratings_total']}")
        print("-" * 40)

    # Write the results to an Excel file
    write_to_excel(nearby_places, filename='beauty_salons_Lahore.xlsx')

    # Write the results to a JSON file
    write_to_json(nearby_places, filename='beauty_salons_Lahore.json')
