# Product_reviews_in_czech

FIT VUT <br />
KNOT@FIT - Knowledge Technology Research Group - KNOT <br />

= Product_reviews_in_czech =
__NOTITLE____NOTOC__
__TOC__

<!-- Začátek automaticky generované sekce --><!-- ID: 1134 -->
__FORCETOC__

= Úvod =

Cílem projektu je stáhnou veškeré recenze výrobků z webové stránky zboží.cz a převést je do jednotného formátu.

= Řešení =

Řešení je rozděleno do 3 skriptů, první '''categories_url_downloader.py''' stáhne veškeré URL jednotlivých kategorií(např: https://www.zbozi.cz/domaci-spotrebice/). Druhý '''products_url_downloader.py''' projde tyto kategorie a stáhne veškeré url jednotlivých výrobků(např: https://www.zbozi.cz/vyrobek/sencor-sac-mt9021c/) z webu a poslední '''review_downloader.py''' stáhne recenze z URL adres jednotlivých výrobků.

= Problematika webu =

Jelikož web zboží.cz pří rychlém scrapování dat ukončí komunikaci, tak se skripty(product_url_download.py a review_download.py) spouští na všech serverech KNOTU zároveň (athena1 ..athena20, knot1 ..30, minerva1 ..3 ), a to z důvodu velké časové náročnosti. Každý server má tedy svůj vstupní soubor, podle hostnamu serveru.

Ke spuštění stahovacích skriptů jsou použitý shell skripty využívající parallel ssh (paralel_ssh_run_product_download.sh, paralel_ssh_run_review_download.sh). Aby se programy neukončovaly při ukončení ssh spojení je použitá utilita tmux ve spouštěcích skriptech. (run_product_download.sh, run_review_download.sh)

= Soubory =

Soubory jsou rozděleny do logických celků, podle toho k jakému python skriptu se vztahují(categories, products, reviews).

Veškeré výstupní a vstupní soubory(logy) se nachází ve složce: 
   /mnt/minerva1/knot/projects/product_reviews_in_czech/logs_and_input_files
Chrome drivery různých verzí jsou ve složce:
    /mnt/minerva1/knot/projects/product_reviews_in_czech/drivers

@hostname == hostname serveru (př: minerva1)

== Categories url download ==

Stáhne veškeré kategorie z webu zboží.cz
   /mnt/minerva1/knot/projects/product_reviews_in_czech/categories_url_downloader.py

=== Výstupní soubory ===

Soubor obsahuje všechny kategorie webu. Je to výstupní soubor skriptu categories_url_downloader.py. Jednotlivé kategorie jsou odděleny znakem konce řádku.
   /mnt/minerva1/knot/projects/product_reviews_in_czech/logs_and_input_files/all_zbozi.cz_categories_url.log

== Product url download ==

Stáhne veškeré url adresy produktů, které web zboží.cz obsahuje. Skript je velmi časově náročný, čili se musí spouštět na všech serverech najednou, a k tomu slouží '''paralel_ssh_run_product_download.sh''' ten všude zapíná '''run_product_download.sh'''

Některé servery potřebovaly jinou verzi chrome driveru. Proto se verze driveru zadává jako parametr. '''python3 products_url_downloader.py 80''' spustí skript s chrome driverem verze 80
  /mnt/minerva1/knot/projects/product_reviews_in_czech/products_url_downloader.py

=== Vstupní soubory ===
   /mnt/minerva1/knot/projects/product_reviews_in_czech/logs_and_input_files/input_files_for_each_server/@hostname

=== Výstupní soubory ===
  /mnt/minerva1/knot/projects/product_reviews_in_czech/logs_and_input_files/all_zbozi.cz_products_url.log

== Review download ==

Stáhne všechny recenze jednotlivých výrobků a uloží ho do jednotného json formátu. Skript je časově náročný, čili se musí spouštět na všech serverech najednou, a k tomu slouží '''paralel_ssh_run_review_download.sh''' ten všude zapíná '''run_revew_download.sh'''

=== Vstupní soubory ===
  
   /mnt/minerva1/knot/projects/product_reviews_in_czech/logs_and_input_files/input_files_for_each_server_reviews/@hostname

=== Výstupní soubory ===
  /mnt/minerva1/knot/projects/product_reviews_in_czech/logs_and_input_files/all_zbozi.cz_reviews.log


Prochází jednotlivé odkazy a stáhne veškeré recenze
   '''/mnt/minerva1/knot/projects/product_reviews_in_czech/review_downloader.py'''

== Ostatní ==
=== Spouštěcí skripty ===

Pomocí parallel ssh spustí '''run_product_download.sh''' na všech serverech.
    /mnt/minerva1/knot/projects/product_reviews_in_czech/paralel_ssh_run_product_download.sh

Pomocí parallel ssh spustí '''run_review_download.sh''' na všech serverech.
    /mnt/minerva1/knot/projects/product_reviews_in_czech/paralel_ssh_run_review_download.sh

Přes program tmux spustí '''products_url_downloader.py'''.
    /mnt/minerva1/knot/projects/product_reviews_in_czech/run_product_download.sh

Přes program tmux spustí '''review_downloader.py'''.
    /mnt/minerva1/knot/projects/product_reviews_in_czech/paralel_ssh_run_review_download.sh

=== Line separator ===

Program slouží k zpracování velkých logů do jednotlivých vstupních souborů. (například rozdělí 30 000 odkazů na produkty mezi 30 serverů po 1000 odkazech)
 /mnt/minerva1/knot/projects/product_reviews_in_czech/line_separator.c
Makefile pro line_separator.c
 /mnt/minerva1/knot/projects/product_reviews_in_czech/Makefile
Generuje parametry spuštění programu line_separator.c pro každý server.
 /mnt/minerva1/knot/projects/product_reviews_in_czech/start_line_separator.sh
Výstup programu start_line_separator.sh, který lze spustit.
 /mnt/minerva1/knot/projects/product_reviews_in_czech/start_line_separator.sh_output

=== FINISH.sh ===

Měl by se zapnout po každém dokončení jednoho z programů. Nakopíruje veškeré logy a recenze na potřebná místa zálohuje je a odstraní duplicitu.
 /mnt/minerva1/knot/projects/product_reviews_in_czech/FINISH.sh

= Výstupní formát =

== Categories url download ==
Kategorie jsou odděleny znakem konce řádku.

   #url_kategorie\n
   https://www.zbozi.cz/dum-byt-a-zahrada/
   https://www.zbozi.cz/dum-byt-a-zahrada/zahrada/

== Product url download ==
Produkty mají url adresy označeny slovem výrobek př: "<nowiki>https://www.zbozi.cz</nowiki>/'''vyrobek'''/de-longhi-ecam-22-110-b/"

Ukládá se url výrobku a kategorie, ze které byl výrobek získán, to slouží pro jednoduší zapsaní do jednotného json formátu. Tyto dvě složky jsou odděleny znakem ';'

   #url_produktu'''';''''url_kategorie\n
   https://www.zbozi.cz/vyrobek/aveflor-arpalit-dog-elektronicky-repelent/;https://www.zbozi.cz/dum-byt-a-zahrada/
   https://www.zbozi.cz/vyrobek/bayer-foresto/?varianta=do-8-kg-38-cm;https://www.zbozi.cz/dum-byt-a-zahrada/

== Review download ==

Pro výstupní formu recenzí byl navrhnut JSON formát, jehož kostra vypadá následovně:

=== Formát recenze ===
<pre>
{
   "REVIEWS": [
      {
         "product": [
            {
               "review": {	
                  "author":"name_surname",
                  "date":"DD Month YYYY",
                  "rating":"XY%",
                  "pros":[],
                  "cons":[],
                  "summary":"some text",
                  "usefulness_of_review":["ANO (X)","NE (Y)"]
               }
            }, ...
         ]
      }, ...
   ]
}
</pre>

Popis jednotlivých prvků json formátu:

 "REVIEWS" - obsahuje seznam všech produktů
 "product" - název produktu + název kategorie, ve které je produkt nabízen
 "review"  - jednotlivá recenze obsahující všechny informace z diskuzního příspěvku
           - obsah všech složek závisí na vyplnění recenzentem, pokud nějakou položku nevyplnil, bude obsahovat hodnotu null
           - "author" - jméno autora
           - "date" - datum vytvoření příspěvku
           - "rating" - hodnocení produktu v %
           - "pros" - seznam všech kladů produktu
           - "cons" - seznam všech záporů produktu
           - "summary" - volný text vyjádření recenzenta k produktu
           - "usefulness_of_review" - užitečnost recenze z pohledu ostatních recenzentů označená palci nahoru nebo dolů



----
<!-- Konec automaticky generované sekce -->





Veškeré soubory jsou majetkem VUT


