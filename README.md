The brick breaker flash game "Bernds Albtraum" offered functionality to collect global highscores on its servers. Since these have been shut down, this python script provides a crude re-implementation of this highscore ranking functionality.

The game was available [here](http://www.kika.de/spielspass/spielen/alle_spiele/cbb_breakout/popup.shtml) and can still be found on [archive.org](https://archive.org).

By running the game locally from its swf file using the Flash Player emulator [Ruffle](https://ruffle.rs) you can specify a base url for outgoing http requests. Inserting a url pointing to your score server will make the game fetch and submit scores to and from your own server instance, e.g.:
```sh
ruffle --base "http://localhost:8000" breakout.swf
```
