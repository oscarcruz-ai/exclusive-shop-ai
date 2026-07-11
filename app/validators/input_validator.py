import re


class InputValidator:

    def validar(self, texto: str):

        texto = texto.strip()

        if not texto:
            return "🤔 No recibí ninguna consulta. ¿En qué producto puedo ayudarte?"

        # Muy corto
        if len(texto) <= 1:
            return "😊 ¿Podrías escribir un poco más para poder ayudarte?"

        # Solo números
        if texto.isdigit():
            return "🔎 ¿Podrías indicarme qué producto estás buscando?"

        # Solo símbolos
        if re.fullmatch(r"[^\w\s]+", texto):
            return "😊 ¿Podrías escribir tu consulta con más detalle?"

        # Solo emojis (o caracteres no alfanuméricos)
        if not re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñ0-9]", texto):
            return "😊 ¿En qué producto puedo ayudarte?"

        texto_lower = texto.lower()

        # Letras repetidas
        repetidas = [
            "aaaa", "bbbb", "cccc", "dddd",
            "eeee", "ffff", "gggg", "hhhh",
            "iiii", "jjjj", "kkkk", "llll",
            "mmmm", "nnnn", "oooo", "pppp",
            "qqqq", "rrrr", "ssss", "tttt",
            "uuuu", "vvvv", "wwww", "xxxx",
            "yyyy", "zzzz"
        ]

        for r in repetidas:
            if r in texto_lower:
                return "😊 Estoy para ayudarte a encontrar productos. ¿Qué estás buscando?"

        # Palabras típicas sin sentido
        basura = {
            "asdf",
            "asdfgh",
            "qwerty",
            "zxcv",
            "abc",
            "prueba",
            "test",
            "xxxxx",
            "jeje",
            "jaja",
            "xd",
            "xdxd"
        }

        if texto_lower in basura:
            return "😊 ¿Qué producto o marca te gustaría consultar?"

        # Spam muy largo
        if len(texto.split()) > 30:
            return "😊 ¿Podrías resumir un poco tu consulta?"

        return None