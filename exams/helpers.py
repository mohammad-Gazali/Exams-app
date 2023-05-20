import re


def format_right_answer_essay(text: str):

    text_list = re.split(r"\s+|\n+", text.strip())

    # deleting empty texts
    filtered_text_list = filter(lambda x: x != "", text_list)

    # removing "," "." "!" "?" from the text
    edited_text_list = map(
        lambda x: x.replace(",", "").replace(".", "").replace("!", "").replace("?", ""),
        filtered_text_list,
    )

    return edited_text_list
