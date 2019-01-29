import falcon
import json
import wsd2

class CORSMiddleware:
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')

class WSD2Resource:
    def on_post(self, req, resp):
        data = req.stream.read()
        score = wsd2.calc_song_score(data.decode("utf-8"))
        resp.body = json.dumps(score, ensure_ascii=False)

app = falcon.API(middleware=[CORSMiddleware()])
app.add_route('/', WSD2Resource())

if __name__ == "__main__":
    from wsgiref import simple_server

    httpd = simple_server.make_server("0.0.0.0", 8000, app)
    httpd.serve_forever()
