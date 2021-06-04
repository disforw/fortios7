# FortiOS7
Fixes the core FortiOS integration for Fortigate firmware 7.0

Fortinet changed their REST API in the latest FortiOS, this integration fixes the calls for the device tracker.
In the current version it queries "wifi/clients" which means the integration will ONLY work if you are using FotiAPs! I am working on finding a URI that gives me all clients. Work in progress.

Example Configuration:

device_tracker:
  - platform: fortios7
    host: 192.168.1.1
    verify_ssl: false
    token: !secret fortilink_api
    new_device_defaults:
      track_new_devices: false

