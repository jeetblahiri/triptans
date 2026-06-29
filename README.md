# Triptans - static deployment app

Static migraine response questionnaire for GitHub Pages and Vercel.

## Project structure

```text
triptans/
├─ site/
│  ├─ index.html
│  ├─ styles.css
│  ├─ app.js
│  └─ model.mjs
├─ scripts/
│  └─ build-vercel.mjs
├─ .github/workflows/pages.yml
├─ package.json
├─ vercel.json
└─ test_static_model.mjs
```

## Local run

The app is fully static. Serve the `site/` folder locally to test the same shape
GitHub Pages will host:

```bash
npm run dev
# open http://localhost:3000
```

## Test

```bash
npm test
```

## Build for Vercel

```bash
npm run build
```

The build copies `site/` to `dist/`. Vercel deploys `dist/` using the settings in
`vercel.json`.
No external npm dependencies are required.
Vercel import settings can be left as:

| Setting | Value |
| --- | --- |
| Framework Preset | Other |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Install Command | Auto / default |

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

This repository publishes the `site/` folder to a `gh-pages` branch. On each push
to `main`, `.github/workflows/pages.yml` updates that branch automatically.

Expected URL:

```text
https://jeetblahiri.github.io/triptans/
```

If this is the first Pages deployment for the repository, open GitHub:

1. Go to `Settings` -> `Pages`.
2. Set `Build and deployment` source to `Deploy from a branch`.
3. Select branch `gh-pages` and folder `/ (root)`.
4. Save, then wait for GitHub Pages to publish the site.

## Vercel deploy

1. Import `jeetblahiri/triptans` in Vercel.
2. Keep the project root as the repository root.
3. Vercel will read `vercel.json`, run `npm run build`, and publish `dist/`.
4. After deployment, Vercel will provide a production URL for the calculator.
