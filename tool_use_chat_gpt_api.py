import openai

# ✅ Nastavení API
openai.api_key = 'YOUR_OPENAI_API_KEY'

# 🔧 Definice výpočetní funkce
def calculate(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Chyba při výpočtu: {e}"

# 🧠 Funkce volající LLM a nástroj
def run_conversation(user_input):
    # 1️⃣ Pošleme dotaz LLM s instrukcí, aby použil nástroj pokud je třeba
    system_message = {
        "role": "system",
        "content": (
            "Jsi chytrý asistent. Pokud uživatel zadá matematický výraz, napiš 'TOOL: výraz' "
            "a já nástroj použiju a výsledek ti pošlu zpět."
        )
    }
    messages = [
        system_message,
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",  # nebo "gpt-3.5-turbo"
        messages=messages,
        temperature=0
    )

    reply = response.choices[0].message["content"]
    print("LLM odpověď:", reply)

    # 2️⃣ Pokud LLM chce použít nástroj:
    if reply.startswith("TOOL:"):
        expression = reply.replace("TOOL:", "").strip()
        tool_result = calculate(expression)
        print("Výsledek nástroje:", tool_result)

        # 3️⃣ Pošleme výsledek nástroje zpět LLM
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"Výsledek: {tool_result}"})

        final_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0
        )
        return final_response.choices[0].message["content"]
    else:
        return reply

# 🧪 Test
if __name__ == "__main__":
    user_query = "Kolik je (25 + 17) * 3?"
    result = run_conversation(user_query)
    print("\n🔚 Finální odpověď:", result)


# Test
if __name__ == "__main__":
    user_query = "Kolik je (25 + 17) * 3?"
    result = run_conversation(user_query)
    print("\n🔚 Finální odpověď:", result)
