```mermaid
  classDiagram
       Pelaaja "2..8" -- "1" Pelilauta
       Ruutu "40" -- "1" Pelilauta
       Ruutu "1" --> "1" Ruutu
       Pelinappula "1" -- "1" Pelaaja
       Pelinappula "1" -- "1" Ruutu
       Pelilauta "1" --> "2" Noppa
```