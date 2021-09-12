import re


def to_safe(text):
    text = re.sub('<script>.*</script>', '', text)
    text = re.sub('<style>.*</style>', '', text)
    text = text.replace('<script>', '').replace('</script>', '').replace('<style>', '').replace('</style>', '')
    return text


clean = lambda text: re.sub('<.+?>', ' ', text)
