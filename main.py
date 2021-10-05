from src.website import create_app


def app():
    return create_app()


if __name__ == '__main__':
    app().run(debug=True, use_reloader=False, host='0.0.0.0', port=8000)
