import pygame
from pygame.locals import *
import time
import string
from tkinter import *
from tkinter import messagebox
import random
 
# Funkcja pozwalajaca na renderowanie tesktu w wielu liniach
def blit_text(surface, text, pos, font, color, img, rect, cursor):
    # words to lista zawireająca wszystkie słowa tekstu
    words = [word.split(' ') for word in text.splitlines()]
    # Rozmiar znaku spacji
    space = font.size(' ')[0]  
    # surface.get_size() pozwala na wydobycie szerokosci i wysokości powierzchni
    max_width, max_height = surface.get_size()
    # Współrzedne x,y na ekranie
    x, y = pos

    x_cursor = x
    word_h = 0
    line_w = 0 
    
    for line in words:
        
        line_surface = font.render(' '.join(line), 0, color)
        line_width, line_height = line_surface.get_size()
        line_w = line_width
        for word in line:
            word = word + ' '
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()

            # jeżeli napotkamy na koniec powierzchni, zmieniamy współrzedne renderowania
            if x + word_width >= max_width - 20:
                x = pos[0] # Zresetowanie współrzędnej x
                x_cursor = pos[0]
                y += word_height # Rozpoczecie od nowej linii

            for char in word:
                char_surface = font.render(word, 0, color)
                char_width, char_height = char_surface.get_size()

            x_cursor += char_width + space 
            word_surface = font.render(word[:-1], 0, color)

            surface.blit(word_surface, (x, y))
            # Dla kazdego słowa aktualizujemy współrzedną x o rozmiar spacji
            x += word_width + space
        
        x = pos[0]  # Zresetowanie współrzędnej x
        y += word_height  # Rozpoczecie od nowej linii
        word_h = word_height
        

    img = font.render(text, True, (0,0,0))
    rect.topleft = (x_cursor - 12 - line_w, y - word_h)
    rect.size=img.get_size()
    cursor.topleft = rect.topright

    # Zwracamy informacje o kursorze
    return img, rect, cursor


# Funkcja pobierająca tekst z pliku i losująca jeden z nich
def get_random_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if not lines:
            return "File with text is empty"
        return random.choice(lines)[:-1]

# Funkcja główna, dzięki której mozemy zagrać ponownie
def game():
    
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GRAY = (200, 200, 200)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)

    testText = get_random_text('text_test.txt')

    testLen = len(testText)

    text = ''
    text_color = BLACK
    #print(pygame.font.get_fonts())
    font = pygame.font.SysFont('calibri', 30)
    font_small = pygame.font.SysFont('calibri', 25)

    # Utworzenie kursora
    img = font.render(text, True, BLACK)
    rect = img.get_rect()
    rect.topleft = (20, 3000)
    cursor = Rect(rect.topright, (3, rect.height))

    running = True
    background = WHITE

    # Zbiór CHARACTERS zawiera znaki, które bedą dostępne od użycia, chr(8) to backspace
    CHARACTERS = set(string.ascii_letters + string.digits + string.punctuation + "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ" + " " + chr(8) )

    index = 0
    count = 0
    word_count = 0
    start_time_measurement = True
    while running:

        if testLen == len(text):
            # Gdy długość wspianego tekstu jest równa długości tekstu testowego, wywołujemy okno yesno z zapytaniem o ponowne zagranie            
            play_again = messagebox.askyesno('Play again?' , 'Do you want to play again?')
            if play_again:
                # Wywołujemy rekurencyjnie funckje glówna game()
                game()
            else:
                # Przerywamy działanie petli
                running = False

        for event in pygame.event.get():
            #print(count)
            if event.type == QUIT:
                running = False
            
            # Jeżeli zostanie wciśniety przycisk klawiatury oraz unicode jest w zbiorze CHARACTERS
            # event.unicode pozwala na przechwytywanie kombinacji klawiszów np. shift + a daje A
            if event.type == KEYDOWN and testLen != len(text) and event.unicode in CHARACTERS: 
                if event.key == K_SPACE and text != "":
                    word_count += 1
                    print(word_count)
                # Rozpoczęcie pomiary czasu
                if start_time_measurement:
                    start_time_measurement = False
                    timer_start = time.time()

                # Jezeli wpisany znak zgadza się ze znakiem w tekście, to kursorma kolor zielony
                # W przeciwnym wypadku kolor czerwony
                if  event.unicode == testText[index]: 
                    text_color = GREEN
                    print(event.key)
                    count += 1
                else:
                    text_color = RED
                
                # Po wcisnieciu backspace zmniejszamy długość tekstu o 1
                # oraz aktualizujemy celność oraz index
                if event.key == K_BACKSPACE:
                    text_color = GREEN
                    if len(text)>0:
                        last = text[-1]
                        text = text[:-1]  

                        if last == testText[index-1]:
                            count -= 1
                        index -= 1           

                # W przeciwnym wypadku dodajemy do tekstu nowy znak      
                else:
                    index += 1
                    text += event.unicode



        #print(index)
        if testLen != len(text):
            timer_end = time.time()
            
        accuracy = count/max(len(text),1) * 100
        
        # (try except) gdy wystąpi błąd w try np. dzelenie przez zero, wykonuje się except
        try:
            time_elapsed = timer_end - timer_start
        except:
            time_elapsed = 0

        try:
            WPM = word_count/(time_elapsed/60)
        except:
            WPM = 0
        #print("acc", accuracy)


        # Wypełnienie powierzchnii screen kolorem
        screen.fill(background)
        # Renderowanie tekstu do napisania oraz obecnie pisanego tekstu
        img, rect, cursor = blit_text(screen, testText, (20, 20), font, BLACK, img, rect, cursor)
        img, rect, cursor = blit_text(screen, text, (20, 300), font, BLACK, img, rect, cursor)
        # Rednerowanie wyniku w czasie rzeczywistym
        screen.blit(font_small.render("Accuracy " + str(round(accuracy,2)) + "% ", True, BLACK),(240,500))
        screen.blit(font_small.render("Time elapsed " + str(round(time_elapsed,2)) + "s ", True, BLACK),(500,500))
        screen.blit(font_small.render("WPM " + str(round(WPM)) + " ", True, BLACK),(50,500))

        # Renderowanie migajacego co 0.5 sekundy kursora
        if time.time() % 1 > 0.5:
            pygame.draw.rect(screen, text_color, cursor)

        # Zaktualizowanie ekranu
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":

    # inicjalizacja pygame
    pygame.init()
    # Ustawienie rozmiaru ekranu
    screen = pygame.display.set_mode((800, 600))
    # Wywołanie głownej funkcji
    game()
    # Zamknięcie pygame
    pygame.quit()