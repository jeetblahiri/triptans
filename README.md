# Triptans - GitHub Pages app

Static migraine response questionnaire for GitHub Pages.

## Project structure

```text
triptans/
├─ site/
│  ├─ index.html
│  ├─ styles.css
│  ├─ app.js
│  └─ model.mjs
├─ .github/workflows/pages.yml
└─ test_static_model.mjs
```

## Local run

The app is fully static. Serve the `site/` folder locally to test the same shape
GitHub Pages will host:

```bash
python3 -m http.server 8080 --directory site
# open http://localhost:8080
```

## Test

```bash
node test_static_model.mjs
```

## Model scoring

The app uses a seven-item yes/no questionnaire:

| S.No. | Question | Yes score |
| --- | --- | --- |
| 1 | Is the HIT-6 score between 60-78? | 2 |
| 2 | Does the patient experience photophobia or phonophobia during headache? | 1 |
| 3 | Does severe headache last for more than 2 hours? | 1 |
| 4 | Do headache attacks last for more than 4 hours? | 1 |
| 5 | Does headache limit daily activities? | 1 |
| 6 | Does the patient experience headache on more than 15 days per month? | 1 |
| 7 | Is the NPRS score more than 7/10? | 1 |

Maximum total score is 8.

| Total score | Interpretation |
| --- | --- |
| `> 4` | Triptan Failure |
| `<= 4` | Triptan Responder |

## GitHub Pages deploy

This repository deploys the `site/` folder with GitHub Actions. On each push to
`main`, `.github/workflows/pages.yml` publishes the app to GitHub Pages.

Expected URL:

```text
https://jeetblahiri.github.io/triptans/
```

If this is the first Pages deployment for the repository, open GitHub:

1. Go to `Settings` -> `Pages`.
2. Set `Build and deployment` source to `GitHub Actions`.
3. Open the `Actions` tab and rerun the latest `Deploy GitHub Pages` workflow if it did not start automatically.
