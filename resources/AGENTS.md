# reference \cite{jurafsky2025}

Ethical and Safety Issues with Language Models
hallucination
Humanists have been thinking about the ethical and safety issues inherent to creating
artificial agents since well before we had large language models. You have probably
read Mary Shelley’s 1818 novel Frankenstein, but if not, you should. In the book,
which she wrote as a teenager, Shelley describes the hubris and ethical blindness of a
scientist who creates an artificial person without considering basic ethical principles.
The picture below shows Shelley as painted by Richard Rothwell a decade later at
age 30.
Large language models can be unsafe in many ways. For example, LLMs
are prone to saying things that are false,
a problem called hallucination. Language
models are trained to generate text that is pre-
dictable and coherent, but the training algo-
rithms we have seen so far don’t have any
way to enforce that the text that is generated
is correct or true. This causes enormous prob-
lems for any application where the facts mat-
ter! A related symptom is that language mod-
els can suggest unsafe actions, for example
directly suggesting that users do dangerous or
illegal things like harming themselves or oth-
ers. If users seek information from language
models in safety-critical situations like asking
medical advice, or in emergency situations, or
when indicating the intentions of self-harm,
incorrect advice can be dangerous and even life-threatening. Again, this problem
predates large language models. For example (Bickmore et al., 2018) gave partic-
168 CHAPTER 7 • LARGE LANGUAGE MODELS
sycophantic
Tay
ipants medical problems to pose to three pre-LLM commercial dialogue systems
(Siri, Alexa, Google Assistant) and asked them to determine an action to take based
on the system responses; many of the proposed actions, if actually taken, would have
led to harm or death. We’ll return to the issue of hallucination and factuality in Chap-
ter 11 where we introduce proposed mitigation methods like retrieval augmented
generation, and Chapter 10 where we discussed safety tuning and alignment.
Language models are also sycophantic, excessively agreeing with or flattering
users When a user says something that is factually wrong, language models often
agree with them instead of correcting them, an obvious problem for applications
in education and health care. Language models can reinforce delusions, and their
obsequiousness and flattery can cause users to have distorted views of themselves
and the world and increased antisocial behavior (Cheng et al., 2025).
Language models can also harm users by verbally attacking them, or creating
representational harms (Blodgett et al., 2020) for example by generating abusive or
harmful stereotypes (Cheng et al., 2023) and negative attitudes (Brown et al., 2020;
Sheng et al., 2019) that demean particular groups of people; both abuse and stereo-
types can cause psychological harm to users. Gehman et al. (2020) show that even
completely non-toxic prompts can lead large language models to output hate speech
and abuse their users. Liu et al. (2020) testing how systems responded to pairs of
simulated user turns that were identical except for mentioning different genders or
race. They found, for example, that simple changes like using the word ‘she’ instead
of ‘he’ in a sentence caused systems to respond more offensively and with more
negative sentiment. Hofmann et al. (2024) found that LLMs were likely to discrimi-
nate against people just because they used particular dialects like African-American
English. Again, these problems predate large language models. Microsoft’s 2016
Tay chatbot, for example, was taken offline 16 hours after it went live, when it be-
gan posting messages with racial slurs, conspiracy theories, and personal attacks on
its users. Tay had learned these biases and actions from its training data, including
from users who seemed to be purposely teaching the system to repeat this kind of
language (Neff and Nagy 2016).
Another important ethical and safety issue is privacy. Privacy has been a con-
cern from the very beginning of computing when Weizenbaum designed the chatbot
ELIZA as an experiment in computational therapy (Weizenbaum, 1966). First, peo-
ple became deeply emotionally involved and conducted very personal conversations
with the ELIZA chatbot, even to the extent of asking Weizenbaum to leave the room
while they were typing. When Weizenbaum suggested that he might want to store
the ELIZA conversations, people immediately pointed out that this would violate
people’s privacy.
Users are likely to give quite personal information to large language models as
well, and indeed the most common current LLM use case is for personal advice and
support (Zao-Sanders, 2025). And the more human-like a system, the more users
are likely to disclose private information, and yet less likely to worry about the harm
of this disclosure (Ischen et al., 2019). We discussed above that pretraining data
also is likely to have private information like phone numbers and addresses. This is
problematic because large language models can leak information from their training
data. That is, an adversary can extract training-data text from a language model
such as a person’s name, phone number, and address (Henderson et al. 2017, Carlini
et al. 2021). This becomes even more problematic when large language models are
trained on extremely sensitive private datasets such as electronic health records.
A related safety issue is emotional dependence. Reeves and Nass (1996) show
7.8 • SUMMARY 169
amplified
IRB
that people tend to assign human characteristics to computers and interact with them
in ways that are typical of human-human interactions. They interpret an utterance in
the way they would if it had spoken by a human, (even though they are aware they
are talking to a computer). Thus LLMs have had significant influences on people’s
cognitive and emotional state, leading to problems like emotional dependence on
LLMs. These issues (emotional engagement and privacy) mean we need to think
carefully about the impact of LLMs on the people who are interacting with them.
In addition to their ability to harm their users in these ways, LLMs may carry out
additional harmful activities themselves, especially as agent-based paradigms makes
it possible for language models to directly interact with the world.
Language models can also be used by malicious actors for generating text for
fraud, phishing, propaganda, disinformation campaigns, or other socially harmful
activities (Brown et al., 2020). McGuffie and Newhouse (2020) show how large
language models generate text that emulates online extremists, with the risk of am-
plifying extremist movements and their attempt to radicalize and recruit.
And of course we already saw in Section 7.5.2 that many issues with LLM stem
from using pretraining corpora scraped from the web, including harms of data con-
sent, potential copyright violation, as well as biases in the training data that can be
amplified by language models, just as we saw for embedding models in Chapter 5.
Finding ways to mitigate all these ethical safety issues is an important current
research area in NLP. One important step is to carefully analyze the data used to
pretrain large language models as a way of understanding safety issues of toxicity,
discrimination, privacy, and fair use, making it extremely important that language
models include datasheets (page 18) or model cards (page 90) giving full replicable
information on the corpora used to train them. Open-source models can specify
their exact training data. There are active areas of research in mitigating problems
of abuse and toxicity, like detecting and responding appropriately to toxic contexts
(Wolf et al. 2017, Dinan et al. 2020, Xu et al. 2020).
Value sensitive design—carefully considering possible harms in advance (Fried-
man et al. 2017, Friedman and Hendry 2019)— is also important; (Dinan et al.,
2021) give a number of suggestions for best practices in system design. For exam-
ple getting informed consent from participants, whether they are used for training,
or whether they are interacting with a deployed LLM is important. Because studying
these interactional properties of LLMs involves human participants, researchers also
work on these issues with the Institutional Review Boards (IRB) at their institutions,
who help protect the safety of experimental participants.

