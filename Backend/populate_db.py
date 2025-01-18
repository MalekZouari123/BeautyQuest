from models import db, Clinic, Procedure, ClinicProcedure
from app import app

app.app_context().push()
db.create_all()

# Create procedures with a default price range
rhinoplasty = Procedure(name="Rhinoplasty (Nose Reshaping)", price_range="$$$")
blepharoplasty = Procedure(name="Blepharoplasty (Eyelid Surgery)", price_range="$$")
facelift = Procedure(name="Facelift (Rhytidectomy)", price_range="$$$")
brow_lift = Procedure(name="Brow Lift (Forehead Lift)", price_range="$$")
chin_augmentation = Procedure(name="Chin Augmentation", price_range="$$")
cheek_augmentation = Procedure(name="Cheek Augmentation", price_range="$$")
lip_augmentation = Procedure(name="Lip Augmentation", price_range="$$")
ear_surgery = Procedure(name="Ear Surgery (Otoplasty)", price_range="$$")

db.session.add_all([rhinoplasty, blepharoplasty, facelift, brow_lift, chin_augmentation, cheek_augmentation, lip_augmentation, ear_surgery])
db.session.commit()

# Create clinics with photos and locations
clinics = [
    Clinic(name="Clinic Ezzahra", location="Clinique Ezzahra, Rue Abu El Kacem Ezzahraoui, Ezzahra, Tunisia", price_range="$$$", rating=4.7, photo_url="https://th.bing.com/th/id/OIP.z3DO39zmPeukt8Bx-UudyAHaFO?w=217&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7",url="https://www.taoufikhospitalsgroup.com/clinique-ezzahra/", latitude=36.7485, longitude=10.2745),
    
    Clinic(name="Clinique Internationale Hannibal", location="Clinique Hannibal, Rue de la feuille d'Erable, Tunis, Tunisia", price_range="$$$", rating=4.3, photo_url="https://th.bing.com/th/id/OIP.45j2J08qjE3woBkJqB994QHaDX?w=311&h=159&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://www.taoufikhospitalsgroup.com/clinique-hannibal/", latitude=36.8065, longitude=10.1815),
    Clinic(name="Clinique Avicennes", location="Clinique Avicenne, 4 Rue Mohamed El Heni, Tunis, Tunisia", price_range="$$", rating=4.2, photo_url="https://th.bing.com/th/id/OIP.71piTGJAdIVFGnlOLzSemgHaE8?w=190&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://www.cliniqueavicenne.com/", latitude=36.8065, longitude=10.1815),
    Clinic(name="Cliniques les Jasmins", location="Polyclinique Les Jasmins, Centre Urbain Nord, Tunis, Tunisie", price_range="$$", rating=4.1, photo_url="https://th.bing.com/th/id/OIP.FrHrTpUGO139uBMJnE_HVwHaDp?w=346&h=172&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://polycliniquelesjasmins.com/", latitude=36.8065, longitude=10.1815),
    Clinic(name="Clinique Carthagène", location="Clinique Carthagène, Tunis, Tunisia", price_range="$$", rating=4.0, photo_url="https://th.bing.com/th/id/OIP.ddUHBvF-xcCqzoFA1BCYpwAAAA?w=184&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://www.carthagene.tn/", latitude=36.8065, longitude=10.1815),
    Clinic(name="Clinique La Rose", location="Clinique La Rose, Rue De La Bourse, Tunis, Tunisia", price_range="$$$", rating=4.5, photo_url="https://th.bing.com/th/id/OIP.YAZxbaJ2HRQtq7i5ABjUXgHaEW?w=252&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://clinique-larose.com/", latitude=36.8065, longitude=10.1815),
    Clinic(name="Clinique du Lac", location="Polyclinique Les Berges Du Lac, Les Berges Du Lac Rue Du Lac De Constance, Tunis, Tunis Governorate, Tunisie", price_range="$$$", rating=4.4, photo_url="https://th.bing.com/th/id/OIP.1vJ7NUF3H5D4cT2Na8EregHaE8?w=291&h=194&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="http://www.polyclinique-lac.com/", latitude=36.8065, longitude=10.1815),
    Clinic(name="Clinique El Amen", location="Clinique Amen Mutuelleville, 20 Rue Aziza Othmana, Tunis, Éthiopie", price_range="$$", rating=4.3, photo_url="https://th.bing.com/th/id/OIP.4O_EKOSLaZ7nj42HKAGh_gAAAA?w=215&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://mutuelleville.amensante.com/Fr/", latitude=36.8065, longitude=10.1815),
    Clinic(name="Clinique Les Narcisses", location="Clinique Internationale les Narcisses, 2001 Ariana, Tunisie", price_range="$$", rating=4.0, photo_url="https://th.bing.com/th/id/OIP.biZI2RaSqxD7LLlEO5Y0UgAAAA?w=208&h=119&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://www.facebook.com/Clinique.les.Narcisses/", latitude=36.8065, longitude=10.1815),
    Clinic(name="Clinique Pasteur", location="SOCIETE NUTRIS CLINIQUE PASTEUR,,CENTRE URBAIN NORD, EL MENZAH, Tunisia", price_range="$$$", rating=4.0, photo_url="https://th.bing.com/th/id/OIP.T0MMTDsrKoOz770FOsbn4AHaDP?w=332&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://www.cliniquepasteurtunis.com.tn/", latitude=36.8065, longitude=10.1815),
    Clinic(name="CLINIQUE DE LA SOUKRA", location="Rue Cheikh Mohamed Enneifer, Tunis, Tunis 2036", price_range="$$", rating=4.1, photo_url="https://www.taoufikhospitalsgroup.com/clinique-soukra/contact/", latitude=36.8065, longitude=10.1815),
    
    Clinic(name="Clinique La Corniche", location="Clinique La Corniche Sousse, 1 Boulevard Mongi Bali, Sousse, Tunisie", price_range="$$", rating=4.0, photo_url="https://th.bing.com/th/id/OIP.w_LfNzV-55ZSkEzQzBbvVAHaDa?w=330&h=161&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="http://www.clinique-lacorniche.com/", latitude=35.8256, longitude=10.6369),
    Clinic(name="CLINIQUE LA MARSA", location="CLINIQUE LA MARSA, 15 AVENUE DE LA REPUBLIQUE, La Marsa, Tunisia", price_range="$$$", rating=4.3, photo_url="https://th.bing.com/th/id/OIP.fItYPxI7d8olkbp9paIoewHaEj?w=292&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://marsa.amensante.com/Fr/", latitude=36.8781, longitude=10.3244),
    Clinic(name="clinique le bardo", location="clinique le bardo, Tunis, Tunisia", price_range="$$", rating=4.1, photo_url="https://th.bing.com/th/id/OIP.Ci3__bCXuXEmsOafVES7TwHaEK?w=291&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://www.clinibardo.tn/", latitude=36.8065, longitude=10.1815),
    Clinic(name="Clinique Saint Augustin", location="Clinique Saint Augustin, Rue Abou Hanifa, Tunis, Tunisia", price_range="$$", rating=4.0, photo_url="https://th.bing.com/th/id/OIP.y9dme8GfCee5qPC3x8l6KgHaEJ?w=307&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://clinique-saint-augustin.com/", latitude=36.8065, longitude=10.1815),
    Clinic(name="Polyclinique L'Excellence", location="Polyclinique l'Excellence, Avenue Taieb Mhiri, Mahdia, Tunisia", price_range="$$", rating=4.0, photo_url="https://th.bing.com/th/id/OIP.hy2-CifsFTUsjUCAITOSngAAAA?w=206&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://polyclinique-excellence.com/", latitude=35.5047, longitude=11.0622),
    Clinic(name="Centre International Carthage Medical", location="Centre International Carthage Médical, Zone Touristique JINEN EL OUEST, Monastir, Tunisia", price_range="$$", rating=3.8, photo_url="https://th.bing.com/th/id/OIP.hU6MXVC9pRIMv6VstkUWYwHaEL?w=290&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7", url="https://carthagemedical.com.tn/", latitude=35.7770, longitude=10.8262)
]

db.session.add_all(clinics)
db.session.commit()

# Associate procedures with clinics
for clinic in clinics:
    clinic.procedures.extend([rhinoplasty, blepharoplasty, facelift, brow_lift, chin_augmentation, cheek_augmentation, lip_augmentation, ear_surgery])

db.session.commit()