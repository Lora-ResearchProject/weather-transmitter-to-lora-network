# Weather Transmitter To LoRa Network

## Description

Because the LoRa network cannot transmit large weather data packets over long distances, this simple algorithm converts the data into a compact format ready for transmission.

## Working Flow

Request -> OpenWeatherAPI -> OpenAI API -> response

## Installation

### For macOs:

1. Rename .example.env file into .env and fill the reqeusted configuration within the file
2. Create python virtual environment `python3 -m venv venv`
3. Active the virtual environment `source venv/bin/activate`
4. Command to diactivate the virtual environment (if needed) `deactivate`
5. Install all the dependencies `pip install -r requirements.txt`
6. Start the server `uvicorn app.main:app --reload`

### Other commands:

1. Generate the requirements.txt file `pip freeze > requirements.txt`

## API Integration

## Error Handling

## Deployment

## Current Deployemnt
