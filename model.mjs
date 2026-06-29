export const QUESTIONS = [
  { key: "q1", text: "Is the HIT-6 score between 60-78?", score: 2 },
  { key: "q2", text: "Does the patient experience photophobia or phonophobia during headache?", score: 1 },
  { key: "q3", text: "Does severe headache last for more than 2 hours?", score: 1 },
  { key: "q4", text: "Do headache attacks last for more than 4 hours?", score: 1 },
  { key: "q5", text: "Does headache limit daily activities?", score: 1 },
  { key: "q6", text: "Does the patient experience headache on more than 15 days per month?", score: 1 },
  { key: "q7", text: "Is the NPRS score more than 7/10?", score: 1 },
];

export const MAX_SCORE = QUESTIONS.reduce((total, question) => total + question.score, 0);
export const FAILURE_THRESHOLD = 4;

export function calculateScore(answers) {
  return QUESTIONS.reduce((total, question) => {
    return total + (answers[question.key] ? question.score : 0);
  }, 0);
}

export function diagnose(answers) {
  return calculateScore(answers) > FAILURE_THRESHOLD
    ? "Triptan Failure"
    : "Triptan Responder";
}
