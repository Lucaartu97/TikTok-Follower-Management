from flask import Flask, request, render_template, send_file
import os
import re

app = Flask(__name__)

# Funzione per leggere file txt e restituire una lista di nomi utente
def leggi_file_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return {line.strip() for line in file}

# Funzione per scrivere i nomi utente in un file txt
def scrivi_file_txt(file_path, usernames):
    with open(file_path, 'w', encoding='utf-8') as file:
        if usernames:
            for username in usernames:
                file.write(username + '\n')
        else:
            file.write("Tutti i seguiti ti seguono indietro. Nessun risultato.\n")

# Funzione per pulire il file follower e seguire
def pulisci_file(followers_path, following_path):
    # Definisci una regex per individuare date e orari (formato yyyy-mm-dd hh:mm:ss)
    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

    # Funzione interna per pulire un file e restituire il percorso del file pulito
    def pulisci_file_individuale(file_path, output_file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Rimuovi tutte le occorrenze di date e orari
        new_content = re.sub(pattern, '', content)

        # Definisci le parole da sostituire con spazi vuoti
        parole_da_sostituire = ['Date:', 'Username:', ' ']
        
        # Sostituisci le parole specificate
        for parola in parole_da_sostituire:
            new_content = new_content.replace(parola, '')

        # Rimuovi le righe vuote o con solo spazi
        new_lines = [line.strip() for line in new_content.splitlines() if line.strip()]

        # Scrivi il nuovo contenuto in un file
        with open(output_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write("\n".join(new_lines))

    # Pulire i file follower e following
    cleaned_followers_path = 'follower_puliti.txt'
    cleaned_following_path = 'following_puliti.txt'
    
    pulisci_file_individuale(followers_path, cleaned_followers_path)
    pulisci_file_individuale(following_path, cleaned_following_path)

    return cleaned_followers_path, cleaned_following_path  # Ritorna i percorsi dei file puliti

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pulisci' in request.form:
            # Salva i file di follower e seguiti
            followers_file = request.files['followers']
            following_file = request.files['following']
            
            # Salva i file caricati
            followers_file.save('followers.txt')
            following_file.save('following.txt')

            # Pulisci i file dei follower e dei seguiti
            cleaned_followers_path, cleaned_following_path = pulisci_file('followers.txt', 'following.txt')

            # Restituisci un messaggio di conferma e i file puliti per il download
            return render_template('index.html', pulito=True, cleaned_followers=cleaned_followers_path, cleaned_following=cleaned_following_path)

        elif 'check' in request.form:
            # Carica i file di testo dopo la pulizia
            follower_usernames = leggi_file_txt('follower_puliti.txt')  # Usa il file pulito
            following_usernames = leggi_file_txt('following_puliti.txt')

            # Trova i seguiti che non ti ricambiano
            non_ricambiati = following_usernames - follower_usernames

            # Scrivi i risultati in un file di output
            output_path = 'non_ricambiati.txt'
            scrivi_file_txt(output_path, non_ricambiati)

            # Ritorna la pagina con il link per scaricare il file
            return render_template('index.html', non_ricambiati=non_ricambiati, output_file=output_path)

    return render_template('index.html', non_ricambiati=None, output_file=None, pulito=False, cleaned_followers=None, cleaned_following=None)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
