SET search_path TO peakform;


TRUNCATE TABLE exercise CASCADE;


INSERT INTO exercise (name, description, category, difficulty_level, image_url) VALUES 


('Bänkpress', $$Förberedelse:
Placera skivstången i en höjd där du kan lyfta av den utan att tappa positionen.
Lägg dig på bänken med ögonen ungefär rakt under stången.
Placera fötterna stadigt i golvet.

Hitta rätt startposition:
Greppa stången något bredare än axelbrett.
Dra skulderbladen bakåt och nedåt mot bänken.
Spänn bålen och lyft stången från ställningen med raka armar.
Håll bröstet högt och fötterna stabilt i golvet.

Utför övningen:
Andas in och behåll spänningen i bålen och övre ryggen.
Sänk stången kontrollerat mot nedre delen av bröstet.
Håll armbågarna lätt vinklade inåt.
Pressa stången uppåt tills armarna är raka igen.
Behåll skulderbladen stabila under hela rörelsen.$$, 'Push', 2, 'benchpress.jpg'),

('Militärpress', $$Förberedelse:
Placera skivstången ungefär i övre brösthöjd.
Greppa stången strax utanför axelbrett.
Stå nära stången innan du lyfter av den.

Hitta rätt startposition:
Placera stången mot övre delen av bröstet/framsida axlar.
Lyft av stången och ta ett steg bakåt.
Stå med fötterna ungefär höft- till axelbrett.
Spänn bålen och sätesmusklerna.
Håll handlederna raka och armbågarna lätt framför stången.

Utför övningen:
Andas in och håll kroppen stabil.
Pressa stången rakt upp över huvudet.
För huvudet lätt bakåt när stången passerar ansiktet.
För huvudet tillbaka framåt när stången är över huvudet.
Sänk stången kontrollerat tillbaka till övre bröstet.$$, 'Push', 3, 'military_press.jpg'),

('Lutande Hantelpress', $$Förberedelse:
Ställ in bänken i en lutning på ungefär 30–45 grader.
Välj två hantlar och sätt dig på bänken.
Placera fötterna stadigt i golvet.

Hitta rätt startposition:
Lägg dig bakåt med hantlarna vid sidan av bröstet.
Dra skulderbladen bakåt och nedåt mot bänken.
Håll bröstet högt och bålen spänd.
Håll armbågarna lätt vinklade inåt.

Utför övningen:
Andas in och sänk hantlarna kontrollerat mot övre delen av bröstet.
Pressa hantlarna uppåt tills armarna nästan är helt raka.
Låt hantlarna röra sig lätt mot varandra i toppen.
Sänk hantlarna långsamt tillbaka till startpositionen.
Behåll kontrollen över axlar och skulderblad.$$, 'Push', 2, 'incline_dumbell_press.jpg'),

('Dips', $$Förberedelse:
Greppa handtagen med båda händerna.
Hoppa eller kliv upp till startpositionen.
Håll kroppen stabil med raka armar.

Hitta rätt startposition:
Dra skulderbladen lätt nedåt.
Spänn bålen och håll kroppen kontrollerad.
Böj knäna om det behövs.
Luta kroppen lätt framåt för mer fokus på bröst.
Håll kroppen mer upprätt för mer fokus på triceps.

Utför övningen:
Andas in och sänk kroppen kontrollerat.
Böj armbågarna medan du håller kroppen stabil.
Gå ner tills överarmarna ungefär är parallella med golvet, eller så djupt som axlarna tillåter.
Pressa dig tillbaka upp tills armarna är raka.
Undvik att gunga kroppen fram och tillbaka.$$, 'Push', 3, 'dips.jpg'),

('Sidolyft med hantlar', $$Förberedelse:
Välj två hantlar.
Stå upp med en hantel i varje hand.
Placera fötterna ungefär höftbrett.

Hitta rätt startposition:
Låt armarna hänga längs sidan av kroppen.
Spänn bålen lätt och håll ryggen neutral.
Håll armbågarna lätt böjda.
Slappna av i axlarna och undvik att dra upp dem mot öronen.

Utför övningen:
Andas in och lyft hantlarna ut åt sidorna.
Lyft tills armarna är ungefär i axelhöjd.
Behåll en lätt böjning i armbågarna.
Sänk hantlarna kontrollerat tillbaka.
Undvik att svinga vikterna med kroppen.$$, 'Push', 1, 'dumbbell_lateral_raises.jpg'),

