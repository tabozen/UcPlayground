# Third-party notices

NNOs, Ardugurl and the other firmwares published in this repository are
closed source. Copyright (c) 2024-2026 pyreht. All rights reserved, except
for the third-party components listed below, which remain under their own
licences.

Binaries built from this project include some or all of these components,
depending on the board.

Last reviewed: September 2026.

## Libraries

| Component | Version | Used for | Licence | Upstream |
|---|---|---|---|---|
| ggwave | git | data over sound | MIT | https://github.com/ggerganov/ggwave |
| ssd1306 (lexus2k) | 1.8.8 | I2C OLED | MIT | https://github.com/lexus2k/ssd1306 |
| NimBLE-Arduino | 2.5.0 | Bluetooth LE | Apache-2.0 | https://github.com/h2zero/NimBLE-Arduino |
| JPEGDEC | 1.8.4 | JPEG decoding | Apache-2.0 | https://github.com/bitbank2/JPEGDEC |
| PNGdec | 1.1.6 | PNG decoding | Apache-2.0 | https://github.com/bitbank2/PNGdec |
| ArduinoJson | 7.4.3 | JSON parsing | MIT | https://github.com/bblanchon/ArduinoJson |
| MicroPython | 1.24.1 | Python runtime | MIT | https://github.com/micropython/micropython |
| TFT_eSPI | 16e3759 | T-Deck, PicoCalc display | FreeBSD (BSD-2-Clause) and MIT | https://github.com/Bodmer/TFT_eSPI |
| M5Unified, M5GFX | 0.2.x | M5Stack boards | MIT | https://github.com/m5stack/M5Unified |
| M5Cardputer | 1.1.1 | Cardputer keyboard | MIT | https://github.com/m5stack/M5Cardputer |
| M5PM1 | git | StickS3 power management | MIT | https://github.com/m5stack/M5PM1 |
| mlx90640-library | vendored | thermal camera | Apache-2.0 | https://github.com/melexis/mlx90640-library |
| minimp3 | vendored | MP3 decoding | CC0-1.0 | https://github.com/lieff/minimp3 |
| esp_littlefs, littlefs | component | filesystem | MIT, BSD-3-Clause | https://github.com/joltwallet/esp_littlefs |
| esp_tinyusb, usb_host_* | component | USB device and host | Apache-2.0 | https://github.com/espressif/esp-usb |
| TinyUSB | via esp_tinyusb | USB stack | MIT | https://github.com/hathach/tinyusb |
| esp_lcd_co5300 | component | AMOLED display | Apache-2.0 | https://components.espressif.com |

## Frameworks

| Component | Licence | Upstream |
|---|---|---|
| ESP-IDF, including FreeRTOS, lwIP, Mbed TLS, FatFs | Apache-2.0 (bundled components under their own licences) | https://github.com/espressif/esp-idf |
| Arduino core for ESP32 | LGPL-2.1 | https://github.com/espressif/arduino-esp32 |

## Fonts

| Font | Licence | Upstream |
|---|---|---|
| FreeMono (GNU FreeFont, via the GFX font headers) | GPL-3.0-or-later with font exception | https://www.gnu.org/software/freefont/ |

## LGPL components

The Arduino core for ESP32 is licensed under the LGPL. Its source code is
available from the upstream link, at the version used. For LGPL
inquiries, contact u/pyreht on Reddit.
