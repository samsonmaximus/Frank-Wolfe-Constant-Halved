# The paper in plain language

This page explains what the paper does, and how, for readers with no background
in mathematics or computer science. A glossary of the paper's terms follows at the
end.

## The problem: finding the lowest point without leaving the field

Imagine you are standing in a fenced field in thick fog, and you want to reach
its lowest point. You can't see the bottom. All you can feel is the slope of the
ground under your feet. The fence has a complicated shape, so if you wander
outside it, finding your way back in is hard work.

Many real problems look like this. A streaming service wants to fill in the
ratings its users haven't given yet. A city planner wants to predict how traffic
will spread over a road network. In both, there is a quantity to make as small as
possible (the height of the ground) and a set of rules the answer must obey (the
fence).

The **Frank–Wolfe method**, invented in 1956, handles the fence with one trick.
Wherever you stand, you feel which way the ground tilts. Then you ask a simpler
question: if the whole field tilted exactly like this, which point inside the
fence would be lowest? That question is easy to answer, even when the fence is
complicated. You walk part of the way toward that point, stop, feel the slope
again, and repeat.

Because you only ever walk toward points inside the fence, you never leave the
field. The share of the distance you walk shrinks on a fixed schedule: all the
way on the first step, then two-thirds, then a half, then two-fifths, and so on.

## The question: how fast does it get there?

Nobody runs the method forever. You stop after some number of steps, and you
want to know how close to the bottom you are. A **convergence rate** is a
promise of the form: "After N steps, you are within this much of the lowest
height, whatever the field looks like."

The standard promise, in the form textbooks quote (Jaggi, 2013), is: after N
steps, the distance to the bottom is at most **2 / (N + 2)**, measured in a unit
set by how sharply the ground can curve and how wide the field is. The important
part is the number 2 in front.

That number matters for a reason that is easy to miss. A separate result proves
that no method of this kind can ever beat a promise of about **1/4 divided by
N**. So the shape of the promise, "something divided by N", cannot be improved.
The only open question is the number in front. Before this paper it was known to
lie somewhere between 1/4 and 2.

In 2017, researchers used a computer to work out the true worst case for each
number of steps up to 100. They found that the standard promise was two to three
times too pessimistic. But a table of numbers is not a proof, and nobody had
proved a number smaller than 2.

## What we proved

The number in front is at most 1, not 2. The exact promise is a little more
complicated than 1/N, but it gets closer and closer to 1/N as the number of steps
grows, and for a single step it cannot be improved at all.

In practical terms, the guaranteed number of steps for a given accuracy falls by
about half. To guarantee you are within 1% of the bottom (in the units above),
the old promise needed 198 steps. The new one needs 101.

Nothing about the method changes. It takes exactly the same steps as before. What
changes is what we can prove about it: the method was always this good, and now
we can say so.

## How we proved it

### Where the old proof gives away too much

Every step does two things. It brings you closer to the bottom by a fixed share
of the remaining distance. And it costs you a small penalty for overshooting,
which grows with the square of how far you walked. A long step carries a bigger
penalty than a short one.

The old proof makes the most pessimistic assumption at every single step: that
you walked as far as the field is wide, and so paid the largest penalty possible.
Any one step really can be that long. Our proof shows that they cannot all be
that long, and that is where the factor of two comes from.

To see why, the old proof's way of looking at things, one step at a time, is not
enough. We need a way to look at the whole history of the walk at once.

### Your position is a team average

Here is the first observation. Your position after any number of steps is an
average of all the points you have walked toward so far, with later points
counting more. After four steps, for example, the four target points count for
10%, 20%, 30% and 40% of your position.

So think of those target points as the members of a team, each with a weight, and
your position as the team's centre. The question "how long can my next step be?"
becomes a question about this team.

### A spread-out team means a short step

The next target point lies somewhere in the field, so it is no farther than the
field's width from any member of the team. Now use a fact that physicists use
when they work out how hard an object is to spin (the parallel-axis theorem): the
average squared distance from a point to the members of a team equals the
squared distance from that point to the team's centre, plus the team's spread.

Put those together and you get the key inequality of the paper:

> (length of the next step)² ≤ (width of the field)² − (spread of the team)

A team bunched in one spot leaves room for a full-length step. A team spread
across the field does not: its centre sits somewhere in the middle, and no point
in the field is far from the middle. Call the right-hand side the **room**: it is
the most the next step can use.

### Long steps spread the team out

The second observation runs the other way. A long step adds a new team member far
from the centre, and that spreads the team out. We worked out exactly how much:
the spread after a step depends only on the spread before it and on the length of
the step.

So the room behaves like a budget. Short steps let it build back up, because new
members land close to the centre and the team tightens. Long steps drain it. The
method can take a long step whenever it likes, but every long step leaves less
room for the steps after it.

### Keeping the accounts

Now there are two quantities to track: how far you are from the bottom, and how
much room you have left. A long step makes the first worse (a bigger penalty)
but also drains the second (smaller penalties later). The proof needs to weigh
one against the other.

It does this the way an accountant would: by giving room a price. We put a value
on each unit of room left, and then add up "distance from the bottom + price ×
room". The prices are chosen so that this total grows by the same fixed amount at
every step, whether the method takes a long step or a short one. The gain on one
side of the ledger exactly offsets the loss on the other. That means we no longer
need to know what the method actually did: we can add up the fixed amounts and
get a guarantee.

The prices are worked out backwards, starting from the last step. After the last
step there is nothing left to spend the room on, so its price there is zero.
Room one step earlier is worth whatever it can buy at the last step, and so on
back to the start.

### Why the answer is exactly half

