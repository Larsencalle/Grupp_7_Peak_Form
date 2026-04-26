Repository (GitHub): https://github.com/Larsencalle/Grupp_7_Peak_Form 

Release ID: halftime

Datum för inlämning: 2026-04-26

Grupp: Grupp 7

1. Systemkrav och programvara
För att kunna köra denna applikation lokalt krävs att följande programvara är nedladdad och installerad på datorn:

Python (3.x): Kan laddas ner från python.org. 

PostgreSQL: Kan laddas ner från postgresql.org. Behövs för att driva databasen lokalt.

2. Installation av projekt och beroenden
När Python är installerat måste projektets specifika bibliotek laddas ner via terminalen.

Öppna projektmappen i VS Code.

Öppna en ny terminal i VS Code.

Kör följande kommando för att installera Flask och kopplingen till PostgreSQL (psycopg2):

pip install Flask psycopg2
(Vid installationsproblem med psycopg2 på Mac/Windows, kör istället: pip install Flask psycopg2-binary)

3. Konfiguration av databas
Applikationen kräver en specifik databasstruktur och inloggningsuppgifter för att fungera.

A. Skapa inloggningsfilen (config.ini)
I projektmappen finns en mallfil som heter config.example.

Skapa en kopia av config.example i samma mapp och döp den till config.ini.

Öppna config.ini och fyll i dina lokala inloggningsuppgifter (användarnamn och lösenord) för din PostgreSQL-installation.

B. Skapa databasstrukturen
Öppna PostgreSQL.

Skapa ett nytt schema med namnet peakform.

Lokalisera filen schema.sql i projektets rotmapp i VS Code.

Kopiera allt innehåll i schema.sql och kör det som ett SQL-skript i ditt nyskapade schema (peakform). Detta genererar alla tabeller applikationen behöver.

4. Starta applikationen
När alla paket är installerade och databasen är konfigurerad startas den lokala servern.

Säkerställ att du befinner dig i projektets rotmapp i VS Code-terminalen.

Kör kommandot:
python app.py (eller tryck på play-knappen när du är inne i filen app.py)

Terminalen kommer nu att visa att servern är igång och ge en lokal adress, vanligtvis http://127.0.0.1:5000.

Håll ner Ctrl (eller Cmd på Mac) och klicka på länken i terminalen. Applikationen öppnas nu i din standardwebbläsare.

5. Projektets struktur
Filstrukturen är uppbyggd enligt följande:

app.py: Huvudfil för Flask-servern och routing-logik.

db.py: Hanterar applikationens uppkoppling mot PostgreSQL-databasen.

schema.sql: Skript för databaslayout och skapande av tabeller.

config.example: Mall för databaskonfiguration.

templates/: Mapp som innehåller alla HTML-vyer (index.html, inlogg.html, regkonto.html, dashboard.html).

static/: Mapp som innehåller applikationens styling (style.css) och frontend-logik (script.ts).

.gitignore: Exkluderar dolda filer, cache (__pycache__) och känsliga filer (som config.ini) från versionshanteringen.
