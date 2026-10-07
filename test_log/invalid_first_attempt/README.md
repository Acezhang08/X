INVALID - not used in the report or video.
Bug in the first version of run_tests.sh: `claude -p` inherited the loop's stdin
(questions.txt), so each run received all 4 questions instead of one.
Kept only for transparency. The clean reruns are in the parent folder.
