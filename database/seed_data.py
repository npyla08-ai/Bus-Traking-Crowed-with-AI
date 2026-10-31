import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "vizag_bus.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Run schema.sql to recreate clean tables
    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())

    # =========================================================================
    # 2. EXTENSIVE VIZAG BUS STOPS (72 major stops covering all zones & suburbs)
    # =========================================================================
    stops_data = [
        # Central Vizag & Coastal
        ("RTC Complex (Dwaraka Nagar)", 17.7265, 83.3073, "Central Vizag", "APSRTC Central Bus Terminal"),
        ("Siripuram Junction", 17.7205, 83.3168, "Central Vizag", "Near RTIH & AU Ingate"),
        ("Maddilapalem", 17.7384, 83.3289, "Central Vizag", "BRTS Terminal & AU Engineering"),
        ("MVP Colony Circle", 17.7412, 83.3375, "Central Vizag", "Sector 3 MVP Circle"),
        ("Ushodaya Junction", 17.7440, 83.3340, "Central Vizag", "MVP Main Road"),
        ("Jagadamba Junction", 17.7121, 83.3015, "Old City & Commercial", "Cinema & Shopping Center"),
        ("Visakhapatnam Railway Station", 17.7224, 83.2922, "Central Vizag", "Main Junction Railway Station"),
        ("Town Kotharoad", 17.6970, 83.2990, "Old City", "Old Post Office & Port Area"),
        ("Collector Office", 17.7080, 83.3080, "Central Vizag", "District Collectorate & Police Barracks"),
        ("Waltair Uplands", 17.7270, 83.3210, "Central Vizag", "AU North Gate & Medical Area"),
        ("Andhra University", 17.7310, 83.3250, "Central Vizag", "AU North Campus Main Gate"),
        ("Gurudwara Junction", 17.7315, 83.3005, "Central Vizag", "City Central Junction"),
        ("Satyam Junction", 17.7350, 83.3080, "Central Vizag", "Near Rama Talkies & Maddilapalem"),
        ("Seethammadhara", 17.7410, 83.3130, "Central Vizag", "North Central Residential Area"),
        ("Venkojipalem", 17.7490, 83.3380, "North Corridor", "NH16 Zoo Road Junction"),
        ("Hanumanthawaka Junction", 17.7600, 83.3420, "North Corridor", "Major BRTS Transit Hub"),
        ("Arilova / Health City", 17.7690, 83.3270, "North Suburbs", "VIMS & Apollo Health City"),
        ("Zoo Park Stop", 17.7670, 83.3450, "North Corridor", "Indira Gandhi Zoological Park"),
        ("Pothinamallayya Palem", 17.8010, 83.3510, "North Suburbs", "PM Palem Terminal"),
        ("ACA-VDCA Cricket Stadium", 17.7980, 83.3530, "North Suburbs", "PM Palem International Stadium"),
        ("Car Shed Junction", 17.8100, 83.3520, "North Suburbs", "Madhurawada Entrance"),
        ("Madhurawada", 17.8170, 83.3530, "North Suburbs", "IT & Educational Hub"),
        ("Kommadi Junction", 17.8340, 83.3560, "North Suburbs", "Gayatri College Junction"),
        ("Marikavalasa", 17.8520, 83.3620, "North Suburbs", "NH16 North Suburb"),
        ("Anandapuram Junction", 17.9050, 83.3980, "Suburban North", "Highway Intersection"),
        ("Tagarapuvalasa", 17.9300, 83.4280, "Suburban North", "Vizag-Vizianagaram Highway"),

        # Beach Road & Suburbs
        ("RK Beach", 17.7142, 83.3239, "Beach Road", "Submarine Museum & Beach Front"),
        ("Pandurangapuram", 17.7130, 83.3180, "Beach Road", "Near Coastal Battery"),
        ("Sagar Nagar", 17.7650, 83.3600, "Beach Road", "Beach Road Scenic Junction"),
        ("Rushikonda Beach Stop", 17.7816, 83.3831, "Beach Road", "Rushikonda Blue Flag Beach"),
        ("GITAM University", 17.7820, 83.3770, "Beach Road", "Main Campus Entrance"),
        ("IT SEZ (Rushikonda Hills)", 17.7910, 83.3880, "Beach Road", "Millennium Tower IT Park"),
        ("Mangamaripeta", 17.8130, 83.4150, "Beach Road", "Thotlakonda Beach Road"),
        ("INS Kalinga", 17.8380, 83.4350, "Beach Road", "Naval Base & Coastal Road"),
        ("Bheemunipatnam Bus Stand", 17.8920, 83.4540, "Bheemili Suburb", "Historic Bheemili Terminal"),

        # South Industrial Corridor & Highway (NH16)
        ("Kancharapalem", 17.7330, 83.2660, "South Corridor", "Urdu Junior College / Kancharapalem"),
        ("Urvasi Junction", 17.7370, 83.2560, "South Corridor", "Kancharapalem Highway Junction"),
        ("Marripalem", 17.7410, 83.2450, "South Corridor", "Railway Quarters & NH16"),
        ("NAD Junction", 17.7447, 83.2319, "Major Transit Hub", "NAD Double Flyover Hub"),
        ("Visakhapatnam Airport", 17.7225, 83.2245, "South Corridor", "International Airport Terminal"),
        ("Sheela Nagar", 17.7095, 83.2045, "Industrial South", "Near Port Connectivity Road"),
        ("BHPV Junction", 17.7032, 83.1950, "Industrial South", "Heavy Plates Engineering Unit"),
        ("Autonagar Gate", 17.6970, 83.2020, "Industrial South", "Industrial Estate Gate"),
        ("Gajuwaka Junction", 17.6904, 83.2095, "Industrial South", "Gajuwaka Commercial Center"),
        ("Old Gajuwaka", 17.6880, 83.2140, "Industrial South", "Market Road Bus Stop"),
        ("New Gajuwaka", 17.6920, 83.2050, "Industrial South", "Gajuwaka RTC Depot Hub"),
        ("Sriharipuram", 17.6880, 83.2350, "Port Corridor", "Industrial Suburb"),
        ("Coromandel Gate", 17.6850, 83.2480, "Port Corridor", "Coromandel Plant"),
        ("Malkapuram", 17.6870, 83.2620, "Port Corridor", "HPCL Refinery Gate"),
        ("Scindia Junction", 17.6910, 83.2770, "Port Corridor", "Hindustan Shipyard Entrance"),
        ("Naval Dockyard", 17.6990, 83.2870, "Port Corridor", "INHS Kalyani & Port Gate"),
        ("Kurmannapalem Junction", 17.6850, 83.1670, "Industrial South", "Steel Plant Highway Junction"),
        ("Steel Plant Main Gate", 17.6650, 83.1600, "Ukkunagaram", "RINL Visakhapatnam Steel Plant"),
        ("Steel Plant Township Sector 6", 17.6480, 83.1680, "Ukkunagaram", "Ukkunagaram Central Township"),
        ("Duvvada Railway Station", 17.7050, 83.1550, "South Suburb", "Major Express Train Station"),
        ("Desapatrunipalem", 17.6400, 83.1250, "South Suburb", "Steel Plant Outskirts"),
        ("Parawada Junction", 17.6200, 83.0850, "Industrial South", "Pharma City Entrance"),
        ("NTPC Simhadri Gate", 17.6020, 83.0700, "Industrial South", "NTPC Thermal Power Station"),
        ("Atchutapuram", 17.5500, 82.9900, "Industrial SEZ", "APSEZ & Multi-Product SEZ"),
        ("Lankelapalem Junction", 17.6600, 83.1000, "South Highway", "NH16 Junction to Anakapalle"),
        ("Anakapalle RTC Complex", 17.6900, 83.0030, "Anakapalle Suburb", "Anakapalle Major Transit Hub"),

        # West Vizag / Simhachalam / Pendurthi / Kothavalasa
        ("Gopalapatnam", 17.7563, 83.2185, "West Transit Hub", "Gopalapatnam Petrol Bunk"),
        ("Simhachalam Foothills", 17.7660, 83.2420, "Simhachalam", "Varaha Narasimha Temple Foothills"),
        ("Simhachalam Temple", 17.7680, 83.2500, "Simhachalam", "Hill Top Temple Complex"),
        ("Vepagunta Junction", 17.7710, 83.2110, "West Suburbs", "BRTS West Hub"),
        ("Sujatha Nagar", 17.7800, 83.2080, "West Suburbs", "Residential Suburb Stop"),
        ("Chintalagraharam", 17.7950, 83.2020, "West Suburbs", "Pendurthi Highway Stop"),
        ("Pendurthi Junction", 17.8220, 83.2010, "West Transit Hub", "Pendurthi Railway & Market Hub"),
        ("Sabbavaram Junction", 17.7850, 83.1250, "West Suburbs", "DSNLU & Maritime University"),
        ("Kothavalasa", 17.9000, 83.1900, "Suburban West", "Kothavalasa Junction Terminal")
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO bus_stops (stop_name, lat, lng, area, landmark) VALUES (?, ?, ?, ?, ?)",
        stops_data
    )

    # =========================================================================
    # 3. COMPREHENSIVE BUS ROUTES MASTER (30 Popular Visakhapatnam Bus Lines)
    # =========================================================================
    routes_data = [
        # 1. 400K
        ("400K", "Gajuwaka to Maddilapalem Express", "Gajuwaka Junction", "Maddilapalem",
         "Via Airport, NAD Junction, RTC Complex, Siripuram", "Metro Express", 8, "05:00 AM", "11:30 PM", 10, 30, 12),
        # 2. 400
        ("400", "Kurmannapalem to Maddilapalem", "Kurmannapalem Junction", "Maddilapalem",
         "Via Gajuwaka, NAD Junction, Gurudwara, Siripuram", "City Ordinary", 15, "05:30 AM", "10:45 PM", 10, 35, 10),
        # 3. 400H
        ("400H", "Steel Plant to Maddilapalem", "Steel Plant Main Gate", "Maddilapalem",
         "Via Kurmannapalem, Gajuwaka, Airport, Railway Station, RTC Complex", "Metro Express", 20, "06:00 AM", "10:15 PM", 15, 40, 9),
        # 4. 400Y
        ("400Y", "Anakapalle to RTC Complex Express", "Anakapalle RTC Complex", "RTC Complex (Dwaraka Nagar)",
         "Via Lankelapalem, Kurmannapalem, Gajuwaka, NAD, Kancharapalem", "Metro Express", 12, "05:00 AM", "11:00 PM", 15, 45, 10),
        # 5. 900K
        ("900K", "RTC Complex to Bheemili Beach Road", "RTC Complex (Dwaraka Nagar)", "Bheemunipatnam Bus Stand",
         "Via Siripuram, Maddilapalem, MVP Colony, Rushikonda, GITAM, IT SEZ", "Metro Express", 10, "05:30 AM", "10:30 PM", 10, 40, 11),
        # 6. 900T
        ("900T", "RTC Complex to Rushikonda IT SEZ", "RTC Complex (Dwaraka Nagar)", "IT SEZ (Rushikonda Hills)",
         "Via Siripuram, Maddilapalem, MVP Colony, Sagar Nagar, Rushikonda Beach", "City Sheetal AC", 15, "06:00 AM", "09:45 PM", 15, 35, 9),
        # 7. 900
        ("900", "Railway Station to Bheemunipatnam", "Visakhapatnam Railway Station", "Bheemunipatnam Bus Stand",
         "Via Jagadamba, RTC Complex, Siripuram, Maddilapalem, Rushikonda", "City Ordinary", 25, "06:15 AM", "09:30 PM", 10, 40, 9),
        # 8. 28A
        ("28A", "RK Beach to Simhachalam Foothills", "RK Beach", "Simhachalam Foothills",
         "Via Jagadamba, RTC Complex, Gurudwara, NAD Junction, Gopalapatnam", "Metro Express", 10, "05:15 AM", "11:00 PM", 10, 25, 11),
        # 9. 28
        ("28", "RK Beach to Pendurthi Junction", "RK Beach", "Pendurthi Junction",
         "Via Jagadamba, RTC Complex, NAD, Gopalapatnam, Vepagunta, Sujatha Nagar", "City Ordinary", 12, "05:30 AM", "10:30 PM", 10, 30, 9),
        # 10. 28K
        ("28K", "Town Kotharoad to Kothavalasa", "Town Kotharoad", "Kothavalasa",
         "Via Jagadamba, RTC Complex, NAD, Simhachalam, Pendurthi", "City Ordinary", 25, "05:45 AM", "09:30 PM", 10, 40, 9),
        # 11. 38
        ("38", "Kurmannapalem to Siripuram Junction", "Kurmannapalem Junction", "Siripuram Junction",
         "Via Gajuwaka, Airport, NAD Junction, Urvasi, Railway Station, RTC Complex", "Metro Express", 10, "05:30 AM", "11:00 PM", 10, 30, 11),
        # 12. 38K
        ("38K", "Duvvada Railway Station to RTC Complex", "Duvvada Railway Station", "RTC Complex (Dwaraka Nagar)",
         "Via Kurmannapalem, Gajuwaka, Airport, NAD, Gurudwara", "Metro Express", 15, "05:00 AM", "11:15 PM", 10, 25, 7),
        # 13. 38A
        ("38A", "Steel Plant Sector 6 to Siripuram", "Steel Plant Township Sector 6", "Siripuram Junction",
         "Via Steel Plant Main Gate, Kurmannapalem, Gajuwaka, NAD, RTC Complex", "Metro Express", 20, "06:00 AM", "10:00 PM", 10, 35, 8),
        # 14. 38H
        ("38H", "Gajuwaka to Maddilapalem via Scindia", "Gajuwaka Junction", "Maddilapalem",
         "Via Sriharipuram, Malkapuram, Scindia, Dockyard, Kotharoad, Jagadamba, RTC Complex", "City Ordinary", 20, "05:30 AM", "10:00 PM", 10, 30, 9),
        # 15. 500
        ("500", "RTC Complex to Anandapuram via Pendurthi", "RTC Complex (Dwaraka Nagar)", "Anandapuram Junction",
         "Via Gurudwara, NAD Junction, Gopalapatnam, Vepagunta, Pendurthi", "Metro Express", 15, "05:30 AM", "10:00 PM", 10, 35, 7),
        # 16. 500A
        ("500A", "Railway Station to Pendurthi Junction", "Visakhapatnam Railway Station", "Pendurthi Junction",
         "Via RTC Complex, Kancharapalem, NAD, Gopalapatnam, Vepagunta", "City Ordinary", 18, "06:00 AM", "10:00 PM", 10, 25, 7),
        # 17. 500D
        ("500D", "Maddilapalem to Pendurthi BRTS", "Maddilapalem", "Pendurthi Junction",
         "Via Satyam Junction, Gurudwara, NAD, Gopalapatnam, Sujatha Nagar", "Metro Express", 15, "05:45 AM", "10:15 PM", 10, 30, 8),
        # 18. 60
        ("60", "Simhachalam Foothills to Town Kotharoad", "Simhachalam Foothills", "Town Kotharoad",
         "Via Gopalapatnam, NAD, Urvasi, Kancharapalem, Railway Station, Jagadamba", "City Ordinary", 15, "05:30 AM", "10:30 PM", 10, 25, 9),
        # 19. 60C
        ("60C", "Simhachalam Foothills to RK Beach", "Simhachalam Foothills", "RK Beach",
         "Via Gopalapatnam, NAD Junction, Kancharapalem, RTC Complex, Jagadamba", "Metro Express", 15, "06:00 AM", "10:00 PM", 10, 25, 8),
        # 20. 10K
        ("10K", "Town Kotharoad to Gopalapatnam", "Town Kotharoad", "Gopalapatnam",
         "Via Jagadamba, RTC Complex, Gurudwara, Marripalem, NAD Junction", "City Ordinary", 12, "05:30 AM", "10:45 PM", 10, 20, 7),
        # 21. 222
        ("222", "RTC Complex to Tagarapuvalasa Highway", "RTC Complex (Dwaraka Nagar)", "Tagarapuvalasa",
         "Via Maddilapalem, Hanumanthawaka, PM Palem, Madhurawada, Kommadi, Anandapuram", "Metro Express", 10, "05:00 AM", "11:00 PM", 10, 40, 12),
        # 22. 222V
        ("222V", "Railway Station to Tagarapuvalasa", "Visakhapatnam Railway Station", "Tagarapuvalasa",
         "Via RTC Complex, Maddilapalem, Hanumanthawaka, Madhurawada, Anandapuram", "City Ordinary", 25, "06:00 AM", "09:30 PM", 10, 40, 7),
        # 23. 55
        ("55", "Scindia to Simhachalam Foothills", "Scindia Junction", "Simhachalam Foothills",
         "Via Malkapuram, Sriharipuram, Gajuwaka, Sheela Nagar, NAD, Gopalapatnam", "Metro Express", 20, "05:45 AM", "10:00 PM", 10, 30, 10),
        # 24. 55K
        ("55K", "Scindia to Kothavalasa", "Scindia Junction", "Kothavalasa",
         "Via Sriharipuram, Gajuwaka, NAD, Gopalapatnam, Vepagunta, Pendurthi", "City Ordinary", 30, "06:00 AM", "09:00 PM", 10, 45, 8),
        # 25. 68
        ("68", "RTC Complex to Sabbavaram Junction", "RTC Complex (Dwaraka Nagar)", "Sabbavaram Junction",
         "Via NAD, Gopalapatnam, Vepagunta, Pendurthi Junction, Sabbavaram", "City Ordinary", 30, "06:30 AM", "09:15 PM", 15, 35, 6),
        # 26. 88K
        ("88K", "Maddilapalem to Atchutapuram SEZ", "Maddilapalem", "Atchutapuram",
         "Via Siripuram, RTC Complex, NAD, Gajuwaka, Kurmannapalem, Parawada, NTPC", "Metro Express", 20, "05:30 AM", "10:00 PM", 20, 50, 10),
        # 27. 99K
        ("99K", "Town Kotharoad to Bheemili Coastal Route", "Town Kotharoad", "Bheemunipatnam Bus Stand",
         "Via Collector Office, RK Beach, Sagar Nagar, Rushikonda, GITAM", "City Ordinary", 20, "06:00 AM", "09:30 PM", 10, 35, 8),
        # 28. 111
        ("111", "Kurmannapalem to Madhurawada Car Shed", "Kurmannapalem Junction", "Car Shed Junction",
         "Via Gajuwaka, Airport, NAD, Gurudwara, Maddilapalem, Hanumanthawaka, PM Palem, Madhurawada", "Metro Express", 15, "05:30 AM", "10:30 PM", 15, 40, 10),
        # 29. 211
        ("211", "Railway Station to Health City / VIMS", "Visakhapatnam Railway Station", "Arilova / Health City",
         "Via RTC Complex, Gurudwara, Seethammadhara, Hanumanthawaka", "City Ordinary", 20, "06:15 AM", "10:00 PM", 10, 25, 6),
        # 30. 541
        ("541", "Maddilapalem to Kothavalasa Express", "Maddilapalem", "Kothavalasa",
         "Via Gurudwara, NAD Junction, Gopalapatnam, Vepagunta, Pendurthi", "Metro Express", 25, "06:00 AM", "09:30 PM", 15, 40, 7)
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO bus_routes
        (bus_number, route_name, source, destination, via, bus_type, frequency_mins, first_bus_time, last_bus_time, fare_min, fare_max, total_stops)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, routes_data)

    # =========================================================================
    # 4. ROUTE STOPS (Ordered sequence of stops for each bus number)
    # =========================================================================
    route_stops_map = {
        "400K": [
            ("Gajuwaka Junction", 0.0, 0),
            ("Autonagar Gate", 1.8, 4),
            ("BHPV Junction", 3.2, 7),
            ("Sheela Nagar", 5.0, 11),
            ("Visakhapatnam Airport", 7.5, 16),
            ("NAD Junction", 10.8, 22),
            ("Marripalem", 12.3, 26),
            ("Urvasi Junction", 14.0, 30),
            ("Kancharapalem", 15.5, 34),
            ("RTC Complex (Dwaraka Nagar)", 18.2, 42),
            ("Siripuram Junction", 20.0, 47),
            ("Maddilapalem", 22.5, 54)
        ],
        "400": [
            ("Kurmannapalem Junction", 0.0, 0),
            ("Gajuwaka Junction", 4.2, 9),
            ("BHPV Junction", 7.4, 16),
            ("Sheela Nagar", 9.2, 20),
            ("Visakhapatnam Airport", 11.7, 26),
            ("NAD Junction", 15.0, 33),
            ("Gurudwara Junction", 19.5, 43),
            ("RTC Complex (Dwaraka Nagar)", 21.0, 48),
            ("Siripuram Junction", 22.8, 53),
            ("Maddilapalem", 25.3, 60)
        ],
        "400H": [
            ("Steel Plant Main Gate", 0.0, 0),
            ("Kurmannapalem Junction", 3.5, 8),
            ("Gajuwaka Junction", 7.7, 18),
            ("Visakhapatnam Airport", 15.2, 33),
            ("NAD Junction", 18.5, 41),
            ("Kancharapalem", 23.2, 51),
            ("Visakhapatnam Railway Station", 25.5, 57),
            ("RTC Complex (Dwaraka Nagar)", 27.2, 62),
            ("Maddilapalem", 30.0, 70)
        ],
        "400Y": [
            ("Anakapalle RTC Complex", 0.0, 0),
            ("Lankelapalem Junction", 9.5, 16),
            ("Kurmannapalem Junction", 18.0, 30),
            ("Gajuwaka Junction", 22.2, 39),
            ("Sheela Nagar", 27.2, 49),
            ("Visakhapatnam Airport", 29.7, 55),
            ("NAD Junction", 33.0, 62),
            ("Urvasi Junction", 36.2, 69),
            ("Kancharapalem", 37.7, 73),
            ("RTC Complex (Dwaraka Nagar)", 40.5, 80)
        ],
        "900K": [
            ("RTC Complex (Dwaraka Nagar)", 0.0, 0),
            ("Siripuram Junction", 1.8, 5),
            ("Maddilapalem", 4.3, 12),
            ("MVP Colony Circle", 6.2, 17),
            ("Sagar Nagar", 11.0, 27),
            ("Rushikonda Beach Stop", 14.5, 34),
            ("GITAM University", 15.2, 36),
            ("IT SEZ (Rushikonda Hills)", 17.0, 40),
            ("Mangamaripeta", 21.0, 48),
            ("INS Kalinga", 24.5, 55),
            ("Bheemunipatnam Bus Stand", 31.0, 70)
        ],
        "900T": [
            ("RTC Complex (Dwaraka Nagar)", 0.0, 0),
            ("Siripuram Junction", 1.8, 5),
            ("Maddilapalem", 4.3, 12),
            ("MVP Colony Circle", 6.2, 17),
            ("Ushodaya Junction", 7.0, 19),
            ("Sagar Nagar", 11.0, 27),
            ("Rushikonda Beach Stop", 14.5, 34),
            ("GITAM University", 15.2, 36),
            ("IT SEZ (Rushikonda Hills)", 17.0, 41)
        ],
        "900": [
            ("Visakhapatnam Railway Station", 0.0, 0),
            ("Jagadamba Junction", 1.5, 5),
            ("RTC Complex (Dwaraka Nagar)", 3.2, 10),
            ("Siripuram Junction", 5.0, 15),
            ("Maddilapalem", 7.5, 22),
            ("MVP Colony Circle", 9.4, 27),
            ("Sagar Nagar", 14.2, 37),
            ("Rushikonda Beach Stop", 17.7, 44),
            ("Bheemunipatnam Bus Stand", 34.2, 80)
        ],
        "28A": [
            ("RK Beach", 0.0, 0),
            ("Pandurangapuram", 1.2, 4),
            ("Jagadamba Junction", 2.8, 8),
            ("RTC Complex (Dwaraka Nagar)", 4.5, 13),
            ("Gurudwara Junction", 6.0, 18),
            ("Kancharapalem", 9.0, 26),
            ("Urvasi Junction", 10.5, 30),
            ("Marripalem", 12.2, 34),
            ("NAD Junction", 13.8, 38),
            ("Gopalapatnam", 16.0, 44),
            ("Simhachalam Foothills", 18.5, 52)
        ],
        "28": [
            ("RK Beach", 0.0, 0),
            ("Jagadamba Junction", 2.8, 8),
            ("RTC Complex (Dwaraka Nagar)", 4.5, 13),
            ("Gurudwara Junction", 6.0, 18),
            ("NAD Junction", 13.8, 38),
            ("Gopalapatnam", 16.0, 44),
            ("Vepagunta Junction", 18.5, 50),
            ("Sujatha Nagar", 20.0, 54),
            ("Pendurthi Junction", 24.0, 64)
        ],
        "28K": [
            ("Town Kotharoad", 0.0, 0),
            ("Jagadamba Junction", 1.6, 5),
            ("RTC Complex (Dwaraka Nagar)", 3.3, 10),
            ("NAD Junction", 12.6, 33),
            ("Gopalapatnam", 14.8, 39),
            ("Simhachalam Foothills", 17.3, 47),
            ("Vepagunta Junction", 19.8, 53),
            ("Pendurthi Junction", 25.3, 67),
            ("Kothavalasa", 35.0, 90)
        ],
        "38": [
            ("Kurmannapalem Junction", 0.0, 0),
            ("Gajuwaka Junction", 4.2, 9),
            ("BHPV Junction", 7.4, 16),
            ("Sheela Nagar", 9.2, 20),
            ("Visakhapatnam Airport", 11.7, 26),
            ("NAD Junction", 15.0, 33),
            ("Urvasi Junction", 18.2, 41),
            ("Kancharapalem", 19.7, 45),
            ("Visakhapatnam Railway Station", 22.0, 51),
            ("RTC Complex (Dwaraka Nagar)", 23.7, 56),
            ("Siripuram Junction", 25.5, 62)
        ],
        "38K": [
            ("Duvvada Railway Station", 0.0, 0),
            ("Kurmannapalem Junction", 3.0, 7),
            ("Gajuwaka Junction", 7.2, 16),
            ("Sheela Nagar", 12.2, 27),
            ("Visakhapatnam Airport", 14.7, 33),
            ("NAD Junction", 18.0, 40),
            ("Gurudwara Junction", 22.5, 50),
            ("RTC Complex (Dwaraka Nagar)", 24.0, 55)
        ],
        "38A": [
            ("Steel Plant Township Sector 6", 0.0, 0),
            ("Steel Plant Main Gate", 2.2, 5),
            ("Kurmannapalem Junction", 5.7, 13),
            ("Gajuwaka Junction", 9.9, 22),
            ("Sheela Nagar", 14.9, 33),
            ("NAD Junction", 20.7, 45),
            ("RTC Complex (Dwaraka Nagar)", 26.7, 60),
            ("Siripuram Junction", 28.5, 66)
        ],
        "38H": [
            ("Gajuwaka Junction", 0.0, 0),
            ("Sriharipuram", 3.2, 8),
            ("Malkapuram", 5.5, 14),
            ("Scindia Junction", 7.2, 19),
            ("Naval Dockyard", 9.0, 24),
            ("Town Kotharoad", 11.5, 30),
            ("Jagadamba Junction", 13.1, 35),
            ("RTC Complex (Dwaraka Nagar)", 14.8, 40),
            ("Maddilapalem", 17.3, 48)
        ],
        "500": [
            ("RTC Complex (Dwaraka Nagar)", 0.0, 0),
            ("Gurudwara Junction", 1.5, 5),
            ("NAD Junction", 9.3, 23),
            ("Gopalapatnam", 11.5, 29),
            ("Vepagunta Junction", 14.0, 35),
            ("Pendurthi Junction", 19.5, 48),
            ("Anandapuram Junction", 33.0, 75)
        ],
        "500A": [
            ("Visakhapatnam Railway Station", 0.0, 0),
            ("RTC Complex (Dwaraka Nagar)", 1.7, 5),
            ("Kancharapalem", 4.4, 13),
            ("NAD Junction", 9.2, 23),
            ("Gopalapatnam", 11.4, 29),
            ("Vepagunta Junction", 13.9, 35),
            ("Pendurthi Junction", 19.4, 48)
        ],
        "500D": [
            ("Maddilapalem", 0.0, 0),
            ("Satyam Junction", 1.6, 5),
            ("Gurudwara Junction", 3.0, 9),
            ("NAD Junction", 10.8, 27),
            ("Gopalapatnam", 13.0, 33),
            ("Vepagunta Junction", 15.5, 39),
            ("Sujatha Nagar", 17.0, 43),
            ("Pendurthi Junction", 21.0, 53)
        ],
        "60": [
            ("Simhachalam Foothills", 0.0, 0),
            ("Gopalapatnam", 2.5, 7),
            ("NAD Junction", 4.7, 13),
            ("Marripalem", 6.3, 17),
            ("Urvasi Junction", 8.0, 21),
            ("Kancharapalem", 9.5, 25),
            ("Visakhapatnam Railway Station", 11.8, 31),
            ("Jagadamba Junction", 13.3, 36),
            ("Town Kotharoad", 14.9, 41)
        ],
        "60C": [
            ("Simhachalam Foothills", 0.0, 0),
            ("Gopalapatnam", 2.5, 7),
            ("NAD Junction", 4.7, 13),
            ("Marripalem", 6.3, 17),
            ("Kancharapalem", 8.2, 22),
            ("RTC Complex (Dwaraka Nagar)", 10.9, 29),
            ("Jagadamba Junction", 12.6, 34),
            ("RK Beach", 15.4, 42)
        ],
        "10K": [
            ("Town Kotharoad", 0.0, 0),
            ("Jagadamba Junction", 1.6, 5),
            ("RTC Complex (Dwaraka Nagar)", 3.3, 10),
            ("Gurudwara Junction", 4.8, 15),
            ("Marripalem", 8.6, 25),
            ("NAD Junction", 10.2, 29),
            ("Gopalapatnam", 12.4, 35)
        ],
        "222": [
            ("RTC Complex (Dwaraka Nagar)", 0.0, 0),
            ("Maddilapalem", 2.5, 7),
            ("Venkojipalem", 4.2, 12),
            ("Hanumanthawaka Junction", 5.8, 17),
            ("Zoo Park Stop", 6.9, 20),
            ("PM Palem", 10.8, 29),
            ("Madhurawada", 13.2, 35),
            ("Car Shed Junction", 14.0, 37),
            ("Kommadi Junction", 16.5, 43),
            ("Marikavalasa", 19.0, 49),
            ("Anandapuram Junction", 25.5, 63),
            ("Tagarapuvalasa", 31.0, 75)
        ],
        "222V": [
            ("Visakhapatnam Railway Station", 0.0, 0),
            ("RTC Complex (Dwaraka Nagar)", 1.7, 5),
            ("Maddilapalem", 4.2, 12),
            ("Hanumanthawaka Junction", 7.5, 21),
            ("Madhurawada", 14.9, 39),
            ("Kommadi Junction", 18.2, 47),
            ("Anandapuram Junction", 27.2, 67),
            ("Tagarapuvalasa", 32.7, 79)
        ],
        "55": [
            ("Scindia Junction", 0.0, 0),
            ("Malkapuram", 1.7, 5),
            ("Sriharipuram", 4.0, 11),
            ("Gajuwaka Junction", 7.2, 19),
            ("BHPV Junction", 10.4, 26),
            ("Sheela Nagar", 12.2, 30),
            ("Visakhapatnam Airport", 14.7, 36),
            ("NAD Junction", 18.0, 43),
            ("Gopalapatnam", 20.2, 49),
            ("Simhachalam Foothills", 22.7, 57)
        ],
        "55K": [
            ("Scindia Junction", 0.0, 0),
            ("Sriharipuram", 4.0, 11),
            ("Gajuwaka Junction", 7.2, 19),
            ("NAD Junction", 18.0, 43),
            ("Gopalapatnam", 20.2, 49),
            ("Vepagunta Junction", 22.7, 55),
            ("Pendurthi Junction", 28.2, 69),
            ("Kothavalasa", 37.9, 92)
        ],
        "68": [
            ("RTC Complex (Dwaraka Nagar)", 0.0, 0),
            ("NAD Junction", 9.3, 23),
            ("Gopalapatnam", 11.5, 29),
            ("Vepagunta Junction", 14.0, 35),
            ("Pendurthi Junction", 19.5, 48),
            ("Sabbavaram Junction", 28.5, 68)
        ],
        "88K": [
            ("Maddilapalem", 0.0, 0),
            ("Siripuram Junction", 2.5, 7),
            ("RTC Complex (Dwaraka Nagar)", 4.3, 12),
            ("NAD Junction", 13.6, 35),
            ("Gajuwaka Junction", 22.8, 54),
            ("Kurmannapalem Junction", 27.0, 63),
            ("Lankelapalem Junction", 35.5, 79),
            ("Parawada Junction", 42.0, 92),
            ("NTPC Simhadri Gate", 45.5, 99),
            ("Atchutapuram", 55.0, 120)
        ],
        "99K": [
            ("Town Kotharoad", 0.0, 0),
            ("Collector Office", 1.8, 5),
            ("Pandurangapuram", 3.2, 9),
            ("RK Beach", 4.4, 12),
            ("Sagar Nagar", 11.0, 26),
            ("Rushikonda Beach Stop", 14.5, 33),
            ("GITAM University", 15.2, 35),
            ("Bheemunipatnam Bus Stand", 31.0, 70)
        ],
        "111": [
            ("Kurmannapalem Junction", 0.0, 0),
            ("Gajuwaka Junction", 4.2, 9),
            ("Visakhapatnam Airport", 11.7, 24),
            ("NAD Junction", 15.0, 31),
            ("Gurudwara Junction", 19.5, 41),
            ("Maddilapalem", 22.5, 48),
            ("Hanumanthawaka Junction", 25.8, 55),
            ("PM Palem", 30.8, 65),
            ("Madhurawada", 33.2, 71),
            ("Car Shed Junction", 34.0, 74)
        ],
        "211": [
            ("Visakhapatnam Railway Station", 0.0, 0),
            ("RTC Complex (Dwaraka Nagar)", 1.7, 5),
            ("Gurudwara Junction", 3.2, 10),
            ("Seethammadhara", 5.0, 15),
            ("Hanumanthawaka Junction", 8.0, 22),
            ("Arilova / Health City", 10.5, 29)
        ],
        "541": [
            ("Maddilapalem", 0.0, 0),
            ("Gurudwara Junction", 3.0, 9),
            ("NAD Junction", 10.8, 27),
            ("Gopalapatnam", 13.0, 33),
            ("Vepagunta Junction", 15.5, 39),
            ("Pendurthi Junction", 21.0, 53),
            ("Kothavalasa", 30.7, 75)
        ]
    }

    route_stops_inserts = []
    for bus_num, stops in route_stops_map.items():
        for seq, (stop_name, dist, eta) in enumerate(stops, start=1):
            route_stops_inserts.append((bus_num, seq, stop_name, dist, eta))

    cursor.executemany("""
        INSERT INTO route_stops (bus_number, stop_sequence, stop_name, distance_km, eta_from_start_mins)
        VALUES (?, ?, ?, ?, ?)
    """, route_stops_inserts)

    # Update total_stops in bus_routes
    cursor.execute("""
        UPDATE bus_routes
        SET total_stops = (
            SELECT COUNT(*) FROM route_stops WHERE route_stops.bus_number = bus_routes.bus_number
        )
    """)

    # =========================================================================
    # 5. LIVE RUNNING BUSES (54 active buses distributed across Vizag)
    # =========================================================================
    # (bus_number, source, destination, current_location, lat, lng, eta_minutes, crowd_percentage, crowd_status, next_bus_eta, speed_kmh, bus_type)
    buses_data = [
        # 400K Fleet (Gajuwaka <-> Maddilapalem)
        ("400K", "Gajuwaka Junction", "Maddilapalem", "NAD Junction", 17.7447, 83.2319, 4, 88, "Overcrowded", 12, 35, "Metro Express"),
        ("400K", "Gajuwaka Junction", "Maddilapalem", "Visakhapatnam Airport", 17.7225, 83.2245, 12, 42, "Comfortable", 22, 40, "Metro Express"),
        ("400K", "Gajuwaka Junction", "Maddilapalem", "Kancharapalem", 17.7330, 83.2660, 6, 76, "Overcrowded", 16, 28, "Metro Express"),
        ("400K", "Maddilapalem", "Gajuwaka Junction", "Siripuram Junction", 17.7205, 83.3168, 5, 35, "Comfortable", 15, 32, "Metro Express"),
        ("400K", "Maddilapalem", "Gajuwaka Junction", "Gurudwara Junction", 17.7315, 83.3005, 14, 60, "Moderate", 25, 30, "Metro Express"),

        # 400 Fleet (Kurmannapalem <-> Maddilapalem)
        ("400", "Kurmannapalem Junction", "Maddilapalem", "Gajuwaka Junction", 17.6904, 83.2095, 8, 30, "Comfortable", 20, 34, "City Ordinary"),
        ("400", "Kurmannapalem Junction", "Maddilapalem", "Sheela Nagar", 17.7095, 83.2045, 18, 52, "Moderate", 30, 36, "City Ordinary"),

        # 400H Fleet (Steel Plant <-> Maddilapalem)
        ("400H", "Steel Plant Main Gate", "Maddilapalem", "Kurmannapalem Junction", 17.6850, 83.1670, 7, 72, "Moderate", 22, 38, "Metro Express"),
        ("400H", "Steel Plant Main Gate", "Maddilapalem", "Railway Station", 17.7224, 83.2922, 19, 85, "Overcrowded", 35, 25, "Metro Express"),

        # 400Y Fleet (Anakapalle <-> RTC Complex)
        ("400Y", "Anakapalle RTC Complex", "RTC Complex (Dwaraka Nagar)", "Lankelapalem Junction", 17.6600, 83.1000, 9, 65, "Moderate", 21, 45, "Metro Express"),
        ("400Y", "Anakapalle RTC Complex", "RTC Complex (Dwaraka Nagar)", "NAD Junction", 17.7447, 83.2319, 15, 91, "Overcrowded", 27, 32, "Metro Express"),

        # 900K Fleet (RTC Complex <-> Bheemili Beach Road)
        ("900K", "RTC Complex (Dwaraka Nagar)", "Bheemunipatnam Bus Stand", "Siripuram Junction", 17.7205, 83.3168, 3, 90, "Overcrowded", 11, 28, "Metro Express"),
        ("900K", "RTC Complex (Dwaraka Nagar)", "Bheemunipatnam Bus Stand", "Maddilapalem", 17.7384, 83.3289, 11, 62, "Moderate", 21, 35, "Metro Express"),
        ("900K", "RTC Complex (Dwaraka Nagar)", "Bheemunipatnam Bus Stand", "Rushikonda Beach Stop", 17.7816, 83.3831, 20, 38, "Comfortable", 32, 42, "Metro Express"),
        ("900K", "Bheemunipatnam Bus Stand", "RTC Complex (Dwaraka Nagar)", "Mangamaripeta", 17.8130, 83.4150, 8, 40, "Comfortable", 18, 40, "Metro Express"),

        # 900T Fleet (RTC Complex <-> Rushikonda IT SEZ)
        ("900T", "RTC Complex (Dwaraka Nagar)", "IT SEZ (Rushikonda Hills)", "MVP Colony Circle", 17.7412, 83.3375, 6, 28, "Comfortable", 18, 30, "City Sheetal AC"),
        ("900T", "RTC Complex (Dwaraka Nagar)", "IT SEZ (Rushikonda Hills)", "Sagar Nagar", 17.7650, 83.3600, 16, 45, "Moderate", 28, 36, "City Sheetal AC"),

        # 900 Fleet (Railway Station <-> Bheemunipatnam)
        ("900", "Visakhapatnam Railway Station", "Bheemunipatnam Bus Stand", "Jagadamba Junction", 17.7121, 83.3015, 5, 78, "Overcrowded", 25, 24, "City Ordinary"),

        # 28A Fleet (RK Beach <-> Simhachalam Foothills)
        ("28A", "RK Beach", "Simhachalam Foothills", "Jagadamba Junction", 17.7121, 83.3015, 4, 82, "Overcrowded", 14, 25, "Metro Express"),
        ("28A", "RK Beach", "Simhachalam Foothills", "NAD Junction", 17.7447, 83.2319, 14, 38, "Comfortable", 24, 34, "Metro Express"),
        ("28A", "Simhachalam Foothills", "RK Beach", "Gopalapatnam", 17.7563, 83.2185, 6, 48, "Moderate", 16, 32, "Metro Express"),

        # 28 Fleet (RK Beach <-> Pendurthi)
        ("28", "RK Beach", "Pendurthi Junction", "RTC Complex (Dwaraka Nagar)", 17.7265, 83.3073, 7, 79, "Overcrowded", 19, 28, "City Ordinary"),
        ("28", "Pendurthi Junction", "RK Beach", "Vepagunta Junction", 17.7710, 83.2110, 10, 50, "Moderate", 22, 35, "City Ordinary"),

        # 28K Fleet (Town Kotharoad <-> Kothavalasa)
        ("28K", "Town Kotharoad", "Kothavalasa", "Town Kotharoad", 17.6970, 83.2990, 5, 30, "Comfortable", 25, 25, "City Ordinary"),
        ("28K", "Town Kotharoad", "Kothavalasa", "Simhachalam Foothills", 17.7660, 83.2420, 22, 68, "Moderate", 42, 30, "City Ordinary"),

        # 38 Fleet (Kurmannapalem <-> Siripuram)
        ("38", "Kurmannapalem Junction", "Siripuram Junction", "Sheela Nagar", 17.7095, 83.2045, 5, 58, "Moderate", 15, 36, "Metro Express"),
        ("38", "Kurmannapalem Junction", "Siripuram Junction", "BHPV Junction", 17.7032, 83.1950, 15, 22, "Comfortable", 25, 38, "Metro Express"),
        ("38", "Siripuram Junction", "Kurmannapalem Junction", "Railway Station", 17.7224, 83.2922, 8, 84, "Overcrowded", 18, 25, "Metro Express"),

        # 38K Fleet (Duvvada <-> RTC Complex)
        ("38K", "Duvvada Railway Station", "RTC Complex (Dwaraka Nagar)", "Kurmannapalem Junction", 17.6850, 83.1670, 6, 40, "Comfortable", 18, 38, "Metro Express"),
        ("38K", "Duvvada Railway Station", "RTC Complex (Dwaraka Nagar)", "Gajuwaka Junction", 17.6904, 83.2095, 17, 75, "Overcrowded", 29, 32, "Metro Express"),

        # 38A Fleet (Steel Plant Sector 6 <-> Siripuram)
        ("38A", "Steel Plant Township Sector 6", "Siripuram Junction", "Steel Plant Main Gate", 17.6650, 83.1600, 4, 32, "Comfortable", 20, 35, "Metro Express"),

        # 38H Fleet (Gajuwaka <-> Maddilapalem via Scindia)
        ("38H", "Gajuwaka Junction", "Maddilapalem", "Scindia Junction", 17.6910, 83.2770, 8, 64, "Moderate", 24, 28, "City Ordinary"),
        ("38H", "Gajuwaka Junction", "Maddilapalem", "Town Kotharoad", 17.6970, 83.2990, 18, 86, "Overcrowded", 36, 22, "City Ordinary"),

        # 500 Fleet (RTC Complex <-> Anandapuram)
        ("500", "RTC Complex (Dwaraka Nagar)", "Anandapuram Junction", "Gurudwara Junction", 17.7315, 83.3005, 4, 55, "Moderate", 16, 32, "Metro Express"),
        ("500", "RTC Complex (Dwaraka Nagar)", "Anandapuram Junction", "Pendurthi Junction", 17.8220, 83.2010, 24, 34, "Comfortable", 38, 42, "Metro Express"),

        # 500A Fleet (Railway Station <-> Pendurthi)
        ("500A", "Visakhapatnam Railway Station", "Pendurthi Junction", "Kancharapalem", 17.7330, 83.2660, 7, 70, "Moderate", 22, 28, "City Ordinary"),

        # 500D Fleet (Maddilapalem <-> Pendurthi)
        ("500D", "Maddilapalem", "Pendurthi Junction", "Satyam Junction", 17.7350, 83.3080, 5, 48, "Moderate", 17, 30, "Metro Express"),

        # 60 Fleet (Simhachalam <-> Town Kotharoad)
        ("60", "Simhachalam Foothills", "Town Kotharoad", "Gopalapatnam", 17.7563, 83.2185, 4, 85, "Overcrowded", 15, 30, "City Ordinary"),
        ("60", "Simhachalam Foothills", "Town Kotharoad", "NAD Junction", 17.7447, 83.2319, 13, 38, "Comfortable", 25, 34, "City Ordinary"),

        # 60C Fleet (Simhachalam <-> RK Beach)
        ("60C", "Simhachalam Foothills", "RK Beach", "Marripalem", 17.7410, 83.2450, 6, 62, "Moderate", 18, 32, "Metro Express"),

        # 10K Fleet (Town Kotharoad <-> Gopalapatnam)
        ("10K", "Town Kotharoad", "Gopalapatnam", "RTC Complex (Dwaraka Nagar)", 17.7265, 83.3073, 5, 68, "Moderate", 15, 26, "City Ordinary"),

        # 222 Fleet (RTC Complex <-> Tagarapuvalasa)
        ("222", "RTC Complex (Dwaraka Nagar)", "Tagarapuvalasa", "Maddilapalem", 17.7384, 83.3289, 4, 84, "Overcrowded", 12, 32, "Metro Express"),
        ("222", "RTC Complex (Dwaraka Nagar)", "Tagarapuvalasa", "Hanumanthawaka Junction", 17.7600, 83.3420, 12, 50, "Moderate", 22, 38, "Metro Express"),
        ("222", "RTC Complex (Dwaraka Nagar)", "Tagarapuvalasa", "Madhurawada", 17.8170, 83.3530, 22, 32, "Comfortable", 32, 45, "Metro Express"),

        # 222V Fleet
        ("222V", "Visakhapatnam Railway Station", "Tagarapuvalasa", "RTC Complex (Dwaraka Nagar)", 17.7265, 83.3073, 6, 75, "Overcrowded", 25, 26, "City Ordinary"),

        # 55 Fleet (Scindia <-> Simhachalam)
        ("55", "Scindia Junction", "Simhachalam Foothills", "Sriharipuram", 17.6880, 83.2350, 6, 60, "Moderate", 20, 30, "Metro Express"),
        ("55", "Scindia Junction", "Simhachalam Foothills", "NAD Junction", 17.7447, 83.2319, 18, 42, "Comfortable", 32, 35, "Metro Express"),

        # 55K Fleet (Scindia <-> Kothavalasa)
        ("55K", "Scindia Junction", "Kothavalasa", "Gajuwaka Junction", 17.6904, 83.2095, 10, 52, "Moderate", 35, 32, "City Ordinary"),

        # 68 Fleet (RTC Complex <-> Sabbavaram)
        ("68", "RTC Complex (Dwaraka Nagar)", "Sabbavaram Junction", "NAD Junction", 17.7447, 83.2319, 12, 72, "Moderate", 32, 34, "City Ordinary"),

        # 88K Fleet (Maddilapalem <-> Atchutapuram)
        ("88K", "Maddilapalem", "Atchutapuram", "Gajuwaka Junction", 17.6904, 83.2095, 15, 89, "Overcrowded", 30, 38, "Metro Express"),
        ("88K", "Maddilapalem", "Atchutapuram", "Kurmannapalem Junction", 17.6850, 83.1670, 25, 45, "Moderate", 40, 42, "Metro Express"),

        # 99K Fleet (Town Kotharoad <-> Bheemili)
        ("99K", "Town Kotharoad", "Bheemunipatnam Bus Stand", "RK Beach", 17.7142, 83.3239, 7, 56, "Moderate", 22, 28, "City Ordinary"),
        ("99K", "Town Kotharoad", "Bheemunipatnam Bus Stand", "Rushikonda Beach Stop", 17.7816, 83.3831, 21, 35, "Comfortable", 38, 38, "City Ordinary"),

        # 111 Fleet (Kurmannapalem <-> Madhurawada)
        ("111", "Kurmannapalem Junction", "Car Shed Junction", "Airport", 17.7225, 83.2245, 8, 66, "Moderate", 20, 40, "Metro Express"),
        ("111", "Kurmannapalem Junction", "Car Shed Junction", "Maddilapalem", 17.7384, 83.3289, 22, 80, "Overcrowded", 35, 30, "Metro Express"),

        # 211 Fleet (Railway Station <-> VIMS Health City)
        ("211", "Visakhapatnam Railway Station", "Arilova / Health City", "Seethammadhara", 17.7410, 83.3130, 8, 44, "Comfortable", 24, 28, "City Ordinary"),

        # 541 Fleet (Maddilapalem <-> Kothavalasa)
        ("541", "Maddilapalem", "Kothavalasa", "Gopalapatnam", 17.7563, 83.2185, 14, 58, "Moderate", 30, 36, "Metro Express")
    ]

    cursor.executemany("""
        INSERT INTO buses (bus_number, source, destination, current_location, lat, lng, eta_minutes, crowd_percentage, crowd_status, next_bus_eta, speed_kmh, bus_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, buses_data)

    # =========================================================================
    # 6. EXPANDED MULTIMODAL ALTERNATIVE ROUTES
    # =========================================================================
    alternatives_data = [
        ("Gajuwaka Junction", "Maddilapalem", "Connecting Bus",
         "Board Bus 38 to NAD Junction (5 mins away), then transfer to Metro Express 500D or 111 to Maddilapalem.", 28),
        ("Gajuwaka Junction", "Maddilapalem", "Shared Auto + Bus Combo",
         "Take Auto from Gajuwaka to Scindia (8 mins), board less-crowded Beach Bus 38H to Maddilapalem via Kotharoad.", 35),
        ("RTC Complex (Dwaraka Nagar)", "Rushikonda Beach Stop", "Auto + Bus Combo",
         "Take Shared Auto to MVP Colony (8 mins), then hop on Beach Bus 900T (AC / Less Crowded).", 22),
        ("RTC Complex (Dwaraka Nagar)", "Rushikonda Beach Stop", "Direct Metro Express",
         "Wait 10 mins for next Metro Express 900K departing Platform 4 directly along coastal road.", 25),
        ("Simhachalam Foothills", "RK Beach", "Connecting Bus",
         "Board Bus 55 or 60 to NAD Junction, transfer to City Direct 10K or 60C to RK Beach.", 32),
        ("Simhachalam Foothills", "RK Beach", "Fast Direct Metro",
         "Take Express 28A via Jagadamba directly to Submarine Museum (estimated 38 mins).", 38),
        ("Kurmannapalem Junction", "Siripuram Junction", "Cab + Express Bus",
         "Take Rapido / Auto to Gajuwaka Depot (5 mins), board Express 400K direct to Siripuram.", 26),
        ("NAD Junction", "Madhurawada", "Connecting BRTS",
         "Board Bus 400K or 38 to Maddilapalem BRTS, switch to 222 or 111 Express to Madhurawada.", 30),
        ("RTC Complex (Dwaraka Nagar)", "Tagarapuvalasa", "Express Bypass",
         "Take Bus 222 Non-Stop to Anandapuram, transfer to local auto to Tagarapuvalasa.", 42),
        ("Visakhapatnam Railway Station", "Rushikonda Beach Stop", "City Connection",
         "Board Bus 900 or take Auto to RTC Complex (6 mins), transfer to 900T Sheetal AC Bus.", 30)
    ]
    cursor.executemany("""
        INSERT INTO alternative_routes (source, destination, option_type, route_details, total_time_mins)
        VALUES (?, ?, ?, ?, ?)
    """, alternatives_data)

    # =========================================================================
    # 7. INITIAL COMPLAINT TICKETS
    # =========================================================================
    cursor.execute("""
        INSERT INTO complaints (ticket_id, bus_number, complaint_text, ai_category, ai_priority, status)
        VALUES ('TICK-INIT01', '400K', 'Bus skipped the NAD Junction stop during peak evening hours due to heavy crowd.', 'Route / Stop Violation', 'High', 'Open')
    """)
    cursor.execute("""
        INSERT INTO complaints (ticket_id, bus_number, complaint_text, ai_category, ai_priority, status)
        VALUES ('TICK-INIT02', '900K', 'AC was not functioning properly on Rushikonda Beach route bus during afternoon.', 'Vehicle Maintenance', 'Medium', 'Open')
    """)

    conn.commit()
    conn.close()
    print(f"Database successfully seeded at: {DB_PATH}")
    print(f"   - {len(stops_data)} Bus Stops added")
    print(f"   - {len(routes_data)} Bus Routes added")
    print(f"   - {len(route_stops_inserts)} Route Stops mapped")
    print(f"   - {len(buses_data)} Live Running Buses tracked")
    print(f"   - {len(alternatives_data)} Multimodal Routes added")

if __name__ == "__main__":
    seed_database()
