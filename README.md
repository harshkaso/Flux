<h1 align='center'>Flux</h1>
Flux is an interactive Python application that brings flow fields to life, creating mesmerizing particle animations in real time. With configurable flow field functions, color schemes, and particle dynamics, Flux is perfect for both artistic expression and technical exploration.

## Features
- **Customizable Flow Field**: Choose from various mathematical functions to define the behavior of particles in the field.
- **Interactive Particle Control**: Modify particle speed, lifespan, radius, and more via an intuitive GUI.
- **Real-Time Rendering**: Smoothly renders particle animations with frame-by-frame updates.
- **User-Friendly Interface**: Built with a modern and responsive design using dearpygui.


## Screenshots
<p align='center'>
    <img src='assets\screenshots\Flux_FranksLabText_Light.png'>
</p>
<p align='center'>
    <img src='assets\screenshots\Purple_10_Vortex.png'>
</p>
<p align='center'>
    <img src='assets\screenshots\Greens_Swirly.png'>
</p>
<p align='center'>
    <img src='assets\screenshots\SeaAnemone_FNS.png'>
</p>

**_For additional screenshots, visit the full folder: [Screenshots Folder](assets/screenshots)_**

## System Support
|     OS    | Supported |
|   :---:   |   :---:   |
|**Windows**|    ✔️    |
| **Linux** |    ✔️    |
| **macOS** |    ❌    |

**Note for macOS users:**
> At this time, our application is not tested on macOS and is probably not compatible with macOS due to an incompatible library function essential to run the application. We apologize for any inconvenience this may cause. However, we are working on making our app accessible to macOS users in the future. Stay tuned for updates!



## Usage

1. Clone this repository to your local machine.
2. Navigate to the directory where you have cloned the repository.
3. Install the required dependencies.

```shell
pip install -r requirements.txt
```

4. Run the app

```shell
python flux.py
```

5. Sit back, relax and enjoy!

## Building from Source

This project uses Nuitka to compile the Python code into standalone executables for different operating systems. Build scripts (`build.sh` for Linux/macOS, `build.bat` for Windows) are provided in the root directory to automate this process.

### Prerequisites

*   **Python 3.x**: Ensure you have Python 3 installed (Python 3.7 or newer recommended for Nuitka compatibility). You can download it from [python.org](https://www.python.org/downloads/).
*   **pip**: Python's package installer, usually included with Python. Make sure it's upgraded: `python -m pip install --upgrade pip`.
*   **C Compiler**: Nuitka compiles Python code to C, so a C compiler is required.
    *   **For Windows**:
        *   MinGW64 is recommended. Install it via [MSYS2](https://www.msys2.org/) (install the `mingw-w64-x86_64-toolchain` group) or use the standalone installer from the [MinGW-w64 project page](https://www.mingw-w64.org/downloads/). Ensure the `bin` directory of your MinGW64 installation (e.g., `C:\msys64\mingw64\bin`) is added to your system's PATH environment variable.
        *   The `build.bat` script uses the `--mingw64` flag by default.
        *   Alternatively, Microsoft Visual C++ (MSVC) can be used if configured correctly with Nuitka.
    *   **For Linux**:
        *   GCC (GNU Compiler Collection) is typically used. Install it via your distribution's package manager (e.g., `sudo apt update && sudo apt install build-essential` on Debian/Ubuntu).
    *   **For macOS**:
        *   Xcode Command Line Tools provide Clang, which Nuitka can use. Install them by running `xcode-select --install` in your terminal.
*   **Virtual Environment (Recommended)**: The build scripts create a temporary virtual environment (`venv_build`) to isolate build dependencies.

### Running the Build Scripts

1.  **Clone the repository** (if you haven't already). If you have, navigate to the project directory. Example (replace with the actual repository URL if known):
    ```bash
    git clone https://github.com/YourUsername/Flux.git
    cd Flux
    ```

2.  **For Linux and macOS**:
    *   Open your terminal.
    *   Make the script executable (if it isn't already):
        ```bash
        chmod +x build.sh
        ```
    *   Run the script:
        ```bash
        ./build.sh
        ```
        (If you encounter issues, you can try `bash build.sh`)

3.  **For Windows**:
    *   Open Command Prompt (`cmd.exe`) or PowerShell.
    *   Navigate to the project directory.
    *   Run the script:
        ```bat
        build.bat
        ```

### Output

The build scripts will:
1.  Create a Python virtual environment named `venv_build` (if it doesn't exist).
2.  Activate it.
3.  Upgrade pip.
4.  Install Nuitka, setuptools, and wheel.
5.  Install dependencies from `requirements.txt`.
6.  Run Nuitka to compile `flux/__main__.py` into an executable.

The final executable will be placed in the `dist/` directory:
*   Linux: `dist/Flux_Linux`
*   macOS: `dist/Flux_macOS` (Note: macOS support is currently listed as "not compatible" in the README. The build script will still attempt to create a macOS executable.)
*   Windows: `dist/Flux_Windows.exe`

## Testing the Executables

After building, it's crucial to test the executables on relatively clean environments for each respective platform (Windows, macOS, Linux) to ensure they are truly standalone and function as expected. A "clean environment" means a system (or virtual machine) that does not have Python or the project's specific dependencies installed globally.

### What to Look For During Testing:

*   **Application Starts**: The executable should launch without errors and without requiring an existing Python installation or any external project-specific dependencies.
*   **Core Functionality**: Test the main features of Flux:
    *   Does the GUI load correctly and appear as expected?
    *   Can you interact with all GUI elements (buttons, sliders, input fields)?
    *   Do particle animations start and run?
    *   Can you change flow field functions, color schemes, and particle parameters? Do these changes take effect?
*   **Assets Loading**: Verify that all necessary assets are correctly bundled and displayed/used by the application. This includes:
    *   Fonts (e.g., Space Mono from `flux/Space_Mono/`).
    *   Images or icons used in the UI (from `assets/`).
*   **Console Window (Windows)**: The Windows executable is built with the `--windows-disable-console` flag, so no background command prompt window should appear when you run `Flux_Windows.exe`.
*   **Performance**: Is the application reasonably responsive? Does it perform comparably to running from source?
*   **Error Messages**: Look for any error messages, either displayed in the application's UI or printed to system logs (like Event Viewer on Windows, or console output if not disabled for testing).
*   **Directory Independence**: Try running the executable from a different directory than `dist/` to ensure it's not relying on relative paths to files outside its own bundled content (unless those files are intentionally meant to be user-provided).

By testing thoroughly on different platforms, you can gain confidence that the Nuitka build process has correctly packaged all necessary components and that the application is portable.

## Credits

Special thanks to

> - [Vladimir Ein](https://github.com/v-ein)
> - [Alexander G. Morano](https://github.com/Amorano)
> - [Quattro](https://github.com/QuattroMusic)

For contributing, fixing issues and optimizing various aspects of the application.
