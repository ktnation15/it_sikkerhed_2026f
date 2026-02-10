# Kryptering og Hashing

## Valgte algoritmer
- **Password hashing:** bcrypt, fordi det er langsomt og modstandsdygtigt mod brute-force.
- **Kryptering:** Fernet (AES 128 CBC med HMAC), fordi det er simpelt, sikkert og giver autentificitet.

## Kryptering
- Data krypteres **før gemning** på disk.
- Formålet er at sikre følsomme oplysninger mod uautoriseret adgang.

## Dekryptering
- Data dekrypteres **kun når de skal bruges**.
- Formålet er at minimere tiden følsomme oplysninger er i hukommelsen.

## Fjernelse af dekrypteret data
- Dekrypterede data fjernes straks efter brug.
- Dette reducerer risikoen for memory-dumps eller malware, der læser følsomme data.

## Andre hensyn
- Nøgler bør opbevares sikkert (miljøvariabler, key vault, eller password manager).
- Krypteringsnøgler må ikke hardcodes i koden.
