import googlemaps
import xlsxwriter
import time


def get_nearby_places(api_key, location, radius=3000, place_type='hospital'):
    gmaps = googlemaps.Client(key=api_key)

    places = []
    next_page_token = None

    while True:
        places_result = gmaps.places_nearby(location=location, radius=radius, type=place_type,
                                            page_token=next_page_token)

        for place in places_result['results']:
            place_id = place['place_id']
            place_details = gmaps.place(place_id=place_id)['result']

            name = place_details.get('name')
            address = place_details.get('formatted_address')
            phone_number = place_details.get('formatted_phone_number', 'N/A')
            rating = place_details.get('rating', 'N/A')
            user_ratings_total = place_details.get('user_ratings_total', 'N/A')
            opening_hours = place_details.get('opening_hours', {}).get('weekday_text', 'N/A')
            website = place_details.get('website', 'N/A')

            place_info = {
                'name': name,
                'address': address,
                'phone_number': phone_number,
                'rating': rating,
                'user_ratings_total': user_ratings_total,
                'opening_hours': opening_hours,
                'website': website
            }

            places.append(place_info)

        next_page_token = places_result.get('next_page_token')
        if not next_page_token:
            break

        time.sleep(2)

    return places


def write_to_excel(data, filename='places.xlsx'):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    headers = ['Name', 'Address', 'Phone Number', 'Rating', 'User Ratings Total', 'Opening Hours', 'Website']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    for row_num, place in enumerate(data, start=1):
        worksheet.write(row_num, 0, place['name'])
        worksheet.write(row_num, 1, place['address'])
        worksheet.write(row_num, 2, place['phone_number'])
        worksheet.write(row_num, 3, place['rating'])
        worksheet.write(row_num, 4, place['user_ratings_total'])
        worksheet.write(row_num, 5,
                        ', '.join(place['opening_hours']) if isinstance(place['opening_hours'], list) else place[
                            'opening_hours'])
        worksheet.write(row_num, 6, place['website'])

    workbook.close()


def create_grid(center, radius, step):
    # Create a grid of coordinates around the center
    lat, lng = center
    coordinates = []
    for lat_offset in range(-radius, radius + 1, step):
        for lng_offset in range(-radius, radius + 1, step):
            coordinates.append((lat + (lat_offset * 0.0001), lng + (lng_offset * 0.0001)))
    return coordinates


if __name__ == "__main__":
    API_KEY = '' #Your API key within ''
    CENTER = (31.582045, 74.329376) #Location's longitude and Latitude
    PLACE_TYPE = 'hospital' #To be chosen from one below
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


    RADIUS = 3000  # Search radius for each cell in meters
    GRID_STEP = 3  # Number of steps for grid

    grid_coordinates = create_grid(CENTER, 10, GRID_STEP)

    all_places = []

    for coord in grid_coordinates:
        places = get_nearby_places(api_key=API_KEY, location=coord, radius=RADIUS, place_type=PLACE_TYPE)
        all_places.extend(places)
        print(f"Fetched {len(places)} places from location {coord}")

    # Remove duplicates
    unique_places = {place['name']: place for place in all_places}.values()

    write_to_excel(unique_places, filename='Hospitals_in_Lahore_Pakistan.xlsx')
