

# Open5GS UDM/NUDR Modification with External Random Number Generator

This repository contains modified components from Open5GS (https://github.com/open5gs/open5gs) and UERASIM for RAN Authentication, with a simple API that simulates a random number source (like a QRNG).

## Overview

The standard Open5GS code generates cryptographic random numbers internally. This modified version demonstrates how the UDM/NUDR component (`nudr-handler.c`) can be altered to fetch the required random number (RAND) for authentication vector generation from an external QRNG HTTP endpoint.

## Files

1.  **`nudr-handler.c`**:
    * This is a modified version of a handler file likely from the Open5GS UDM/NUDR function.
    * The key modification is in the `udm_nudr_dr_handle_subscription_authentication` function.
    * Instead of generating RAND locally, it makes an HTTP GET request to the simulated QRNG to fetch the RAND value.
    * It uses the `libcurl` library to perform the HTTP request.
    * The fetched hex value is converted to binary and used in the subsequent Milenage and KDF functions.
    * **Note**: This file retains the original Open5GS copyright and license information (GNU Affero General Public License v3 or later).

2.  **`random_number_api.py`**:
    * A simple Flask web server that provides a basic random number generation endpoint.
    * It listens on `http://localhost:5000`.
    * When a GET request is made to `/random`, it generates 16 bytes (128 bits) of random data using Python's `os.urandom` and returns it as a JSON object containing the hexadecimal representation of the random bytes (e.g., `{"rand": "..."}`).

## How to Run

1.  **Start the Random Number API:**
    * Make sure you have Python and Flask installed (`pip install Flask`).
    * Open a terminal and navigate to the repository directory.
    * Run the command: `python random_number_api.py`
    * The API will start listening on `http://0.0.0.0:5000`.

2.  **Compile and Run Modified Open5GS:**
    * Integrate `nudr-handler.c` into your Open5GS source code build process (this requires familiarity with building Open5GS).
    * Ensure the UDM/NUDR component using this modified code is running.
    * When the UDM requires an authentication vector, it will attempt to contact `http://localhost:5000/random` (served by the Python script) to get the RAND value.

## Disclaimer

This is a proof-of-concept modification. Using `os.urandom` in the Python script provides pseudorandom numbers, not true quantum random numbers. The original `nudr-handler.c` is part of Open5GS and is licensed under the GNU AGPLv3. Ensure you comply with the license terms.
