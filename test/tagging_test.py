from api.service.tagging_service import BaseTaggingService


text = "hi"
tagger = BaseTaggingService()


while text != "quit":
    text = input("Test Text: ")

    p = tagger.predict(text)

    print(p)