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
import os
import random
import string
from datetime import datetime, timedelta
from typing import List, Tuple

import pytz


# Deterministic counters for VCR - used for both recording and playback
_vcr_string_counter = 0
_vcr_ip_counter = 0
_vcr_port_counter = 1000


def generate_random_string(length=10):
    """
    Generate a deterministic string for testing with VCR.
    
    ALWAYS returns deterministic values (counter-based) to ensure
    recording and playback use the same values.
    
    This ensures VCR cassettes capture and replay with matching request data.
    
    The format is "vcr{counter:04d}" which generates strings like:
    vcr0001, vcr0002, etc. (8 characters, fits within default length=10)
    """
    global _vcr_string_counter
    
    # Always use deterministic strings for VCR consistency
    # This ensures recording and playback generate identical values
    _vcr_string_counter += 1
    # Use short base "vcr" so "vcr0001" (8 chars) fits within default length=10
    return f"vcr{_vcr_string_counter:04d}"


def generate_random_ip(subnet):
    """
    Generate a deterministic IP address from a subnet for VCR testing.
    
    ALWAYS returns deterministic IPs (counter-based) to ensure
    recording and playback use the same values.
    """
    global _vcr_ip_counter
    
    network = ipaddress.ip_network(subnet)
    hosts = list(network.hosts())
    
    # Always use deterministic IPs for VCR consistency
    _vcr_ip_counter += 1
    index = _vcr_ip_counter % len(hosts)
    return str(hosts[index])


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
    Generate a list of unique, non-overlapping TCP port ranges for VCR testing.
    Each range is returned as a string formatted as "start-end".

    ALWAYS returns deterministic port ranges to ensure recording and playback
    use the same values.

    Args:
        count: The number of unique port ranges to generate.
        range_size: The number of consecutive ports in each range (default is 1).

    Returns:
        A list of port range strings.
    """
    global _vcr_port_counter
    
    # Always use deterministic port ranges for VCR consistency
    port_ranges = []
    for i in range(count):
        start_port = _vcr_port_counter
        end_port = start_port + range_size - 1
        port_ranges.append(f"{start_port}-{end_port}")
        _vcr_port_counter += range_size + 10  # Leave gaps between ranges
    return port_ranges


def reset_vcr_counters():
    """
    Reset all VCR deterministic counters.
    Call this at the start of each test to ensure consistent values.
    """
    global _vcr_string_counter, _vcr_ip_counter, _vcr_port_counter
    _vcr_string_counter = 0
    _vcr_ip_counter = 0
    _vcr_port_counter = 1000
