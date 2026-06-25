import unittest

from app import KEYS, MAX_SCORE, calculate_score, diagnose, app


class TriptanScoringTest(unittest.TestCase):
    def test_hit6_question_counts_two_points(self):
        answers = {key: False for key in KEYS}
        answers["q1"] = True

        self.assertEqual(calculate_score(answers), 2)

    def test_score_four_is_responder(self):
        answers = {key: False for key in KEYS}
        for key in ["q1", "q2", "q3"]:
            answers[key] = True

        self.assertEqual(calculate_score(answers), 4)
        self.assertEqual(diagnose(answers), "Triptan Responder")

    def test_score_above_four_is_failure(self):
        answers = {key: False for key in KEYS}
        for key in ["q1", "q2", "q3", "q4"]:
            answers[key] = True

        self.assertEqual(calculate_score(answers), 5)
        self.assertEqual(diagnose(answers), "Triptan Failure")

    def test_all_yes_reaches_max_score(self):
        answers = {key: True for key in KEYS}

        self.assertEqual(calculate_score(answers), MAX_SCORE)
        self.assertEqual(diagnose(answers), "Triptan Failure")

    def test_diagnose_route_shows_score_and_result(self):
        client = app.test_client()
        response = client.post(
            "/diagnose",
            data={key: "yes" for key in KEYS},
        )

        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("Triptan Failure", body)
        self.assertIn("Total Score: <strong>8/8</strong>", body)


if __name__ == "__main__":
    unittest.main()