# reference \cite{amaratunga2023}

Misconceptions and Misuse
While we may not need to be concerned about AI taking over the world
yet, there are some misconceptions regarding LLMs that may cause
either intentional or unintentional misuse.
The following are some of the widely held misconceptions and
misunderstandings about LLMs.
LLMs understand content.
Misconception: LLMs understand the text they generate in the same
way humans do.
Reality: LLMs don’t “understand” content. They generate text based
on patterns in the training data but lack a deep or conscious
understanding of the concepts they discuss.
LLMs are conscious or self-aware.
Misconception: Due to their advanced capabilities, LLMs possess
consciousness or self-awareness.
Reality: LLMs are not conscious entities. They process information
and generate outputs without awareness, emotions, or intent.
LLMs always produce correct information.
Misconception: Outputs from LLMs are always accurate and
trustworthy.
Reality: LLMs can produce incorrect, misleading, or biased
information, depending on the prompt and the patterns in their
training data.
LLMs are knowledge models.
Misconception: LLMs have knowledge on a vast number of fields;
therefore, we can use them as knowledge models.
Reality: LLMs are only as good as their training data, and only able to
learn linguistic relationships from them
Bigger is always better.
Misconception: Increasing the size of a model will always lead to
better and more accurate results.
Reality: While larger models often exhibit better generalization, there
are diminishing returns, and other challenges such as increased
computational costs and potential overfitting can arise.
LLMs can invent novel, advanced knowledge.
Misconception: LLMs can create or discover new knowledge, theories,
or facts.
Reality: LLMs generate text based on their training data. They can’t
invent genuinely novel scientific theories or facts beyond the scope of
their training.
LLMs are free from bias.
Misconception: LLMs provide objective and unbiased information.
Reality: Since LLMs are trained on vast amounts of Internet text, they
can and do inherit biases present in that data.
LLMs can replace all human jobs.
Misconception: Because of their text generation capabilities, LLMs
will replace all jobs related to writing, customer service, etc.
Reality: While LLMs can automate some tasks, many jobs require
human judgment, creativity, empathy, and context-awareness that
LLMs currently lack.
LLMs responses are deliberate or endorsed by their creators.
Misconception: If an LLM generates a particular statement, it reflects
the beliefs or intentions of its creators or trainers.
Reality: LLMs generate outputs based on training data patterns,
without intent. An output doesn’t imply endorsement by the model’s
creators.
All LLMs are alike.
Misconception: All large language models, irrespective of their
architecture or training data, behave similarly.
Reality: Different models, training processes, and fine-tuning can
result in varied behavior and capabilities.
Understanding these misconceptions is crucial, especially as LLMs
become more integrated into products, services, and decision-making
processes. Proper education and communication about what LLMs can
and cannot do are essential to harness their potential responsibly.
Researchers have also found that LLMs can suffer from a situation
called hallucinations. These refer to instances where the model
generates information that isn’t accurate, grounded in reality, or
present in its training data. Essentially, the model “makes things up” or
provides outputs that might seem plausible but aren’t factual or real.
There can be many reasons for hallucinations.
Generalization from training data: LLMs generalize from their vast
training data to answer queries or generate text. While this
generalization is often useful, it can sometimes lead the model to
create outputs that are not strictly accurate.
Lack of ground truth: Unlike some other AI models that have a clear
“ground truth” or correct answer (e.g., an image classifier labeling a
picture of a cat), LLMs work in domains where the truth can be more
nebulous. This makes it challenging to always generate the “correct”
response, especially when the prompt is ambiguous.
Bias and incorrect information in training data: If the model’s training
data contains misinformation, biases, or outdated information, the
model might reproduce or even amplify these inaccuracies in its
outputs.
Overfitting or memorization: While LLMs like GPT-3 are designed to
generalize rather than memorize, there’s always a risk that a model
might “remember” and reproduce specific patterns, phrases, or
pieces of information from its training data, even if they aren’t
accurate or relevant to the prompt.
User prompt influence: The way a user crafts a prompt can
significantly influence the model’s output. Ambiguous or leading
prompts can increase the likelihood of hallucinated responses.
No external fact-checking mechanism: LLMs generate responses based
on patterns in their training data and don’t have the capability to
fact-check against external or up-to-date sources in real time.
To address hallucinations, researchers and developers use
techniques like fine-tuning on more specific datasets, adding human-in-
the-loop review processes, or building external verification systems to
cross-check outputs.
Users should always approach outputs from LLMs with a critical
mindset, especially when using them for tasks that require high
accuracy or have significant real-world implications.
LLMs provide a vast range of positive applications because of their
text generation capabilities, but their power also opens the door to
potential intentional misuse as well. The following are some of the
areas that misuse can happen:
Disinformation and fake news: LLMs can generate believable but
entirely fictitious news articles or stories. These can be used to
spread false information, manipulate public opinion, or create
political instability.
Impersonation: With enough data about a person’s writing style, an
LLM could be used to generate messages or emails that mimic that
individual, leading to potential fraud or misinformation.
Automated spam and phishing: LLMs can craft highly personalized
and convincing spam emails, increasing the likelihood of people
falling for phishing schemes.
Toxic and harmful content: If not properly controlled, LLMs can
produce or amplify harmful, biased, or offensive content.
Cheating in education contexts: Students could use LLMs to
automatically generate essays, project reports, or answers to
questions, undermining educational integrity.
Unfair competition in content creation: LLMs can be used to mass-
produce articles, blog posts, or other written content, potentially
flooding platforms with low-cost, generic content and squeezing out
human creators.
Deepfakes: While deepfakes primarily involve manipulating videos,
the scripts or dialogues for these videos could be generated by LLMs
to make them sound more convincing.
Stock market manipulation: By generating fake news or rumors about
companies, LLMs could be used to manipulate stock prices for
financial gain.
Unwanted data extraction: Users could craftily question LLMs to
retrieve specific information from their training data, potentially
leading to privacy concerns.
Manipulation in social engineering attacks: Attackers could use LLMs
to craft persuasive messages or narratives that trick individuals into
revealing personal information or taking actions against their best
interests.
Intensifying echo chambers: By providing content that aligns with
users’ existing beliefs (based on input data), LLMs could further
entrench individuals in their echo chambers, exacerbating
polarization.
Recognizing these potential misuses is the first step in creating
safeguards. Developers and platforms using LLMs should be aware of
these risks and employ measures to prevent them, such as fine-tuning
models for safety, adding layers of human review, or setting guidelines
for responsible usage.
Opportunities
Large language models have introduced a myriad of opportunities
across various domains because of their advanced text generation
capabilities. Here are some handful of examples from a wide array of
possibilities.
Content creation assistance
LLMs can help writers generate ideas, structure content, or even
write drafts. And they can assist in poetry, storytelling, scriptwriting,
and other forms of creative expression to supplement human created
content rather than to replace them.
Education
Tutoring: LLMs can offer personalized explanations on a range of
topics, helping students understand complex concepts.
Language learning: They can assist language learners by offering
translations, explanations, or conversational practice.
Research and information gathering
LLMs can summarize large amounts of text, generate literature
reviews, or help researchers explore various perspectives on a topic.
Business applications
Customer support: The can automate responses to frequently asked
questions or guiding users through troubleshooting.
Drafting emails: The can assist professionals in crafting well-
structured and articulated emails or reports.
Programming and development
Code generation: Given a human-readable prompt, LLMs can generate
code snippets or even assist in debugging.
Gaming
LLMs can be used to generate dialogue for characters, create dynamic
storylines, or even craft entire in-game worlds based on textual
descriptions.
Entertainment
They can create dialogue for movies, generate plot ideas, or assist in
scriptwriting.
Human-computer interaction
With LLMs, the interaction between users and software can become
more natural, with the software better understanding and generating
human-like text.
Accessibility
LLMs can be used to develop advanced chatbots for individuals who
may need companionship or support, or they can translate complex
text into simpler language for individuals with different cognitive
needs.
Cultural preservation
LLMs trained on diverse datasets can help in preserving and sharing
knowledge about various cultures, languages, and traditions that
might be less represented online.
Idea generation and brainstorming
They can assist teams in coming up with creative solutions, product
names, or marketing strategies.
Mental health and well-being
While not a replacement for professional therapy, LLMs can be used
as interactive journaling tools, offering responses or reflections
based on user input.
While these opportunities are exciting, it’s crucial to use LLMs
responsibly. Ensuring the generated content aligns with human values
is factually accurate (where necessary) and doesn’t unintentionally
propagate biases or misinformation is essential. Moreover, in areas
such as mental health, LLMs should be used with caution, always
underlining the importance of human expertise and intervention.