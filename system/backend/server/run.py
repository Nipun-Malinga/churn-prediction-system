from application import create_app

# Turn the debugger False or remove it before push to the production.
# If not this cause issues for the custom error handlers
if __name__ == '__main__':
    create_app().run(debug=True, threaded=True)