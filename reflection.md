# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?


The 3 core actions that a user should be able to perfrom are adding an owner and a pet so the app knows who the care plan is for. Second add and edit care task with duration and priority. And lastly generate a daily plan that fits the owners' avalaible time and explains why tasks were chosen and ordered this way


My initial UML design has four classes. Owner stores the owner's name and how much time they have each day, and keeps track of their pets. Pet stores the pet's name and species and holds its list of care tasks. Task represents one care activity with a title, duration, priority, and whether it's completed. Scheduler takes the owner's tasks and builds a daily plan that fits their available time, then explains why it chose that plan.
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

**b. Design changes**

Yes, my design changed after I had AI look over my class skeleton. The first thing I changed was adding a `pet_name` to `Task`, because the Scheduler only got one big list of tasks and couldn't tell which pet each one was for. Second, I added `plan` and `skipped` lists to `Scheduler` so `explain_plan()` could say why a task was left out, not just what got picked. Third, I added a `PRIORITY_ORDER` dictionary, because if you sort "high", "medium", and "low" like normal words you get high, low, medium, which is wrong.

I also decided that completed tasks don't go in the plan or the skipped list, and that generate_plan() clears both lists every time it runs so tasks don't get doubled. Last, I made Owner a dataclass so it matches Pet and Task. After the changes I updated the UML diagram so it matches the code.



---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
My scheduler looks at three things: how many minutes the owner has available, each task's priority (high, medium, or low), and how long each task takes. It also skips tasks that are already completed. I decided time matters most because the plan has to fit the owner's day or it isn't useful. Priority comes next so important things like feeding and meds get picked before optional things like grooming. Duration is the tiebreaker, so when two tasks have the same priority the shorter one goes first and more tasks fit. I left owner preferences out of this version to keep things simple.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
My scheduler fills the day greedily. It sorts tasks by priority and then duration, and adds each one if it still fits in the time left. This isn't always the best possible plan. A long high-priority task could get skipped even if a few shorter low-priority tasks would have fit in the leftover time. I think that's okay here because it's simple, fast, and easy to explain to the owner, and the app is supposed to explain its plan.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to brainstorm the four classes, draw the UML diagram, write the class skeleton, review that skeleton, and then implement the logic, the demo script, and the tests. The most helpful prompts were specific ones, like asking it to suggest changes first and wait for my approval before editing any files.


**b. Judgment and verification**


- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I didn't just accept everything the AI suggested. After it reviewed my skeleton, I went through its suggestions and picked which ones to approve, and I told it not to touch the starter repo's `uml.mmd`. To check its work, I read the changed files, ran `python main.py` to make sure the schedule looked right and that Grooming got skipped when time ran short, and ran pytest myself. The AI's pytest run failed because its shell was using a different project's Python, so I ran the tests in my own `.venv` to confirm they passed. I also noticed that the "skipped" message compares a task to the time left after the whole plan is filled, which isn't exactly the time left when that task was considered.

When I asked the AI how to simplify detect_conflicts(), it suggested a list comprehension to build the warnings. I kept the plain loop instead, because the comprehension packs too much into one line and is harder to read. I did take its suggestions to use defaultdict and to reuse filter_tasks(), and I checked that the existing tests still passed.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?


My conflict detection only checks for exact matching start times, not overlapping durations. For example, a 30-minute walk at 08:00 and a feeding at 08:15 overlap, but my scheduler won't flag them. I chose this because it's simple, fast, and easy to explain, and it returns a warning instead of crashing. Checking real overlaps would be more accurate, but it needs end times and more edge cases. My scheduler also still schedules conflicting tasks and just warns about them, so the owner can decide what to do.
**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
