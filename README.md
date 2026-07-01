# Tower Defense — Gabriel Pawłowski

Gra 2D typu tower defense na `<canvas>`, projekt dodatkowy (poza zadaniami StażystApp).

## Zasady
Wrogowie idą ścieżką od lewej do prawej. Stawiaj wieże na trawie (koszt 50 💰) — strzelają do wrogów w zasięgu. Za każdego pokonanego wroga dostajesz złoto. Jeśli wróg dojdzie do końca ścieżki, tracisz życie. Przetrwaj **8 fal**, żeby wygrać.

## Funkcje
- Ścieżka + fale wrogów o rosnącej wytrzymałości
- Stawianie wież za złoto, automatyczne strzelanie do celu w zasięgu
- Złoto / życia / licznik fal, ekran wygranej i przegranej
- **Responsywność**: mysz i dotyk (telefon + komputer), canvas skaluje się do ekranu

## Stack
Czysty HTML + CSS + JavaScript (canvas, bez zależności runtime). Wdrożone na **GitHub Pages**.

## Testy e2e (Playwright)
Gra wystawia hook `window.TD` (stan + akcje), dzięki czemu testy deterministycznie sprawdzają: HUD startowy, start fali, spawn wrogów, koszt wież, zakaz budowy na ścieżce, blokadę przy braku złota i reset.

```bash
npm install
npx playwright install chromium
npm run test:e2e
```

## Uruchomienie lokalnie
Otwórz `index.html` w przeglądarce (lub `npm run serve`).