('Triceps Pushdowns', $$Förberedelse:
Fäst ett rep eller en stång högt upp i kabelmaskinen.
Ställ in en passande vikt.
Stå nära maskinen med fötterna ungefär höftbrett.

Hitta rätt startposition:
Greppa handtaget med båda händerna.
Håll armbågarna nära kroppen.
Spänn bålen och håll kroppen stabil.
Håll överarmarna stilla och nära sidorna.

Utför övningen:
Andas in och håll överarmarna stilla.
Pressa handtaget nedåt genom att sträcka ut armbågarna.
Tryck hela vägen ner tills armarna är raka.
Pausa kort i bottenläget och spänn triceps.
Släpp kontrollerat tillbaka handtaget.
Undvik att använda kroppsvikten för att få ner vikten.$$, 'Push', 1, 'triceps_pushdowns.jpg'),


('Marklyft', $$Förberedelse:
Placera skivstången över mitten av fötterna.
Stå med fötterna ungefär höftbrett.
Greppa stången strax utanför benen.

Hitta rätt startposition:
Böj knäna tills smalbenen nästan nuddar stången.
Håll bröstet upp och ryggen neutral.
Spänn bålen.
Dra skulderbladen lätt nedåt och bakåt.
Håll blicken något framför dig.

Utför övningen:
Andas in och skapa tryck i bålen.
Tryck fötterna genom golvet.
Lyft stången genom att sträcka knän och höfter samtidigt.
Håll stången nära kroppen under hela lyftet.
Pressa höfterna framåt när stången passerar knäna.
Stå helt upprätt utan att luta dig bakåt.
Sänk stången genom att föra höfterna bakåt och sedan böja knäna.$$, 'Pull', 3, 'deadlift.jpg'),

('Pull-ups', $$Förberedelse:
Greppa stången med handflatorna bort från dig.
Placera händerna något bredare än axelbrett.
Häng med raka armar.

Hitta rätt startposition:
Spänn bålen lätt.
Dra skulderbladen nedåt innan du börjar dra.
Håll benen stilla, antingen raka eller lätt böjda.
Håll kroppen kontrollerad utan att börja gunga.

Utför övningen:
Andas in och dra kroppen uppåt.
För armbågarna ner mot sidan av kroppen.
Dra tills hakan är över stången eller bröstet närmar sig stången.
Sänk dig långsamt tillbaka till startpositionen.
Sträck ut armarna kontrollerat i bottenläget.$$, 'Pull', 3, 'pullups.jpg'),

('Skivstångsrodd', $$Förberedelse:
Placera skivstången framför dig.
Stå med fötterna ungefär höft- till axelbrett.
Greppa stången något bredare än axelbrett.

Hitta rätt startposition:
Fäll fram överkroppen genom att skjuta höfterna bakåt.
Håll ryggen neutral och bålen spänd.
Låt stången hänga med raka armar under axlarna.
Håll nacken neutral och blicken snett nedåt.

Utför övningen:
Andas in och dra stången mot nedre delen av bröstet eller övre delen av magen.
För armbågarna bakåt och håll dem nära kroppen.
Pressa ihop skulderbladen i toppläget.
Sänk stången kontrollerat tillbaka.
Håll överkroppen stabil under hela rörelsen.$$, 'Pull', 2, 'barbell_rowing.jpg'),

('Latsdrag', $$Förberedelse:
Sätt dig i latsdragsmaskinen.
Justera knästödet så att benen sitter stadigt.
Greppa stången något bredare än axelbrett.

Hitta rätt startposition:
Sitt upprätt med bröstet högt.
Placera fötterna stadigt i golvet.
Spänn bålen lätt.
Dra skulderbladen lätt nedåt innan du börjar dra.
Håll armarna raka i startläget utan att tappa kontrollen.

Utför övningen:
Andas in och dra stången ner mot övre delen av bröstet.
För armbågarna neråt och lätt bakåt.
Håll bröstet uppe.
Pausa kort när stången är nära bröstet.
Släpp kontrollerat tillbaka stången tills armarna är raka igen.$$, 'Pull', 1, 'lat_pull.jpg'),

('Bicepscurl med hantlar', $$Förberedelse:
Välj två hantlar.
Stå upp med en hantel i varje hand.
Placera fötterna ungefär höftbrett.

Hitta rätt startposition:
Håll armarna längs sidorna.
Låt handflatorna peka framåt eller inåt beroende på variant.
Spänn bålen lätt och håll ryggen neutral.
Håll armbågarna nära kroppen.
Håll axlarna avslappnade.

Utför övningen:
Andas in och böj armbågarna.
Lyft hantlarna uppåt mot axlarna.
Håll överarmarna stilla.
Spänn biceps kort i toppläget.
Sänk hantlarna kontrollerat tillbaka.
Undvik att svinga kroppen eller kasta upp vikterna.$$, 'Pull', 1, 'bicep_curl.jpg'),


