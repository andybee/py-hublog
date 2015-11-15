# py-hublog
Python script to log and reset downstream stats from Virgin Media SuperHub web interface

Designed to scratch a personal itch, I've been experiencing problems with poor performance on my
Virgin Media broadband due to unusually high error rates.

The router itself has a continiously incrementing error counter, which makes getting a feel for
the current state tricky.

This script when run grabs the downstream data table from the web interface, then resets the
counter.

Used in conjunction with a CRON task, it can provide stats at periodic intervals.
