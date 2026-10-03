# PSN-Presepe PCB assembly BOM

This file contains assembly-critical mechanical items that are not optional.

| Item | Qty | Description | Assembly status | Notes |
|---|---:|---|---|---|
| HDR-MEGA-STACK | 1 set | Arduino Mega 2560 R3 complete stackable/pass-through female header set | FITTED / MANDATORY | Female sockets on top, long male tails below; includes all Mega R3 shield header groups and the non-standard D7-D8 spacing. Do not substitute closed female headers. |

## Stack construction

`future shield -> PSN-Presepe PCB -> Arduino Mega 2560 R3`

`HDR-MEGA-STACK` must be installed and soldered when the PCB is assembled. It is never DNI/DNP.
