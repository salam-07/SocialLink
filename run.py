# run this file to serve application for development and testing locally

from sociallinkapp import app

if __name__ == "__main__":
    # The app will run on port 5000 on all interfaces, in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)