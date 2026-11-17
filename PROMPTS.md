# PROMPTS.md – tärkeimmät agenttipromptit

Alla olevat promptit ovat tehtävän vaiheistuksen mukainen esimerkkiloki. Lisää omat havaintosi, kun käytät opencodea.

## 1. Suunnittelu (Plan)
> Lue weather.py. Suunnittele Python-sovellus, jossa on Flask-palvelin, yksinkertainen index.html-chat ja tool use -työkalu web_search, joka hakee curlilla. Käytä samaa openai-kirjastoa, OpenRouteria ja mallia kuin weather.py:ssä. Älä kirjoita vielä koodia. Listaa tiedostot, funktiot ja toteutusjärjestys pieninä testattavina askelina.

Huomio: suunnitelman tulee erottaa hakufunktio, mallin työkalusilmukka ja käyttöliittymä.

## 2. Hakufunktio
> Toteuta search.py, jossa on funktio web_search(query, max_results=5). Käytä subprocess.run-kutsua listamuodossa ilman shell=True-asetusta, URL-enkoodaa hakusana ja aseta curlille aikaraja. Palauta lista sanakirjoja {title, url}. Lisää __main__-lohko testausta varten.

Huomio: tarkista erityisesti komentoinjektiosuojaus ja virhetilanteet.

## 3. Tool use -silmukka
> Tee chat_core.py, jossa on funktio chat(messages). Se kuvaa web_search-työkalun mallille, suorittaa työkalukutsut ja kutsuu mallia uudelleen, kunnes tulee tekstivastaus (enintään 5 kierrosta). Tulosta konsoliin aina, kun työkalua kutsutaan.

Huomio: varmista, että assistant-työkalukutsu ja työkalun tulos lisätään keskusteluhistoriaan oikealla tool_call_id-tunnisteella.

## 4. Flask-rajapinta
> Tee app.py (Flask), joka tarjoaa index.html:n ja POST /api/chat -rajapinnan chat_core.chat-funktion päälle. Palauta virheet JSON-muodossa. Palvelimen pitää kuunnella vain 127.0.0.1-osoitetta.

Huomio: tarkista, ettei API-avain päädy selaimelle.

## 5. Käyttöliittymä
> Tee yksi index.html ilman kehyskirjastoja: viestilista, tekstikenttä, Lähetä-nappi, Enter lähettää. Säilytä keskusteluhistoria selainistunnossa, näytä haun hakusana ja tee vastausten URL-osoitteista klikattavia.

Huomio: lisää sisältö DOM-solmuina, älä käytä innerHTML:ää mallin vastaukseen.

## 6. Turvatarkastus ja testaus
> Tarkista koko projekti tehtävän turvallisuustaulukkoa vasten: komentoinjektio, prompt injection, aikarajat, vastausten kokorajat, API-avaimen suojaus ja paikallinen bind-osoite. Aja testit ja listaa puutteet. Älä väitä testanneesi ominaisuuksia, joita et oikeasti suorittanut.

Huomio: kirjaa tähän omat havaintosi ja mahdolliset korjaukset.
