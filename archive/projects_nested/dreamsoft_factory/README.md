
---

# Środowisko deweloperskie
**Spis submodułów:**
- **authApp**: Aplikacja odpowiedzialna za autoryzację.
- **manager**: Aplikacja do zarządzania treścią i personalizacją strony internetowej.
- **backend**: Aplikacja dostarczająca zasoby dla innych aplikacji (API).
- **frontend**: Frontend strony internetowej.
- **editor-backend**: Backend dostarczający zasoby dla edytora oraz pewne dane dla frontu.
- **editor**: Frontend edytora.

Wszystkie aplikacje korzystają z authapp w celu obsługi tokenów i autoryzacji.
# Inicjalizacja reopozytorium
#
 ``` bash
git clone git@github.com:dreamsoft-pro/Dockerized.git -b master
cd Dockerized
git submodule update --init --recursive

```
#
## Struktura katalogów

Główna struktura katalogów projektu:


### Opis katalogów:

- **data/**: Zawiera pliki statyczne wykorzystywane przez aplikacje.
- **database/**: Zawiera pliki bazy danych oraz zrzuty.
- **docker/**: Skrypty i pliki pomocnicze do konfiguracji środowiska Docker.
- **proxy/**: Konfiguracje dla serwera proxy.

## Konfiguracja docker compose

W pliku `docker-compose.yml` skonfigurowane są usługi używane przez aplikację, m.in.:

- **proxy**: Serwer proxy NGINX.
- **mongo**: MongoDB.
- **mysql**: MariaDB.
- **phpmyadmin** 
- **authapp**
- **backend**
- **manager**
- **frontend**
- **editor-backend**
- **editor**

### Kluczowe zmienne środowiskowe:

- **secretKey**: Klucz wykorzystywany do szyfrowania JsonWebToken.
- **COMPANY_ID**: Identyfikator firmy (w tym przypadku: 25).
- **STATIC_URL**: URL plików statycznych.
- **DB_MASTER_HOST**: Adres hosta bazy danych MySQL.
- **DB_MASTER_USER**: Użytkownik główny bazy danych.
- **DB_MASTER_PASSWORD**: Hasło do bazy danych.
- **MONGODB_HOST**: Adres hosta MongoDB.
- **MONGODB_USER**: Użytkownik bazy MongoDB.
- **MONGODB_PASS**: Hasło do bazy MongoDB.
- **APP_PORT**: Port, na którym działa dana aplikacja.

Większość zmiennych środowiskowych przechowuje dane związane z integracją aplikacji z innymi usługami

## Ważne instrukcje

## Uruchamianie aplikacji

Aby uruchomić całe środowisko deweloperskie, wykonaj:

1. Skonfiguruj plik `.env` dla każdej aplikacji, upewniając się, że wszystkie wymagane zmienne są ustawione poprawnie.

2. Uruchom kontenery Docker przy użyciu polecenia:

   ```bash
   docker compose -f docker-compose-dev.yml up --build -d
   ```

Zbuduje obrazy Docker dla wszystkich usług i uruchomi je.

3. Po uruchomieniu należy zbudować node poleceniem 

   ```bash
   docker compose -f docker-compose-dev.yml run -it editor npm i
   ``` 

4. Budujemy backend poleceniem
   ```bash
   docker compose -f ./docker-compose-dev.yml exec -it backend composer install
   ``` 

5. Zaaduj baze mongodb poleceniem

   ```bash
   docker compose -f ./docker-compose-dev.yml exec -it mongo mongorestore -u admin -p M0nG0f69b54 -h 127.0.0.1 --port=27017
   ``` 

6. Zresetuj aplikacje poleceniem

   ```bash
   docker compose -f ./docker-compose-dev.yml restart
   ``` 
7. Aplikacje będą dostępne pod odpowiednimi adresami, np. `http://localtest.me/`.

### Dostosowanie pliku hosts (opcjonalne)

Aby móc korzystać z niestandardowych domen lokalnych, należy dodać wpisy do pliku `hosts`:

```
127.0.0.1 localtest.me
127.0.0.1 authapp.localtest.me
127.0.0.1 editor.localtest.me
...
```

**Uwaga:** Domeny `*.localtest.me` wskazują automatycznie na `127.0.0.1`, ale warto upewnić się, że wszystko działa poprawnie.


### Backup i przywracanie danych:

- Kopie zapasowe bazy danych MongoDB są przechowywane w katalogu `./docker/mongo-import/mongo-backup`.
- Przywracanie danych MongoDB można uruchomić z kontenera `mongo-restore`.

### Zarządzanie bazą MySQL:

- Zarządzanie bazą MySQL odbywa się za pośrednictwem phpMyAdmin dostępnego pod adresem `http://myadmin.localtest.me/`.

---
### Zarządzanie proxy:

- Zarządzanie proxy odbywa sie za pośrednictwem aplikacji pod adresem: `http://proxy.localtest.me/`
- login: ``admin@example.dev``
- hasło: ``>,8*,%!zCkUMGX_``
- po uruchomieniu należy odświeżyć hosty klikając w przycisk "Edit" i "Save"  

### editor-backend
- Działa w trybie deweloperskim.

### editor
- Działa w trybie developerskim, administracyjnym (`npm run user`).
- Działa w trybie developerskim, użytkownika (`npm run user`).


---
## Instrukcja Pobierania Plików Static
Aby pobrać wszystkie pliki static, wykonaj poniższe kroki w katalogu głównym repozytorium:

### 1. Zmień właściciela folderu `data`
Wykonaj polecenie, aby zmienić właściciela folderu `data` na swojego użytkownika. Możesz użyć nazwy użytkownika lub jego ID.

   ```bash
   sudo chown <nazwa_użytkownika_lub_ID> <folder> -R
   ```

**Przykład:**

   ```bash
   sudo chown 1000:1000 ./data -R
   ```

### 2. Skopiuj pliki z kontenera Kubernetes
Użyj polecenia `kubectl cp`, aby skopiować pliki z kontenera Kubernetes do lokalnego folderu `data`.

   ```bash
   kubectl cp --namespace=<nazwa_namespace> <id_kontenera>:/var/www/app/ ./data/
   ```

**Przykład dla aktualnego wdrożenia:**

   ```bash
   kubectl cp --namespace=printworks static-655cbd95cf-b6fl2:/var/www/app/data/ ./data/
   ```

**Zmień prawa dostępu dla styli:**
w katalogu Dockerized

   ```bash
   sudo chmod 777 ./data/25/styles/ -R
   ```


### Uwagi ###
- **Czas Kopiowania:** Folder `data` ma rozmiar około 10 GB, więc proces kopiowania może potrwać kilka minut.
- **Błędy Sieci:** Jeśli podczas kopiowania pojawi się błąd sieci, możesz go zignorować. Proces powinien kontynuować poprawnie.
- **Gdyby kopiowanie z cloud'a nie działało:** ściągnij dane z google drive https://drive.google.com/drive/folders/1FOt8MYLTKWxPZAOL6u1vh0qNRMU9XpIs?usp=drive_link

