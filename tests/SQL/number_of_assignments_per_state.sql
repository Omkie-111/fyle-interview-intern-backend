-- Write query to get number of assignments for each state
SELECT state, COUNT(id) AS assignment_count
FROM assignments
WHERE state IN ('DRAFT', 'GRADED', 'SUBMITTED')
GROUP BY state;
