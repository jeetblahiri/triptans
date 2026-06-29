import assert from "node:assert/strict";

import { MAX_SCORE, calculateScore, diagnose } from "./site/model.mjs";

const keys = ["q1", "q2", "q3", "q4", "q5", "q6", "q7"];
const blankAnswers = () => Object.fromEntries(keys.map((key) => [key, false]));

{
  const answers = blankAnswers();
  answers.q1 = true;
  assert.equal(calculateScore(answers), 2);
}

{
  const answers = blankAnswers();
  answers.q1 = true;
  answers.q2 = true;
  answers.q3 = true;
  assert.equal(calculateScore(answers), 4);
  assert.equal(diagnose(answers), "Triptan Responder");
}

{
  const answers = blankAnswers();
  answers.q1 = true;
  answers.q2 = true;
  answers.q3 = true;
  answers.q4 = true;
  assert.equal(calculateScore(answers), 5);
  assert.equal(diagnose(answers), "Triptan Failure");
}

{
  const answers = Object.fromEntries(keys.map((key) => [key, true]));
  assert.equal(calculateScore(answers), MAX_SCORE);
  assert.equal(diagnose(answers), "Triptan Failure");
}

console.log("Static scoring tests passed.");
