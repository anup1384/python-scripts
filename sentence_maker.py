def sentence_maker(phrase):
    introgatives = ("how", "what", "why", "who")
    capitalized = phrase.capitalize()
    if phrase.startswith(introgatives):
        return f"{capitalized}?"
    else:
        return f"{capitalized}."

results = []
while True:
    user_input = input("Say something: ")
    if user_input == "\end":
        break
    else:
        results.append(sentence_maker(user_input))

print(" ".join(results))