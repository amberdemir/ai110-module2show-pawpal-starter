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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

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
