# Chrome Dashboards for Combined Metal Roofing
This project automates a sequence of actions in a Chrome browser using Selenium and Python. The actions include opening a specific web page, clicking at a specified position, and simulating the `CTRL + HOME` key press. The project also includes setting up the Python script to run at system startup.

## Getting Started

### Prerequisites

You will need the following installed on your system:

- Python 3.x
- Selenium (`pip install selenium`)
- ChromeDriver ([download here](https://sites.google.com/chromium.org/driver/))
- webdriver_manager (`pip install webdriver_manager`)

Ensure that Python and ChromeDriver are in your user/system's PATH.

### Preparation

While we won't be using Windows Kiosk mode, we do use these preparation guide: https://learn.microsoft.com/en-us/windows/configuration/kiosk-prepare

### Project Structure

- `automation.py`: This Python script uses Selenium to automate actions in Chrome.
- `run_automation.bat`: This batch file runs the Python script. It should be placed in the Startup folder to run the script at system startup.

## Setup

1. Download or clone this repository to your local system.
2. Install the prerequisites mentioned above.
3. Update the paths and parameters in `automation.py` and `run_automation.bat` as necessary.
4. To have the script run at system startup, press `Win + R` to open the Run dialog, type `shell:startup`, and press Enter. This will open the Startup folder. Copy `run_automation.bat` into this folder.

## Usage

Once setup is complete, the Python script will run automatically at system startup. You can also run `automation.py` manually at any time, or run `run_automation.bat` to test the startup process.

## Notes

- The `--window-position` flag may not behave consistently across different operating systems and window managers. Adjust the coordinates as necessary based on your monitor setup and resolution.
- The JavaScript key codes might not always correspond to the same keys across different operating systems and browsers. Adjust the key codes as necessary if the `CTRL + HOME` key combination does not work as expected.
- Depending on your script and network conditions, the script might fail if your internet connection hasn't been established yet when the script runs at startup.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Thanks to the Selenium team for their great work on Selenium.
- Thanks to OpenAI for their work on GPT-3 and GPT-4, which helped in creating this project.
