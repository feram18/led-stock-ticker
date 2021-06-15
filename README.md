# LED Stock Ticker Display
***
An LED display for real-time prices of stocks and cryptocurrencies. 
Requires a Raspberry Pi, and a 64x32 LED board connected to the Raspberry Pi via the GPIO pins.

## Features
### Real-time prices

It can display the real-time prices (refreshing every 90 seconds) of your selected stocks and cryptocurrencies.

![Demo-Image](assets/img/LED-Stock-Ticker-Demo.gif)

## Installation
### Hardware

Materials needed:
- Raspberry Pi
- Adafruit RGB Matrix HAT or Bonnet
- 64x32 RGB LED matrix


### Software

**Pre-requisites**

You'll need to make sure Git and PIP are installed on your Raspberry Pi.

```sh
sudo apt-get update
sudo apt-get install git python-pip
```

**Installation**

First, clone this repository. Using the `--recursive` flag will install the rgbmatrix binaries, which come from hzeller's 
[rpi-rgb-led-matrix] library. This library is being used to render the data onto the LED matrix.

```sh
git clone --recursive https://github.com/feram18/led-stock-ticker.git
cd led-stock-ticker
chmod +x install.sh
./install.sh
```

Secondly, you'll need to create an account at [Twelve Data] to get your free API key. 

## Usage
From the `/led-stock-ticker` directory run the following command (include additional [flags](#Flags) as necessary):

`sudo python main.py --led-gpio-mapping="adafruit-hat" --led-slowdown-gpio=2 --led-cols=64`.

Running as root is necessary in order for the matrix to render.


### Configuration
A default `config.json.example` file is included for reference. 
Edit the generated `config.json` file to add your API key, and other default values as desired.
```
  "api_key"         String    An API key is required for the application to work.
                              You can get a free API key at twelvedata.com.

  "symbols"         Array     Pass an array of symbols. Maximum limit of 8.
                              Example: ["TSLA", "AMZN", "MSFT"].
                              When adding a cryptocurrency, add the currency next to the symbol.
                              Example: "BTC/USD", "ETH/EUR".

  "country"         String    Country name of the stocks. Example: "US"/"United States"
  "currency"        String    Currency in which you would like to see the prices displayed.
                              Example: "USD", "MXN", "EUR"
  "timezone"        String    Timezone where you are located. Example: "UTC", "EST"
  "time_format"     String    Sets the preferred hour format for displaying time.
                              Accepted values are "12h" or "24h".
  "debug"           Bool      Enables debugging messages to be displayed in the console when running the software.

```

### Flags
You can configure your LED matrix with the same flags used in the [rpi-rgb-led-matrix] library. 
More information on these arguments can be found in the library documentation.
```
--led-rows                Display rows. 16 for 16x32, 32 for 32x32. (Default: 32)
--led-cols                Panel columns. Typically 32 or 64. (Default: 32)
--led-chain               Daisy-chained boards. (Default: 1)
--led-parallel            For Plus-models or RPi2: parallel chains. 1..3. (Default: 1)
--led-pwm-bits            Bits used for PWM. Range 1..11. (Default: 11)
--led-brightness          Sets brightness level. Range: 1..100. (Default: 100)
--led-gpio-mapping        Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm
--led-scan-mode           Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced. (Default: 1)
--led-pwm-lsb-nanosecond  Base time-unit for the on-time in the lowest significant bit in nanoseconds. (Default: 130)
--led-show-refresh        Shows the current refresh rate of the LED panel.
--led-slowdown-gpio       Slow down writing to GPIO. Range: 0..4. (Default: 1)
--led-no-hardware-pulse   Don't use hardware pin-pulse generation.
--led-rgb-sequence        Switch if your matrix has led colors swapped. (Default: RGB)
--led-pixel-mapper        Apply pixel mappers. e.g Rotate:90, U-mapper
--led-row-addr-type       0 = default; 1 = AB-addressed panels. (Default: 0)
--led-multiplexing        Multiplexing type: 0 = direct; 1 = strip; 2 = checker; 3 = spiral; 4 = Z-strip; 5 = ZnMirrorZStripe; 6 = coreman; 7 = Kaler2Scan; 8 = ZStripeUneven. (Default: 0)
```

## Roadmap
- [ ] Support different matrix dimensions
- [ ] Improve visuals and layout configuration
- [ ] Create configuration script

## Sources
This project relies on [Twelve Data]'s API to retrieve the stock prices, and the [rpi-rgb-led-matrix] library to make 
everything work with the LED board, and is included into this repository as a submodule, so when cloning the repository 
it is necessary to use the `--recursive` flag.

## Disclaimer
This application is dependent on [Twelve Data]'s API relaying accurate and updated data.

## Limitations
[Twelve Data]'s Basic (free) tier only allows for 8 API requests per minute, with a maximum of 800 API requests a day.
Assuming that the board will be in use during regular trading hours (9:30 AM to 4:00 PM EST - U.S. stock market), 
the software will refresh the price data at least every 90 seconds. This is to ensure the API's request limit is not exceeded
while real-time prices are available (regular stock market trading hours).

[comment]: <> (In addition, [Twelve Data] only provides real-time prices during regular trading hours, meaning that the API does not)

[comment]: <> (reflect changes in the price happening after hours &#40;between 4:00 PM and 9:30 AM EST&#41;.)

## License
GNU General Public License v3.0

[Twelve Data]: <https://twelvedata.com>
[rpi-rgb-led-matrix]: <https://github.com/hzeller/rpi-rgb-led-matrix>
