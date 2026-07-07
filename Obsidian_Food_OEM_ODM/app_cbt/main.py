from app import app

__all__ = ["app"]


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8010, debug=False)
