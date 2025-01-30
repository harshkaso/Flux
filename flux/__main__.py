from flux_app import FluxApp
import sys

def main():
    try:
        app = FluxApp()
        app.run()
        return 0
    except:
        return 1

if __name__ == '__main__':
    sys.exit(main())
