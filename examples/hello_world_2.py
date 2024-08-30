import shinybroker as sb

# Create an instance of a ShinyBroker App object using the default ui and server
app = sb.sb_app(
    host='127.0.0.1',  # localhost TWS is being served on your local machine
    port=7497,         # make this match the port in your API Settings config
    client_id=10742    # picked at random, choose another Client ID if preferred
)

# Run the app
app.run()
