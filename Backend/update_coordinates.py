import requests
from models import db, Clinic
from app import app

def get_coordinates(location, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

# Simplified locations
locations = [
    "Clinique Ezzahra, Rue Abu El Kacem Ezzahraoui, Ezzahra, Tunisia",
    "Clinique Hannibal, Rue de la feuille d'Erable, Tunis, Tunisia",
    "Clinique Avicenne, 4 Rue Mohamed El Heni, Tunis, Tunisia",
    "Polyclinique Les Jasmins, Centre Urbain Nord, Tunis, Tunisie",
    "Clinique Carthagène, Tunis, Tunisia",
    "Clinique La Rose, Rue De La Bourse, Tunis, Tunisia",
    "Polyclinique Les Berges Du Lac, Les Berges Du Lac Rue Du Lac De Constance, Tunis, Tunis Governorate, Tunisie",
    "Clinique Amen Mutuelleville, 20 Rue Aziza Othmana, Tunis, Éthiopie",
    "Clinique Internationale les Narcisses, 2001 Ariana, Tunisie",
    "SOCIETE NUTRIS CLINIQUE PASTEUR, CENTRE URBAIN NORD, EL MENZAH, Tunisia",
    "Clinique La Corniche Sousse, 1 Boulevard Mongi Bali, Sousse, Tunisie",
    "CLINIQUE LA MARSA, 15 AVENUE DE LA REPUBLIQUE, La Marsa, Tunisia",
    "clinique le bardo, Tunis, Tunisia",
    "Clinique Saint Augustin, Rue Abou Hanifa, Tunis, Tunisia",
    "Polyclinique l'Excellence, Avenue Taieb Mhiri, Mahdia, Tunisia",
    "Centre International Carthage Médical, Zone Touristique JINEN EL OUEST, Monastir, Tunisia"
]

api_key = "AIzaSyDc1L2y7OnZgKqukCC4rcUMevlmWoIA9Yc"

app.app_context().push()

for location in locations:
    latitude, longitude = get_coordinates(location, api_key)
    if latitude and longitude:
        print(f"Location: {location}")
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        print(f"Google Maps Link: https://www.google.com/maps/search/?api=1&query={latitude},{longitude}")
        
        # Update the clinic in the database
        clinic = Clinic.query.filter_by(location=location).first()
        if clinic:
            clinic.latitude = latitude
            clinic.longitude = longitude
            db.session.commit()
    else:
        print(f"Failed to get coordinates for location: {location}")