Adding up the accounts comes down to one imagined walk: the one that always
takes the longest step the room allows. No real problem has to behave this way;
it is simply the worst the accounts permit. We can follow that walk exactly. Measured as a
share of the field's width squared, its squared step lengths go

> 1, 1, 0.78, 0.69, 0.65, 0.62, 0.60, … , 0.56 at step 10, 0.507 at step 100,
> 0.5007 at step 1000

and they settle at **one half**. The old proof charged the full penalty, 1, at
every step. The true accounts never charge more than a penalty that settles at
1/2. Half the penalty, step after step, is half the number in front: 1 instead
of 2.

The exact bookkeeping gives the precise formula in the paper. Each step adds
1 + 1/(3k) to the running total at step k, which is where the paper's harmonic
number H comes from.

## How we know it is right

- Every formula in the proof was checked by computer in exact arithmetic, using
  fractions rather than decimals, so no rounding can hide a mistake.
- An independent automated reviewer re-derived the whole proof line by line.
- The new promise sits above the computer's worst-case table at every step count
  the table covers, as it must, and it matches the table exactly after one step.

## What the paper does not claim

- **It is a worst-case promise.** On a typical problem the method usually does
  better than any guarantee says.
- **1 is not the final answer.** The computer studies suggest the true number is
  about 0.9. Our accounts capture most of the gap between 2 and the truth, but
  not all of it, because the single number "spread" summarises the team's shape
  rather than tracking every pair of members. Finding the exact number is still
  open.

## Glossary

**Asymptotically.** In the long run, as the number of steps grows without limit.
"Tends to LD²/N" means that for large N the bound is almost exactly LD²/N.

**Bound (upper and lower).** An upper bound is a promise that something is at most
a given amount. A lower bound shows that something is at least a given amount,
usually by exhibiting a hard example.

**Constant (leading constant).** The fixed number in front of a formula such as
c·LD²/N. This paper lowers c from 2 to 1.

**Convergence rate.** How fast the error shrinks as the method takes more steps.
Here the error shrinks like 1/N: ten times more steps, ten times less error.

**Convex function.** A bowl-shaped function. It has no false valleys, so walking
downhill always leads toward the true bottom.

**Convex set (C).** A shape with no dents or holes: the straight line between any
two of its points stays inside it. The "field" in the story above.

**Corollary, lemma, theorem.** A theorem is a main result. A lemma is a smaller
result used to prove it. A corollary follows quickly from a theorem.

**Diameter (D).** The greatest distance between two points of the set: how wide
the field is.

**Dirac mass.** A probability distribution that puts all its weight on a single
point. The paper builds the "team" out of these, one for every target point.

**Error (f(x_N) − f\*).** How far the current value is above the best possible
value. Also called the primal gap.

**Frank–Wolfe method (conditional gradient method).** The step-by-step method
described above: feel the slope, find the lowest point of the set under that
slope, move part of the way toward it.

**Frank–Wolfe gap (duality gap, g_k).** A number the method can compute at every
step that is always at least as large as the true error. Software uses it to
decide when to stop, because the true error can't be computed without knowing
the answer. The paper improves its guarantee from 27/4 to 3.

**Gradient (∇f).** The direction and steepness of the slope at a point: what you
feel under your feet.

**Harmonic number (H_m).** The sum 1 + 1/2 + 1/3 + … + 1/m. It grows very slowly,
roughly like the natural logarithm of m, which is why it barely affects the bound.

**Iterate (x_k).** The position after k steps.

**L-smooth (L).** The slope changes gradually rather than abruptly. L is the
largest rate at which it can change: how sharply the ground can curve.

**LD².** The natural unit for measuring error in this problem. It combines how
sharply the function can curve (L) with how wide the set is (D).

**Linear minimization oracle.** The subroutine that answers the simpler question:
which point of the set is lowest if the ground tilted exactly as it does here?
"Oracle" just means a subroutine treated as a black box.

**Nuclear-norm ball.** A set of matrices (tables of numbers) whose total "size"
in a particular sense is limited. Used when filling in missing ratings, because
it favours simple patterns.

**Open-loop step size (h_k = 2/(k+2)).** A schedule of step lengths fixed in
advance, which does not react to what the method observes.

**Optimum (x\*, f\*).** The best point and the best value: the bottom of the
field and its height.

**Parallel-axis theorem.** A fact from mechanics: the average squared distance
from any point to a group of points equals the squared distance to the group's
centre plus the group's spread. It is the key step of the proof.

**Performance estimation problem (PEP).** A way of asking a computer to find the
worst possible problem for a method, by setting up and solving an optimization
problem. It gives exact numbers for each step count, but not a formula for all of
them.

**Potential function (Φ).** The accountant's total in the proof: "distance from
the bottom + price × room". It grows by a known amount each step, which turns
many step-by-step facts into one final bound.

**Preprint.** A paper shared publicly before formal peer review.

**Price (α_k).** The value the proof assigns to each unit of room at step k.
Worked out backwards from the last step, where it is zero.

**Projection.** Finding the nearest point of the set to a point outside it:
getting back inside the fence. For complicated sets this is expensive, which is
the reason the Frank–Wolfe method exists.

**Room (W_k).** The width of the field squared, minus the team's spread: the most
the next step can use (its squared length). Called W_k in the paper.

**Semidefinite program.** A type of optimization problem that computers solve
reliably. The PEP computations are semidefinite programs.

**Simplex.** The set of lists of non-negative numbers that add up to 1, such as
the shares of a budget split among several options.

**Variance (V_k), spread.** The average squared distance of the team's members
from their centre: how spread out the team is.

**Worst case.** The hardest possible problem allowed by the assumptions. A
worst-case guarantee holds for every problem, including the hardest.
