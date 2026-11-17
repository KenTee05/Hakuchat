# Hakuchat – Nemotron + verkkohaku

Pieni selainchat, jossa OpenRouterin kautta käytetty Nemotron-malli päättää, milloin se tarvitsee verkkohakua. Hakutyökalu käyttää `curl`-komentoa ja DuckDuckGon HTML-hakua.

## Vaatimukset

- Python 3.10 tai uudempi
- `curl`
- OpenRouter API-avain
- Verkkoyhteys hakua ja mallikutsuja varten

## Asennus Linuxissa / WSL2:ssa

```bash
sudo apt update
sudo apt install -y curl python3 python3-venv
mkdir -p ~/projektit/hakuchat
cd ~/projektit/hakuchat
# Kopioi projektin tiedostot tähän kansioon.
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Aseta API-avain nykyiseen terminaali-istuntoon (älä kirjoita sitä lähdekoodiin):

```bash
export OPENROUTER_API_KEY="OMA_OPENROUTER_API_AVAIN"
```

Käynnistä sovellus:

```bash
python app.py
```

Avaa selaimessa <http://127.0.0.1:5000>. Lopeta palvelin terminaalissa näppäinyhdistelmällä `Ctrl+C`.

## Testaus

Aja yksikkötestit projektin juuressa:

```bash
python -m unittest discover -s tests -v
```

Testaa hakufunktiota erikseen:

```bash
python search.py "Python asyncio"
```

Chatin testisyötteet:
1. `Mikä on rekursio?` – mallin pitäisi vastata ilman hakua.
2. `Etsi linkkejä aiheesta Python asyncio` – mallin pitäisi käyttää verkkohakua.
3. `Etsi vielä suomenkielisiä` – jatkokysymyksen pitäisi hyödyntää keskusteluhistoriaa.
4. Kokeile verkkoyhteyden katketessa – sovelluksen pitäisi kertoa haun epäonnistumisesta kaatumatta.

Komennon turvallisuuden voi tarkistaa myös hakusanalla `test; touch /tmp/hakkeroitu`. Hakusana käsitellään yhtenä URL-enkoodattuna argumenttina, eikä sen pidä luoda tiedostoa `/tmp/hakkeroitu`.

## Miten tool use -silmukka toimii?

1. `chat_core.py` lähettää mallille keskusteluhistorian ja `web_search`-työkalun JSON-skeeman.
2. Malli voi vastata suoraan tekstillä tai palauttaa `tool_calls`-pyynnön. Malli ei itse suorita curlia.
3. Jos malli pyytää hakua, Python-ohjelma tarkistaa työkalun nimen ja argumentit.
4. `search.py` muodostaa URL-osoitteen URL-enkoodatusta hakusanasta ja suorittaa curlin `subprocess.run`-kutsulla argumenttilistana. `shell=True`-asetusta ei käytetä.
5. Hakutuloksen otsikot ja URL-osoitteet palautetaan mallille `role: "tool"` -viestissä samalla `tool_call_id`-tunnisteella.
6. Mallia kutsutaan uudelleen. Silmukka päättyy tekstivastaukseen tai viimeistään viiden työkalukutsukierroksen jälkeen.

Selain pitää saman välilehden keskusteluhistorian JavaScript-muuttujassa ja lähettää historian palvelimelle jokaisessa pyynnössä. API-avain pysyy Python-palvelimella.

## Tietoturva ja rajoitteet

- API-avain luetaan vain `OPENROUTER_API_KEY`-ympäristömuuttujasta.
- `.env`, `.venv` ja välimuistit on rajattu pois Gitistä.
- Haku käyttää `subprocess.run([...])`-argumenttilistaa, ei komentorivin merkkijonoa eikä `shell=True`-asetusta.
- Hakusana URL-enkoodataan; curlin aikaraja on 10 sekuntia ja Pythonin vararaja 12 sekuntia.
- Hakutulosten määrä, hakusanan pituus ja otsikoiden pituus rajataan.
- System-viesti käskee mallia käsittelemään hakutuloksia epäluotettavana datana.
- Palvelin kuuntelee vain `127.0.0.1`-osoitteessa.
- Käyttöliittymä ei lisää mallin vastausta HTML:nä, vaan tekstisolmuina; linkit avataan `noopener noreferrer`-asetuksilla.

DuckDuckGo voi rajoittaa automaattisia pyyntöjä tai muuttaa HTML-rakennetta. Silloin hakutulosten jäsennintä voi joutua päivittämään tai vaihtamaan hakulähteen Wikipedian haku-APIin.

## Tiedostot

- `app.py` – Flask-palvelin ja `/api/chat`-rajapinta.
- `chat_core.py` – OpenRouter-yhteys ja enintään viiden kierroksen tool use -silmukka.
- `search.py` – curl-pohjainen verkkohaku ja tulosten jäsennys.
- `static/index.html` – käyttöliittymä ilman kehyskirjastoja.
- `AGENTS.md` – projektin toteutus- ja turvallisuussäännöt.
- `PROMPTS.md` – vaiheistetut agenttipromptit.
- `tests/test_search.py` – hakutulosten jäsentimen yksikkötestit.

Reflektio
Agentin virhe tai huono ratkaisu: [Kuvaa konkreettinen tilanne, mitä agentti ehdotti, miten huomasit ongelman ja miten korjasit sen.]
Ongelma oli etten kotona saanut syistä ladattua pythonille uutta päivitystä terminaalissa. laitoin virhe tekstin ai:lle se ehdotti mitä piti tehdä mutta antoi koko ajan melkeinpä samaa korjaus tapaa joka ei toiminut eli käski asentaa uudelleen terminaalissa. Ongelman siis huomasin päivitystä ladattaessa ja korjasin tilanteen vaihtamalla kotiverkosta puhelimen mobiili verkko jakoon ja sitten toimi oikein
Oma ymmärrys: [Kerro, mikä koodin osa tuntuu vaikeimmalta ja miten aiot opetella sen.]
Omasta mielestäni searc ja chat core ovat vaikeimmat. Aion ainakin etsiä netistä tietoa ja pistämällä AI:lle koodin ja selittää kohta kohdalla miten osat toimi
Oppiminen: [Vertaa agentin ohjaamista siihen, että olisit kirjoittanut koodin itse. Anna konkreettinen esimerkki.]vat ja miten ne yhdistyvät toisiiinsa.
Agentin ohjaamana koodin rakentaminen on helpompaa mutta se pitää lukea läpi huolella mutaa kun itse kirjoittaa asia jää paremmin muistiin vaikka sekin pitää katsoa
läpi virheitä varten
Haun valinta: [Kuvaa, milloin malli haki ja milloin vastasi ilman hakua. Oliko valinta mielestäsi järkevä?]
malli haki kun siltä kysyi hakemaan netistä kuin taas jos tiedosto oli olemassa tiedostossa se haki sen ja otti sieltä tiedot. Valinta on mielestäni melko järkevä.

