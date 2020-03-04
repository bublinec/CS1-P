import requests
from bs4 import BeautifulSoup
import tkinter as tk


def get_html(url: str, parser='lxml'):
    """
    Takes url and returns BeautifulSoap object for parsing.
    BeautifulSoap object contains html.
    """
    # get response from the web site
    sc_response = requests.get(url)  # sc - source code
    # transfer response to text
    sc = sc_response.text
    # create object of class Beautiful soup, with lxml tool, which will be used for parsing
    sc_soup = BeautifulSoup(sc, parser)
    return sc_soup

def get_rate(url='https://transferwise.com/gb/currency-converter/eur-to-gbp-rate') -> float:
    """Return actual eruo to pound rate according to the website""" 
    soup = get_html(url) 
    # find all occuarnces of span with given class (that span conains the rate)
    rate = soup.find_all('span', class_='text-success')
    rate = rate[0].text # take the first occurance and convert it to text
    return float(rate)


def run_calculator(rate:float, round_places=4):
    # DEFINITIONS (to avoid magic numbers)
    title = " CURRENCY CONVERTER"
    dark = "#0e2f44" # blue
    light = "#eeeeee"
    intense = "#800000" # burgundy
    width = 35
    text_width = 10 

    def display_result():
        """Calculate and display the result"""
        euro = textVar.get()
        pounds = rate * float(euro.strip()) 
        pounds = str(round(pounds, round_places))
        result_label.configure(text=pounds)
    

    # initialise window
    root = tk.Tk()

    # TOP FRAME
    frame = tk.Frame(root, bg=dark)
    frame.pack()

    # TITLE
    result_label = tk.Label(frame, text=title, bg=light)
    result_label.pack(padx=width, pady=15)

    # CHOOSE CURRENCY
    currency_frame = tk.Frame(frame, bg=dark)
    currency_frame.pack()

    choice = tk.IntVar(0)
    helloButton = tk.Radiobutton(currency_frame,text="£", bg=dark,  fg=light,
                                  variable=choice, value=0)
    helloButton.pack(side="left")
    goodbyeButton = tk.Radiobutton(currency_frame,text="$", bg=dark, fg=light,
                                    variable=choice, value=1)
    goodbyeButton.pack(side="left")

    # INPUT
    textVar = tk.StringVar()
    textEntry = tk.Entry(frame,textvariable=textVar,width=text_width, bg=light)
    textEntry.pack(padx=width, pady=20) 

    # GO BUTTON
    button = tk.Button(frame, text=" GO! ", padx=text_width,
                       fg=light, bg=intense, command=display_result)
    button.pack(padx=width, pady=0)

    # RESULT LABEL
    result_label = tk.Label(frame, text="0", width=8, bg=light)
    result_label.pack(padx=width, pady=20) 

    # Exit LABEL
    exitButton = tk.Button(frame,text="EXIT", padx=text_width, 
                           fg=light, bg=intense, command=root.destroy)
    exitButton.pack(pady=10)

    return root.mainloop() # open the widow


if __name__ == "__main__":
    # rate = get_rate()
    rate = 0.86
    run_calculator(rate)