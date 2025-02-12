# Weather Transmitter To LoRa Network

## Description

LoRa networks are optimized for low-power, long-range communication and therefore impose strict limits on packet sizes. This algorithm overcomes that limitation by extracting only the essential weather information—such as overall conditions, humidity, and cloud coverage—and compressing it into a compact format. This streamlined data package ensures that critical weather updates can be transmitted efficiently over long distances without overwhelming the network or draining device power.Because the LoRa network cannot transmit large weather data packets over long distances, this simple algorithm converts the data into a compact format ready for transmission.

## Working Flow

The working flow begins when the API receives the latitude and longitude, triggering a call to the OpenWeather API to fetch current weather data. Once received, the algorithm filters out non-essential information, extracting only critical fields such as the main weather condition, description, cloud coverage, and humidity. This streamlined data is then formatted into a concise message and sent to the ChatGPT API with a prompt asking for a rain likelihood percentage. The response is checked for the correct percentage format; if it meets the criteria, the value is returned, otherwise, the system retries before ultimately returning an error if a valid response cannot be obtained.

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

### Get the rain percentage

- **Endpoint: POST /weather-check**
- This API endpoint use to get the currnet rain presentage of the specific location
- Query Parameters:

  - `lat`: latitude
  - `lon` : longitude

- Query parameter Examples:

  ```
  /weather-check?lat=44.34&lon=10.99
  ```

- Response:

  - Success:

    ```
    {"rain_percentage":"0%"}
    ```

  - Faliure:

    ```
    {
      "detail": "Both 'lat' and 'lon' query parameters are required."
    }
    ```

## Error Handling

- **400 Bad Request:** Return when input data is invalid (e.g., incorrect format).
- **500 Internal Server Error:** Returned for unexpected server-side issues.

## Compatible versions

## Deployment

- Make the Docker environment
- Clone the repository
- Build the following command to build the service:

  ```
  docker build -t fishing-hotspots-api .
  ```

- Run the docker image

  - The port number might be change

  ```
  docker run -d -p 9003:9003 fishing-hotspots-api
  ```

- Check the status of the container

  ```
  docker ps
  ```

## Current Deployemnt

`http://159.223.194.167:9003/`
