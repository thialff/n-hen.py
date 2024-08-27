# n-henpy

An `n-hentai.net` downloader written in Python for downloading individual books and all favorites easily.

## Usage

The project is still nowhere from done and thus the user experience is lacking.

To start the project, clone the repository, setup a virtual environment and install the following dependencies
using `pip`:

- `beautifulsoup4`
- `requests`
- `pillow`

Afterward, run `main_controller.py` to start the program.

### Download individual entries

`n-henpy` can download an entry/chapter similar to the native download available on the website. The main difference
being that the website download uses a torrent. `n-henpy` downloads the images directly.

1. Go to the "Download" tab
2. Enter the URL of the entry you want to download (`https://nhentai.net/g/144725/`) or its digits (`144725`)
3. Click "Search"
4. Confirm the correct entry by checking out the information overview and cover image
5. (Optional) Select the directory you want to download entries to (every entry will be downloaded to a subdirectory
   named after its digits)
6. Click "Download"
7. Wait for the process to finish

### Download all favorites

`n-henpy` can download all favorites of an account you have access to. This makes it easy to keep a copy of all
favorites and no longer fear they might disappear.

1. Go to the "Favorites" tab
2. Grab and enter the `sessionid`

   This is a bit more complicated, but the main reason for this is that the application will not ask for your login
   credentials. Instead, it will use a currently active session, which will expire after use, making it a bit safer than
   supplying your password.

   1. Open your browser, navigate to `n-hentai.net` and log in
   2. Open your browser's developer tools (usually `F12` or `Ctrl+Shift+I`)
   3. Go to the "Application" tab
   4. Under "Cookies", find the `sessionid` cookie, copy its value
   5. Paste the value into the input field in the application
3. Click "Load"
4. Confirm the correct account by checking out the information overview
5. (Optional) Select the directory you want to download favorites to (every favorite will be downloaded to a
   subdirectory
   named after its digits)
6. Click "Download"

   This process can take a while, depending on the number of favorites you have. The process will wait between entries
   as to not warrant any rate limits.
7. Wait for the process to finish

Note that this process can be re-run on the same directory to update the favorites. The application will only download
newly added favorites, but not delete old ones, meaning it can be run without the danger of losing any entries.
