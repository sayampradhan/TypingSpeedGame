# import necessary library
from faker import Faker

# create Faker instance
fake = Faker()


def count():
    with open("text_sample.txt", 'r') as t:
        a = t.readlines()
        count = 0
        for i in a:
            count += 1

        print(count)


def generate_paragraphs(num_paragraphs, max_length, batch_size=100):
    count = 0
    batch = []
    while count < num_paragraphs:
        paragraph = fake.paragraph()
        if len(paragraph) < max_length:
            batch.append(paragraph)
            count += 1
            if len(batch) == batch_size:
                yield '\n'.join(batch) + '\n'
                batch = []
    if batch:
        yield '\n'.join(batch) + '\n'


# Write each batch of paragraphs
with open('text_sample.txt', 'a') as t:
    for batch in generate_paragraphs(100, 100):
        t.write(batch)

print("Success...!!")
