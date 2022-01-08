from flask_ngrok import run_with_ngrok
import search_frontend as se


if __name__ == '__main__':
    run_with_ngrok(se.app)
    se.app.run()
