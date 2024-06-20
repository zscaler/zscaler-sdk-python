# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import ipaddress
import random
import string
from datetime import datetime, timedelta
from typing import List, Tuple

import pytz


# Function to generate a random string
def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


# Function to generate a random IP address from a given subnet
def generate_random_ip(subnet):
    network = ipaddress.ip_network(subnet)
    # Generate a random IP within the subnet, excluding the network and broadcast addresses
    random_ip = random.choice(list(network.hosts()))
    return str(random_ip)


def generate_random_password(length=12):
    """Generate a random string of letters, digits, and special characters."""
    if length < 4:
        raise ValueError("Password length must be at least 4")

    # Ensure the password has at least one lowercase, one uppercase, one digit, and one special character
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*()"),
    ]

    # Fill the rest of the password length with random characters
    password += random.choices(characters, k=length - 4)

    # Shuffle to ensure the characters are in random order
    random.shuffle(password)

    return "".join(password)


def generate_time_bounds(time_zone: str, format: str = "RFC1123Z") -> Tuple[str, str]:
    """
    Generates start and end time strings in the specified time zone.
    Ensures start time is the current time and the end time does not exceed 1 year from today.

    Args:
        time_zone (str): A string representing the IANA time zone.
        format (str): The desired string format of the time, "RFC1123" or "RFC1123Z".

    Returns:
        Tuple[str, str]: A tuple containing the start time and end time as strings.
    """
    tz = pytz.timezone(time_zone)
    start_time = datetime.now(tz)

    # Ensure end time does not exceed 1 year from today
    end_time = start_time + timedelta(days=365 - 1)  # Subtracting one day to ensure it's within a year

    if format.upper() == "RFC1123":
        time_format = "%a, %d %b %Y %H:%M:%S %Z"
    else:  # RFC1123Z format
        time_format = "%a, %d %b %Y %H:%M:%S %z"

    formatted_start_time = start_time.strftime(time_format)
    formatted_end_time = end_time.strftime(time_format)

    return formatted_start_time, formatted_end_time


def generate_random_port_ranges(count: int, range_size: int = 1) -> List[str]:
    """
    Generate a list of unique, non-overlapping TCP port ranges.
    Each range is returned as a string formatted as "start-end".

    Args:
        count: The number of unique port ranges to generate.
        range_size: The number of consecutive ports in each range (default is 1).

    Returns:
        A list of port range strings.
    """
    max_port = 65535
    selected_ports = set()
    port_ranges = []

    while len(port_ranges) < count:
        start_port = random.randint(1, max_port - range_size + 1)
        end_port = start_port + range_size - 1

        if all(p not in selected_ports for p in range(start_port, end_port + 1)):
            port_ranges.append(f"{start_port}-{end_port}")
            selected_ports.update(range(start_port, end_port + 1))

    return port_ranges
