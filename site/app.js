import { FAILURE_THRESHOLD, MAX_SCORE, QUESTIONS, calculateScore, diagnose } from "./model.mjs";

const form = document.querySelector("#questionnaire-form");
const questionsContainer = document.querySelector("#questions");
const resultPanel = document.querySelector("#result-panel");
const decisionElement = document.querySelector("#decision");
const scoreElement = document.querySelector("#score");
const answerSummary = document.querySelector("#answer-summary");
const resetButton = document.querySelector("#reset-button");

function renderQuestions() {
  questionsContainer.innerHTML = QUESTIONS.map((question, index) => {
    return `
      <div class="question-item" role="group" aria-labelledby="${question.key}-label">
        <div class="question-copy">
          <p id="${question.key}-label" class="question-text">${index + 1}. ${question.text}</p>
          <div class="question-score">Yes score: ${question.score}</div>
        </div>
        <div class="option-group" role="radiogroup" aria-label="${question.text}">
          <label class="option">
            <input type="radio" name="${question.key}" value="yes" required>
            <span>Yes</span>
          </label>
          <label class="option">
            <input type="radio" name="${question.key}" value="no">
            <span>No</span>
          </label>
        </div>
      </div>
    `;
  }).join("");
}

function collectAnswers() {
  return QUESTIONS.reduce((answers, question) => {
    const selected = form.elements[question.key].value;
    answers[question.key] = selected === "yes";
    return answers;
  }, {});
}

function renderResult(answers) {
  const totalScore = calculateScore(answers);
  const decision = diagnose(answers);
  const isFailure = totalScore > FAILURE_THRESHOLD;

  decisionElement.textContent = decision;
  decisionElement.classList.toggle("failure", isFailure);
  decisionElement.classList.toggle("responder", !isFailure);
  scoreElement.innerHTML = `Total Score: <strong>${totalScore}/${MAX_SCORE}</strong>`;

  answerSummary.innerHTML = QUESTIONS.map((question) => {
    const points = answers[question.key] ? question.score : 0;
    const answerText = answers[question.key] ? "Yes" : "No";
    const plural = points === 1 ? "point" : "points";

    return `
      <li>
        <span><strong>${question.text}</strong> - ${answerText}</span>
        <span class="answer-points">${points} ${plural}</span>
      </li>
    `;
  }).join("");

  resultPanel.hidden = false;
  resultPanel.tabIndex = -1;
  resultPanel.focus({ preventScroll: true });
  resultPanel.scrollIntoView({ behavior: "smooth", block: "start" });
}

renderQuestions();

form.addEventListener("submit", (event) => {
  event.preventDefault();
  renderResult(collectAnswers());
});

resetButton.addEventListener("click", () => {
  form.reset();
  resultPanel.hidden = true;
  document.querySelector("input[name='q1']").focus();
});
