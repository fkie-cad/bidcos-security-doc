# Tabel collection

This document is an appendix to the [main documentation](1-bidcos.md) and contains tables which have been moved here for readability reasons.

## Payload

The following tables refer to section [BidCos > Message structure > Payload](1-bidcos.md#payload).

### DEVICE_INFO

| Byte  | Usecase        |
| ----- | -------------- |
| 10    | FIRMWARE       |
| 11-12 | TYPE           |
| 13-23 | SERIAL_NUMBER  |
| 24    | PEER_CHANNEL_A |
| 25    | PEER_CHANNEL_B |
| 26    | UNKOWN         |

### CONFIG_PEER_ADD

| Byte  | Usecase        |
| ----- | -------------- |
| 10    | CHANNEL        |
| 11    | SUBTYPE_2      |
| 12-15 | PEER_ADRESS    |
| 16    | PEER_CHANNEL_A |
| 17    | PEER_CHANNEL_B |

### CONFIG_PEER_REMOVE

| Byte  | Usecase        |
| ----- | -------------- |
| 10    | CHANNEL        |
| 11    | SUBTYPE_2      |
| 12-15 | PEER_ADRESS    |
| 16    | PEER_CHANNEL_A |
| 17    | PEER_CHANNEL_B |

### CONFIG_PEER_LIST_REQ

| Byte | Usecase   |
| ---- | --------- |
| 10   | CHANNEL   |
| 11   | SUBTYPE_2 |

### CONFIG_PARAM_REQ

| Byte  | Usecase      |
| ----- | ------------ |
| 10    | CHANNEL      |
| 11    | SUBTYPE_2    |
| 12-15 | PEER_ADRESS  |
| 16    | PERR_CHANNEL |
| 17    | PARAM_LIST   |

### CONFIG_START

| Byte  | Usecase      |
| ----- | ------------ |
| 10    | CHANNEL      |
| 11    | SUBTYPE_2    |
| 12-15 | PEER_ADRESS  |
| 16    | PERR_CHANNEL |
| 17    | PARAM_LIST   |

### CONFIG_END

| Byte | Usecase   |
| ---- | --------- |
| 10   | CHANNEL   |
| 11   | SUBTYPE_2 |

### CONFIG_WRITE_INDEX

| Byte | Usecase   |
| ---- | --------- |
| 10   | CHANNEL   |
| 11   | SUBTYPE_2 |
| 12   | ADDRESS   |
| 13-? | DATA      |

### CONFIG_WRITE_INDEX

| Byte | Usecase   |
| ---- | --------- |
| 10   | CHANNEL   |
| 11   | SUBTYPE_2 |
| 12-? | DATA      |

### CONFIG_SERIAL_REQ

| Byte | Usecase   |
| ---- | --------- |
| 10   | ?         |
| 11   | SUBTYPE_2 |

### PAIR_SERIAL

| Byte | Usecase   |
| ---- | --------- |
| 10   | ?         |
| 11   | SUBTYPE_2 |
| 12-? | SERIALNO  |

### CONFIG_STATUS_REQUEST

| Byte | Usecase   |
| ---- | --------- |
| 10   | CHANNEL   |
| 11   | SUBTYPE_2 |

### ACK

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |

### ACK_STATUS

| Byte | Usecase            |
| ---- | ------------------ |
| 10   | SUBTYPE            |
| 11   | CHANNEL            |
| 12   | STATUS             |
| 13   | DOWN / UP / LOWBAT |
| 14   | RSSI               |

### ACK2

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |

### AES_REQ

| Byte  | Usecase |
| ----- | ------- |
| 10    | SUBTYPE |
| 11-12 | PARA1   |
| 13-14 | PARA2   |
| 15-16 | PARA3   |
| 17    | KEYNO   |

### NACK

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |

### NACK_TARGET_INVALID

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |

### ACK/NACK_UNKNOWN

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |

### AES_REPLY

| Byte | Usecase |
| ---- | ------- |
| 10-? | DATA    |

### AES_KEY_TO_LAN

| Byte | Usecase   |
| ---- | --------- |
| 10   | CHANNEL ? |
| 11   | TYPE      |

### AES_KEY_TO_ACTOR

| Byte | Usecase |
| ---- | ------- |
| 10-? | KEY     |

### INFO_SERIAL

| Byte  | Usecase  |
| ----- | -------- |
| 10    | SUBTYPE  |
| 11-20 | SERIALNO |

### INFO_PEER_LIST

| Byte  | Usecase |
| ----- | ------- |
| 10    | SUBTYPE |
| 11-14 | PEER1   |
| 15-18 | PEER2   |
| 19-22 | PEER3   |
| 23-26 | PEER4   |

### INFO_PARAM_RESPONSE_PAIRS

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |
| 11-? | DATA    |

### INFO_PARAM_RESPONSE_SEQ

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |
| 11   | OFFSET  |
| 12-? | DATA    |

### INFO_PARAMETER_CHANGE

| Byte  | Usecase    |
| ----- | ---------- |
| 10    | SUBTYPE    |
| 11    | CHANNEL    |
| 12-15 | PEER       |
| 16    | PARAM_LIST |
| 17-?  | DATA       |

### INFO_ACTUATOR_STATUS

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |
| 11   | CHANNEL |
| 12   | STATUS  |
| 13   | UNKNOWN |
| 14   | RSSI    |

### INFO_TEMP

| Byte | Usecase            |
| ---- | ------------------ |
| 10   | SUBTYPE            |
| 11   | SET                |
| 12   | ACT                |
| 13   | ERR / VALVE / MODE |

### INHIBIT_OFF

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |
| 11   | CHANNEL |

### INHIBIT_ON

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |
| 11   | CHANNEL |

### SET

| Byte  | Usecase  |
| ----- | -------- |
| 10    | SUBTYPE  |
| 11    | VALUE    |
| 12-13 | RAMPTIME |
| 14-15 | DURATION |

### STOP_CHANGE

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |
| 11   | CHANNEL |

### RESET

| Byte | Usecase   |
| ---- | --------- |
| 10   | SUBTYPE   |
| 11   | SUBTYPE_2 |

### LED

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |
| 11   | CHANNEL |
| 12   | COLOR   |

### LED_ALL

| Byte  | Usecase     |
| ----- | ----------- |
| 10    | SUBTYPE     |
| 11    | SUBTYPE_2   |
| 12-15 | LED_1_TO_16 |

### LEVEL

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |
| 11   | CHANNEL |
| 12   | TIME    |
| 13   | SPEED   |

### SLEEPMODE

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |
| 11   | CHANNEL |
| 12   | MODE    |

### ENTER_BOOTLOADER

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |

### ?

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |

### ?

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |

### SET_TEMP

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |
| 11   | B1      |
| 12   | B2      |

### ADAPTION_DRIVE_SET

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |

### ENTER_BOOTLOADER

| Byte | Usecase |
| ---- | ------- |
| 10   | SUBTYPE |

### HAVE_DATA

| Byte | Usecase |
| ---- | ------- |

### SWITCH

| Byte  | Usecase |
| ----- | ------- |
| 10-12 | PEER    |
| 13    | FIX     |
| 14    | CHANNEL |
| 15    | COUNTER |

### TIME_STAMP

| Byte  | Usecase |
| ----- | ------- |
| 10-11 | UNKNOWN |
| 12    | TIME    |

### REMOTE

| Byte | Usecase                |
| ---- | ---------------------- |
| 10   | BUTTON / LONG / LOWBAT |
| 11   | COUNTER                |

### SENSOR_EVENT

| Byte | Usecase                |
| ---- | ---------------------- |
| 10   | BUTTON / LONG / LOWBAT |
| 11   | NBR                    |
| 12   | VALUE                  |

### SWITCH_LEVEL

| Byte | Usecase |
| ---- | ------- |
| 10   | BUTTON  |
| 11   | NBR     |
| 12   | LEVEL   |

### SENSOR_DATA

| Byte  | Usecase |
| ----- | ------- |
| 10    | CMD     |
| 11    | FIELD_1 |
| 12-13 | VALUE_1 |
| 14    | FIELD_2 |
| 15-16 | VALUE_2 |
| 17    | FIELD_3 |
| 18-19 | VALUE_3 |
| 20    | FIELD_4 |
| 21-22 | VALUE_4 |

### GAS_EVENT

| Byte  | Usecase |
| ----- | ------- |
| 10-13 | ENERGY  |
| 14-16 | POWER   |

### CLIMATE_EVENT

| Byte | Usecase        |
| ---- | -------------- |
| 10   | CMD            |
| 11   | VALVE_POSITION |

### SET_TEAM_TEMPERATURE

| Byte | Usecase                |
| ---- | ---------------------- |
| 10   | CMD                    |
| 11   | DES_TEMPERATURE / MODE |

### THERMAL_CONTROL

| Byte       | Usecase                             |
| ---------- | ----------------------------------- |
| 10 / 10-11 | SET_TEMPERATURE / ACTOR_TEMPERATURE |
| 11 / 12    | HUMIDITY                            |

### POWER_EVENT_CYCLIC

| Byte  | Usecase   |
| ----- | --------- |
| 10-12 | ENERGY    |
| 13-15 | POWER     |
| 16-17 | CURRENT   |
| 18-19 | VOLTAGE   |
| 20    | FREQUENCY |

### WEATHER_EVENT

| Byte  | Usecase     |
| ----- | ----------- |
| 10-11 | TEMPERATURE |
| 12    | HUMIDITY    |

[*FHEM Source Code*](https://github.com/mhop/fhem-mirror/blob/master/fhem/FHEM/HMConfig.pm)
[*AskSin++ Source Code*](https://github.com/jp112sdl/AskSinPP/blob/master/Defines.h)