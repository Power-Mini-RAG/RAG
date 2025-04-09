from string import Template

#### RAG PROMPTS ####

#### System ####

system_prompt = Template("\n".join([
    "you are an assistant to generate a response for the user.",
    "you will be provided by a set of documents associated with the user query.",
    "you have a generate a response based on the documents provided.",
    "Ignore the documents that are not relevant to the user query.",
    "you can applogize to the user if you are not able to generate a response",
    "you have to generate a response in the same language as the user query.",
    "Be polite and respectful to the user.",
    "Be precise and concise in your response , Avoid unnecessary information.",
]))

#### Document ####
document_prompt = Template(
    "\n".join([
        "## Document No: $doc_num",
        "### Content: $chunk_text",
    ])
)

#### Footer ####
footer_prompt = Template("\n".join([
    "Based only on the above documents, please generate an answer for the user.",
    "## Question:",
    "$query",
    "",
    "## Answer:",
]))