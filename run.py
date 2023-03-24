# import logging

from dotenv import load_dotenv

from app import app

if __name__ == "__main__":
    load_dotenv()
    # logging.basicConfig(filename='server.log', level=logging.INFO)
    # logging.info("Starting server")
    app.run()