('Knäböj (Squats)', $$Förberedelse:
Placera skivstången i ungefär axelhöjd.

Hitta rätt startposition:
Kliv under stången och placera den på övre delen av ryggen (inte nacken).
Ta tag i stången med båda händerna, lyft den och ta ett steg bakåt. Spänn din bröstrygg genom att trycka ner och ihop skulderbladen.
Stå med fötterna ungefär axelbrett, tårna lätt pekade utåt (Hållningen kan variera då det beror på individens anatomi och rörlighet).

Utför övningen:
Andas in och spänn din core (bålen).
Börja med att trycka höfterna bakåt, böj sedan knäna för att sänka kroppen.
Håll en neutral ryggrad under hela rörelsen.
Böj dina ben tills dina höfter är i eller under knähöjd (djupet kan variera beroende på rörlighet).
Tryck tillbaka upp genom hälarna och sträck ut benen och höfterna.$$, 'Legs', 3, 'squats.jpg'),

('Benpress', $$Förberedelse:
Sätt dig i benpressmaskinen.
Placera ryggen stadigt mot ryggstödet.
Ställ in maskinen så att du kan röra dig kontrollerat.

Hitta rätt startposition:
Placera fötterna på plattan ungefär axelbrett.
Låt tårna peka lätt utåt vid behov.
Justera sitsen så att du kan böja benen utan att bäckenet lyfter.
Greppa handtagen och spänn bålen lätt.
Håll knäna i linje med tårna.

Utför övningen:
Andas in och sänk vikten kontrollerat.
Böj knäna och gå ner så djupt du kan med god kontroll.
Undvik att ländryggen rundas.
Pressa plattan tillbaka upp genom hela foten.
Sträck ut benen utan att låsa knäna hårt.
Behåll ryggen mot ryggstödet.$$, 'Legs', 2, 'legpress.jpg'),

('Utfall med hantlar', $$Förberedelse:
Välj två hantlar.
Stå upprätt med en hantel i varje hand.
Placera fötterna ungefär höftbrett.

Hitta rätt startposition:
Låt armarna hänga längs sidorna.
Spänn bålen och håll bröstet uppe.
Håll blicken framåt.
Håll ryggen neutral.
Stå stabilt innan du tar steget framåt.

Utför övningen:
Andas in och ta ett kontrollerat steg framåt.
Sänk kroppen genom att böja båda knäna.
Gå ner tills det bakre knät nästan nuddar golvet.
Håll främre knät i linje med tårna.
Tryck dig tillbaka upp genom främre foten.
Återgå till startpositionen och upprepa med andra benet.$$, 'Legs', 2, 'lunge_with_dumbells.jpg'),

('Liggande Lårcurl', $$Förberedelse:
Lägg dig med magen mot bänken i lårcurlmaskinen.
Justera maskinen så att dynan ligger strax ovanför hälarna.
Se till att knäleden hamnar i linje med maskinens rotationspunkt.

Hitta rätt startposition:
Greppa handtagen.
Håll höfterna stabila mot bänken.
Spänn bålen lätt.
Håll benen nästan raka i startläget.
Undvik att lyfta höfterna från bänken.

Utför övningen:
Andas in och böj knäna.
Dra hälarna mot sätet.
Håll höfterna nere mot bänken.
Pausa kort i toppläget och spänn baksida lår.
Sänk vikten kontrollerat tillbaka.
Sträck benen nästan helt i bottenläget.$$, 'Legs', 1, 'lying_thigh_curl.jpg'),

('Sittande Vadpress', $$Förberedelse:
Sätt dig i maskinen.
Placera främre delen av fötterna på fotplattan.
Placera dynan över låren, strax ovanför knäna.
Justera höjden så att hälarna kan röra sig fritt.

Hitta rätt startposition:
Håll ryggen neutral.
Greppa handtagen.
Spänn bålen lätt.
Håll fötterna stabilt på fotplattan.
Börja med hälarna i ett kontrollerat neutralt läge.

Utför övningen:
Andas in och sänk hälarna kontrollerat.
Gå så långt ner du kan utan att tappa kontrollen.
Känn en stretch i vaderna i bottenläget.
Pressa upp hälarna så högt som möjligt.
Pausa kort i toppläget och spänn vaderna.
Sänk långsamt tillbaka till bottenläget.
Undvik att studsa i rörelsen.$$, 'Legs', 1, 'seated_calf_raise.jpg');