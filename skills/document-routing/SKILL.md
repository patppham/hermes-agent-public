# Private document routing

Use this contract when a question may depend on household, identity, property,
insurance, tax, legal, or medical documents.

Start with a private manifest and source order. Search only the configured
private index or document store, preserve document scope and freshness, and
read exact sensitive values only when the authorized owner asks for them.
Return a short answer with source location and uncertainty. If there is no
match, say so instead of filling the gap from memory.

Do not publish document metadata, index raw documents into a public corpus, or
send a document-derived answer to a shared audience without an explicit
redaction and routing decision. Retrieval adapters and credentials remain
private.
