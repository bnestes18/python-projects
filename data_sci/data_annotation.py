import requests
from bs4 import BeautifulSoup

def plot_table_grid(url):
    if not url:
        raise Exception("Please provide a URL to the Google Doc.")
    
    # Send an HTTP GET request to retrieve the content of the Google Doc
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table element in the Google Doc
    table = soup.find("table")

    if table:
        # Extract data from the table
        table_data = []
        rows = table.find_all('tr')
        
        # Iterate table rows. Skip header.
        for row in rows[1:]:
            columns = row.find_all(["td"])
            
            # Each row contains 3 columns. If row has corrupt data, skip it.
            if len(columns) < 3:
                continue
            else:
                try:
                    x = int(columns[0].get_text(strip=True))
                    y = int(columns[2].get_text(strip=True))
                except ValueError:
                    print("x or y value cannot be converted to an integer. Skipping row.")
                    continue
                
                char = columns[1].get_text(strip=True)
                if not char:
                    print("Cannot plot empty character. Skipping row.")
                    continue
                # Creates list of tuples
                table_data.append((x, y, char))
            
        # Get max values for x and y. Min is 0.
        x_max = max(x for x, y, c in table_data)
        y_max = max(y for x, y, c in table_data)
        
        # Create grid with whitespaces
        grid = []
        
        for y in range(y_max + 1):
            row = []
            for x in range(x_max + 1):
                row.append(' ')
            grid.append(row)
            
        # Plot x and y coordinates on grid. Whitespace is overwritten by unicode characters.
        for x, y, c in table_data:
            grid[y][x] = c
        
        for y in range(y_max, -1, -1):
            print(''.join(grid[y]))
    else:
        print("No table found in the Google Doc.")
        
# Provide Google Doc URL to the line below and uncomment
# plot_table_grid("")
        
# Provide Google Doc URL to the line below and uncomment
plot_table_grid("https://docs.google.com/document/d/e/2PACX-1vSFTq6KR8ER5h9_bFVliDvYBntK6Wv8L7x6hLp2Sm58Zkhpo7Vsba9BmC82wcy8WoR3Q47J-brCiH3c/pub")