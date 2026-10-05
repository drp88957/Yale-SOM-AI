---
type: story
source: SuperFreakonomics — Steven Levitt & Stephen Dubner (Ch. 2, "Why Should Suicide Bombers Buy Life Insurance?")
concepts: [incentives, information-asymmetry, surveillance-and-privacy]
situations: [reading-data, managing-risk, designing-a-system]
verified_by_deep: false
---

# The Banker Who Hunted Terrorists in Bank Data

**One-line hook:** After the London bombings, a British bank fraud officer built an algorithm to spot terrorists from ordinary banking habits, and one of the clearest warning signs was that they didn't buy life insurance.

## The Story
Levitt and Dubner set up this story with a sober look at **terrorism**. The image of the terrorist as a poor, uneducated, desperate young man is mostly wrong. Research by the economist Alan Krueger found that terrorists tend to come from middle-class backgrounds and are often better educated than average. Terrorism is attractive to its practitioners for a cold economic reason: it is **cheap**, and its effects go far beyond the people it kills. A handful of attackers can make millions of people afraid to fly, shop or ride a train, and can push governments into spending enormous sums on security. The fear is the point.

So the question becomes practical. How do you find a terrorist **before** he acts? Intelligence agencies have their methods. The authors tell the story of a man coming at it from a very different angle. They call him **Ian Horsley**, a pseudonym, because his work was sensitive. Horsley worked in the fraud department of a large British bank. He was not a spy or a policeman. His job was to catch people stealing from the bank's customers, and he was good at reading the patterns that money leaves behind.

After the **July 2005 London bombings**, when suicide bombers attacked the Underground and a bus, Horsley started wondering whether the same techniques he used to catch fraudsters could catch terrorists. Every person who lives in a modern economy leaves a financial trail: where they bank, how they get paid, what they spend money on, how they move money around. Terrorists have to live somewhere, eat, travel and buy things too. Maybe their trails looked different.

Horsley had an advantage most researchers don't. The bank held the records of a number of people who had been arrested or identified as terrorism suspects. He could compare their banking behaviour with that of the bank's millions of ordinary customers and look for the habits that set them apart. Working with Levitt, he built an **algorithm**, a set of markers that, taken together, flagged the accounts most likely to belong to someone involved in terrorism.

Some of the markers were what you might expect, demographic and lifestyle traits common among the known suspects. Others were more subtle, patterns in how and when money moved. One of the strongest signs was **the absence of life insurance**. That made grim sense. Life insurance policies generally don't pay out for suicide, and a man planning to blow himself up has no reason to buy a policy that will not protect his family. Ordinary young men with families and jobs often had life insurance. The suspects didn't.

The authors add a deliberate tease. There was another marker in the algorithm that was especially powerful, and they **refuse to reveal it**, so that terrorists can't learn to avoid it. The life-insurance marker, by contrast, they happily share, which leads to the chapter's title. If you are a would-be suicide bomber and want to avoid being caught by the bank's algorithm, the authors suggest, you should go and **buy some life insurance**. The joke has a real point: once a marker is public, people can game it, and the most useful signals are the ones the target doesn't know about.

The story also contains a sobering lesson about prediction. The trouble with hunting terrorists is that **real terrorists are extremely rare**. Imagine an algorithm that is right 99 percent of the time. Run it over tens of millions of bank customers and that 1 percent error rate still flags hundreds of thousands of innocent people, burying the handful of real suspects. To be useful, an algorithm must be accurate to an extraordinary degree. Horsley's ended up producing a short list of high-probability accounts small enough for authorities to examine, and the authors report that it looked promising, though they are careful about how much they can say.

The deeper message runs through the whole chapter. People's lives are shaped by forces they don't see, and **their behaviour leaves traces they don't notice**. A data analyst who asks the right question can find patterns that even trained investigators miss.

It is also a story about **where expertise comes from**. Horsley was not a counter-terrorism specialist. He was a bank employee who knew one kind of data extremely well and asked whether his tools could answer a question outside his job description. The authors return to this kind of figure again and again in the book: the outsider who brings an unusual dataset to an old problem.

## Details Worth Remembering
- Research by Alan Krueger found terrorists are often middle-class and educated, not poor and illiterate
- Terrorism is cheap for attackers and spreads fear and costs far beyond its direct damage
- "Ian Horsley" is a pseudonym for a fraud officer at a large British bank
- After the 2005 London bombings, he built an algorithm comparing known suspects' banking habits with ordinary customers'
- A strong marker: suspects rarely had **life insurance**, which doesn't pay out for a suicide attack
- The authors keep one powerful marker secret, so it can't be gamed
- Because terrorists are so rare, even a highly accurate algorithm flags many innocent people (the false-positive problem)

## The Lesson
Behaviour leaves a data trail, and the absence of something (like insurance) can be as revealing as its presence. But when you hunt for something rare, even a very accurate test produces mostly false alarms, and any signal that becomes public will be gamed.

## When to Use This
- You're building a model to detect rare events such as fraud, churn, defects or security threats
- Someone proposes flagging people based on a test that is "99 percent accurate"
- You're deciding which warning signs to publish and which to keep internal
- You're looking for overlooked signals in data your organisation already holds
- You're weighing the privacy cost of using customer data against its safety value

## Try This
- Before trusting a detection rule, estimate how many false positives it will produce when the real cases are rare.
- Look for "missing" behaviour in your data: things your target group conspicuously doesn't do.
- Keep your most useful detection signals private, and assume any public rule will be gamed.

## Related
- [[How to Lie with Statistics]]: how impressive accuracy figures can mislead
- [[No Place to Hide]]: the privacy cost of mining personal data for security
- [[The Data Detective]]: asking what a number really tells you
- [[Freakonomics]]: the first book's algorithms for catching cheating teachers and sumo wrestlers

## Aha Prompt
*"If the thing I'm hunting is rare, how many false alarms will my test raise for every real catch?"*
