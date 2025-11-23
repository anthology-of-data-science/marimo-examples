default: build serve

build:
    python3 build.py

serve:
    python3 -m http.server --directory _site