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

Zunächst müssen die vier Eckpunkte bzw. Kanten des Tischs durch einen Klick der linken Maustaste ausgewählt werden. Idealerweise wird dabei wie folgt vorgegangen: 
-	Auswahl der linken vorderen Ecke
-	Auswahl der linken hinteren Ecke
-	Auswahl der rechten vorderen Ecke
-	Auswahl der rechten hinteren Ecke

Anschließend werden anhand dieser Punkte zwei entsprechende Fluchtpunkte und aus diesen wiederum die horizontale Fluchtlinie berechnet. Mit Abschließen dieser Berechnung werden auf der Benutzeroberfläche die entsprechenden vier geraden eingezeichnet - diese stellen die Fluchtlinien dar, von welchen sich immer zwei in jeweils einem Fluchtpunkt schneiden.

Daraufhin muss der Nutzer zunächst die Höhe der Flasche auf dem Tisch kennzeichnen. Dabei wird per Mausklick ein Punkt in der Boden- und ein weiterer Punkt in der Deckelebene gesetzt. Ebenso wird dann auch bei der Tasse verfahren, so dass auch hier zwei Punkte die Höhe der Tasse markieren.
Die Höhe der Tasse ist mit 26cm gegeben und anhand dieser wird anschließend die Höhe der Tasse mit Hilfe eines neu berechneten Fluchtpunkts "v" ermittelt.

Nun wird die Größe des Bildes den Fluchtpunkten entsprechend größer gerechnet, so dass diese, wie auch die horizontale Fluchtlinie im Bild angezeigt werden können. Hier wird das ursprüngliche Bild relativ zu den Fluchtpunkten und mit Berücksichtigung der Seitenverhältnisse im neuen Bild platziert.


Durch die N-Taste kann zum nächsten Bild navigiert werden. Hier kann nun derselbe Vorgang wie oben beschrieben durchgeführt werden. Dies ist danach noch mit einem weiteren Bild möglich. Durch die unterschiedlichen Blickwinkel kann durch anschließendes Summieren der berechneten Höhe (der Tasse) die durchschnittliche Höhe berechnet werden. 

So soll ein möglichst genaues Ergebnis ermittelt werden. Hier gilt zu beachten, dass die Genauigkeit der Berechnung jedoch von der exakten Positionierung aller, zur Berechnung benötigter, Punkte abhängig ist. Anschließend wird das Programm automatisch beendet.
Mit der Q-Taste kann das Programm manuell beendet werden.


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
