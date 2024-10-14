document.addEventListener("DOMContentLoaded", function () {
    const startButton = document.getElementById("startButton");
    const tutorialSection = document.getElementById("tutorial");
    const uploadSection = document.getElementById("uploadSection");
    const downloadButton = document.getElementById("downloadButton");

    // Mostra la sezione di upload quando si clicca su "Avvia"
    startButton.addEventListener("click", function () {
        tutorialSection.style.display = "none";
        uploadSection.style.display = "block";
    });

    // Funzione per scaricare il file di output
    window.downloadOutput = function() {
        const link = document.createElement('a');
        link.href = "{{ url_for('static', filename='non_ricambiati.txt') }}"; // Path al file non ricambiati
        link.download = 'non_ricambiati.txt';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
});
