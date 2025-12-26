from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from dict2xml import dict2xml
from collections import OrderedDict
import json

Host = "localhost"
Port = 8000
Badwords_nickname = []
Badwords_city = []
HighscoresFileName = "highscores.json"


def sortHighScores():
    global highscores
    highscores.sort(key=lambda d: d["points"], reverse=True)

def createHighscoreListEntry(position, nickname, age, city, points):
    return OrderedDict([
        ("position", position),
        ("nickname", nickname),
        ("age", age),
        ("city", city),
        ("points", points)
    ])

highscores = []
try:
    with open(HighscoresFileName, "r") as highscoreFile:
        highscores = json.load(highscoreFile)
except FileNotFoundError:
    pass
sortHighScores()


class BerndServer(BaseHTTPRequestHandler):
    def do_GET(self):
        response = OrderedDict([
            ("data", 
                OrderedDict(
                    [
                        ("success", str(True).lower()),
                        ("quantity", len(highscores)),
                    ] 
                        +
                    [
                        (F"entry{i}", createHighscoreListEntry(i+1, **v)) for i,v in enumerate(highscores[0:100])
                    ]
                )
            )
        ])
        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(dict2xml(response, newlines=False).encode())
    
    def do_POST(self):
        entry = self.readHighScoreSubmissionPost()

        badword_nickname = any(b in entry["nickname"] for b in Badwords_nickname)
        badword_city     = any(b in entry["city"] for b in Badwords_city)

        response = OrderedDict([
            ("data",
                OrderedDict([
                    ("success",          str(not badword_nickname and not badword_city).lower()),
                    ("badword_nickname", str(badword_nickname).lower()),
                    ("badword_city",     str(badword_city).lower()),
                ])
            )
        ])
        if not badword_nickname and not badword_city:
            highscores.append(entry)
            sortHighScores()
        
        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(dict2xml(response, newlines=False).encode())

    def readHighScoreSubmissionPost(self):
        content_length = int(self.headers.get('Content-Length', 0))
        raw_data = self.rfile.read(content_length)
        form_data = parse_qs(raw_data)
        return {
            "points":   int(form_data[b"points"]  [0].decode()),
            "city":         form_data[b"city"]    [0].decode() ,
            "age":      int(form_data[b"age"]     [0].decode()),
            "nickname":     form_data[b"nickname"][0].decode()
        }


if __name__ == "__main__":
    webServer = HTTPServer((Host, Port), BerndServer)
    print(F"Server started http://{Host}:{Port}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        json.dump(highscores, open(HighscoresFileName, "w"))
        print("Scores saved")

    webServer.server_close()