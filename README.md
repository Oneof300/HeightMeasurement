# HeightMeasurement

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Inhalt</summary>
  <ol>
    <li>
      <a href="#anleitung-zur-nutzung-des-programms">Anleitung zur Nutzung des Programms</a>
    </li>
    <li>
        <a href="#schlüssel-zu-den-indizes-des-arrays-currentimgpts">Schlüssel zu den Indizes des Arrays currentImgPts</a></li>
    <li><a href="#verwendete-module">Verwendete Module</a></li>
  </ol>
</details>

# Anleitung zur Nutzung des Programms 
[Zum Programm "HeightMeasurement"](HeightMeasurement.py)

Zunächst müssen vier Eckpunkte eines Prallelogramms bzw. des Tisches durch einen Klick der linken Maustaste ausgewählt werden. Idealerweise werden diese in der folgenden Reihenfolge markiert: 
1.	rechte vordere Ecke
2.	rechte hintere Ecke
3.	linke vordere Ecke
4.	linke hintere Ecke

Anschließend werden anhand dieser Punkte zwei entsprechende Fluchtpunkte und aus diesen wiederum die horizontale Fluchtlinie berechnet. Mit Abschließen dieser Berechnung werden auf der Benutzeroberfläche vier geraden eingezeichnet, die durch die markierten Punkte verlaufen bis hin zu den FLuchtpunkten wo sie sich schneiden.

Daraufhin muss der Nutzer zunächst das untere und obere Ende der Flasche kennzeichnen. Dabei sollte jeweils möglichst die Mitte des Flaschenbodens und -deckels getroffen werden. Ebenso wird danach bei der Tasse verfahren.
Die Höhe der Flasche ist mit 26cm gegeben. Anhand dieser und mit Hilfe eines neu berechneten Fluchtpunkts "v" wird anschließend die Höhe der Tasse ermittelt.

Nun wird die Größe des Bildes den Fluchtpunkten entsprechend erweitert, sodass diese, sowie die horizontale Fluchtlinie, im Bild angezeigt werden können. Hier wird das ursprüngliche Bild relativ zu den Fluchtpunkten im neuen Bild platziert. Das neue Bild wird abschließend verkleinert, sodass sich die Fenstergröße nicht ändert.

Durch die N-Taste kann zum nächsten Bild navigiert werden. Hier kann nun derselbe Vorgang wie oben beschrieben durchgeführt werden. Dies ist danach noch mit einem weiteren Bild möglich. Durch die unterschiedlichen Blickwinkel kann durch anschließendes Summieren der berechneten Höhe (der Tasse) die durchschnittliche Höhe berechnet werden. 

So soll ein möglichst genaues Ergebnis ermittelt werden. Hier gilt zu beachten, dass die Genauigkeit der Berechnung jedoch von der exakten Positionierung aller, zur Berechnung benötigter, Punkte abhängig ist. Anschließend wird das Programm automatisch beendet.
Mit der Q-Taste kann das Programm vorzeitig beendet werden.


# Schlüssel zu den Indizes des Arrays currentImgPts
|Index  |Mathematische Bezeichnung  |
|-------|---------------------------|
|0 - 3  |Eckpunkte des Tischs       |
|4 - 5  |Fluchtpunkte Vx und Vy     |
|6      |b                          |
|7      |r                          |
|8      |b0                         |
|9      |t0                         |
|10     |Fluchtpunkt v              |
|11     |t                          |




# Referenzen


# Verwendete Module
|Modul          |Version    |
|---------------|-----------|
|numpy          |1.22.3     |
|opencv-python  |4.5.5.64   |
