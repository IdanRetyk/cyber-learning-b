import pandas as pd
import subprocess

def data_to_html(data, columns, table_name, output_file='output.html'):
    """
    Converts a list of tuples (data) into an HTML table, saves it to a file, and displays it.
    
    Args:
    - data (list of tuples): The data to be converted into an HTML table.
    - columns (list of str): The column names for the data.
    - output_file (str): Path to the output HTML file.
    
    Returns:
    - None
    """
    # Convert the list of rows into a DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Convert DataFrame to HTML and save it
    html_content = f"<h2>{table_name}</h2>" + df.to_html(index=False)

    with open(output_file, 'w') as file:
        file.write(html_content)

    chrome_exe = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    # subprocess.run([chrome_exe, fr'D:\Cyber\summer_task\SQL-client-server\{output_file}'])
    subprocess.run([chrome_exe, fr'C:\Ophir\SQL-client-server\{output_file}'])