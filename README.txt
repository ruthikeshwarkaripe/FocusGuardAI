FOCUSGUARD AI — STEP 3 — WINDOWS PROTOTYPE

NEW IN STEP 3
- Context-aware decision engine.
- Classification uses Subject + Topic + Goal + Activity.
- Same app can receive different classifications depending on study context.
- Productive / Uncertain / Distracting decisions include confidence and reasons.
- WhatsApp is not automatically blocked.
- YouTube can be Productive when the study context suggests lectures/tutorials.
- Chrome can be Productive for research/documentation contexts.
- Instagram is currently treated as high-probability distracting.
- Focus score responds to decision results.
- Session stores the decision history.
- Session summary shows decision counts.
- Existing timer, local storage, dashboard and statistics remain.

TEST CASES
1. Start a Physics session with:
   Topic: Electromagnetic Induction
   Goal: Complete 20 practice questions
2. Test YouTube:
   It should be Productive or Uncertain depending on the context.
3. Test WhatsApp:
   It should be Uncertain unless the context has collaboration/study signals.
4. Test Instagram:
   It should be Distracting and open the alert.
5. Try Chrome with a research/documentation goal:
   It can be Productive.

IMPORTANT
This is still a browser prototype.
The decision engine is rule-based, NOT Gemini yet.
It does NOT monitor real Windows applications.
It does NOT block applications.

NEXT STEP
Step 4: create a Python FastAPI backend and move the decision engine into a real API.
After that, Gemini can be connected as the semantic AI layer.
