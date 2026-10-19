# DEMO - Little Breaks Swipe Cards

Q1. Which of these short breaks would appeal to you?

Question type: one required single-select matrix. One answer per row. Exactly one question and one page. Static rows and columns; no loops, routing, additional fields, or termination resource.

Instructions: For each idea, choose Dislike, Skip, or Like. Skip is an explicit response.

Rows in fixed order:

r1: Sketching for ten minutes

r2: Listening to a new album

r3: Making a cup of tea

Columns in fixed order:

c1: Dislike (code 1)

c2: Skip (code 2)

c3: Like (code 3)

Presentation: Use the imported SwipeCards component unchanged. Show the question, cards and Dislike/Skip/Like only. After the final animation, hide the deck and invoke the original native Continue action once. Restore the matrix and Continue on validation or stalled submission; preserve native handlers and do not automatically retry. Keep its fading swipe motion, threshold cancellation, locked single commit and next-card preview. No review page, Back, Undo, debugging or demo explanation.
