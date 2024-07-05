# news_factory_server

**news_factory_server** is a robust Python-based server template designed to dynamically serve Forex News Event iCal calendar files. 

It leverages Flask for the web framework and supports flexible endpoint configurations via JSON files. Key features include:

- **Dynamic Calendar Updates**: Automatically updates calendar data in response to file changes.
- **Flexible Configuration**: Supports configurable endpoints via JSON files.
- **Real-Time Data**: Ideal for applications requiring real-time calendar updates.
- **Command-Line Interface**: Easy-to-use command-line interface for configuration.
- **Comprehensive Configuration Options**: Allows for extensive customization and setup.

This project serves as a foundational template for building sophisticated calendar-based applications.

See sister project [news_factory](https://github.com/kjpou1/news_factory) for generating forex news events.

## Table of Contents

- [news_factory_server](#news_factory_server)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command Line Arguments](#command-line-arguments)
    - [Examples](#examples)
  - [Configuration](#configuration)
  - [Shell Script](#shell-script)
    - [Shell Script Examples](#shell-script-examples)
    - [Running the Shell Script](#running-the-shell-script)
  - [License](#license)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/project_name.git
    cd project_name
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set environment file**

    Copy or rename the `example_env` file to `.env` before running

    ```bash
    cp example_env .env
    ```

## Usage

To run the server, use the provided `run.py` script with appropriate command-line arguments.

### Command Line Arguments

- `--server` or `-s`: Server host (default: `0.0.0.0`).
- `--port` or `-p`: Server port (default: `8036`).
- `--config` or `-c`: Path to the configuration JSON file (required).

### Examples

To run the program with a specific configuration file:

```bash
python run.py --config /path/to/config.json
```

## Server Configuration

The configuration settings are managed through environment variables and can be set in a `.env` file in the root directory of the project. 
Example `.env` file:

``` 
SERVER_HOST=0.0.0.0
SERVER_PORT=8036
```

> [!NOTE]
> An `example_env` file is provided to get started.  Copy the file to `.env` before running:

## Endpoint Configuration

The `EndPoint` configuration settings are managed through a JSON configuration file. Each configuration entry specifies an endpoint, the description, and the file path to the data.

Example configuration file (config.json):

```json
{
    "configurations": [
        {
            "name": "today",
            "description": "Today's event data",
            "end_point": "today.ics",
            "file": "/path/to/calendar_data_today_cleaned_data.json"
        },
        {
            "name": "today_nnfx",
            "description": "Today's event data with NNFX filter",
            "end_point": "today_nnfx.ics",
            "file": "/path/to/calendar_data_today_nnfx_cleaned_data.json"
        }
    ]
}
````

Place the configuration file in the desired location and provide its path using the `--config` argument when running the server.

## URL Endpoints, Filters, and Query Parameters

> [!NOTE]
> The URL Endpoints used and referenced below come from the example config mentioned above.

> [!IMPORTANT]
> The URL Endpoints used and referenced below do not exist by default and are here only as documentation purposes from the example config above.


### URL Endpoints

#### `today.ics` Endpoint

**URL:** `/today.ics`

**Description:** Serves the iCal calendar for today's events.

**Curl Command:**

```bash
curl -X GET "http://localhost:8036/today.ics"
```

#### `today_nnfx.ics` Endpoint

**URL:** `/today_nnfx.ics`

**Description:** Serves the iCal calendar for today's events with NNFX filter.

**Curl Command:**

```bash
curl -X GET "http://localhost:8036/today_nnfx.ics"
```

## Filters and Query Parameters

All dynamically generated endpoints support query parameters for filtering the events based on currencies, impact classes, and calendar implementation.

### Query Parameters

- **`currencies`**: Comma-separated list of currency codes (e.g., `AUD,GBP`).
- **`impact-classes`**: Comma-separated list of impact classes (e.g., `yellow,red`).
- **`implementation`**: Specifies which library to use for formatting the calendar. Accepted values are `ical` and `icalendar`. Default is `icalendar`.

### `currencies` Parameter

The `currencies` parameter filters events by the specified currencies. The accepted values are:

- `AUD` (Australian Dollar)
- `CAD` (Canadian Dollar)
- `CHF` (Swiss Franc)
- `EUR` (Euro)
- `GBP` (British Pound)
- `JPY` (Japanese Yen)
- `NZD` (New Zealand Dollar)
- `USD` (United States Dollar)

**Example Curl Command:**

```bash
curl -X GET "http://localhost:8036/today.ics?currencies=AUD,GBP"
```

### `impact-classes` Parameter

The `impact-classes` parameter filters events by the specified impact classes. The accepted values are:

- `yellow` (Low Impact)
- `orange` (Medium Impact)
- `red` (High Impact)
- `gray` (Non-Economic)

**Example Curl Command:**

```bash
curl -X GET "http://localhost:8036/today.ics?impact-classes=yellow,red"
```

### `implementation` Parameter

The `implementation` parameter specifies which library to use for formatting the calendar. The accepted values are:

- `ical` (uses the `ical` library to format the calendar)
- `icalendar` (uses the `icalendar` library to format the calendar)
- Default: `icalendar`

**Example Curl Command:**

```bash
curl -X GET "http://localhost:8036/today.ics?implementation=ical"
```

### Combined Filters

You can combine `currencies`, `impact-classes` parameters to filter events based on multiple criteria.

**Example Curl Command:**

```bash
curl -X GET "http://localhost:8036/today.ics?currencies=AUD,GBP&impact-classes=yellow,red&implementation=ical"
```

## Example Configurations

### Configuration Snippet for `today.ics`

```json
{
    "configurations": [
        {
            "name": "today",
            "description": "Today's event data",
            "end_point": "today.ics",
            "file": "/path/to/calendar_data_today_cleaned_data.json"
        }
    ]
}
```

### Configuration Snippet for `today_nnfx.ics`

```json
{
    "configurations": [
        {
            "name": "today",
            "description": "Today's event data",
            "end_point": "today.ics",
            "file": "/path/to/calendar_data_today_cleaned_data.json"
        },
        {
            "name": "today_nnfx",
            "description": "Today's event data with NNFX filter",
            "end_point": "today_nnfx.ics",
            "file": "/path/to/calendar_data_today_nnfx_cleaned_data.json"
        }
    ]
}
```

## Full Example Curl Commands

1. **Simple Request:**

   ```bash
   curl -X GET "http://localhost:8036/today.ics"
   ```

2. **Request with Currency Filter:**

   ```bash
   curl -X GET "http://localhost:8036/today.ics?currencies=AUD,GBP"
   ```

3. **Request with Impact Class Filter:**

   ```bash
   curl -X GET "http://localhost:8036/today.ics?impact-classes=yellow,red"
   ```

4. **Request with Implementation Parameter:**

   ```bash
   curl -X GET "http://localhost:8036/today.ics?implementation=ical"
   ```

5. **Request with Combined Filters:**

   ```bash
   curl -X GET "http://localhost:8036/today.ics?currencies=AUD,GBP&impact-classes=yellow,red&implementation=ical"
   ```

6. **NNFX Endpoint Request:**

   ```bash
   curl -X GET "http://localhost:8036/today_nnfx.ics"
   ```

7. **NNFX Endpoint Request with Filters:**

   ```bash
   curl -X GET "http://localhost:8036/today_nnfx.ics?currencies=USD,EUR&impact-classes=orange,gray"
   ```
```

## Endpoint JSON Data

Each endpoint configuration points to a JSON file containing event data. Below is an example of the JSON data structure and the documentation for each field.

Example JSON Data:

```json
[
    {
        "meta_date": "Thu <span>Jul 4</span>",
        "date": "2024-07-04T00:00:00",
        "country": "AU",
        "currency": "AUD",
        "impactClass": "icon--ff-impact-yel",
        "impactTitle": "Low Impact Expected",
        "name": "Goods Trade Balance",
        "trimmedPrefixedName": "AUD Goods Trade Balance",
        "dateline": 1720056600,
        "forecast": "6.20B",
        "previous": "6.55B",
        "timeLabel": "3:30am",
        "timeMasked": false,
        "timestamp": "2024-07-03T21:30:00-04:00",
        "timestamp_local": "2024-07-04T03:30:00+02:00",
        "event_date": "2024-07-03",
        "event_time": "21:30:00",
        "event_date_local": "2024-07-04",
        "event_time_local": "03:30:00"
    },
    {
        "meta_date": "Thu <span>Jul 4</span>",
        "date": "2024-07-04T00:00:00",
        "country": "UK",
        "currency": "GBP",
        "impactClass": "icon--ff-impact-red",
        "impactTitle": "High Impact Expected",
        "name": "Parliamentary Elections",
        "trimmedPrefixedName": "GBP Parliamentary Elections",
        "dateline": 1720078200,
        "forecast": "",
        "previous": "",
        "timeLabel": "All Day",
        "timeMasked": true,
        "timestamp": "2024-07-04T03:30:00-04:00",
        "timestamp_local": "2024-07-04T09:30:00+02:00",
        "event_date": "2024-07-04",
        "event_time": "03:30:00",
        "event_date_local": "2024-07-04",
        "event_time_local": "09:30:00"
    }
]
```

### Field Documentation

- **`meta_date`**: Formatted date with HTML tags (e.g., `"Thu <span>Jul 4</span>"`).
- **`date`**: Date in ISO 8601 format (e.g., `"2024-07-04T00:00:00"`).
- **`country`**: Country code (e.g., `"AU"` for Australia).
- **`currency`**: Currency code (e.g., `"AUD"` for Australian Dollar).
- **`impactClass`**: CSS class for impact level (e.g., `"icon--ff-impact-yel"` for low impact).
- **`impactTitle`**: Human-readable impact description (e.g., `"Low Impact Expected"`).
- **`name`**: Event name (e.g., `"Goods Trade Balance"`).
- **`trimmedPrefixedName`**: Event name with currency prefix (e.g., `"AUD Goods Trade Balance"`).
- **`dateline`**: Unix timestamp of the event (e.g., `1720056600`).
- **`forecast`**: Forecasted value for the event (e.g., `"6.20B"`).
- **`previous`**: Previous value for the event (e.g., `"6.55B"`).
- **`timeLabel`**: Time label (e.g., `"3:30am"`).
- **`timeMasked`**: Boolean indicating if the time is masked (e.g., `false`).
- **`timestamp`**: Original timestamp in ISO 8601 format (e.g., `"2024-07-03T21:30:00-04:00"`).
- **`timestamp_local`**: Local timestamp in ISO 8601 format (e.g., `"2024-07-04T03:30:00+02:00"`).
- **`event_date`**: Date part of the event (e.g., `"2024-07-03"`).
- **`event_time`**: Time part of the event (e.g., `"21:30:00"`).
- **`event_date_local`**: Local date part of the event (e.g., `"2024-07-04"`).
- **`event_time_local`**: Local time part of the event (e.g., `"03:30:00"`).

## Shell Script

A shell script run.sh is provided to automate the execution of the script.

### Shell Script Examples

Example `run.sh`

```bash
#!/bin/bash
source ./.venv/bin/activate
python ./run.py
deactivate

```

### Running the Shell Script

To run the script and clear the directory before running:

```bash
./run.sh
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
