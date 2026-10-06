"""Build and preview the website. Run this file directly in PyCharm."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser

from build_site import build_site


if __name__ == "__main__":
    input_dir = Path(__file__).resolve().parent
    output_dir = input_dir / "site"
    host = "127.0.0.1"
    port = 8000
    open_browser = True

    build_site(input_dir, output_dir)
    handler = partial(SimpleHTTPRequestHandler, directory=str(output_dir))
    with ThreadingHTTPServer((host, port), handler) as server:
        url = f"http://{host}:{port}/"
        print(f"Preview: {url}\nStop the run in PyCharm or press Ctrl+C to close the server.")
        if open_browser:
            webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nPreview stopped.")
