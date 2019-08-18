#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2019 Märt Põder <tramm@wikimedia.ee>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import mwapi
from mwtypes import Timestamp

import datetime, time

from dataclasses import dataclass, asdict
from typing import List

@dataclass
class User:
    name: str
    participant: bool
    count: int

@dataclass
class Revision:
    id: int
    minor: bool
    size: int
    user: str
    time: datetime

@dataclass
class Article:
    id: int
    title: str
    #redirects: List[str]
    revisions: List[Revision]
    text: str
    size: int
    #media: List[str]
    #categories: List[str]
    author: str

@dataclass
class Contest:
    users: List[User]
    articles: List[Article]
    start: datetime
    end: datetime

def load_article(a):
    #print(a, cont.start, cont.end)
    pages = session.get(action='query', prop='revisions', titles=a, redirects="redirects", rvlimit=1, rvdir="newer")['query']['pages']
    if "-1" in pages:
        return
    page_id = next(iter(pages.values()))['pageid']
    
    first = session.get(action='query', prop='revisions', titles=a, redirects="redirects", rvlimit=1, rvdir="newer")['query']['pages'][str(page_id)]['revisions'][0]
    #print(first["user"], first["timestamp"])
    #print(first["user"], first["timestamp"])
    #print(first["user"], first["timestamp"])

    #print(session.get(action='query', prop='redirects', redirects="redirects", titles=a))    
    #print(session.get(action='query', prop='revisions', titles=a, redirects="redirects", rvlimit=1, rvstart=cont.end, rvprop="content|user|timestamp", rvslots="main", format="json", rvdir="older")['query']['pages'][str(page_id)])

    last = session.get(action='query', prop='revisions', titles=a, redirects="redirects", rvlimit=1, rvstart=cont.end, rvprop="content|user|timestamp|size", rvslots="main", format="json", rvdir="older")['query']['pages'][str(page_id)]['revisions'][0]
    #print(last["user"], last["timestamp"])
    
    revisions = []
    
    user_names = [users["name"] for users in asdict(cont)["users"]]
    #print(user_names)
    #print(cont.start, cont.end)
    chunks = session.get(action='query', prop='revisions', titles=a, redirects="redirects", rvprop='ids|user|timestamp|size|flags|tags', rvlimit=100, rvdir="newer", rvstart=cont.start, continuation=True)
    for chunk in chunks:
        if "revisions" in chunk['query']['pages'][str(page_id)]:
            revs = chunk['query']['pages'][str(page_id)]["revisions"]
            #print(revs["revid"])
            for rev in revs:
                if rev['timestamp'] > cont.end: # break on next chunks too
                    break
                if rev['user'] not in user_names:
                    #print("*", rev)
                    cont.users.append(User(rev['user'], False, -1))
                    user_names.append(rev["user"])
                #print(rev)
                revisions.append(Revision(rev["revid"],"minor" in rev, rev["size"], rev["user"], rev["timestamp"]))
                #revisions.append())

    #print(last["slots"]["main"]["*"])

    article=Article(page_id,a,revisions,last["slots"]["main"]["*"], last["size"], first["user"])
    cont.articles.append(article)

def get_user_articles(u):
    print("TODO")

session = mwapi.Session('https://et.wikipedia.org', "vagavesi bot <tramm@wikimedia.ee>")
token = session.get(action='query', meta='tokens', type="login")['query']['tokens']['logintoken']
session.post(action='login', lgname="Märt Põder@AndmeKaeveBot", lgpassword="7bnsl52b31r9860aa2l7u603192jtmfu", lgtoken=token)


#print(session.get(action='query', meta='userinfo'))

#maxrevs = session.get(action='query', prop='revisions', titles="Wiki", redirects="redirects", rvlimit="max")
#print(maxrevs)
#print(len(maxrevs['query']['pages']['1291']['revisions']))

cont = Contest([],[],"2018-01-28T20:32:09Z", "2019-08-15T20:53:50Z")

users = ["Kamma", 'Tunguuz', 'Antimust', "Punnivinn", "Alevtiina", "Andi.hektor", "Pkarro", "Notaator", "Sirkin23", "Urvastemiis", "Hans Krämer", "Martk83", "MKunnus", "Mare Kõiva", "Puumarju", "Birgylorenz", "Sillu12", "Endla", "AK720", "Tambetm", "Maakaru", "Velmaja", "Ullike", "Utvikipedist", "Proosamanna", "Nadosdelatsebenik", "Puik", "Taivop", "Fideelia", "Hsoosalu", "Vingianodepina", "Berkvaher", "MV", "Päevakoer", "Mat Petheny", "Els.heinsalu", "Dequodlibet", "AnniAet", "Katlakytja", "Trtrlp", "Andrus Kallastu", "Kristaaru", "Curious NW", "DoktorFaustus123", "Marie Krause", "Ulvarkaart", "Nobenäpp"]

for user in users:
    cont.users.append(User(user, True, -1))

