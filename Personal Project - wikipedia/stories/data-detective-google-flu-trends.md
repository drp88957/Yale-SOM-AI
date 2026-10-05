---
type: story
source: The Data Detective — Tim Harford (Rule 7, "Demand Transparency When the Computer Says No")
concepts: [correlation-vs-causation, misleading-statistics, information-networks]
situations: [technology-and-society, reading-data, managing-risk]
verified_by_deep: false
---

# Google Flu Trends: The Algorithm That Knew Everything Until It Didn't

**One-line hook:** Google claimed it could spot flu outbreaks from search data faster than the government, and for a while it could, until the correlations it never understood quietly fell apart.

## The Story
In 2009 a team of researchers at Google published a paper in the scientific journal *Nature* that seemed to announce a new era. Every day, millions of people type their symptoms into Google: "fever", "sore throat", "flu remedies". The team reasoned that the volume of such searches in a region should rise when flu spread there. They took the company's enormous archive of search queries and compared it with the records of flu cases kept by the US **Centers for Disease Control and Prevention** (CDC).

The CDC's figures were reliable but slow, because they depended on reports from doctors' surgeries and took a week or two to compile. Google's idea was to beat them. Its engineers tested tens of millions of possible search terms, looking for the ones whose ups and downs best matched the CDC's historical flu data. They found a set of terms that tracked flu remarkably well. The result was **Google Flu Trends**, a model that could estimate flu levels across America almost in real time, about a week or two ahead of the official numbers.

It was quick, cheap and seemed almost magical. It needed no doctors, no lab tests and no theory of what caused people to search for what. Just enough data and enough computing power. Enthusiasts hailed it as proof that **big data** would transform science: that with enough data, you could find patterns without needing to understand them, and correlation would be enough.

For a few years, it worked. Then it went wrong. In the winter of 2012 to 2013, Google Flu Trends predicted a huge flu outbreak. Its estimate was roughly **double** what the CDC eventually recorded. The model that had been faster than the experts was now badly, embarrassingly wrong, and nobody could say exactly why.

Harford explains the problem. Google's engineers had found correlations between search terms and flu, but they didn't know **which searches were causally linked to flu and which were coincidences**. Among millions of search terms, some will match flu seasons by pure chance, such as searches related to winter activities that happen to peak at the same time. And even the genuinely flu-related searches depended on human behaviour that could change. A frightening news story about flu could send healthy people rushing to search for symptoms. Changes in how Google itself suggested search terms could shift what people typed. A model built purely on correlation has no way to know when the world it learned from has changed.

For Harford, this is the danger of treating algorithms as oracles. Google Flu Trends was not a fraud or a disaster. It was a clever experiment that broke. The real problem was the hype around it, and the fact that its details were hidden. Outsiders couldn't easily see which terms it used or why. When things went wrong, there was little chance for independent experts to spot the problem early or help fix it.

He sets this alongside other cases from the same chapter. The retailer **Target** was famously said to have predicted a teenage girl's pregnancy from her shopping before her father knew. Harford points out that we hear about the dramatic hit, but not about the many women sent baby-product coupons who were not pregnant at all. He also describes **COMPAS**, a tool used in American courts to predict whether defendants would reoffend. Journalists argued it was unfair to black defendants; its makers argued it was equally accurate across races. Both could be true at once, because there are different, mathematically incompatible definitions of fairness. The only way to have that debate at all was to be able to see how the algorithm worked.

Harford's rule is not "distrust computers". Algorithms can be enormously useful, and often more consistent than human judges. It is that **algorithms should be open to scrutiny**, the way scientific claims are. Science advanced when researchers began sharing their methods and results openly rather than hiding them, the way alchemists once guarded their secrets. When a computer makes a decision that affects people's lives, someone outside the company should be able to check it.

## Details Worth Remembering
- Google Flu Trends was announced in a 2009 paper in *Nature*.
- It matched search-term patterns to CDC flu records and claimed to be a week or two ahead of official data.
- In the 2012 to 2013 winter it overestimated flu by roughly double.
- The model found correlations without knowing which search terms really reflected flu.
- Target's pregnancy-prediction story ignores the false positives; COMPAS shows that "fair" has more than one mathematical definition.

## The Lesson
Patterns found in big data without understanding can break the moment the world shifts. Treat algorithms like scientific claims: insist they be tested, explained and open to inspection, especially when they affect people's lives.

## When to Use This
- Someone proposes a model that "just works" without anyone knowing why
- A vendor sells a black-box tool for hiring, lending or risk scoring
- Your forecasting model suddenly starts drifting from reality
- Leaders want to replace expert judgement with an algorithm overnight
- A story about an algorithm's uncanny accuracy goes viral

## Try This
- For any predictive model you use, ask: "What would make this correlation stop holding?"
- Keep comparing the model against slower, ground-truth data, as Google could have with the CDC.
- Ask for the false-positive rate, not just the success stories.

## Related
- [[The Chaos Machine]]: what happens when opaque algorithms shape what billions see
- [[Nexus]]: Harari on algorithms, information networks and the need for self-correction
- [[The Islanders Who Believed Lice Kept You Healthy]]: correlation mistaken for causation, the old-fashioned way
- [[Think Like a Rocket Scientist]]: testing assumptions before trusting them

## Aha Prompt
*"Do I know why this model works, and would I notice the day it stopped?"*
