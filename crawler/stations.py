S1_stops_1 = """Flughafen München
Flughafen Besucherpark
Neufahrn
Eching
Lohhof
Unterschleißheim
Oberschleißheim
Feldmoching
Fasanerie
Moosach
Laim
Hirschgarten
Donnersbergerbrücke
Hackerbrücke
Hauptbahnhof
Karlsplatz
Marienplatz
Isartor
Rosenheimer Platz
Ostbahnhof München""".split('\n')

S1_stops_2 = """Freising
Pulling
Neufahrn
Eching
Lohhof
Unterschleißheim
Oberschleißheim
Feldmoching
Fasanerie
Moosach
Laim
Hirschgarten
Donnersbergerbrücke
Hackerbrücke
Hauptbahnhof
Karlsplatz
Marienplatz
Isartor
Rosenheimer Platz
Ostbahnhof München""".split('\n')


S2_stops_1 = """Altomünster
Kleinberghofen
Erdweg
Arnbach
Markt Indersdorf
Niederroth
Schwabhausen
Bachern
Dachau Stadt
Dachau
Karlsfeld
Allach
Untermenzing
Obermenzing
Laim
Hirschgarten
Donnersbergerbrücke
Hackerbrücke
Hauptbahnhof
Karlsplatz
Marienplatz
Isartor
Rosenheimer Platz
Ostbahnhof München
Leuchtenbergring
Berg am Laim
Riem
Feldkirchen
Heimstetten
Grub
Poing
Markt Schwaben
Ottenhofen
St. Koloman
Aufhausen
Altenerding
Erding""".split('\n')

S2_stops_2 = """Petershausen
Vierkirchen-Esterhofen
Röhrmoos
Hebertshausen
Dachau
Karlsfeld
Allach
Untermenzing
Obermenzing
Laim
Hirschgarten
Donnersbergerbrücke
Hackerbrücke
Hauptbahnhof
Karlsplatz
Marienplatz
Isartor
Rosenheimer Platz
Ostbahnhof München
Leuchtenbergring
Berg am Laim
Riem
Feldkirchen
Heimstetten
Grub
Poing
Markt Schwaben
Ottenhofen
St. Koloman
Aufhausen
Altenerding
Erding""".split('\n')

S3_stops = """Mammendorf
Malching
Maisach
Gernlinden
Esting
Olching
Gröbenzell
Lochhausen
Langwied
Pasing
Laim
Hirschgarten
Donnersbergerbrücke
Hackerbrücke
Hauptbahnhof
Karlsplatz
Marienplatz
Isartor
Rosenheimer Platz
Ostbahnhof München
St.-Martin-Straße
Giesing
Fasangarten
Fasanenpark
Unterhaching
Taufkirchen
Furth
Deisenhofen
Sauerlach
Otterfing
Holzkirchen""".split('\n')

S4_stops = """Geltendorf
Türkenfeld
Grafrath
Schöngeising
Buchenau
Fürstenfeldbruck
Eichenau
Puchheim
Aubing
Leienfelsstraße
Pasing
Laim
Hirschgarten
Donnersbergerbrücke
Hackerbrücke
Hauptbahnhof
Karlsplatz
Marienplatz
Isartor
Rosenheimer Platz
Ostbahnhof München
Leuchtenbergring
Berg am Laim
Trudering
Gronsdorf
Haar
Vaterstetten
Baldham
Zorneding
Eglharting
Kirchseeon
Grafing
Grafing Stadt
Ebersberg""".split('\n')

S6_stops = """Tutzing
Feldafing
Possenhofen
Starnberg
Starnberg Nord
Gauting
Stockdorf
Planegg
Gräfelfing
Lochham
Westkreuz
Pasing
Laim
Hirschgarten
Donnersbergerbrücke
Hackerbrücke
Hauptbahnhof
Karlsplatz
Marienplatz
Isartor
Rosenheimer Platz
Ostbahnhof München
Leuchtenbergring
Berg am Laim
Trudering
Gronsdorf
Haar
Vaterstetten
Baldham
Zorneding
Eglharting
Kirchseeon
Grafing
Grafing Stadt
Ebersberg""".split('\n')

S7_stops = """Wolfratshausen
Icking
Ebenhausen-Schäftlarn
Hohenschäftlarn
Baierbrunn
Buchenhain
Höllriegelskreuth
Pullach
Großhesselohe Isartalbahnhof
Solln
Siemenswerke
Mittersendling
Harras
Heimeranplatz
Donnersbergerbrücke
Hackerbrücke
Hauptbahnhof
Karlsplatz
Marienplatz
Isartor
Rosenheimer Platz
Ostbahnhof München
St.-Martin-Straße
Giesing
Perlach
Neuperlach Süd
Neubiberg
Ottobrunn
Hohenbrunn
Wächterhof
Höhenkirchen-Siegertsbrunn
Dürrnhaar
Aying
Peiß
Großhelfendorf
Kreuzstraße""".split('\n')

S8_stops = """Herrsching
Seefeld-Hechendorf
Steinebach
Weßling
Neugilching
Gilching-Argelsried
Geisenbrunn
Germering-Unterpfaffenhofen
Harthaus
Freiham
Neuaubing
Westkreuz
Pasing
Laim
Hirschgarten
Donnersbergerbrücke
Hackerbrücke
Hauptbahnhof
Karlsplatz
Marienplatz
Isartor
Rosenheimer Platz
Ostbahnhof München
Leuchtenbergring
Daglfing
Englschalking
Johanneskirchen
Unterföhring
Ismaning
Hallbergmoos
Flughafen Besucherpark
Flughafen München""".split('\n')

S20_stops = """Pasing
Heimeranplatz
Mittersendling
Siemenswerke
Solln
Großhesselohe Isartalbahnhof
Pullach
Höllriegelskreuth""".split('\n')


S1_STATIONS_1 = S1_stops_1
S1_STATIONS_2 = S1_stops_2
S2_STATIONS_1 = S2_stops_1
S2_STATIONS_2 = S2_stops_2
S3_STATIONS = S3_stops
S4_STATIONS = S4_stops
S6_STATIONS = S6_stops
S7_STATIONS = S7_stops
S8_STATIONS = S8_stops
S20_STATIONS = S20_stops

LINES = {
    'S1a': S1_STATIONS_1,
    'S1b': S1_STATIONS_2,
    'S2a': S2_STATIONS_1,
    'S2b': S2_STATIONS_2,
    'S3': S3_STATIONS,
    'S4': S4_STATIONS,
    'S6': S6_STATIONS,
    'S7': S7_STATIONS,
    'S8': S8_STATIONS,
    'S20': S20_STATIONS
}


STATIONS = sorted(list(set(
    S1_stops_1 + S1_stops_2 + S2_stops_1 + S2_stops_2 + S3_stops + S4_stops + S6_stops + 
    S7_stops + S8_stops + S20_stops
)))