to_load = [ "Ad hoc", "Agenda 2000", "Agrément", "Agressioon", "Ajalooline pärimus", "Ajutine asjur", "Alaline Vahekohus", "Aleksei Gastev", "Andrei Toporkov", "Andres Kuperjanov", "Andres Põldroo", "Anneksioon", "Arenguantropoloogia", "Arengupartei", "Asta Niinemets", "Atašee", "Benelux" ] #, "Carl Zeller", "Charles Gounod", "Cosmos, The journal of The Traditional Cosmology Society", "Daiva Vaitkevičienė", "David J Beerling", "David John Beerling", "De facto", "De iure", "Delirium Brothers", "Desarmeerimine", "Disputatsioon", "Dōgen", "Eduards Veidenbaums", "Eesti Komitee (Stockholm)", "Eesti lugu", "Eesti-uuringute tippkeskus", "Eesti Vabariigi pagulasvalitsus", "Ekspansioon", "Elmina Otsman", "Elurikkuse ja ökosüsteemi teenuste koostöökogu", "Elutempo sündroom", "Emanuela Timotin", "Emily Lyle", "Encore", "Enoshima", "Euroopa Nüüdiskeelte Keskus", "Feministeerium", "Ferenc Lehár", "Folklore", "Franz von Suppé", "Fred Raymond", "Fromental Halévy", "Gaetano Donizetti", "Galina Gluhhova", "Geomorfoloog", "Geoökoloog", "Giacomo Meyerbeer", "Gioachino Rossini", "Harálampos Passalís", "Harald Arman", "Helsingi Kodanike Komitee", "Hääl (muusika)", "Impressaario", "Imre Kálmán", "Incantatio", "Indoeuroopa algkeel", "Infoturbe põhimõisted", "Interluudium", "IORAN", "Irina Sedakova", "Irina Vinokurova", "Isemajandava Eesti ettepanek", "Itk", "Jacques Offenbach", "James Kapaló", "Jane Goodall", "Jenny Butler", "Jodokus Clodt von Jürgensburg", "Johan Huizinga", "Jordan Peterson", "Journal of the Baltic Institute of Folklore", "Jules Massenet", "Julius Made", "Juulilepped", "Kaitserüü", "Kaitsevägede ülemjuhataja", "Karl Lamprecht", "Keele Infoleht", "Keelesaade", "Kelti- ja Šoti-uuringute Kool", "KesKus", "Kęstutis Navakas", "Klassikaraadio", "Klaus Ferdinand Hasselmann", "Klaus Hasselmann", "Kolm tarka ahvi", "Komplekssüsteem", "Konfidentsiaalsus", "Kultuuriajaloolane", 'Kultuuriajalugu', "Käideldavus", "Küberolümpia", "Küllike Tohver", "Laavatunnel", "Laupäevak", "Leo Fall", "Loitsude, loitsimise ja loitsijate uurimise töörühm", "Luigi Bonardi", "Luigi Malerba", "Luise Vaher", "Luna 9", "Luna (kosmoseprogramm)", "Lääne-Euroopa Liit", "Lytton Strachey", "Maastikuökoloog", "Majandusantropoloogia", "Majandussanktsioonid", "Menandros", "Mirjam Mencej", "Mitmeplatvormne", "Muna ja kana probleem", "Muusikaarheoloogia", "Naised ettevõtluses", "Nikolai Anisimov", "Nikolai Anissimov", "Nikolay Anisimov", "NSV Liidu TA", "NSV Liidu TA Okeanoloogia Instituut", "NSV Liidu Teaduste Akadeemia Okeanoloogia Instituut", "Oktoberfest", "Olga Hristoforova", "Olga Sedakova", "Operett", "Oscar Straus", "Oskar Elevant", "Paleoklimatoloog", "Pat Metheny", "Paul Laan", "Pietro Mascagni", "Pikaealisuse piirkond", "Pildiraamat", "Piret Põldver", "Pitsat", "Pommtsüklon", "Põltsamaa Teataja", "Päästeliit", "Rahvusvaheline Etnoloogia ja Folkloori Selts", "Ralf Benatzky", "Robert Stolz", "Ruggero Leoncavallo", "Salgamatus", "Sator", "Saverio Mercadante", "Sigmund Romberg", "Simon Wanradt", "Slaavi vanavara: Etnolingvistiline sõnastik", "Spektrite püsisälkamine", "STARTUp HUB", "Startup Hub", "Širšovi-nimeline NSV Liidu Teaduste Akadeemia Okeanoloogia Instituut", "Širšovi-nimeline okeanoloogia instituut", "Širšovi-nimeline Venemaa Teaduste Akadeemia Okeanoloogia Instituut", "Živaja Starina", "Tarkuse püramiid", "Tatjana Panina", "Tatjana Vladõkina", "Teet Velling", "Theater an der Wien", "The Traditional Cosmology Society", "Tiit Kukk", "Tiiu Talvistu", "Tuule kõrts", "Vallo Kalamees", "Vastastikuse Majandusabi Nõukogu", "Vastastikusus", "Verism", "Vincenzo Bellini", "VOSK", ]

for article in to_load:
    load_article(article)

for a in cont.articles:
    rev_users = []
    for r in a.revisions:
        if r.user not in rev_users:
            rev_users.append(r.user)
    print(a.title, a.size, len(a.revisions), len(rev_users), rev_users)

print("===")

for u in cont.users:
    printed = False
    count = 0
    for a in cont.articles:
        if a.author == u.name:
            if not printed:
                print(u.name)
                printed = True
            print(" -", a.title)
            count += 1
    u.count = count




#print(cont)

exit(1)


# https://et.wikipedia.org/wiki/Eesti?action=raw
# https://et.wikipedia.org/w/api.php?action=query&titles=Eesti&prop=revisions&rvprop=content&format=json
# https://et.wikipedia.org/w/api.php?action=query&titles=Eesti&prop=revisions&rvprop=content&rvslots=main&format=json










article = revs['query']['pages']['1291']['title']
#print(article)

first = session.get(action='query', prop='revisions', titles="Wiki", redirects="redirects", rvlimit=1, rvdir="newer")['query']['pages']['1291']['revisions'][0]

#print(first["user"], first["timestamp"])

#print(Timestamp(first["timestamp"]))

for rev in revs['query']['pages']['1291']['revisions']:
    user = rev["user"]
    if user not in cont.users:
        cont.users.append(user)
    #print(rev)

print(cont.users)
