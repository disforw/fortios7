# FortiOS7
Fixes the core FortiOS integration for Fortigate firmware 7.0

Fortinet changed their REST API in the latest FortiOS, this integration fixes the calls for the device tracker.
In the current version it queries "wifi/clients" which means the integration will ONLY work if you are using FotiAPs! I am working on finding a URI that gives me all clients. Work in progress.

Example Configuration:

device_tracker:<br>
    platform: fortios7<br>
    host: 192.168.1.1<br>
    verify_ssl: false<br>
    token: !secret fortilink_api<br>
    new_device_defaults:<br>
      track_new_devices: false
