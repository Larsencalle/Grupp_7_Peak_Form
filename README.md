PeakForm
Repository (GitHub): https://github.com/Larsencalle/Grupp_7_Peak_Form
Release ID: Slutlig inlämning (Final)
Datum för inlämning: Juni 2026
Grupp: Grupp 7

1. Systemkrav och programvara
För att kunna starta och köra PeakForm lokalt på din egen dator krävs att följande program är installerade:

Python (3.x): Språket applikationen är byggd i. Kan laddas ner från python.org.

PostgreSQL: Databassystemet som driver lagringen. Kan laddas ner från postgresql.org (eller anslutas till via Malmö universitets databasserver).

2. Installation av projekt och beroenden
När Python är installerat behöver du ladda ner de bibliotek som applikationen förlitar sig på.

Öppna projektmappen i ditt kodredigeringsprogram (förslagsvis Visual Studio Code).

Öppna en ny terminal i programmet.

Kör följande kommando för att installera webbramverket Flask och uppkopplingen till PostgreSQL:
pip install Flask psycopg2-binary
(Vi rekommenderar psycopg2-binary då det minskar risken för installationsproblem på Mac och Windows).

3. Konfiguration av databas
Applikationen kräver en specifik databasstruktur för att hantera medlemmar, program och övningar.

A. Skapa inloggningsfilen

Lokalisera filen config.example i projektets huvudmapp.

Gör en kopia av filen och döp kopian till config.ini.

Öppna config.ini och fyll i dina lokala inloggningsuppgifter (användarnamn, lösenord och host) för din PostgreSQL-server.

B. Bygg strukturen och fyll på med data

Öppna ditt databasprogram (t.ex. pgAdmin).

Skapa ett nytt schema och döp det till peakform.

Gå tillbaka till VS Code och öppna mappen sql.

Kopiera all text i filen schema.sql och kör detta som ett skript i databasen för att generera alla tabeller.

Kopiera därefter all text i filen data.sql och kör det på samma sätt. Detta fyller databasen med standardövningar och rätt bildlänkar så att appen inte är tom när du loggar in.

4. Starta applikationen
När allt är konfigurerat är det dags att starta servern.

Säkerställ att du befinner dig i projektets rotmapp i terminalen.

Kör kommandot: python app.py (alternativt klicka på "Play"-knappen inne i filen).

Terminalen meddelar när servern är igång och ger dig en lokal webbadress, oftast http://127.0.0.1:5000.

Håll ner Ctrl (eller Cmd på Mac) och klicka på länken för att öppna PeakForm i din webbläsare!

5. Projektets struktur
Projektet är logiskt uppdelat för att separera design, sidlogik och databashantering:

app.py: Huvudfilen som startar servern.

db.py: Etablerar den säkra kopplingen till PostgreSQL-databasen.

utils.py: Innehåller globala hjälpfunktioner och logik.

routes/: Mapp som innehåller all sidlogik (routing). Här ligger Python-filerna som styr de olika delarna av appen, såsom inloggning (auth.py), träningsprogram (programs.py) och passhistorik (log_workout.py).

sql/: Mapp för databasuppbyggnad. Innehåller schema.sql (skapar tabeller) och data.sql (fyller biblioteket med övningar).

templates/: Mapp som innehåller alla HTML-vyer (sidorna som användaren ser).

static/: Innehåller applikationens styling (style.css), frontend-skript (timer-countdown.js) och mappen images/ för alla träningsbilder.

config.example: Mall för hur inloggningsuppgifterna till databasen ska fyllas i.

.gitignore: Dolda filer som säkerställer att känslig inloggningsdata (som config.ini) och arbetsyteinställningar inte hamnar på GitHub.
