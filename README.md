# vagavesi
Still waters run deep, that's why we need to visualize Wikipedia article contest results

## Why?

Visualisation is to give people overview of what happened during article contest or editathon and present it in an appealing way. This is also to present the contest for media in press releases. So not exactly metrics, but more a tailored insight into the event in data story style.

## Project status

Started to write clean code during [Wikimedia Hackathon 2019 in Prague](https://phabricator.wikimedia.org/T216260). The dirty code was written to visualise results of [EV100 anniversary contest](https://ev100.miljonpluss.ut.ee/).

* Phabricator task for Wikimania 2019 hackathon: https://phabricator.wikimedia.org/T230464
* Example input data: https://infoaed.ee/vagavesi/data.json
* Example visualisation: https://infoaed.ee/vagavesi
* Wikimandia hackathon showcase presentation: https://youtu.be/SomTEzaoROQ?t=2440

## TODO

## Gather and structure useful data

Gather data from Wikimedia API on users, articles and everything that might be interesting to present. [Dirty code from 2018](https://gist.github.com/boamaod/2e2ad993059d10ee42b8ca43fc0c7f41) and some ideas:

* amount of changes by participant
* amount of changes by others
* amount of changes by other participants
* length of changes in bytes
* length of changes in actual text
* changes in wiki extras (like infoboxes)
* instances of multimedia files used
* amount of articles by participant
* new articles by participants
* amount of edits to other articles
* interactions in discussion pages
* declared categories
* harvested categories
* thankyous?!
* importance of articles
  - in other wikis
  - in special article lists (ccc)
  - most wanted lists
  - most referred
* experience of users
  - when registered
  - monthly edits
  - total new articles
  - total text
* multimedia used
* keyword clouds
* geographical of articles
* geographical locations mentioned (or persons connected)
* articles about persons?
* persons mentioned (male/female?)
* amount of references
* minor revisions
* revision messages!!!
* disputed references, neutrality etc
  - for participant
  - by participant

### Visualise it in customisable manner

Visualise the data using any of the common visualisation framworks. See [test visualisation in D3](https://ottmartens.github.io/Wiki-visuals-v2/).
