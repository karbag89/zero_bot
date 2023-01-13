import routes
from api import create_app
from helpers.err_helper import Error
import bot

app = create_app()
app.register_blueprint(routes.bp)

# Handling error code 400.
@app.errorhandler(400)
def bad_request(e):
    app.logger.error({"message": e})
    return Error.errorMessage(400, "Bad Request!")


# Handling error code 404.
@app.errorhandler(404)
def page_not_found(e):
    app.logger.error({"message": e})
    return Error.errorMessage(404, "Page not found!")


# Handling error code 500.
@app.errorhandler(500)
def page_not_found(e):
    app.logger.error({"message": e})
    return Error.errorMessage(500, "Internal Server Error.")



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
