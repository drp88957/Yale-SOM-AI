---
type: story
source: The Goal — Eliyahu Goldratt (Ch. 14, "The matchstick game")
concepts: [theory-of-constraints, unintended-consequences]
situations: [fixing-a-bottleneck, designing-a-system, reading-data]
verified_by_deep: false
---

# The Matchsticks-and-Dice Game: Why "Average" Plans Fall Behind

**One-line hook:** A simple game with a die and some matchsticks shows why a plan that works "on average" still ends up late.

## The Story
Halfway through the Boy Scout hike, Alex Rogo is still chewing on Jonah's riddle. Jonah had said that a **balanced plant**, one where every resource has exactly enough capacity to meet demand, is a road to bankruptcy. The reason, he said, is the mix of **dependent events** and **statistical fluctuations**. Alex has watched the line of scouts stretch out on the trail, and he can feel the answer is close. When the troop stops for a break, he decides to test the idea with a game.

He finds a box of matches and some bowls, and he asks a few of the boys to help. Five boys sit in a row. Between each pair of boys he places a bowl. The first boy in the line has the box of matches as his supply. The last boy's matches go into a pile at the end, which counts as the finished output of the whole line.

The rules are simple. On each turn, each boy rolls a single die. Whatever number he rolls is the number of matches he may move from the bowl on his left to the bowl on his right. But there is a catch. He can move only as many matches as are actually in his bowl. If he rolls a five and his bowl holds only two matches, he moves two. The rest of his roll is wasted.

Alex explains it to the boys as a kind of factory. Each boy is a machine or a work station. The matches are parts moving through the plant. The roll of the die is how much a station can do in a given period. Sometimes it does a lot, sometimes only a little, but on average it does a steady amount. The line is perfectly **balanced**: every boy has the same die, so every station has exactly the same capacity.

A die rolls an average of **3.5**. So everyone expects the line to deliver, on average, about 3.5 matches per turn out of the end. Over many turns, the total should be roughly 3.5 times the number of turns. Alex keeps score. He tracks how far the output at the end of the line is above or below that expected average as the game goes on.

It doesn't work out the way anyone expects. The boys roll, move and roll again. Soon matches start to **pile up** in some of the bowls. One boy rolls low a few times in a row, and a stack forms in the bowl in front of him. Further down the line, other boys roll high but have nothing in their bowls to move. Their good rolls are wasted. The last boy, who determines the output of the whole line, keeps having turns where he can move only a few matches or none at all.

As the turns go by, the total at the end of the line falls further and further **below the average**. It doesn't hover around 3.5 per turn and balance out. It drifts down and stays down. Meanwhile, the number of matches sitting in the bowls between the boys keeps growing. The line has more and more work in progress, and less and less finished output.

Alex works out why. In a line of dependent steps, a **low roll** holds back everyone downstream. Its effect passes down the line. But a **high roll** can only be used if the matches have actually arrived. A fast station can never do more than the slow station before it allows. So the slow periods add up as they move down the line, while the fast periods are capped. **Delays accumulate. Gains don't.** The averages don't cancel out, because the system can't bank the good luck to make up for the bad.

The game makes sense of what Alex saw on the trail. The scouts had the same problem. A slow moment for one boy slowed everyone behind him, while a fast moment for a boy behind was blocked by the boy in front. The line stretched out, which was like inventory piling up.

Most of all, the game explains Jonah's warning about a balanced plant. Managers try to cut every resource down to exactly the capacity the average demand requires, with no spare. They think this is efficient. But in a real plant every step varies and depends on the steps before it. With no spare capacity anywhere, a station that falls behind can never catch up, because the stations after it have no extra room to recover. The result is just what Alex's own plant shows: **inventory that keeps growing and orders that keep running late**, even though every machine looks fine on its own.

Alex comes away from the game with a new way to see his plant. Capacity can't be balanced to demand. What has to be managed is the **flow** through the whole line, and where it gets held up.

## Details Worth Remembering
- Alex runs the game during a stop on the scout hike.
- Five boys sit in a row with bowls of matches between them.
- Each boy rolls one die and moves that many matches to the next bowl, but only if they're there.
- Every boy has the same die, so the line is perfectly balanced.
- The expected output is about 3.5 matches per turn, since that is a die's average.
- Real output falls further and further below the average as the game goes on.
- Matches pile up in the bowls between boys while good rolls downstream are wasted.
- The core rule: in dependent steps, delays accumulate but gains are capped.

## The Lesson
**In a chain of dependent steps, delays add up but gains don't.** Plans based on averages fall behind, and cutting all spare capacity makes it worse. Manage the flow through the whole chain, and keep protective capacity and buffers in the right places, especially in front of the constraint.

## When to Use This
- Your project plan assumes every task will take its "expected" time
- A multi-handoff process keeps slipping even though each step looks fine
- Someone wants to cut all slack to make every resource 100% busy
- You're estimating timelines for dependent work
- Work-in-progress keeps growing while finished output stays flat

## Try This
- Play the game yourself with a few colleagues, a die and some coins. It takes ten minutes and makes the point better than any slide.
- Add a protective time buffer in front of the most critical step, not padding on every task.
- Track where work piles up across handoffs, not just how long each step takes.

## Related
- [[Herbie and the Scout Hike: Your Team Is Only as Fast as Its Slowest Hiker]]: the same hike, where the line of scouts shows the same effect
- [[Cut the Batches in Half: Speed as a Weapon]]: how less waiting work shortens the whole line
- [[The Toyota Way]]: leveling the workload so the line runs smoothly
- [[The Data Detective]]: why averages hide what's really going on
- [[It's Not Luck (The Goal 2)]]: buffers and constraints applied beyond the factory

## Aha Prompt
*"Where am I planning on the average and ignoring how delays stack up?"*
