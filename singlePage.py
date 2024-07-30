import googlemaps
import xlsxwriter
import time


def get_nearby_beauty_salons(api_key, location, radius=30000):
    gmaps = googlemaps.Client(key=api_key)

    # https://developers.google.com/maps/documentation/places/web-service/supported_types
    places_result = gmaps.places_nearby(location=location, radius=radius, type='beauty_salon')
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

    beauty_salon = []
    next_page_token = None


    while True:
        # Search for nearby places of the specified type
        places_result = gmaps.places_nearby(location=location, radius=radius, type='beauty_salon',
                                            page_token=next_page_token)

        for place in places_result['results']:
            place_id = place['place_id']
            place_details = gmaps.place(place_id=place_id)['result']
            name = place_details.get('name')
            address = place_details.get('formatted_address')
            phone_number = place_details.get('formatted_phone_number', 'N/A')
            website = place_details.get('website', 'N/A')

        beauty_salon_info = {
            'name': name,
            'address': address,
            'phone_number': phone_number,
            'website': website
        }

        # Check if there is a next page token
        next_page_token = places_result.get('next_page_token')
        if not next_page_token:
            break

        # Google API requires a short delay before requesting the next page
        time.sleep(2)

    return beauty_salon


def write_to_excel(data, filename='beauty_salon_Lahore.xlsx'):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Define the headers
    headers = ['Name', 'Address', 'Phone Number','Website']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Write the data
    for row_num, beauty_salon in enumerate(data, start=1):
        worksheet.write(row_num, 0, beauty_salon['name'])
        worksheet.write(row_num, 1, beauty_salon['address'])
        worksheet.write(row_num, 2, beauty_salon['phone_number'])
        worksheet.write(row_num, 3, beauty_salon['website'])

    workbook.close()


if __name__ == "__main__":
    API_KEY = ''

    LOCATION = (31.582045, 74.329376)

    nearby_beauty_salon = get_nearby_beauty_salons(api_key=API_KEY, location=LOCATION, radius=30000)

    # Print the results
    for beauty_salon in nearby_beauty_salon:
        print(f"Name: {beauty_salon['name']}")
        print(f"Address: {beauty_salon['address']}")
        print(f"Phone Number: {beauty_salon['phone_number']}")
        print(f"Website: {beauty_salon['website']}")
        print("-" * 40)

    write_to_excel(nearby_beauty_salon, filename='beauty_salon_Lahore.xlsx')

