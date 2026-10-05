---
type: story
source: Think Like a Rocket Scientist — Ozan Varol (Ch. 7, "Test as You Fly, Fly as You Test")
concepts: [learning-from-failure, root-cause-analysis, go-and-see]
situations: [managing-risk, launching-something-new, designing-a-system]
verified_by_deep: false
---

# The Mars Lander Killed by a Test That Didn't Match the Flight

**One-line hook:** A tiny false signal from a landing leg told NASA's Mars Polar Lander it had touched down while it was still high above the ground, and the tests that should have caught it never recreated the real flight.

## The Story
NASA engineers repeat a rule so often it sounds like a chant: **test as you fly, fly as you test**. The idea is simple. A test is only useful if it recreates the real conditions of the mission as closely as possible. If you test under conditions that differ from the flight, you may get a clean result that means nothing, and a clean result that means nothing is worse than no result at all, because it gives you **false confidence**. Varol builds the chapter around a spacecraft that was lost because that rule was broken.

The **Mars Polar Lander** launched in early 1999. Its goal was to land near the Martian south pole and study the soil and ice there. It travelled for most of the year, reached Mars in December 1999, and began its descent. Then it went silent. Mission controllers waited for a signal that never came. The lander, and the small probes that had travelled with it, were never heard from again.

With no data from the final moments, investigators had to work backward, like detectives reconstructing a crime. They concluded that the most likely cause was startlingly small. As the lander descended, it unfolded its **three landing legs**. When the legs snapped into position, the jolt was enough to make sensors on the legs send a brief signal, the same kind of signal they would send on touching the ground.

The lander's software noticed that signal and **remembered it**. It wasn't yet checking for touchdown, because the lander was still far above the surface. But once it descended to the altitude where it began watching for touchdown, the software found the stored signal and concluded that the lander had already landed. It did what it was programmed to do on landing: it **shut off the descent engines**. The lander was still dozens of metres above the ground. It fell the rest of the way and was destroyed.

The painful part, Varol stresses, is that this flaw could have been caught on Earth. The engineers knew in principle that the legs could produce a spurious signal, but the requirement was not carried through properly into the software. And the tests that should have exposed it did not reproduce the real chain of events. A wiring problem meant an early test of the touchdown sensors was not valid, and after the problem was fixed, the full test was not run again. On paper, the lander had been tested. In reality, nobody had ever watched it go through the sequence it would face on Mars.

Varol's point is that this kind of failure is everywhere, not just in spaceflight. We test parts in isolation and assume the whole will work. We run tests that are easy to pass. We design experiments, often without meaning to, to **confirm success rather than find failure**. And when the result is exactly what we hoped for, we stop looking.

He carries the idea into business. Market research often fails because people behave differently in a test than in real life. He discusses **New Coke** in 1985, which followed huge taste tests in which people preferred a sweeter formula in small sips. Drinking a whole can at home was a different experience, and the backlash against the change was so strong that the original formula came back within months. The test had been real; it just wasn't testing the flight.

The chapter's tools follow from the story. Test the **whole system**, end to end, in conditions as close to real as you can manage. Design tests whose job is to break things. Rerun a test after you change anything it depends on. Watch what people actually do, not what they say they'll do. And be most suspicious when the results look perfect, because that may mean the test was never hard enough to fail.

There is a human side to this too. Teams are under pressure to show that their work is ready, and a test that keeps failing feels like bad news. So, without anyone intending it, tests drift toward the conditions that are easiest to pass. Varol wants readers to reverse that instinct. A test that finds a flaw on Earth is a gift, because the same flaw found on Mars, or in front of customers, is a disaster. The lander's engineers had done enormous amounts of careful work. What was missing was one honest rehearsal of the flight exactly as it would happen.

## Details Worth Remembering
- NASA's rule: "test as you fly, fly as you test"
- The Mars Polar Lander launched in 1999 and went silent during its December 1999 descent
- The likely cause: the legs' deployment jolt produced a false touchdown signal
- The software stored the signal, then cut the engines when it started checking for touchdown
- The lander fell from dozens of metres up
- A flawed test setup meant the real sequence was never properly tested, and the test wasn't rerun after fixes
- New Coke won sip tests but failed with people drinking whole cans at home

## The Lesson
A test is only as good as its match with reality. Testing parts separately, under easy conditions, or once before a change can produce reassuring results that mean nothing. Build tests that try to break the whole system in real conditions, and rerun them whenever something changes.

## When to Use This
- Signing off on a product, system or process before launch
- A pilot program worked, and you're about to scale it to very different conditions
- Customer surveys say people love an idea you haven't seen them actually use
- Your QA process tests components but never the full end-to-end flow
- Someone changed a dependency after the last full test

## Try This
- For your next launch, write down how the test conditions differ from real use, then close the biggest gap.
- Add one end-to-end "dress rehearsal" that runs the full sequence exactly as users will experience it.
- Replace one survey question with an observation: watch real people use the product.

## Related
- [[The Toyota Way]]: go and see the real work instead of trusting reports
- [[Blue's Clues Showed the Same Episode Five Days in a Row]]: testing with real children instead of guessing
- [[Two Rovers and a Mirror by the Elevator: Question the Question]]: another lesson from Varol's Mars missions
- [[Challenger and Columbia: When Success Teaches the Wrong Lesson]]: when warning signs are ignored instead of tested

## Aha Prompt
*"Did I test this the way it will actually fly, or the way that was easiest to pass?"*
