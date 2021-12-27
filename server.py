#!/usr/bin/python3

import argparse
from contextlib import contextmanager
import http.server
from pathlib import Path
import shutil
import socketserver


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()
    
    def send_head(self):
        if self.path.endswith(".zip"):
            path = Path(self.path)
            if str(path).startswith("/"):
                path = Path("." + str(path)).resolve()

            shutil.make_archive(path.with_suffix(""), "zip", root_dir=path.parent)

        return super().send_head()



def make_parser(parser):
    parser.description = "Start a server"
    parser.add_argument(
        "--port", action="store", type=int, default=8000, help="choose the port"
    )
    return parser


@contextmanager
def server(port):
    httpd = socketserver.TCPServer(("", port), Handler)
    try:
        yield httpd
    finally:
        httpd.shutdown()


def main(args):
    port = args.port
    with server(port) as httpd:
        print(f"serving from {Path(__file__).resolve().parent} at http://localhost:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    parser = make_parser(argparse.ArgumentParser())
    args = parser.parse_args()
    main(args)
